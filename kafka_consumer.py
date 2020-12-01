import argparse
from kafka import KafkaConsumer

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--participants')

if __name__ == '__main__':
    args = parser.parse_args()

    if args.participants:
        phone_no = args.participants

        group_topic = 'new_home_sweet'

        consumer = KafkaConsumer(
            phone_no,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True)
        consumer.subscribe(group_topic)

        for m in consumer:
            print('{} ==== {}'.format(phone_no, m.value))
