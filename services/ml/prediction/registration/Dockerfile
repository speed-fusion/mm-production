FROM python:3.8

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install pulsar-client==2.9.1 fastai==1.0.61 pymysql redis unidecode pymongo

COPY . .

CMD ["python","-u","main.py"]