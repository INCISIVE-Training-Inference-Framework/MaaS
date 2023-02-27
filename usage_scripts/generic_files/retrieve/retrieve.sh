#!/bin/bash

# --> DESCRIPTION
# It is a script that retrieves a Generic File from the MaaS. Including how to list the different files inside, how to download them separately and how to download them in a pack.

# --> PREREQUISITES
# - curl and jq installed
# - the Generic File has been already uploaded to the MaaS

# --> REQUIRED GLOBAL VARIABLES
# - maas_api_hostname
source ../global_variables.sh

# --> REQUIRED LOCAL VARIABLES
id=1

# --> CODE
# obtain metadata
response=$(curl -s -X GET http://${maas_api_hostname}/api/generic_files/${id}/)
echo ${response}

# obtain the distinct urls (no need to -> the urls are always the same, this step can be skip)
listed_contents_url=$(echo ${response} | jq -r '.listed_contents')
individual_contents_download_url=$(echo ${response} | jq -r '.individual_contents_download')
packed_contents_download_url=$(echo ${response} | jq -r '.packed_contents_download')

# list contents
response=$(curl -s -X GET ${listed_contents_url})
echo ${response}

# download individual files
file_path="contents/folder_1/image_2.jpg"
curl -s -X GET ${individual_contents_download_url}?file_path=${file_path} --output individual_file.png

# download all contents
curl -s -X GET ${packed_contents_download_url} --output contents.zip

# --> SUCCESFULL OUTPUT
# code: 200
# content: check succesfull_output.json

# --> FAILED OUTPUT
# returns 4XX for bad requests along the reason and 5XX for internal errors
