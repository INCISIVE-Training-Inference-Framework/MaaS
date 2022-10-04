#!/bin/bash

# --> DESCRIPTION
# It is a script that deletes a metric of an AI Engine model from the MaaS

# --> PREREQUISITES
# - curl installed
# - the metric has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
curl -X DELETE http://${maas_api_hostname}/api/metrics/${id}/

# --> SUCCESFULL OUTPUT
# code: 204
# content: nothing

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
