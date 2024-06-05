FROM python:3.12-slim
RUN apt update && apt upgrade
RUN pip install --no-cache-dir poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    REACT_VERSION=18.2.0

WORKDIR /digital-hospitals.dev-frontpage

COPY ./digital-hospitals.dev-frontpage/ .
RUN poetry install --no-interaction && rm -rf ~/.cache/pypoetry/

CMD poetry run gunicorn digital_hospitals.dev_frontpage:server -b :8050