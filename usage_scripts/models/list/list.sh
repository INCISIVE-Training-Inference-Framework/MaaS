#!/bin/bash

# --> DESCRIPTION
# It is a script that lists the available AI Engine models of the MaaS. It also shows how to perform filtering.

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
filter_ai_engine_id=1

# --> CODE
# list all available models
curl -X GET http://${maas_api_hostname}/api/models/

# list all available models of the desired AI Engine
curl -X GET http://${maas_api_hostname}/api/models/?ai_engine=${filter_ai_engine_id}
# this kind of filtering can be done for the following model attributes: name, type, ai_engine and parent_model

# list all models of the selected page. The response also includes two pointers next and previous for moving around the pages along the count parameter with the total amount of items. It is also possible to specify the number of items per page with the parameter page_size
curl -X GET http://${maas_api_hostname}/api/models/?page=2

# list all models ordered by the updated_at date desc (by default they are sorted by created_at desc)
curl -X GET http://${maas_api_hostname}/api/ai_engines/?sort=-updated_at
# this kind of sorting can be done for the following model attributes: name, type, ai_engine, parent_model, created_at and updated_at

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
