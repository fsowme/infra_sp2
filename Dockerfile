FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN  python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . /code
ENTRYPOINT ["./docker_entrypoint.sh"]
# pytest требует CMD
# CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
