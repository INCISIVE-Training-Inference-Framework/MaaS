#!/bin/bash

# --> DESCRIPTION
# It is a script that updates an AI Engine of the MaaS
# Only PATCH method is allowed, PUT method is forbidden

# --> PREREQUISITES
# - curl installed
# - the AI Engine has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# fields where update is permitted
name="MNIST classifier"
owner="BSC"
description="debug AI Engine"
data_type="[\"breast_cancer_mammography\"]"
role_type="classification"
data_considerations="something different"
trl="dummy"
ethics="dummy"
caveats="dummy"
metrics="dummy"
license="dummy"

# --> CODE
curl -X PATCH http://${maas_api_hostname}/api/ai_engines/${id}/ \
                            -H "Content-Type: application/json" \
                            --data "{
                            \"name\": \"${name}\",
                            \"owner\": \"${owner}\",
                            \"description\": \"${description}\",
                            \"data_type\": ${data_type},
                            \"role_type\": \"${role_type}\",
                            \"data_considerations\": \"${data_considerations}\",
                            \"trl\": \"${trl}\",
                            \"ethics\": \"${ethics}\",
                            \"caveats\": \"${caveats}\",
                            \"metrics\": \"${metrics}\",
                            \"license\": \"${license}\"
                            }"

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
