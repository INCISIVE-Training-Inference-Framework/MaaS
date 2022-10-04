#!/bin/bash

# --> DESCRIPTION
# The deletion of images for now is not a supported feature in the official docker registry API.
# One option is to delete the manifest files that do conform the image tag and are not being used by other images.
# Another option is to push a new image with the same name which is the preferred one.
# For the last option, we need to delete the AI Engine metadata along all its models which is the use case that we are going to show in this script.

# --> PREREQUISITES
# - curl installed
# - the AI Engine has been already uploaded to the MaaS docker registry and to the MaaS API

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
curl -X DELETE http://${maas_api_hostname}/api/ai_engines/${id}/

# --> SUCCESFULL OUTPUT
# code: 204
# content: nothing

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
