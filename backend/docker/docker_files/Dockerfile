# Base image for the application
FROM python:3.10-slim

# Environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Update package lists and install dependencies
RUN set -e && \
    apt-get update && \
    apt-get install -y netcat-openbsd gettext && \
    apt-get install -y python3-pip ;


# Create the application directory
RUN mkdir /code

# Copy all files from the build context to the directory
COPY . /code/

# Set the working directory for the container
WORKDIR /code

# Install Python dependencies from requirements.txt and upgrade pip
RUN set -e && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /code/requirements.txt

# Make the entrypoint script executable
RUN chmod +x /code/docker/entrypoints/entrypoint.sh

# Expose port 8000 for container communication
EXPOSE 8000

# Entrypoint script to run the application
ENTRYPOINT ["/code/docker/entrypoints/entrypoint.sh"]