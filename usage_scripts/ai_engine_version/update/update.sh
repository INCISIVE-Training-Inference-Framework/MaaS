#!/bin/bash

# --> DESCRIPTION
# It is a script that updates an AI Engine Version of the MaaS
# Only PATCH method is allowed, PUT method is forbidden

# --> PREREQUISITES
# - curl installed
# - the AI Engine Version has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# fields where update is permitted
description="something different"

# --> CODE
curl -X PATCH http://${maas_api_hostname}/api/ai_engines_versions/${id}/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"description\": \"${description}\"
                            }"

# --> SUCCESSFUL OUTPUT
# code: 200
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
