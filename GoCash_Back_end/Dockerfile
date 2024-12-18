FROM python:3.8-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update -y

# Copy the requirements file and install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for media files
RUN mkdir /usr/src/app/media

COPY . .

