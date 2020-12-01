import argparse
from kafka import KafkaConsumer

parser = argparse.ArgumentParser()

# Pass user registered phone no as an argument to fetch message from producer
parser.add_argument('-p', '--participant') 

if __name__ == '__main__':
    args = parser.parse_args()
    if args.participants:
        phone_no = args.participants
        consumer = KafkaConsumer(
            phone_no,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True)

        # In case of group conversation, client needs to subscribed the consumers to a particular topic (i.e. Group Name)
        group_topic = 'KAFKA_TOPIC_NAME_GOES_HERE'
        consumer.subscribe(group_topic)

        for m in consumer:
            print('{}'.format(m.value))
