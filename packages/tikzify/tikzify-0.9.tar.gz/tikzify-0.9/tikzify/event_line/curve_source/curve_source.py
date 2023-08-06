from abc import abstractmethod

__all__ = ['CurveSource']


class CurveSource:

    def __init__(self, start_time, end_time):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time

    @abstractmethod
    def keys_and_times(self):
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key, time):
        raise NotImplementedError

    @abstractmethod
    def get_last_key(self):
        raise NotImplementedError
