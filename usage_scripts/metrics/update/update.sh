#!/bin/bash

# --> DESCRIPTION
# It is a script that updates a metric of an AI Engine model of the MaaS

# --> PREREQUISITES
# - curl installed
# - the metric has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
model_id=1

id=1
name="accuracy"
value=2.3
data_partner="data-partner-1"
data_partner_patients="[\"1\", \"2\"]"
description="accuracy metric"

# --> CODE                            
curl -X PUT http://${maas_api_hostname}/api/metrics/${id}/ \
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
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
