# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

LABEL maintainer=sebastien.pittet@exoscale.com

WORKDIR /app

# Copy the requirements.txt to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Start application 
CMD [ "gunicorn" ]
