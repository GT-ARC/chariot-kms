sudo docker-compose -f docker-compose.yml down
sudo docker-compose -f docker-compose.yml up -d --build --force-recreate kafka kafka2 kafka3 mongo flask
