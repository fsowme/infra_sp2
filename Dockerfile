FROM python:3.8.5

RUN mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
CMD rm posts/migrations/000* && rm -r posts/migrations/__pycache__ && \
    rm users/migrations/000* && rm -r users/migrations/__pycache__ && \
    python manage.py makemigrations && python manage.py migrate

CMD gunicorn yatube.wsgi:application --bind 0.0.0.0:8000
