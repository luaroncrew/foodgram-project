FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir /code
COPY ./requirements.txt /code

WORKDIR /code
RUN pip install -r requirements.txt --no-cache-dir

COPY . /code

ENTRYPOINT ["sh", "./entrypoint.sh"]