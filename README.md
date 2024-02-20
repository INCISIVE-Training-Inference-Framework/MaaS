# MaaS
_This component was created as an output of the INCISIVE European project software, forming part of the final platform_

## Introduction
The MaaS is responsible for defining and storing the main AI concepts of the platform. These concepts are used and retrieved from the other components to perform the AI functionalities.

Check the last version of the D.3.X report for the full abstract description of the component, its functionalities and the definition of all concepts.

## Implementation
The MaaS is a simple API that can run all its corresponding use cases. It is implemented in the Python programming language, and it is based on the Django framework. Before developing further the component, please check the official documentation of [Django](https://docs.djangoproject.com/en/4.2/) along the [quick start tutorial](https://docs.djangoproject.com/en/4.2/intro/). Also, it is recommended to check the documentation of the [REST framework](https://www.django-rest-framework.org/) of Django.

Concerning the storage, the MaaS manages both a relational database and a file system storage. The file system storage is administrated directly by Django inside the file system of the component, whereas the relational database uses a framework. It is configured to use a SQLite database in the development environment and an **external** Postgres database in the production environment. The file system storage is used to save all data corresponding natively to files, whereas the relational database stores all other types of data along the pointers to the locations of the stored files.

## How to set up
This section describes how to set up the component with docker and directly with python. 

All the configuration is done through the [Settings](https://docs.djangoproject.com/en/4.2/ref/settings/) environment variables of Django. The important variables are the following:
- DEBUG (str, `true`or `false`): being `true` the development environment and `false` the production environment. This is used to set up, between other things, the different types of database.
- MEDIA_ROOT && MEDIA_URL (str): root path location to store the files in the file system storage.
- VALID_DATA_PARTNERS (list[str]): the nodes that are valid data providers (federated nodes), where training and evaluation AI Executions are meant to be run.
- VALID_AI_ENGINE_FUNCTIONALITIES(list[str]): the values to accept as functionalities.
- VALID_AI_ENGINE_DATA_TYPES(list[str]): the values to accept as data types.
- VALID_AI_ENGINE_ROLE_TYPES(list[str]): the values to accept as role types.

### Python directly
Follows a list with the instructions to set up the component with python directly:
- install python3.9 and pip 
- install the python libraries specified in the requirements.txt file
- create the SQLite database (check the Django documentation for a thorough description): `python3 app/manage.py migrate`
- run the component (check the Django documentation for a thorough description), add `DEBUG=true` to use the SQLite database: `python3 app/manage.py runserver 127.0.0.2:8000`

Notice that both the IP and the port can be changed, remember to modify accordingly the [ALLOWED_HOSTS](https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts) environment variable of Django.

### Docker
Follows a list with the instructions to set up the component with docker. Notice that the docker deployment uses Gunicorn as HTTP server since Django only provides a development server.
- create the docker image: `docker build -f Dockerfile -t orchestrator .`
- run a docker container (use the desired parameters): `docker run -it --rm --network host orchestrator`

The default IP and port is 127.0.0.1:8000, it can be changed inside the Dockerfile.

### Docker compose
You can also run the required MaaS services through the included [`docker-compose.integration.yaml`](/docker-compose.integration.yml).

This deployment also provides a Swagger API web server in port 8080 (can be changed via `.env` file) and an alpine-based service to interact with the rest of the services in the same network.

Just remember to create your own `.env` file with your environment variables (you can use [`dotenv_example_docker_compose_example.env`](/dotenv_example_docker_compose_example.env)) as a template 

Once done, build and run the services with the following commands:
```bash
# Build the images
docker compose -f docker-compose.integration.yaml build
# Run the services
docker compose -f docker-compose.integration.yaml up
```

## How to use
Once the MaaS is set up and its API is running on the determined location, it can be reached in the different endpoints of its API for performing all the functionalities. The way to run all functionalities is showed in a practical manner with shell scripts that can be found in the directory named as *usage_scripts/* in this same repository.

The full list of functionalities is the following (check the official documentation of the component for the description of the concepts):

- AI Engines
  - Listing all available AI Engines (filtering included)
  - Retrieving an AI Engine
  - Adding a new AI Engine
  - Deleting an existing AI Engine
- AI Engine Versions
  - Listing all available AI Engine Versions (filtering included)
  - Retrieving an AI Engine Version along its default configurations
  - Adding a new AI Engine Version
  - Deleting an existing AI Engine Version
  - Listing all AI Engine Versions that the given one explains (XAI)
  - Listing all AI Engine Versions that explain the given one (XAI)
- AI Models
  - Listing all available AI Models (filtering included)
  - Retrieving an AI Model along its contents and configuration
  - Adding a new AI Model
  - Deleting an existing AI Model
  - Updating an existing AI Model
- Evaluation Metrics
  - Listing all available Evaluation Metrics (filtering included)
  - Retrieving an Evaluation Metric
  - Adding a new Evaluation Metric
  - Deleting an existing Evaluation Metric
  - Updating an existing Evaluation Metric
- Inference Results
  - Listing all available Inference Results
  - Listing the contents of an Inference Result
  - Retrieving an Inference Result along its contents (individually or packed)
  - Adding a new Inference Result
  - Deleting an existing Inference Result

Concerning the database, here are the most useful commands to manage it (check the official Django documentation for a full list):
- Create a database migration -> `python3 app/manage.py makemigrations`. This should be executed every time there is a codewise change in the database structure. It will generate a file that will be used by the current database deployments to update their structure.
- Apply a database migration -> `python3 app/manage.py migrate`. It will update the database according to the available migration files.
- Clean all data from the database tables -> `python3 app/manage.py flush && rm -r storage/files/*`. It will delete all the data from the database and all the files from the filesystem storage (the django-cleanup module does not work with the flush command unfortunately).
- Reset the database -> `python3 app/manage.py migrate main zero`. It will clean all the data and tables from the database.
 
## API documentation
The Docker compose deployment also provides a Swagger API web server in port 8080 and an alpine-based service to interact with the rest of the services in the same network: 
- The MaaS init script will auto-generate the static files and the API schema YAML required for Swagger
- The Swagger container depends on the MaaS container being healthy, so it should always execute with the static files already created