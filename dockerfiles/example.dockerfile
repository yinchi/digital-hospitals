FROM python:3.12-slim
RUN apt update && apt upgrade
RUN pip install --no-cache-dir poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0

COPY ./digital-hospitals.common/ /digital-hospitals.common/

WORKDIR /digital-hospitals.example

COPY ./digital-hospitals.example/ /digital-hospitals.example
COPY ./digital-hospitals.common/ /digital-hospitals.common
RUN poetry install --no-interaction && rm -rf ~/.cache/pypoetry/

CMD poetry run fastapi run ./digital_hospitals/example/app.py --root-path /api/example
