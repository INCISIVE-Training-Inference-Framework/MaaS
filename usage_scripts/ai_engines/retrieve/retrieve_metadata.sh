#!/bin/bash

# --> DESCRIPTION
# It is a script that retrieves an AI Engine from the MaaS API

# --> PREREQUISITES
# - curl and jq installed
# - the AI Engine has been already uploaded to the MaaS API

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
# obtain global information
response=$(curl -s -X GET http://${maas_api_hostname}/api/ai_engines/${id}/)
echo ${response}

# obtain configuration files' urls (no need to -> the urls are always the same, this step can be skip)
default_job_config_training_from_scratch_url=$(echo ${response} | jq -r '.default_job_config_training_from_scratch')
default_job_config_training_from_pretrained_model_url=$(echo ${response} | jq -r '.default_job_config_training_from_pretrained_model')
default_job_config_evaluating_from_pretrained_model_url=$(echo ${response} | jq -r '.default_job_config_evaluating_from_pretrained_model')
default_job_config_merging_models_url=$(echo ${response} | jq -r '.default_job_config_merging_models')
default_job_config_inferencing_from_pretrained_model_url=$(echo ${response} | jq -r '.default_job_config_inferencing_from_pretrained_model')

# download configuration files
curl -s -X GET ${default_job_config_training_from_scratch_url} --output default_job_config_training_from_scratch.json
curl -s -X GET ${default_job_config_training_from_pretrained_model_url} --output default_job_config_training_from_pretrained_model.json
curl -s -X GET ${default_job_config_evaluating_from_pretrained_model_url} --output default_job_config_evaluating_from_pretrained_model.json
curl -s -X GET ${default_job_config_merging_models_url} --output default_job_config_merging_models.json
curl -s -X GET ${default_job_config_inferencing_from_pretrained_model_url} --output default_job_config_inferencing_from_pretrained_model.json

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
