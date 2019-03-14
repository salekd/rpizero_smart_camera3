FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl unzip \
    python3-pip python3-dev python3-setuptools build-essential \
    python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Pulling watchdog binary from Github." \
    && curl -sSL https://github.com/openfaas/faas/releases/download/0.6.9/fwatchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog \
    && git clone https://github.com/tensorflow/models.git --branch v1.13.0

WORKDIR /models/research/
RUN curl -L -o protobuf.zip https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip \
    && unzip protobuf.zip \
    && ./bin/protoc object_detection/protos/*.proto --python_out=.

WORKDIR /
RUN curl -O http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
    && tar -zxvf ssd_mobilenet_v1_coco_11_06_2017.tar.gz

ENV PYTHONPATH=/model/research:/model/research/slim
# Disable TensorFlow warning messages
ENV TF_CPP_MIN_LOG_LEVEL=3

WORKDIR /root/

COPY index.py           .
COPY index_output_image.py .
COPY requirements.txt   .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY function           function

RUN touch ./function/__init__.py

WORKDIR /root/function/
COPY function/requirements.txt	.
RUN pip3 install -r requirements.txt

WORKDIR /root/

ENV fprocess="python3 index.py"
# Make sure to allow enough time for the function to run
ENV read_timeout=10
ENV write_timeout=10
ENV exec_timeout=30

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
