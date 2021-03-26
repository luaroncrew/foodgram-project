FROM python:3.8-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir code
COPY . /code
RUN pip install -r /code/requirements.txt &&\
    python code/manage.py migrate --no-input &&\
    python code/manage.py loaddata fixtures.json

CMD foodgram.wsgi:application --bind 0.0.0.0:8000