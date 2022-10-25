# Import KafkaProducer from Kafka library
from kafka import KafkaProducer
import msgpack
import json
import time
import random
import datetime

# Define server with port
bootstrap_servers = ['b-2.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:9094','b-1.tickerkafka.sj49ms.c1.kafka.us-west-2.amazonaws.com:9094']


# Define topic name where the message will publish
topicName = 'multipartition'
price = 100
# Initialize producer variable
producer = KafkaProducer(bootstrap_servers = bootstrap_servers,security_protocol='SSL')
# print(producer.config)
# Publish text in defined topic

def get_data():
    global price 
    price = price + (random.random()*2-1)*10
    price = 0 if price < 0 else price
    return {
        #'EVENT_TIME': datetime.datetime.now().isoformat(),
        'ticker': random.choice(['BTC','ETH','BSC','SOL']),
        'price': price,
        'matchtime': datetime.datetime.now().isoformat()
    }

data = {'id':999, 'ticker':'loading', 'price':100}
for i in range (29):
    data = get_data() 
    data['id'] = i
    
    producer.send(topicName, json.dumps(data).encode('utf-8'))
    producer.flush()
    print('send data: ' + json.dumps(data))
    time.sleep(1)

for i in range(30,200):
    data = get_data() 
    data['id'] = i
    producer.send(topicName, json.dumps(data).encode('utf-8'))
    producer.flush()
    print('send data: ' + json.dumps(data))
    time.sleep(0.1)    

for i in range(201,400):
    data = get_data() 
    data['id'] = i
    producer.send(topicName, json.dumps(data).encode('utf-8'))
    producer.flush()
    print('send data: ' + json.dumps(data))
    time.sleep(0.001)  
# Print message


while True:
    i = i + 1
    data = get_data() 
    data['id'] = i 
    producer.send(topicName, json.dumps(data).encode('utf-8'))
    producer.flush()
    print('send data: ' + json.dumps(data))
    time.sleep(0.5)  

