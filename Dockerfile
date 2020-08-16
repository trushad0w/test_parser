FROM python:3.7-alpine

WORKDIR /dist

RUN apk add --update --no-cache \
        build-base musl-dev postgresql-dev postgresql-contrib \
        linux-headers libpq openssl-dev libffi-dev \
         libxml2-dev libxslt-dev python3-dev \
    && pip3 install --upgrade pip

COPY . /dist

RUN pip install -r requirements

CMD ["python", "manage.py", "runserver"]