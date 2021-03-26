FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /code
COPY ./requirements.txt /code


RUN pip install -r requirements.txt --no-cache-dir

COPY . /code

ENTRYPOINT ["sh", "./entrypoint.sh"]