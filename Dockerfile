# TO-DO: Use multi-stage build to minimize the docker image size - https://haseebmajid.dev/blog/docker-containers-to-setup-nginx-flask-and-postgres
FROM python:3.8

WORKDIR /usr/src/app

ARG DB_DRIVER "postgresql+psycopg2"
ARG DB_PASSWORD "test"
ARG DB_USER "test"
ARG DB_NAME "jobandtalent"
# ARG DB_HOST "host.docker.internal"
# ARG DB_PORT 3306

ENV DB_DRIVER $DB_DRIVER
ENV DB_PASSWORD $DB_PASSWORD
ENV DB_USER $DB_USER
ENV DB_NAME $DB_NAME
ENV DB_HOST $DB_HOST
ENV DB_PORT $DB_PORT
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
