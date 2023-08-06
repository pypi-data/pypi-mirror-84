import json
import pika
import logging
import time
import traceback
from .exception import ConnectionException, ServerException

from pika.exceptions import AMQPConnectionError

logger = logging.getLogger(__name__)


class RabbitMqService(object):

    @classmethod
    def push(cls, message_id, address, params, retry_count=0):
        """
            生产消息
        :param retry_count:
        :param message_id:
        :param address:
        :param params:
        :return:
        """
        try:
            data = {
                "queue_name": "default",
                "actor_name": "dispatch",
                "args": [message_id, json.dumps(params)],
                "kwargs": {},
                "options": {},
                "message_id": message_id
            }
            json_data = json.dumps(data)

            host, port = address.split(":")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, port=int(port)))
            channel = connection.channel()
            channel.basic_publish(exchange='', routing_key='default', body=json_data)
            connection.close()
        except AMQPConnectionError as e:
            time.sleep(1)
            if retry_count > 3:
                raise ConnectionException(code=1000, traceback=str(e))
            retry_count += 1
            cls.push(message_id, address, params, retry_count)
        except Exception as e:
            time.sleep(1)
            if retry_count > 3:
                raise ServerException(code=1001, traceback=traceback.format_exc())
            retry_count += 1
            cls.push(message_id, address, params, retry_count)


