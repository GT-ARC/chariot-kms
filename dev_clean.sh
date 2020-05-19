sudo docker-compose -f docker-compose.global.yml -f docker-compose.local.dev.yml down

sudo rm -rf ./db/*
sudo rm -rf ./docker_local/django_kms_api/server/api/migrations/0*
sudo docker-compose -f docker-compose.global.yml -f docker-compose.local.dev.yml up -d --build --force-recreate kafka kafka2 kafka3 kafka_manager mongo proxy redis flask
