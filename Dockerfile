FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /places_remember
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD python places_remember/manage.py runserver 0.0.0.0:8000
