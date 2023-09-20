#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads an AI Model to the MaaS

# --> PREREQUISITES
# - curl installed
# - the AI Engine Version has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES

# main attributes
ai_engine_version=1 # int, unique along name and data_partners_patients
ai_engine_version_user_vars="./auxiliary_files/user_vars.json" # FILE
name="epochs_1_optimizer_adam" # str, unique along ai_engine_version_id and data_partners_patients
data_partners_patients="{\"data-partner-1\": [\"1\", \"2\"], \"data-partner-2\": [\"1\"]}" # dict[str:list[str]], the partners must exist on the platform, unique along ai_engine_version_id and name
description="dummy description" # str
contents="./auxiliary_files/contents.zip" # FILE

# optional attributes
merge_type="default" # str, optional
parent_ai_model="null" # int, optional, identifier of the parent AI Model, it must exist
download_resume_retries=2 # int greater than 0, optional. Default value is 4

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/ai_models/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"ai_engine_version\": ${ai_engine_version},
                            \"name\": \"${name}\",
                            \"data_partners_patients\": ${data_partners_patients},
                            \"description\": \"${description}\",
                            \"merge_type\": \"${merge_type}\",
                            \"parent_ai_model\": ${parent_ai_model},
			    \"download_resume_retries\": ${download_resume_retries}
                            }" \
                            -F ai_engine_version_user_vars=@${ai_engine_version_user_vars} \
                            -F contents=@${contents}

# --> SUCCESSFUL OUTPUT
# code: 201
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
