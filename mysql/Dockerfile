FROM mysql

ENV MYSQL_ROOT_PASSWORD 123456
ENV MYSQL_DATABASE=chotot_db

COPY ./init_db /docker-entrypoint-init_db.d
EXPOSE 3306