"""Example FastAPI server."""
import importlib.metadata
import os
from typing import Literal

import digital_hospitals.common as common
import digital_hospitals.example
from fastapi import FastAPI, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import PlainTextResponse

version = importlib.metadata.version('digital_hospitals.example')
print(version)

DESCRIPTION = """\
An example FastAPI service with one functional endpoint and one endpoint
that always returns an HTTP 501 error.

[Return to developer portal frontpage](/dev)
"""

example_api = FastAPI(
    title='Example FastAPI server',
    description=DESCRIPTION,
    version=version,
    docs_url=None,  # Use custom_swagger_ui_html()
    redoc_url=None
)


@example_api.get("/",
                 summary='Returns "Hello World"',
                 response_class=PlainTextResponse,
                 responses={
                     "200": {
                         "description": "Successful Response",
                         "content": {"text/plain": {"example": "Hello World"}}
                     }
                 })
async def root():
    return 'Hello World'


@example_api.get("/notimplemented",
                 summary='Not implemented',
                 **common.NOT_IMPLEMENTED_ARGS)
async def not_implemented():
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, 'Not implemented')


@example_api.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    IS_DOCKER = common.check_docker
    root = '/api/example' if IS_DOCKER else ''
    "Serve docs with custom CSS."
    print(example_api.openapi_url)
    return get_swagger_ui_html(
        openapi_url=f"{root}{example_api.openapi_url}",
        title=example_api.title + " - Swagger UI",
        swagger_css_url=(
            "/static/swagger-dark-ui.css" if IS_DOCKER
            else "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css"
        )
    )
