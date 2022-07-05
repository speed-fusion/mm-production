FROM python:3.8

WORKDIR /

COPY ./requirements.txt ./

RUN pip install pulsar-client==2.9.1 pandas numpy

COPY . .

CMD [ "python","-u","main.py" ]