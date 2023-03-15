import json
from configparser import ConfigParser

from kafka import KafkaProducer

##todo：考虑把方法写到Class里还是写道包里
def get_config():
    conf = ConfigParser()
    conf.read('./Config.ini')
    return conf

def get_kafka_producer (Config):

    producer = KafkaProducer(
        bootstrap_servers=['{}:{}'.format(Config.get('kafka_python','bootstrap'),
                                          Config.get('kafka_python','port'))],
        key_serializer=lambda k: json.dumps(k, ensure_ascii=False).encode('utf-8'),
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'))

    return producer

