#!/bin/bash

# --> DESCRIPTION
# It is a script that retrieves an AI Engine Version from the MaaS

# --> PREREQUISITES
# - curl and jq installed
# - the AI Engine Version has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
# obtain global information
response=$(curl -s -X GET http://${maas_api_hostname}/api/ai_engines_versions/${id}/)
echo ${response}

# obtain user vars' urls (no need to -> the urls are always the same, this step can be skip)
default_user_vars_training_from_scratch_url=$(echo ${response} | jq -r '.default_user_vars_training_from_scratch')
default_user_vars_training_from_pretrained_model_url=$(echo ${response} | jq -r '.default_user_vars_training_from_pretrained_model')
default_user_vars_evaluating_from_pretrained_model_url=$(echo ${response} | jq -r '.default_user_vars_evaluating_from_pretrained_model')
default_user_vars_merging_models_url=$(echo ${response} | jq -r '.default_user_vars_merging_models')
default_user_vars_inferencing_from_pretrained_model_url=$(echo ${response} | jq -r '.default_user_vars_inferencing_from_pretrained_model')

# download user vars files
curl -s -X GET ${default_user_vars_training_from_scratch_url} --output default_user_vars_training_from_scratch.json
curl -s -X GET ${default_user_vars_training_from_pretrained_model_url} --output default_user_vars_training_from_pretrained_model.json
curl -s -X GET ${default_user_vars_evaluating_from_pretrained_model_url} --output default_user_vars_evaluating_from_pretrained_model.json
curl -s -X GET ${default_user_vars_merging_models_url} --output default_user_vars_merging_models.json
curl -s -X GET ${default_user_vars_inferencing_from_pretrained_model_url} --output default_user_vars_inferencing_from_pretrained_model.json

# --> SUCCESSFUL OUTPUT
# code: 200
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
