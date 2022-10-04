#!/bin/bash

# --> DESCRIPTION
# It is a script that retrieves an inference result from the MaaS

# --> PREREQUISITES
# - curl and jq installed
# - the inference result has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
# obtain global information
response=$(curl -s -X GET http://${maas_api_hostname}/api/inference_results/${id}/)
echo ${response}

# obtain result files' url (no need to -> the url is always the same, this step can be skip)
result_files_url=$(echo ${response} | jq -r '.result_files')

# download result files
curl -s -X GET ${result_files_url} --output result_files.zip

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
