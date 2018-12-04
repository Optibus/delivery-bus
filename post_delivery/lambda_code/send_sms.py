import os

import boto3


class SMS(object):

    @staticmethod
    def send_sms(message):
        client = boto3.client('sns',
                              aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                              aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                              region_name='us-east-1')
        client.publish(Message=message,
                       TopicArn="arn:aws:sns:us-east-1:008770191051:hackaton-delivery-bus")
