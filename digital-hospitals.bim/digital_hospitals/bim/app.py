"""FastAPI module for the BIM service."""

import importlib.metadata
import json
import tempfile
from datetime import datetime
from typing import Annotated, Literal, Optional, Sequence

import networkx as ntx
from bson import ObjectId
from fastapi import BackgroundTasks, Depends, FastAPI, File, Form, HTTPException, Query, UploadFile, status
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, JsonValue
from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database

import digital_hospitals.bim
from digital_hospitals.bim import models
from digital_hospitals.common import (MONGODB_PASSWORD, MONGODB_PORT, MONGODB_TIMEOUT,
                                      MONGODB_URL, MONGODB_USER, check_docker)

version = importlib.metadata.version('digital_hospitals.bim')


def now() -> float:
    """The current UNIX timestamp."""
    return datetime.now().timestamp()


DESCRIPTION = """\
FastAPI service for the BIM module of the digital hospitals platform. Computes runner times for a
histopathology lab process model given an .ifc file representing the lab's physical layout.

[Return to developer portal frontpage](/dev)
"""

EXAMPLE_GRAPH = ntx.Graph()
EXAMPLE_GRAPH.add_node("1")
EXAMPLE_GRAPH.add_node("2")
EXAMPLE_GRAPH.add_edge("1", "2", weight=10.0)


class BimResult(BaseModel):
    """The result of a runner-times computation request."""
    status: Literal['OK', 'Error', 'Running']

    graph: Optional[JsonValue] = None
    """The logical graph of the lab, with edge weights representing the runner times
    between nodes."""

    err_msg: Optional[str] = None
    """If `status` is "error", the error message."""

    requested_ts: float
    """A timestamp denoting when the computation request was received."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "OK",
                    "graph": ntx.node_link_data(EXAMPLE_GRAPH),
                    "timestamp": datetime.fromisoformat("2024-06-01T12:34:56+01:00"),
                }
            ]
        }
    }


class BimRequestParams(BaseModel):
    """The parameters of a runner-times computation request."""

    door_list: Sequence[str]
    """A list of doors involved in the histopathology process."""

    extra_paths: Sequence[models.Path]
    """A list of paths connecting different floors of the histopathology lab, e.g.,
    via lift or stairs."""


api = FastAPI(
    title='BIM (Building Information Modelling) server',
    description=DESCRIPTION,
    version=version,
    docs_url=None,  # Use custom_swagger_ui_html()
    redoc_url=None
)


def get_db():  # Dependency
    """Get a connection nto the MongoDB server and point it to the 'bim' database."""
    try:
        client = MongoClient(MONGODB_URL, MONGODB_PORT, username=MONGODB_USER,
                             password=MONGODB_PASSWORD, timeoutMS=MONGODB_TIMEOUT)
        yield client['bim']
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(exc)) from exc
    finally:
        client.close()


def handle_bim_request(file: UploadFile,
                       params: BimRequestParams,
                       _id: ObjectId,
                       db: Annotated[Database, Depends(get_db)]):
    """Compute runner times for a given input."""
    # FIXME: This function doesn't seem to run and/or update the database???

    # Since `ifcopenshell.open()` expects a filename rather than a file object,
    # create a temp file. This file is deleted automatically on close (default behaviour).
    try:
        with tempfile.NamedTemporaryFile() as temp_file:
            # Write file and reset pointer
            temp_file.write(file)
            temp_file.seek(0)

            model = models.BimModel.from_ifc(temp_file.name)
            g = models.logical_graph(
                model,
                params.door_list,
                params.extra_paths,
                models.DEFAULT_RUNNER_SPEED
            )
            status = 'OK'
            graph = ntx.node_link_data(g)
    except Exception as exc:
        status = 'Error'
        err_msg = str(exc)

    # Write result to DB -- there should always be at most one document in this collection,
    # i.e. the latest BIM module result.
    try:
        if status == 'OK':
            # Write the result to "collection"
            item = db['results'].find_one_and_update(
                {'_id': _id},
                {'$set': {'status': status, 'result': graph}},
                return_document=ReturnDocument.AFTER
            )

        elif status == 'Error':
            # Write only the status to "collection" and return early
            db['results'].find_one_and_update(
                {'_id': _id},
                {'$set': {'status': status, 'err_msg': err_msg}}
            )
            return

        # Strip MongoDB internal _id field
        if '_id' in item:
            del item['_id']
            item = BimResult.model_validate(item)

        old_item = db['results-latest'].find_one()  # Get the previous "latest" result

        if old_item is None:  # No previous result found: write new result to "latest"
            db['results-latest'].insert_one(item)

        else:
            old_item = BimResult.model_validate(old_item)
            if old_item.requested_ts >= item.requested_ts:
                return  # Old result is newer(!!): ignore new result

            # Default behaviour: write new result to "latest"
            db['results-latest'].find_one_and_replace({}, item)

    except Exception:
        pass


@api.get('/latest',
         summary='Get the latest runner times result from the server.')
def get_latest(db: Annotated[Database, Depends(get_db)]) -> BimResult:
    """Get the latest BimResult from the database server, containing the runner times between
    each pair of marked doors in the BIM model."""

    result = db['results-latest'].find_one()
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    # Validate result and return as object. The result in /latest should always have
    # status "OK", indicating a completed result.
    try:
        validated_result = BimResult.model_validate(result)
        assert validated_result.status == 'OK'
        _ = ntx.node_link_graph(validated_result.graph)
    except Exception as exc:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            'Invalid result, please try resubmitting your BIM configuration.'
                            ) from exc
    return validated_result


class AcceptedResponseModel(BaseModel):
    """Schema for an accepted / (root) POST request"""
    detail: Literal['Accepted'] = 'Accepted'
    id: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"detail": "Accepted", "id": '665cf35cd36468e11afb19c5'}]
        }
    }


@api.post('/',
          summary='Submit new BIM data',
          description="""\
