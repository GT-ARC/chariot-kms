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
        '''
        Thing that puts things into Kafka.
        It holds a queue where (message, topic) tuples are being pushed by controllers
        It runs a thread sending the tuples in the queue to Kafka
        '''
    
        def __init__(self):
            threading.Thread.__init__(self)
            self.queue = Queue()
            self.running = False
            self.stop_event = threading.Event()
    
        def stop(self):
            '''
            Sets the Stop Event the Thread checks for its loop
            @return:
            '''
            self.stop_event.set()
    
        def run(self):
            '''
            Threa.run(). Start thread running
            @return:  None
            '''
            self.running = True
            producer = KafkaProducer(bootstrap_servers='kms_kafka_1:9092',
                                     value_serializer=lambda s: json.dumps(s).encode('utf-8'))
            print("running")
            while not self.stop_event.is_set():
                try:
                    topic, msg = self.queue.get()
                    # print("sending on topic %s: %s" % (topic, model))
                    result = producer.send(topic, msg)
                    # print("result of sending on topic %s: %s: %s" % (result, topic, model))
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

    def add_to_queue(self, msg: str, topic: str = 'kms.global') -> None:
        '''
        add a (msg, topic) tuple to the queue to be sent through Kafka
        @param msg: json string
        @param topic: kafka topic to send on
        @return: None
        '''
        if not LocalKafkaProducer.instance.running:
            LocalKafkaProducer.instance.start()
        self.instance.queue.put((topic, msg))

    def start(self):
        '''
        Starts the Send Thread
        @return: None
        '''
        self.instance.start()

    def stop(self):
        '''
        Stops the send thread by triggering the stop event
        @return: None
        '''
        self.instance.stop()
    
    def __getattr__(self, item):
        return getattr(self.instance, item)
