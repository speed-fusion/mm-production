FROM python:3.8

WORKDIR /usr/src/app

RUN pip install sklearn pulsar-client==2.9.1 redis unidecode pymongo

COPY . .


CMD ["python","-u","main.py"]