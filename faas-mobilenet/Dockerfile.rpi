FROM schachr/raspbian-stretch

ARG ADDITIONAL_PACKAGE

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git unzip \
    python3-pip python3-dev python3-setuptools build-essential python3-tk \
    libblas-dev liblapack-dev libatlas-base-dev gfortran python-setuptools \
    libfreetype6-dev libjpeg-dev libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Pulling watchdog binary from Github." \
    && curl -sSL https://github.com/openfaas/faas/releases/download/0.9.14/fwatchdog-armhf > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog \
    && git clone https://github.com/tensorflow/models.git --branch v1.13.0 \
    && curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v3.7.0/protobuf-all-3.7.0.tar.gz \
    && tar -zxvf protobuf-all-3.7.0.tar.gz

WORKDIR /protobuf-3.7.0
RUN ./configure
RUN make
RUN make check
RUN make install
RUN ldconfig

WORKDIR /protobuf-3.7.0/python
ENV LD_LIBRARY_PATH=/protobuf-3.7.0/src/.libs
RUN python3 setup.py build --cpp_implementation \
    && python3 setup.py test --cpp_implementation \
    && python3 setup.py install --cpp_implementation
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=2

WORKDIR /models/research/
RUN protoc object_detection/protos/*.proto --python_out=.

WORKDIR /
RUN curl -O http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz \
    && tar -zxvf ssd_mobilenet_v1_coco_11_06_2017.tar.gz

ENV PYTHONPATH=/model/research:/model/research/slim
# Disable TensorFlow warning messages
ENV TF_CPP_MIN_LOG_LEVEL=3

# Add non root user
RUN adduser --disabled-password --gecos '' app
RUN chown app /home/app
RUN chown -R app:app /ssd_mobilenet_v1_coco_11_06_2017

USER app
ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .
RUN pip3 install --user -r requirements.txt

RUN mkdir -p function
RUN touch ./function/__init__.py

WORKDIR /home/app/function/
COPY function/requirements.txt    .
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6-dev pkg-config libhdf5-dev
USER app
RUN pip3 install --user -r requirements.txt

WORKDIR /home/app/
COPY function           function

ENV fprocess="python3 index.py"
# Make sure to allow enough time for the function to run
ENV read_timeout=10
ENV write_timeout=10
ENV exec_timeout=60
EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
