#!/bin/bash
export last_file=`ls -rt /home/pi/motion | tail -n 1`
curl 192.168.2.2:8080/async-function/faas-mobilenet \
    -d "$(echo -n '{"filename": "'; echo -n $last_file; echo -n '", "image_data": "'; base64 $last_file | tr -d '\n'; echo '"}')" \
    -H "X-Callback-Url: http://192.168.2.2:8080/function/faas-s3-email"
rm $last_file
