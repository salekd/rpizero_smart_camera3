#!/bin/bash
export img_dir=/home/pi/motion
export last_file=`(cd $img_dir; ls -rt *jpg | tail -n 1)`
curl 192.168.2.2:8080/async-function/faas-mobilenet \
    -d "$(echo -n '{"filename": "'; echo -n $last_file; echo -n '", "image_data": "'; base64 $img_dir/$last_file | tr -d '\n'; echo '"}')" \
    -H "X-Callback-Url: http://192.168.2.2:8080/function/faas-s3-email"
rm -f $img_dir/$last_file
