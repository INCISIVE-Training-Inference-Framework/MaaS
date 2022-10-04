#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads an inference result to the MaaS

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
execution_id=1
result_files="./auxiliary_files/result_files.zip"

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/inference_results/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"execution_id\": \"${execution_id}\"
                            }" \
                            -F result_files=@${result_files}

# --> SUCCESFULL OUTPUT
# code: 201
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
