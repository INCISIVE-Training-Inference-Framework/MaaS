#!/bin/bash

# --> DESCRIPTION
# It is a script that lists the available AI Models of the MaaS. It also shows how to perform filtering and ordering.

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
filter_ai_engine_version_id=1

# --> CODE
# list all available AI Models
curl -X GET http://${maas_api_hostname}/api/ai_models/

# list all available AI Models of the desired AI Engine Version
curl -X GET http://${maas_api_hostname}/api/ai_models/?ai_engine_version=${filter_ai_engine_version_id}
# this kind of filtering can be done for the following attributes: ai_engine_version, name, merge_type and parent_ai_model

# list all AI Models of the selected page. The response also includes two pointers next and previous for moving around the pages along the count parameter with the total amount of items. It is also possible to specify the number of items per page with the parameter page_size
curl -X GET http://${maas_api_hostname}/api/ai_models/?page=2

# list all AI Models ordered by the updated_at date desc (by default they are sorted by created_at desc)
curl -X GET http://${maas_api_hostname}/api/ai_models/?sort=-updated_at
# this kind of sorting can be done for the following model attributes: ai_engine_version, name, merge_type and parent_ai_model, created_at and updated_at

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
