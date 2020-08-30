FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk upgrade --update \
    && apk add bash nano

COPY ./main.py /app
COPY ./requirements.txt /demoapp/requirements.txt
COPY ./app /app/app
COPY ./uwsgi.ini /app

RUN pip install -r /app/requirements.txt
