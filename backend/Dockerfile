FROM python:3.12.4

MAINTAINER Arkady Schoenberg <shasoka@yandex.ru>

ARG APP_CONFIG__DB__URL
ARG APP_CONFIG__PROXY__HTTP
ARG APP_CONFIG__PROXY__HTTPS
ARG APP_CONFIG__DB__ECHO

ENV APP_CONFIG__DB__URL=$APP_CONFIG__DB__URL
ENV APP_CONFIG__PROXY__HTTP=$APP_CONFIG__PROXY__HTTP
ENV APP_CONFIG__PROXY__HTTPS=$APP_CONFIG__PROXY__HTTPS
ENV APP_CONFIG__DB__ECHO=$APP_CONFIG__DB__ECHO

# Debugging
RUN echo "Environment variables during build:" && env

RUN mkdir /backend
WORKDIR /backend
COPY pyproject.toml poetry.lock ./

RUN python -m venv venv
RUN chmod a+x venv/bin/activate
RUN venv/bin/activate

RUN pip install --upgrade pip
RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false && poetry install --only main

COPY . .
WORKDIR ./eQueue

RUN alembic upgrade head

CMD gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --access-logfile -
EXPOSE 8000
