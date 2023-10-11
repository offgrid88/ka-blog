# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt
RUN apt update && apt install -y curl
RUN mkdir -p /usr/src/app/build
RUN python3  /usr/src/app/wsgi.py build
# copy project
#COPY . /usr/src/app/
