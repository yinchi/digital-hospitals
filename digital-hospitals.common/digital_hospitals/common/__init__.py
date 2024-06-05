"""Common values used for the histopathology project."""
import os
from typing import Literal

from pydantic import BaseModel

### MONGO DB ###

# Check if we are in a docker container
check_docker = os.environ.get('IS_DOCKER', False)

MONGODB_URL = 'mongo' if check_docker else 'localhost'
MONGODB_PORT = 27017
MONGODB_USER = 'root'
MONGODB_TIMEOUT = 5000  # ms
PASSWORD_PATH = f"{'/run' if check_docker else '..'}/secrets/mongo-root-pw"
MONGODB_PASSWORD = open(PASSWORD_PATH, 'r', encoding='utf-8').read()


### FASTAPI ###
class NotImplementedType(BaseModel):
    detail: Literal['Not Implemented']


NOT_IMPLEMENTED_ARGS = {
    'description': """\
Example of a placeholder endpoint that will always raise a 501 error.
The function has a nominal return model for the `HTTP 200` status, but this is never used.""",
    'status_code': 501,
    'response_description': 'Not implemented',
    'responses': {501: {'model': NotImplementedType}}
}
