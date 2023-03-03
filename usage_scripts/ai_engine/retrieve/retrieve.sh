#!/bin/bash

# --> DESCRIPTION
# It is a script that retrieves an AI Engine from the MaaS

# --> PREREQUISITES
# - curl installed
# - the AI Engine has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
# obtain global information
response=$(curl -s -X GET http://${maas_api_hostname}/api/ai_engines/${id}/)
echo ${response}

# --> SUCCESSFUL OUTPUT
# code: 200
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
