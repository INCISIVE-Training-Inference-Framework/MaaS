#!/bin/bash

# --> DESCRIPTION
# It is a script that retrieves an AI Engine model from the MaaS

# --> PREREQUISITES
# - curl and jq installed
# - the AI Engine model has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
# obtain global information
curl -X GET http://${maas_api_hostname}/api/models/${id}/

# obtain model files url (no need to -> the url is always the same, this step can be skip)
model_files_url=$(curl -s -X GET http://${maas_api_hostname}/api/models/${id}/ | jq -r '.model_files')

# download model files
curl -s -X GET ${model_files_url} --output model_files.zip

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
