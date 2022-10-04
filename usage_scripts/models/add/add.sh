#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads an AI Engine model to the MaaS

# --> PREREQUISITES
# - curl installed
# - the AI Engine has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
ai_engine_id=1

name="epochs_1_optimizer_adam"
type="default"
data_partners_patients="{\"data-partner-1\": [\"1\", \"2\"], \"data-partner-2\": [\"1\"]}"
description="dummy description"
model_files="./auxiliary_files/model_files.zip"
# it is also possible to add the parent_model attribute with the id of an already existing model

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/models/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"name\": \"${name}\",
                            \"type\": \"${type}\",
                            \"data_partners_patients\": ${data_partners_patients},
                            \"description\": \"${description}\",
                            \"ai_engine\": ${ai_engine_id}
                            }" \
                            -F model_files=@${model_files}

# --> SUCCESFULL OUTPUT
# code: 201
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
