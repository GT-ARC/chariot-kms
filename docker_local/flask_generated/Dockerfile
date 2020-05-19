FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY setup.py /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]
ADD swagger_server /usr/src/app/swagger_server
EXPOSE 8080