#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads a dockerized application to the MaaS

# --> PREREQUISITES
# - docker and curl installed
# - the application docker image has been already created

# --> REQUIRED GLOBAL VARIABLES
# - maas_docker_registry_hostname
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
name="MNIST classifier"
container_name="mnist-classifier"
container_version="latest"
owner="bsc"
job_use_cases="[\"training_from_scratch\", \"training_from_pretrained_model\", \"evaluating_from_pretrained_model\", \"merging_models\", \"inferencing_from_pretrained_model\"]" # less values are possible, only one is mandatory. This array must comply with the supplied configuration files
data_query="data_query"
description="debug AI Engine"
default_job_config_training_from_scratch="./auxiliary_files/default_job_config.json"
default_job_config_training_from_pretrained_model="./auxiliary_files/default_job_config.json"
default_job_config_evaluating_from_pretrained_model="./auxiliary_files/default_job_config.json"
default_job_config_merging_models="./auxiliary_files/default_job_config.json"
default_job_config_inferencing_from_pretrained_model="./auxiliary_files/default_job_config.json"

# --> CODE
# upload docker image to MaaS docker registry
docker tag ${container_name}:${container_version} ${maas_docker_registry_hostname}/${container_name}:${container_version}
docker push ${maas_docker_registry_hostname}/${container_name}:${container_version}

# upload AI Engine metadata to MaaS service API
# we do this step after uploading the docker image because once the metadata is uploaded to the MaaS API, the users can try to download the docker image
curl -X POST http://${maas_api_hostname}/api/ai_engines/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"name\": \"${name}\",
                            \"container_name\": \"${container_name}\",
                            \"container_version\": \"${container_version}\",
                            \"owner\": \"${owner}\",
                            \"job_use_cases\": ${job_use_cases},
                            \"data_query\": \"${data_query}\",
                            \"description\": \"${description}\"
                            }" \
                            -F default_job_config_training_from_scratch=@${default_job_config_training_from_scratch} \
                            -F default_job_config_training_from_pretrained_model=@${default_job_config_training_from_pretrained_model} \
                            -F default_job_config_evaluating_from_pretrained_model=@${default_job_config_evaluating_from_pretrained_model} \
                            -F default_job_config_merging_models=@${default_job_config_merging_models} \
                            -F default_job_config_inferencing_from_pretrained_model=@${default_job_config_inferencing_from_pretrained_model}

# --> SUCCESFULL OUTPUT
# code: 201
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
