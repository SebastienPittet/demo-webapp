FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk upgrade --update \
    && apk add bash nano

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY ./requirements.txt /var/www/requirements.txt
COPY ./main.py /var/www/main.py
COPY ./app /var/www/

RUN pip install -r /var/www/requirements.txt
