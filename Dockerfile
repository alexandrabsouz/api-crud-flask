FROM python:3.6-alpine

RUN adduser -D api_crud_flask

WORKDIR /home/api_crud_flask


RUN apk add libpq
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev build-base
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn psycopg2

COPY app app
COPY migrations migrations
COPY api_crud_flask.py config.py ./

ENV FLASK_APP api_crud_flask.py

RUN chown -R api_crud_flask:api_crud_flask ./
USER api_crud_flask

EXPOSE 5000
CMD venv/bin/gunicorn -b :5000 --access-logfile - --error-logfile - api_crud_flask:app