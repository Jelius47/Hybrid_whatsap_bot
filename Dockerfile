# Use the lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Copy requirements.txt and install dependencies
COPY . ./

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# RUN apt-get update && apt-get install -y httpie
# RUN apk add --no-cache httpie

# RUN apt-get update && apt-get install -y curl


# Copy the application source code into the container
COPY ./app  ./app
COPY ./run.py ./

EXPOSE 8000
# Run the Flask application
CMD ["python", "run.py"]
