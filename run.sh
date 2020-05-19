sudo docker-compose -f docker-compose.global.yml -f docker-compose.local.yml down
sudo docker-compose -f docker-compose.global.yml -f docker-compose.local.yml up -d --build --force-recreate   kafka kafka2 kafka3 mongo proxy flask
