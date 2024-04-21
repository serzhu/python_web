import pika
from mongoengine import Document
from mongoengine.fields import BooleanField, EmailField, StringField
from faker import Faker
from random import choice
import logging
import sys

import connect_mongo
from connect_rabbit import connection, channel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User(Document):
    fullname = StringField()
    email = EmailField()
    phone =  StringField()
    send_method = StringField()
    informed = BooleanField(default=False)

fake = Faker("en-GB")

exchange_email = "Email sender"
exchange_phone = "SMS sender"
queue_email = "Emails"
queue_phone = "Phones"

channel.exchange_declare(exchange=exchange_email, exchange_type='direct')
channel.exchange_declare(exchange=exchange_phone, exchange_type='direct')
channel.queue_declare(queue=queue_email, durable=True)
channel.queue_declare(queue=queue_phone, durable=True)
channel.queue_bind(exchange=exchange_email, queue=queue_email)
channel.queue_bind(exchange=exchange_phone, queue=queue_phone)

def publish(exchange, queue, obj):
    try:
        channel.basic_publish(
            exchange=exchange,
            routing_key=queue,
            body=str(obj.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        logger.info("Published %r to %s exchange" % (obj.id, exchange))
    except Exception as e:
        logger.error("Error while publishing: %s" % str(e))

def main():
    try:
        for i in range(10):
            user = User(fullname=fake.name(), email=fake.email(), phone=fake.phone_number(), send_method=choice(['email', 'sms'])).save()
            if user.send_method == 'email':
                publish(exchange_email, queue_email, user)
            elif user.send_method == 'sms':
                publish(exchange_phone, queue_phone, user)
            logger.info("Sent %r" % user.id)
    finally:
        connection.close()
        logger.info("Connection to RabbitMQ closed.")

if __name__ == '__main__':
    main()