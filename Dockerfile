FROM python:3.8.5
RUN apt-get update && apt-get upgrade -y && python -m pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN  pip install -r requirements.txt
COPY . /code

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
