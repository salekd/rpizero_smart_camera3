FROM schachr/raspbian-stretch

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE

# Alternatively use ADD https:// (which will not be cached by Docker builder)
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

USER app
ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .

USER root
RUN chown -R app /home/app

USER app
ENV PATH=$PATH:/home/app/.local/bin
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

USER root
COPY function           function
RUN chown -R app:app ./
RUN chown -R app:app /ssd_mobilenet_v1_coco_11_06_2017
USER app

# Make sure to allow enough time for the function to run
ENV read_timeout=10s
ENV write_timeout=10s
ENV exec_timeout=30s

ENV fprocess="python3 index.py"
EXPOSE 8080

ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"


HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
