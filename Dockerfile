FROM python:3.6

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "./app.py"]
