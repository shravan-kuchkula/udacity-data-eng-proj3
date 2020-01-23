"""Defines core consumer functionality"""
import logging
import confluent_kafka
from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from tornado import gen

logger = logging.getLogger(__name__)

class KafkaConsumer:
    """Defines the base kafka consumer class"""

    def __init__(
        self,
        topic_name_pattern,
        message_handler,
        is_avro=True,
        offset_earliest=False,
        sleep_secs=1.0,
        consume_timeout=0.1,
    ):
        """Creates a consumer object for asynchronous use"""
        self.topic_name_pattern = topic_name_pattern
        self.message_handler = message_handler
        self.sleep_secs = sleep_secs
        self.consume_timeout = consume_timeout
        self.offset_earliest = offset_earliest

        self.broker_properties = {
            'BROKER_URL':'PLAINTEXT://localhost:9092',
            'SCHEMA_REGISTRY': 'http://localhost:8081',
            'KAFKA_REST_PROXY': 'http://localhost:8082'
        }

        # Create the Consumer, using the appropriate type.
        if is_avro is True:
            self.broker_properties['SCHEMA_REGISTRY'] = "http://localhost:8081"
            self.consumer = AvroConsumer({
                'bootstrap.servers': self.broker_properties['BROKER_URL'],
                'group.id': self.topic_name_pattern,
                'schema.registry.url': self.broker_properties['SCHEMA_REGISTRY'],
                'auto.offset.reset': 'earliest'
            })
        else:
            self.consumer = Consumer({
                'bootstrap.servers': self.broker_properties['BROKER_URL'],
                'group.id': self.topic_name_pattern,
                'auto.offset.reset': 'earliest'
            })

        # Configure the AvroConsumer and subscribe to the topics. Make sure to think about
        # how the `on_assign` callback should be invoked.
        self.consumer.subscribe([self.topic_name_pattern], on_assign=self.on_assign)

    def on_assign(self, consumer, partitions):
        """Callback for when topic assignment takes place"""
        # If the topic is configured to use `offset_earliest` set the partition offset to
        # the beginning or earliest
        for partition in partitions:
            partition.offset = OFFSET_BEGINNING
            logger.info("partition offset set to beginning for %s", self.topic_name_pattern)

        logger.info("partitions assigned for %s", self.topic_name_pattern)
        consumer.assign(partitions)

    async def consume(self):
        """Asynchronously consumes data from kafka topic"""
        while True:
            num_results = 1
            while num_results > 0:
                num_results = self._consume()
            await gen.sleep(self.sleep_secs)

    def _consume(self):
        """Polls for a message. Returns 1 if a message was received, 0 otherwise"""
        # Poll Kafka for messages. Make sure to handle any errors or exceptions.
        # Additionally, make sure you return 1 when a message is processed, and 0 when no message
        # is retrieved.
        message = self.consumer.poll(self.consume_timeout)
        if message is None:
            logger.info("no message received by consumer")
            return 0
        elif message.error() is not None:
            logger.info(f"error from consumer {message.error()}")
            return 0
        else:
            self.message_handler(message)
            logger.info(f"consumed message {message.key()}: {message.value()}")
            return 1

    def close(self):
        """Cleans up any open kafka consumers"""
        logger.info("closing {}".format(self.topic_name_pattern))
        self.consumer.close()
