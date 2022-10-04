#!/bin/bash

# --> DESCRIPTION
# It is a script that downloads an AI Engine docker image from the MaaS docker registry

# --> PREREQUISITES
# - docker installed
# - the AI Engine has been already uploaded to the MaaS docker registry and to the MaaS API

# --> REQUIRED GLOBAL VARIABLES
# - maas_docker_registry_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
container_name="mnist-classifier"
container_version="v1.0"

# --> CODE
docker pull ${maas_docker_registry_hostname}/${container_name}:${container_version}
