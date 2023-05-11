FROM python:3.9

ENV FLASK_APP=app.py

COPY requirements.txt /pythonProject/requirements.txt

WORKDIR /pythonProject

ADD . /pythonProject/

RUN pip install -r requirements.txt

CMD [ "python","./app.py"]

