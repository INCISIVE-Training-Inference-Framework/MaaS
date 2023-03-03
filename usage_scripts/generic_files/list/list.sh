#!/bin/bash

# --> DESCRIPTION
# It is a script that lists the available Generic Files from the MaaS. It also shows how to perform filtering and ordering.

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
name="inference"

# --> CODE
# list all available Generic Files
curl -X GET http://${maas_api_hostname}/api/generic_files/

# list all available Evaluation Metrics with the desired name
curl -X GET http://${maas_api_hostname}/api/generic_files/?name=${name} # this kind of filtering can only be done with the name attribute

# list all Generic Files of the selected page. The response also includes two pointers next and previous for moving around the pages along the count parameter with the total amount of items. It is also possible to specify the number of items per page with the parameter page_size
curl -X GET http://${maas_api_hostname}/api/generic_files/?page=2

# list all Generic Files ordered by the created_at date asc (by default they are sorted by created_at desc)
curl -X GET http://${maas_api_hostname}/api/generic_files/?sort=created_at
# this kind of sorting can only be done with the created_at attribute

# --> SUCCESSFUL OUTPUT
# code: 200
# content: check successful_output.json for the output of the first request (all other requests follow the same format)

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
