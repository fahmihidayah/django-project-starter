FROM python:3.9.6-alpine

RUN mkdir app

WORKDIR app

RUN mkdir logs

RUN apk update  \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && apk add --no-cache libffi-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo \
    && apk del build-deps


RUN pip install --upgrade pip

COPY . .

RUN pip install -r project/requirements.txt

CMD [ "gunicorn", "-c", "gunicorn.conf.py", "project.wsgi" ]

#CMD ["gunicorn", "--env DJANGO_SETTINGS_MODULE=project.settings", "project.wsgi"]
