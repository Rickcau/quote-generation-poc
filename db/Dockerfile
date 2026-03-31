FROM mcr.microsoft.com/mssql/server:2022-latest

USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
USER mssql

COPY entrypoint.sh /opt/entrypoint.sh
COPY init-schema.sql /opt/init-schema.sql
COPY seed-data.sql /opt/seed-data.sql

ENTRYPOINT ["/bin/bash", "/opt/entrypoint.sh"]
