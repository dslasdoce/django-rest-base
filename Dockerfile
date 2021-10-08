# pull official base image
FROM python:3.8.1

ARG DJANGO_SETTINGS_MODULE
ARG DB_NAME
ARG DB_PASSWORD
ARG DB_USER
ARG DB_HOST
ARG FIREBASE_CREDENTIALS
ARG GS_CREDENTIALS
ARG CONVERTER_URL
ARG BASE_DYNAMIC_LINK
ARG ANDROID_APN

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NEW_RELIC_CONFIG_FILE=newrelic.ini
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE}
ENV DB_NAME ${DB_NAME}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_USER ${DB_USER}
ENV DB_HOST ${DB_HOST}
ENV BASE_DYNAMIC_LINK ${BASE_DYNAMIC_LINK}
ENV ANDROID_APN ${ANDROID_APN}
ENV FIREBASE_CREDENTIALS ${FIREBASE_CREDENTIALS}
ENV GS_CREDENTIALS ${GS_CREDENTIALS}

EXPOSE 587/tcp
EXPOSE 587/udp


# create root directory for our project in the container
RUN mkdir /your-project-name

# Set the working directory to /your-project-name
WORKDIR /your-project-name

# Copy the current directory contents into the container at /your-project-name
ADD . /your-project-name/

# install dependencies
RUN pip install -r requirements.txt

# run unit tests
#RUN python manage.py test apps --settings=core.settings.test --no-input

ENTRYPOINT ["/your-project-name/docker/web_entrypoint.sh"]
