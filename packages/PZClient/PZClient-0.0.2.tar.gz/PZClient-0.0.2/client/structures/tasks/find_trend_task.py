class TrendMessage:
    def __init__(self, symbol: str, interval: str, anomaly_candle_count: int):
        self._symbol = symbol
        self._interval = interval
        self._anomaly_candle_count = anomaly_candle_count

    @property
    def symbol(self):
        return self._symbol

    @property
    def interval(self):
        return self._interval

    @property
    def anomaly_candle_count(self):
        return self._anomaly_candle_count
