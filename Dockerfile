# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN pip install --upgrade pip

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

FROM debian:latest
RUN apt-get update && apt-get install -y docker.io

# Install smbus
USER root
RUN  apt-get update && apt-get install -y python3-smbus

COPY Serial.py .
COPY USBdriver.py .
COPY Ethernetdriver.py .
COPY supported_frequency.py .

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "Serial.py"]
