FROM python:3.12.4

RUN mkdir /backend

WORKDIR /backend

COPY pyproject.toml poetry.lock ./

RUN python -m venv venv

RUN chmod a+x venv/bin/activate

RUN venv/bin/activate

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

WORKDIR ./eQueue

RUN alembic upgrade head

CMD gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --access-logfile -
