#!/bin/bash

# --> DESCRIPTION
# It is a script that tries to upload an Evaluation Metric to the MaaS thorugh a specific method that, in case that the AI Model already exists, it updates it with the uploading content.

# --> PREREQUISITES
# - curl installed
# - the AI Model has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES

# main attributes
ai_model=1
name="accuracy"
data_partners_patients="{\"data-partner-1\": [\"1\", \"2\"]}"
value=1.5

# optional attributes
description="something new"

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/evaluation_metrics/update_or_create/ \
                            -H "Content-Type:application/json" \
                            -d "{
                            \"ai_model\":${ai_model},
                            \"name\":\"${name}\",
                            \"data_partners_patients\":${data_partners_patients},
                            \"value\":${value},
                            \"description\":\"${description}\"
                            }"

# --> SUCCESSFUL OUTPUT
# code: 201
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
