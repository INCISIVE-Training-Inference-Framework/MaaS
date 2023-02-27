#!/bin/bash

# --> DESCRIPTION
# It is a script that lists the available Evaluation Metrics of the MaaS. It also shows how to perform filtering and ordering.

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
filter_ai_model_id=1

# --> CODE
# list all available Evaluation Metrics
curl -X GET http://${maas_api_hostname}/api/evaluation_metrics/

# list all available Evaluation Metrics of the desired AI Model
curl -X GET http://${maas_api_hostname}/api/evaluation_metrics/?ai_model=${filter_ai_model_id}
# this kind of filtering can be done for the following Evaluation Metric attributes: ai_model, name and value

# list all Evaluation Metrics of the selected page. The response also includes two pointers next and previous for moving around the pages along the count parameter with the total amount of items. It is also possible to specify the number of items per page with the parameter page_size
curl -X GET http://${maas_api_hostname}/api/evaluation_metrics/?page=2

# list all Evaluation Metrics ordered by the updated_at date desc (by default they are sorted by created_at desc)
curl -X GET http://${maas_api_hostname}/api/evaluation_metrics/?sort=-updated_at
# this kind of sorting can be done for the following metric attributes: ai_model, name, value, created_at and updated_at

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
