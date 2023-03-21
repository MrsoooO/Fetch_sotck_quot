# coding=utf-8
# import ConfigParser
import json


from kafka import KafkaProducer


class Kafka(object):
    def __init__(self,conf_path=None):
        if not conf_path:
            raise Exception('配置文件路径不存在')

        self.conf_path=conf_path

    # def kafka_producer(self):
    #     conf=ConfigParser.ConfigParser()
    #     conf.read('{}'.format(self.conf_path))
    #     bootstrap=conf.get('kafka_python','bootstrap')
    #     producer=KafkaProducer(bootstrap_servers=bootstrap,
    #                            key_serializer=lambda k: json.dumps(k, ensure_ascii=False).encode('utf-8'),
    #                            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'))
    #     return producer