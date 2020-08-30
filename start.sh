#!/bin/bash
app="exoscale.pingtimes"
docker build -t ${app} .
docker run -d -p 55000:80 \
  --name=${app} \
  -v $PWD:/app ${app}


