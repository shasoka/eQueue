FROM python:3.12.4

# RUN goes on image build
RUN mkdir /eQueue_server

WORKDIR /eQueue_server

COPY pyproject.toml poetry.lock ./

RUN python -m venv venv

RUN chmod a+x venv/bin/*.sh

RUN venv/bin/activate

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

RUN mv .env ./eQueue/

WORKDIR ./eQueue

RUN alembic upgrade head

# CMD goes on image run
CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
