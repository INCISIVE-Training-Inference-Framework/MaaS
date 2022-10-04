#!/bin/bash

# --> DESCRIPTION
# It is a script that lists the available inference results from the MaaS.

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
# none

# --> CODE
# list all available inference results
curl -X GET http://${maas_api_hostname}/api/inference_results/

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
