# FROM python:3.9
# ENV PYTHONUNBUFFERED 1
# RUN apt-get update && apt-get install -y \
#     mariadb-client default-libmysqlclient-dev
# RUN mkdir /app
# WORKDIR /app
# COPY . /app/
# RUN pip install --no-cache-dir -r requirements.txt
# EXPOSE 8001
# CMD [ "python","manage.py","runserver","0.0.0.0:8001" ]


FROM docker.io/python:3.11.4 AS BASE
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app
ARG REQUIREMENTS_FILE
COPY ./requirements.txt ./
COPY ./$REQUIREMENTS_FILE ./
RUN pip install -r $REQUIREMENTS_FILE
COPY . .
EXPOSE 8000

