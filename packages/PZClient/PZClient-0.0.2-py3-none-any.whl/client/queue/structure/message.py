from datetime import datetime
import pickle


class Message:
    def __init__(self, body: object, source: str):
        self._body = pickle.dumps(body)
        self._create_time = datetime.now()
        self._source = source

    @property
    def creation_time(self):
        """
        :return: Time of message creation
        """
        return self._create_time

    @property
    def source(self):
        """
        :return: The source of the Message
        """
        return self._source

    @property
    def body(self):
        """
        :return: The message that should pass
        """
        return pickle.loads(self._body)
