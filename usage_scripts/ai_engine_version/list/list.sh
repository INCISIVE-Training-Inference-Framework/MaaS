#!/bin/bash

# --> DESCRIPTION
# It is a script that lists the available AI Engines Versions of the MaaS. It also shows how to perform filtering, paging and sorting.

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
filter_ai_engine=1

# --> CODE
# list all available AI Engines Versions
curl -X GET http://${maas_api_hostname}/api/ai_engines_versions/

# list all available AI Engines Versions of the selected owner
curl -X GET http://${maas_api_hostname}/api/ai_engines_versions/?ai_engine=${filter_ai_engine}
# this kind of filtering can be done for the following AI Engine Version attributes: ai_engine and container_version

# list all AI Engines Versions of the selected page. The response also includes two pointers next and previous for moving around the pages along the count parameter with the total amount of items. It is also possible to specify the number of items per page with the parameter page_size
curl -X GET http://${maas_api_hostname}/api/ai_engines_versions/?page=2

# list all AI Engines Versions ordered by the ai_engine desc (by default they are sorted by created_at desc)
curl -X GET http://${maas_api_hostname}/api/ai_engines_versions/?sort=-ai_engine
# this kind of sorting can be done for the following AI Engine Versions attributes: ai_engine, container_version, created_at and updated_at

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
