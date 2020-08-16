FROM python:3
COPY .bashrc /
RUN apt-get update && apt-get -y install \
	vim 
ENV PYTHONUNBUFFERED 1
RUN mkdir code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/

WORKDIR /code/

CMD gunicorn dbsite.wsgi