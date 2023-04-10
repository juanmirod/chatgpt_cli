FROM python:3.9-slim-buster

# Copy only the requirements file first so that the docker cache is only
# modified if the dependencies change
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

# Set the entrypoint for the container to be the Python script
ENTRYPOINT [ "python", "start.py" ] 
