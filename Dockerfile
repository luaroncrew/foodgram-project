FROM python:slim

RUN mkdir -p /app

ENV APP_HOME=/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt --no-cache-dir

COPY . $APP_HOME

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000