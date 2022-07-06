FROM python:3.8

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w 3", "-b", "0.0.0.0:5000", "main:app"]