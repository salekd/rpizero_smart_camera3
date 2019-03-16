FROM ubuntu:16.04

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE

# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git unzip \
    python3-pip python3-dev python3-setuptools build-essential python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Pulling watchdog binary from Github." \
    && curl -sSL https://github.com/openfaas/faas/releases/download/0.9.14/fwatchdog > /usr/bin/fwatchdog \
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

# Add non root user
#RUN addgroup -S app && adduser app -S -G app
RUN adduser --disabled-password --gecos '' app

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .

RUN chown -R app /home/app

USER app
ENV PATH=$PATH:/home/app/.local/bin
RUN pip3 install --user -r requirements.txt

RUN mkdir -p function
RUN touch ./function/__init__.py

WORKDIR /home/app/function/
COPY function/requirements.txt	.
RUN pip3 install --user -r requirements.txt

WORKDIR /home/app/

USER root
COPY function           function
RUN chown -R app:app ./
RUN chown -R app:app /ssd_mobilenet_v1_coco_11_06_2017
USER app

# Make sure to allow enough time for the function to run
ENV read_timeout=10
ENV write_timeout=10
ENV exec_timeout=30
ENV fprocess="python3 index.py"
EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
