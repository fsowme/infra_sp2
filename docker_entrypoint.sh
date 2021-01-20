#!/bin/bash
apt-get update && apt-get upgrade -y
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000