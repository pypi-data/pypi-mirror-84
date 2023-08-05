import os
import json
import logging
import google.auth
from google.cloud import pubsub_v1
from pyinsight import messager

class PubsubMessager(messager.Messager):
    project_id = ''
    publisher  = None

    def set_publisher(self, project_id, publisher: pubsub_v1.PublisherClient):
        self.project_id = project_id
        self.publisher = publisher

    def check_publish_capacity(self, topic_id):
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        future = self.publisher.publish(topic_path, ''.encode()) # Role publisher can only publish.
        try:
            future.result()
        except Exception as e: # Will throw exception because future is in another thread
            err_msg = format(e)
            if 'non-empty data' in err_msg:
                return True
            else:
                return False

    # Send Message
    def publish(self, topic_id, header, body):
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        header = {key: str(value) for key, value in header.items()}
        try:
            body = body.encode()
        except (UnicodeEncodeError, AttributeError):
            pass
        future = self.publisher.publish(topic_path, body, **header)
        try: # Message should be pushed to pubsub in less than 30 seconds
            message_no = future.result(30)
            logging.info("{} sent to {} Content: {}".format(message_no, topic_id, header))
            return message_no
        except Exception as e:
            logging.error("{}: {}".format(topic_id, e))

class PubsubSuperMessager(PubsubMessager):
    subscriber = None

    def set_publisher(self, project_id, publisher: pubsub_v1.PublisherClient):
        super().set_publisher(project_id, publisher)
        project_path = '/'.join(['projects', project_id])
        topic_list = [t.name.split('/')[-1] for t in self.publisher.list_topics(request={"project": project_path})]
        for topic_id in [t for t in [self.topic_backlog, self.topic_cleaner, self.topic_cockpit, self.topic_merger,
                                     self.topic_loader, self.topic_packager] if t not in topic_list]:
            topic_path = self.publisher.topic_path(self.project_id, topic_id)
            publisher.create_topic(request={"name": topic_path})

    def set_subscriber(self, project_id, subscriber: pubsub_v1.SubscriberClient):
        self.project_id = project_id
        self.subscriber = subscriber

    # Pull Message
    def pull(self, subscription_id):
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        while True:
            counter = 0
            response = self.subscriber.pull(
                request={"subscription": subscription_path, "max_messages": 8}
            )
            for received_message in response.received_messages:
                counter += 1
                yield received_message
            if counter < 8:
                break

    # Acknowledge Reception
    def ack(self, subscription_id, ack_id):
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        self.subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [ack_id]}
        )

    # Translate Message Content
    def extract_message_content(self, message):
        return message.message.attributes, message.message.data, message.ack_id
