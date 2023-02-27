#!/bin/bash

# --> DESCRIPTION
# It is a script that updates an Evaluation Metric of the MaaS
# Only PATCH method is allowed, PUT method is forbidden

# --> PREREQUISITES
# - curl installed
# - the Evaluation Metric has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# fields where update is permitted
value=2.3
description="something different"

# --> CODE                            
curl -X PATCH http://${maas_api_hostname}/api/evaluation_metrics/${id}/ \
                            -H "Content-Type:application/json" \
                            -d "{
                            \"value\": ${value},
                            \"description\":\"${description}\"
                            }"

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
