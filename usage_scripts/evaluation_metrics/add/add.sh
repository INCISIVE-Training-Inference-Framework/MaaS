#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads an Evaluation Metric to the MaaS

# --> PREREQUISITES
# - curl installed
# - the AI Model has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES

# main attributes
ai_model=1 # int, unique along name and data_partner_patients
name="accuracy" # str
data_partners_patients="{\"data-partner-1\": [\"1\", \"2\"]}" # dict[str:list[str]], the partners must exist on the platform, unique along ai_model and name
value=1.5 # float

# optional attributes
description="accuracy metric" # str, optional

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/evaluation_metrics/ \
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
