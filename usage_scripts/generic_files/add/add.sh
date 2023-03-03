#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads a Generic File to the MaaS

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
name="inference results of execution 18" # str
contents="./auxiliary_files/contents.zip" # FILE

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/generic_files/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"name\": \"${name}\"
                            }" \
                            -F contents=@${contents}

# --> SUCCESSFUL OUTPUT
# code: 201
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
