# YamDB API

Educational project made with Django-framework and Django REST framework.
API based on my training yatube project (Django REST framework). Ready to up in Docker.

## Getting Started

These instructions will get you a copy of the project up and running in docker container for development and testing purposes. 

### Prerequisites

Docker and docker-compose must be installed in your system. More information you can take on official site of Docker.

[docker](https://docs.docker.com/engine/install/)

[docker-compose](https://docs.docker.com/compose/install/)


### Installing

Clone this project and go to new folder

```
git clone git@github.com:fsowme/infra_sp2.git
cd infra_sp2/
```

Create .env file with parameters for connecting to the base.

```
touch .env
nano .env
```
.env example:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

```
Save and exit from .env file and run command to create docker containers. After this one you will have two containers, one of them with postgresql database and one with web project.
```
docker-compose up -d

```
After creating enter the container with web project (show running containers: sudo docker-compose ps). Update packages and pip, make migrations and superuser
```
docker exec -it <container_name> bash
apt-get update && apt-get upgrade -y
python -m pip install --upgrade pip
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

```

And now you can start browser and open redoc page http://127.0.0.1:8000/redoc/ with information about API and admin page http://127.0.0.1:8000/admin/

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django REST framework](https://www.django-rest-framework.org/) - API framework


## Authors

* **Vitalii Mikhailov**

