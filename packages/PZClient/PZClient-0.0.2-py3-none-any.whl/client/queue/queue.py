from client.queue.mongodb.mongo_queue import MongoQueue
from client.queue.structure.message import Message
from typing import Dict


class Queue:
    def __init__(self, mongo_connection: Dict, queue_name: str):
        self._queue = MongoQueue(host=mongo_connection["host"], username=mongo_connection["username"],
                                 password=mongo_connection["password"], queue_name=queue_name)

    def put_message(self, message: Message):
        self._queue.put_message(message)

    def get_message(self, source: str):
        return self._queue.get_message(source)

    def monitor(self):
        self._queue.monitor_queue()
