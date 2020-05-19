import json
import threading
import traceback
from queue import Queue

from kafka import KafkaProducer


class LocalKafkaProducer(object):
    '''
    Singleton instance for Kafka Middleware
    '''
    
    class __LoaclKafkaProducer(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.queue = Queue()
            self.running = False
            self.stop_event = threading.Event()
        
        def __str__(self):
            return repr(self)
        
        def stop(self):
            self.stop_event.set()
        
        def run(self):
            self.running = True
            producer = KafkaProducer(bootstrap_servers='kms_kafka_1:9092',
                                     value_serializer=lambda s: json.dumps(s).encode('utf-8'))
            print("running")
            while not self.stop_event.is_set():
                try:
                    topic, msg = self.queue.get()
                    print("sending on topic %s: %s" % (topic, msg))
                    result = producer.send(topic, msg)
                    # print("result of sending on topic %s: %s: %s" % (result, topic, msg))
                except:
                    print("Not sending %s" % msg)
                    traceback.print_exc()
            
            producer.close()
    
    instance = None
    
    def __init__(self):
        if not LocalKafkaProducer.instance:
            LocalKafkaProducer.instance = LocalKafkaProducer.__LoaclKafkaProducer()
        else:
            pass
    
    def add_to_queue(self, msg, topic='kms.global'):
        if not LocalKafkaProducer.instance.running:
            LocalKafkaProducer.instance.start()
        self.instance.queue.put((topic, msg))
    
    def start(self):
        self.instance.start()
    
    def stop(self):
        self.instance.stop()
    
    def __getattr__(self, item):
        return getattr(self.instance, item)
