#!/bin/bash

# --> DESCRIPTION
# It is a script that uploads an AI Engine Version to the MaaS

# --> PREREQUISITES
# - curl installed
# - the AI Engine has been already created

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES

# main attributes
ai_engine=1 # int, unique along container_version
container_version="latest" # str, unique along ai_engine
description="minor changes" # str
functionalities='["training_from_scratch", "training_from_pretrained_model", "evaluating_from_pretrained_model", "merging_models", "inferencing_from_pretrained_model"]' # list[str], possible values -> the ones exposed. This array must comply with the supplied user var files

# optional attributes
explains="false" # bool, optional
default_user_vars_training_from_scratch="./auxiliary_files/default_user_vars.json" # FILE, optional
default_user_vars_training_from_pretrained_model="./auxiliary_files/default_user_vars.json" # FILE, optional
default_user_vars_evaluating_from_pretrained_model="./auxiliary_files/default_user_vars.json" # FILE, optional
default_user_vars_merging_models="./auxiliary_files/default_user_vars.json" # FILE, optional
default_user_vars_inferencing_from_pretrained_model="./auxiliary_files/default_user_vars.json" # FILE, optional

# --> CODE
curl -X POST http://${maas_api_hostname}/api/ai_engines_versions/ \
                            -H "Content-Type:multipart/form-data" \
                            -F data="{
                            \"ai_engine\": ${ai_engine},
                            \"container_version\": \"${container_version}\",
                            \"description\": \"${description}\",
                            \"functionalities\": ${functionalities},
                            \"explains\": ${explains}
                            }" \
                            -F default_user_vars_training_from_scratch=@${default_user_vars_training_from_scratch} \
                            -F default_user_vars_training_from_pretrained_model=@${default_user_vars_training_from_pretrained_model} \
                            -F default_user_vars_evaluating_from_pretrained_model=@${default_user_vars_evaluating_from_pretrained_model} \
                            -F default_user_vars_merging_models=@${default_user_vars_merging_models} \
                            -F default_user_vars_inferencing_from_pretrained_model=@${default_user_vars_inferencing_from_pretrained_model}

# --> SUCCESSFUL OUTPUT
# code: 201
# content: check successful_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
