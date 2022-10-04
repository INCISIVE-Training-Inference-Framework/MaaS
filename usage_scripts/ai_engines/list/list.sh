#!/bin/bash

# --> DESCRIPTION
# It is a script that lists the available AI Engines of the MaaS. It also shows how to perform filtering, paging and sorting.

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
filter_owner="bsc"

# --> CODE
# list all available AI Engines
curl -X GET http://${maas_api_hostname}/api/ai_engines/

# list all available AI Engines of the selected owner
curl -X GET http://${maas_api_hostname}/api/ai_engines/?developer=${filter_owner}
# this kind of filtering can be done for the following AI Engine attributes: name, container_name, container_version, owner and data_query

# list all AI Engines of the selected page. The response also includes two pointers next and previous for moving around the pages along the count parameter with the total amount of items. It is also possible to specify the number of items per page with the parameter page_size
curl -X GET http://${maas_api_hostname}/api/ai_engines/?page=2

# list all AI Engines ordered by the name desc (by default they are sorted by created_at desc)
curl -X GET http://${maas_api_hostname}/api/ai_engines/?sort=-name
# this kind of sorting can be done for the following AI Engine attributes: name, container_name, container_version, owner, data_query and created_at

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
