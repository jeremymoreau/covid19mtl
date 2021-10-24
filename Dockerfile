FROM python:3.9.7-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
COPY ./requirements.txt /tmp/
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
ADD ./ /app

# ENTRYPOINT [ "gunicorn", "app:server", "--preload" ]
