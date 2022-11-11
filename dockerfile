FROM tensorflow/tensorflow:2.8.0

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

CMD uvicorn main:app --host=0.0.0.0 --port 8000 --log-config log.ini
