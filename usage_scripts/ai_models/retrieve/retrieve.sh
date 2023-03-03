#!/bin/bash

# --> DESCRIPTION
# It is a script that retrieves an AI Model from the MaaS

# --> PREREQUISITES
# - curl and jq installed
# - the AI Model has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
# obtain global information
curl -X GET http://${maas_api_hostname}/api/ai_models/${id}/

# obtain user vars and contents files urls (no need to -> the url is always the same, this step can be skip)
ai_engine_version_user_vars_url=$(curl -s -X GET http://${maas_api_hostname}/api/ai_models/${id}/ | jq -r '.ai_engine_version_user_vars')
contents_url=$(curl -s -X GET http://${maas_api_hostname}/api/ai_models/${id}/ | jq -r '.contents')

# download files
curl -s -X GET ${ai_engine_version_user_vars_url} --output ai_engine_version_user_vars.json
curl -s -X GET ${contents_url} --output contents.zip

# --> SUCCESSFUL OUTPUT
# code: 200
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
