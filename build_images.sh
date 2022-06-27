docker build -t authentication_image ./authentication/
docker build -t admin_image ./admin/
docker build -t daemon_image ./daemon/
docker build -t voting_image ./voting/
docker build -t auth_db_migrate_image ./auth_db_migrate/
docker build -t admin_db_migrate_image ./admin_db_migrate/

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker volume prune

docker-compose -f development.yaml up
