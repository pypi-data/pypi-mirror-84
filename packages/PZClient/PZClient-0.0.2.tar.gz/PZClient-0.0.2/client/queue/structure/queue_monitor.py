class QueueMonitor:
    def __init__(self, message_depth, weight_depth, time_depth):
        self._message_depth = message_depth
        self._weight_depth = weight_depth
        self._time_depth = time_depth

    @property
    def message_depth(self):
        """
        :return: Count of messages in queue.
        """
        return self._message_depth

    @property
    def weight_depth(self):
        """
        :return: Size of Queue in Bytes.
        """
        return self._weight_depth

    @property
    def time_depth(self):
        """
        :return: Time from now to the last message in queue.
        """
        return self._time_depth
