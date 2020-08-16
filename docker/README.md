# Django_2.0_Docker
Necessary files to create docker container for django2.0

## How to start things up
Make sure you have docker and docker compose installed.
From the directory with the Dockerfile in it, type the following commands:

```
docker-compose up -d
docker-compose exec web bash ## This will get you into the container's bash shell
## from within the container
django-admin startproject project_name
cd project_name
python manage.py runserver
```

The above commands will start up a django project and run the server.
You can access the server (or rather the starting page) from your host machine by accessing `localhost:8000`.

## Details
### docker-compose.yml web
  - mounts current directory to docker
  - portforward 8000:8000
  - see docker-compose.yml for more info

### docker-compose.yml db
  - uses postgres
  - backs up data to db-data (docker volume)
  - see docker-compose.yml for more info

### Dockerfile
  - Mostly inspired by https://docs.docker.com/compose/django/
  - overwrites runserver.py from django package to change the default port to 0.0.0.0 from 127.0.0.1 so that the running server can be accessed from the host machine.

### requirements.txt
  - Mostly inspired by https://docs.docker.com/compose/django/
  - Adds "pillow" for media management.

### runserver.py
  - as explained above, used by Dockerfile to overwrite default runserver.py to change the default port.
