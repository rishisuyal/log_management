import subprocess
from celery import Celery
from json import dumps
from time import sleep
from celery.contrib.abortable import AbortableTask
from kafka import KafkaProducer

celery_app = Celery('app', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
@celery_app.task(name='app.produce_to_kafka',bind=True,base=AbortableTask)
def produce_to_kafka(self):
    topic = 'topic-1'
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))
    while not producer_stopped:
        if self.is_aborted():
            return
        command = ['tail', '-n', '1', 'app.log']
        output = subprocess.check_output(command, universal_newlines=True)
        output += '\n.................................'
        output = output.split('\n')

        for i in output:
            producer.send(topic, value={'i': i})
            sleep(0.2)
        print('sent.')
        sleep(5)

    return "Producer stopped"


producer_stopped = False
print('.>>>...>>>>>..>>..>>>.>>>>',celery_app.main)
