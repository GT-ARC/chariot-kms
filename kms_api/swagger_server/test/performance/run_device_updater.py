import json
import threading
import time
from uuid import uuid4

import requests


class Runner(object):
    
    def __init__(self, t_num=1, freq=0.0, stop=10):
        """
        
        @param t_num: number of threads running in parallel
        @param freq: frequency (freq = requests/second)
        @param stop: time in seconds to run for
        """
        super(Runner, self).__init__()
        self.threads = []
        self.event = None
        self.t_num = t_num
        self.freq = freq
        self.stop = stop
        if self.stop == -1:
            self.stop = 100000000000
    
    def create(self):
        url = "http://localhost:8080/v1/devices/"
        uuid = uuid4()
        
        payload = ("{\"objectType\": \"sensor\",\"name\": \"string\",\"uuid\": \"%s\", \"identifier\": "
                   "\"string\",\"securitykey\": \"string\",\"ip\": \"198.51.100.42\",\"group_id\": \"abc\","
                   "\"reId\": \"string\",\"location\": {\"identifier\": \"string\",\"type\": "
                   "\"string\",\"name\": \"string\",\"level\": 0,\"position\": {"
                   "\"lat\": 0,\"lng\": 0},\"indoorposition\": {"
                   "\"indoorlat\": 0,\"indoorlng\": 0}},\"groupId\": \"string\","
                   "\"properties\": [{\"type\": \"number\",\"value\": 1,"
                   "\"unit\": \"unit\",\"key\": \"somekey\",\"writable\": true"
                   "}]} " % (uuid))
        headers = {
            'Content-Type': 'application/json',
        }
        j = json.loads(payload)
        
        response = requests.request("POST", url, headers=headers, data=json.dumps(j))
        
        # print(response.text.encode('utf8'))
        
        return uuid
    
    def update(self, uuid=""):
        url = "http://localhost:8080/v1/devices/%s/" % (uuid)
        
        payload = "{\n    \"objectType\": \"sensor\",\n    \"name\": \"string\",\n    \"uuid\": \"%s\",\n    \"identifier\": \"string\",\n    \"securitykey\": \"string\",\n    \"ip\": \"198.51.100.43\",\n    \"group_id\": \"abc\",\n    \"reId\": \"string\",\n    \"location\": {\n        \"identifier\": \"string2\",\n        \"type\": \"string\",\n        \"name\": \"string\",\n        \"level\": 0,\n        \"position\": {\n            \"lat\": 3.0,\n            \"lng\": 0\n        },\n        \"indoorposition\": {\n            \"indoorlat\": -1.0,\n            \"indoorlng\": 0\n        }\n    },\n    \"groupId\": \"string\",\n    \"properties\": [\n        {\n            \"type\": \"number\",\n            \"value\": 1,\n            \"unit\": \"unit2\",\n            \"key\": \"somekey\"\n        }\n    ]\n}" % uuid
        headers = {
            'Content-Type': 'application/json',
        }
        
        response = requests.request("PUT", url, headers=headers, data=payload)
        
        # print(response.text.encode('utf8'))
    
    def setup(self):
        """
        
        for i in range(5):
        t = threading.Thread(target=testThread, arg=(i,))
        t.start()
        @return:
        """
        self.event = threading.Event()
        for t_id in range(self.t_num):
            t = threading.Thread(target=self.start_request, args=[t_id, self.event])
            self.threads.append(t)
    
    def run(self):
        for t in self.threads:
            t.start()
        
        for i in range(self.stop):
            print("Runner has been running for %s/%s seconds" % (i, self.stop))
            if i == self.stop - 1:
                self.event.set()
            time.sleep(1)
        
        for t in self.threads:
            t.join()
    
    def start_request(self, t_id, event):
        # create device
        uuid = self.create()
        print("Thread %s created device with uuid %s" % (t_id, uuid))
        
        while not event.isSet():
            # update device
            print("Thread %s updating device with uuid %s" % (t_id, uuid))
            self.update(uuid)
            time.sleep(1 / self.freq)


def main():
    runner = Runner(t_num=10, freq=4, stop=-1)
    runner.setup()
    runner.run()


if __name__ == '__main__':
    main()
