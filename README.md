Dockerized KMS
Link to the deployment: [http://chariot-km.dai-lab.de:8001/](http://chariot-km.dai-lab.de:8001/)
Device REST endpoint: [http://chariot-km.dai-lab.de:8001/device/](http://chariot-km.dai-lab.de:8001/device/)

**Quick Start / Setup**

1. Install Docker https://docs.docker.com/install/
2. Install docker-compose https://docs.docker.com/compose/install/
3. Edit the clean.sh script to configure setup. Deleting the 'db' folder deletes all stored data. 
4. Run the clean.sh script in /knowledge-layer/kms to deploy

**Restart / Clean**

1. Login: ssh kmsdocker@chariot-km.dai-lab.de pw: dPP88is,
2. cd /home/kmsdocker/knowledge-layer/kms
3. Edit clean.sh: 
*  sudo rm -rf ./db/* : Deletes the database
*  sudo rm -rf ./docker_local/django_kms_api/server/api/migrations/0*: Necessary to recreate database structure
4. sudo sh clean.sh

