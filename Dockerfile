FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk upgrade --update \
    && apk add bash nano

COPY ./requirements.txt /app/requirements.txt
COPY ./app /app

RUN pip install -r /app/requirements.txt
