#!/bin/bash

# --> DESCRIPTION
# It is a script that tries to upload an AI Model to the MaaS thorugh a specific method that, in case that the AI Model already exists, it updates it with the uploading content.

# --> PREREQUISITES
# - curl installed
# - the AI Engine Version has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES

# main attributes
ai_engine_version=1
ai_engine_version_user_vars="./auxiliary_files/user_vars.json"
name="epochs_1_optimizer_adam"
data_partners_patients="{\"data-partner-1\": [\"1\", \"2\"], \"data-partner-2\": [\"1\"]}"
description="new description"
contents="./auxiliary_files/contents.zip"

# optional attributes
merge_type="default"
parent_ai_model="null"

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/ai_models/update_or_create/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"ai_engine_version\": ${ai_engine_version},
                            \"name\": \"${name}\",
                            \"data_partners_patients\": ${data_partners_patients},
                            \"description\": \"${description}\",
                            \"merge_type\": \"${merge_type}\",
                            \"parent_ai_model\": ${parent_ai_model}
                            }" \
                            -F ai_engine_version_user_vars=@${ai_engine_version_user_vars} \
                            -F contents=@${contents}

# --> SUCCESFULL OUTPUT
# code: 201
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
