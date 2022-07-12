FROM python:3.8

WORKDIR /

RUN pip install pulsar-client==2.9.1 pandas numpy pymongo requests Pillow

COPY . .

CMD [ "python","-u","main.py" ]