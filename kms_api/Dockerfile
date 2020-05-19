FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY setup.py /usr/src/app/

ADD swagger_server /usr/src/app/swagger_server
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]
EXPOSE 8080