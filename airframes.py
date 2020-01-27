import json
from datetime import datetime
import uuid
from pykafka import KafkaClient

# CREATE GEOJSON COORDINATES AND OPEN FILE!
input_file = open('./data/airframes.json')
json_array = json.load(input_file)
# strip useless stuff and get only coords list
coordinates = json_array['features'][0]['geometry']['coordinates']

# Generate uuid
def generate_uuid():
    return uuid.uuid4()

client = KafkaClient(hosts='localhost:9092')

topic = client.topics['geodata_final']

producer = topic.get_sync_producer()


# Construct Message and SEND TO KAFKA!!!!!!
data = {}
data['airframe'] = 'AA0049'

def generate_checkpoint(coordinate):
    i = 0
    while i < len(coordinates):
        data['key'] = data['airframe'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))

        # if bus reaches last coord, start from beginning
        if i == len(coordinates)-1:
            i = 0
        else: i += 1

generate_checkpoint(coordinates)

