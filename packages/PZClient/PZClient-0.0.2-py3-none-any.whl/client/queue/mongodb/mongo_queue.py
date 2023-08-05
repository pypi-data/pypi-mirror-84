from client.mongodb.mongo_client import Mongo
from client.queue.structure.message import Message
from client.queue.structure.queue_monitor import QueueMonitor
from datetime import datetime
import pickle


class MongoQueue:
    MESSAGE_FIELD = "message"
    SOURCE_FIELD = "source"
    INSERTION_TIME_FIELD = "insertion_time"

    def __init__(self, host: str, username: str, password: str, queue_name: str, database: str = "queue"):
        self._queue = Mongo(host=host, username=username, password=password, database=database, collection=queue_name)

    def put_message(self, message: Message):
        """
        Puts a message in the queue.
        :param message: From object type Message.
        """
        source = message.source
        binary_message = pickle.dumps(message)
        self._queue.add_document({self.MESSAGE_FIELD: binary_message, self.SOURCE_FIELD: source,
                                  self.INSERTION_TIME_FIELD: datetime.now()})

    def get_message(self, source: str = None) -> Message:
        """
        Return the first Message in queue from the source if delivered.
        :param source: test
        :return: First Message from object type Message
        """
        query = {} if source is None else {self.SOURCE_FIELD: source}
        message = self._queue.get_document_and_remove(query)
        if message:
            return pickle.loads(message[self.MESSAGE_FIELD])
        return None

    def _get_time_depth(self):
        """
        Calculates the delay from the first message to now.
        :return: The time from the first message to now.
        """
        first_document_time = self._queue.get_single_document(sort_field=self.INSERTION_TIME_FIELD)
        return datetime.now() - first_document_time[self.INSERTION_TIME_FIELD] if first_document_time else 0

    def monitor_queue(self):
        """
        Monitors the queue
        :return: A MonitorQueue object
        """
        return QueueMonitor(message_depth=self._queue.get_document_count(),
                            weight_depth=self._queue.get_collection_size(),
                            time_depth=self._get_time_depth())
