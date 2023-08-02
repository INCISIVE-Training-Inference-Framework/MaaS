# we use the slim image which is better optimized
FROM python:3.9-slim

# install os packages, some of them needed to install the dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential gcc git && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --upgrade pip
    
# define and create working directory
WORKDIR /usr/application

# install required python packages
# copy step is done separately to not reinstall the python packages when the code changes
COPY /requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# copy the files inside the working directory (the .gitignore file ignores the not necessary files)
COPY / .

# change directory permissions to allow access for not root users
RUN chmod -R a+rwX .

# specify command to start the container
WORKDIR /usr/application/app
ENV PYTHONUNBUFFERED=TRUE

# Define default timeout value for workers
ENV WORKERS_TIMEOUT=120
ENV WORKERS=3
RUN export WORKERS_TIMEOUT=${WORKERS_TIMEOUT} && \
	export WORKERS=${WORKERS}
# Launch the gunicorn from inside a shell to allow variables expansion
CMD ["sh", "-c", "exec gunicorn --bind :8000 --workers ${WORKERS} --timeout ${WORKERS_TIMEOUT} maas.wsgi:application"]

#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "maas.wsgi:application"]
# port to expose at runtime
EXPOSE 8000/tcp
