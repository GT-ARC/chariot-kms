docker-compose -f docker-compose.yml down
rm -rf ./db/*
docker-compose -f docker-compose.yml up -d --build --force-recreate kafka kafka2 kafka3 mongo flask