Submit new BIM data.

The new data is used to compute the runner times between each pair of marked doors in the BIM
model.""",
          status_code=status.HTTP_202_ACCEPTED,
        #   response_model=AcceptedResponseModel
          )
def update(file: UploadFile,
           background_tasks: BackgroundTasks,
           db: Annotated[Database, Depends(get_db)],
           form_data: Annotated[str, Form()]):
    """Compute new runner times based on the POST request."""
    ts = now()
    params = json.loads(form_data)

    # Create a new request in the Mongo database and set the status to "Running"
    result = db['results'].insert_one(
        BimResult(status='Running', requested_ts=ts).model_dump())
    background_tasks.add_task(handle_bim_request, file, params, result.inserted_id, ts)

    return AcceptedResponseModel(id=str(result.inserted_id))


@api.get('/query',
         summary='Query job status',
         description="""\
Get the status/result of a previously submitted
request to update the BIM data. A request may have a status
of "Running", "Error" or "OK; if the status is "OK" a graph object
containing the runner time data is also returned.""")
def query(id: Annotated[str,
                            Query(
                                title='Job ID',
                                description='MongoDB object ID as a 24-hex-digit string.',
                                example='665ed486d196679480be839a')],
          db: Annotated[Database, Depends(get_db)]):
    """Query request status"""

    _id = ObjectId(id)
    result = db['results'].find_one({'_id': _id})

    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Not found')

    # Validate result and return as object
    try:
        validated_result = BimResult.model_validate(result)

        # Check graph only if status is "OK", i.e. completed result
        if validated_result.status == 'OK':
            _ = ntx.node_link_graph(validated_result.graph)
    except Exception as exc:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            str(exc)
                            ) from exc
    return validated_result


@api.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    IS_DOCKER = check_docker
    root = '/api/bim' if IS_DOCKER else ''
    "Serve docs with custom CSS."
    print(api.openapi_url)
    return get_swagger_ui_html(
        openapi_url=f"{root}{api.openapi_url}",
        title=api.title + " - Swagger UI",
        swagger_css_url=(
            "/static/swagger-dark-ui.css" if IS_DOCKER
            else "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css"
        )
    )
