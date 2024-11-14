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
