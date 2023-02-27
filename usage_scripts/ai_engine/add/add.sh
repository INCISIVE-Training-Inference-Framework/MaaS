#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads an AI Engine to the MaaS

# --> PREREQUISITES
# - curl installed

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES

# main attributes
name="MNIST classifier" # str, unique
container_name="mnist-classifier" # str, must exist on the docker registry
owner="BSC" # str
description="debug AI Engine" # str
data_type='["breast_cancer_mammography"]' # list[str], possible values -> {breast_cancer_mammography, breast_cancer_mri, lung_cancer_x_ray, lung_cancer_ct_scan, lung_cancer_pet_ct_scan, colorectal_cancer_mri, prostate_cancer_mri}
role_type="classification" # str, possible values -> {classification, segmentation, report_generation}

# optional attributes (trl-cargs and ai-passport)
data_considerations="dummy" # str, optional
trl="dummy" # str, optional
ethics="dummy" # str, optional
caveats="dummy" # str, optional
metrics="dummy" # str, optional
license="dummy" # str, optional

# --> CODE
curl -X POST http://${maas_api_hostname}/api/ai_engines/ \
                            -H "Content-Type: application/json" \
                            --data "{
                            \"name\": \"${name}\",
                            \"container_name\": \"${container_name}\",
                            \"owner\": \"${owner}\",
                            \"description\": \"${description}\",
                            \"data_type\": ${data_type},
                            \"role_type\": \"${role_type}\",
                            \"data_considerations\": \"${data_considerations}\",
                            \"trl\": \"${trl}\",
                            \"ethics\": \"${ethics}\",
                            \"caveats\": \"${caveats}\",
                            \"metrics\": \"${metrics}\",
                            \"license\": \"${license}\"
                            }"

# --> SUCCESFULL OUTPUT
# code: 201
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
