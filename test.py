import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
        'test',
        bootstrap_servers='hadoop100:9092',
        group_id='test'
    )
for message in consumer:
    print("receive, key: {}, value: {}".format(
        json.loads(message.key.decode('utf-8')),
        json.loads(message.value.decode('utf-8'))
        )
    )