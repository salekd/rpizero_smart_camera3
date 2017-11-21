FROM ubuntu:16.04

# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    protobuf-compiler \
    python-pip python-dev build-essential \
    python-tk \
    wget \
    && echo "Pulling watchdog binary from Github." \
    && curl -sSL https://github.com/openfaas/faas/releases/download/0.6.9/fwatchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog \
    && git clone https://github.com/tensorflow/models.git \
    && cd /models/research/ \
    && protoc object_detection/protos/*.proto --python_out=. \
    && cd / \
    && wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
    && tar -zxvf ssd_mobilenet_v1_coco_11_06_2017.tar.gz

ENV PYTHONPATH=/model/research:/model/research/slim
# Disable TensorFlow warning messages
ENV TF_CPP_MIN_LOG_LEVEL=3

WORKDIR /root/

COPY index.py           .
COPY index_output_image.py .
COPY requirements.txt   .
RUN pip install -r requirements.txt

COPY function           function

RUN touch ./function/__init__.py

WORKDIR /root/function/
COPY function/requirements.txt	.
RUN pip install -r requirements.txt

WORKDIR /root/

ENV fprocess="python index.py"
ENV read_timeout=10
ENV write_timeout=10
ENV exec_timeout=10

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
