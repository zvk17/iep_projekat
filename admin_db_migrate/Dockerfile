FROM python:3
RUN mkdir -p /opt/src/admin_db_migrate
WORKDIR /opt/src/admin_db_migrate

COPY . .

RUN pip install -r ./requirements.txt

#EXPOSE 7000
ENTRYPOINT ["python", "migration.py"]
