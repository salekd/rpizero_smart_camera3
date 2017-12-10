#!/bin/bash
docker swarm init
cd ../faas
./deploy_stack.sh
./deploy_extended.sh
cd ../rpizero_smart_camera3
faas-cli deploy --image faas-s3-email --name faas-s3-email
faas-cli deploy --image faas-mobilenet --name faas-mobilenet --fprocess "python index_output_image.py"
