set -e

git pull -f

docker build --no-cache --ssh default -f docker/Dockerfile -t url_shortener .
docker rm -f $(docker ps -aq)
docker-compose -f docker/docker-compose.yml up -d
docker rmi -f $(docker images -f 'dangling=true' -q)