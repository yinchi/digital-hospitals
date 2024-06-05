FROM python:3.12-slim
RUN apt update && apt upgrade
RUN apt install gcc -y
RUN pip install --no-cache-dir poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0

COPY ./digital-hospitals.common/ /digital-hospitals.common/

WORKDIR /digital-hospitals.bim

COPY ./digital-hospitals.bim/ /digital-hospitals.bim
COPY ./digital-hospitals.common/ /digital-hospitals.common
RUN poetry install --no-interaction && rm -rf ~/.cache/pypoetry/

CMD poetry run fastapi run ./digital_hospitals/bim/app.py --root-path /api/bim