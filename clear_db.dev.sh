mongo --username kms -password example --host localhost:27017 --authenticationDatabase admin --eval "printjson(db.dropDatabase())" kms_global
sudo docker-compose -f docker-compose.global.yml -f docker-compose.local.dev.yml up -d --build --force-recreate django
