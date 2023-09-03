FROM python:3.11

WORKDIR /app

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD ./ ./

CMD [ "python3", "-u", "./main.py" ]