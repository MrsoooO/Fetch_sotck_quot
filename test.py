import json
import Utils

producer = Utils.KafkaProducer

print(producer)

producer.close()