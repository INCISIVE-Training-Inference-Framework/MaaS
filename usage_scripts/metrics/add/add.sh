#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads a metric for an AI Engine model to the MaaS

# --> PREREQUISITES
# - curl installed
# - the AI Engine model has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
model_id=1

name="accuracy"
value=1.5
data_partner="data-partner-1"
data_partner_patients="[\"1\", \"2\"]"
description="accuracy metric"

# --> CODE                            
curl -X POST http://${maas_api_hostname}/api/metrics/ \
                            -H "Content-Type:application/json" \
                            -d "{
                            \"name\":\"${name}\",
                            \"value\":\"${value}\",
                            \"data_partner\":\"${data_partner}\",
                            \"data_partner_patients\":${data_partner_patients},
                            \"description\":\"${description}\",
                            \"model\":\"${model_id}\"
                            }"

# --> SUCCESFULL OUTPUT
# code: 201
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
