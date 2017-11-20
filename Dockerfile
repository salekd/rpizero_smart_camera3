FROM ubuntu:16.04

# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apt-get update \
    && apt-get install -y curl \ 
    && echo "Pulling watchdog binary from Github." \
    && curl -sSL https://github.com/openfaas/faas/releases/download/0.6.9/fwatchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog \
    && apt-get install -y git \
    && git clone https://github.com/tensorflow/models.git \
    && apt-get install -y protobuf-compiler \
    && cd /models/research/ \
    && protoc object_detection/protos/*.proto --python_out=. \
    && cd / \
    && apt-get install -y wget \
    && wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
    && tar -zxvf ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
    && apt-get install -y python-pip python-dev build-essential \
    && apt-get install -y python-tk

ENV PYTHONPATH=/model/research:/model/research/slim

WORKDIR /root/

COPY index.py           .
COPY requirements.txt   .
RUN pip install -r requirements.txt

COPY function           function

RUN touch ./function/__init__.py

WORKDIR /root/function/
COPY function/requirements.txt	.
RUN pip install -r requirements.txt

WORKDIR /root/

ENV fprocess="python index.py"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
