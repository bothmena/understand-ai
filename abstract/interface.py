from abc import ABCMeta, abstractmethod
from abstract.singleton import Singleton
from utils.data_extractor import DataExtractor


class EventListener(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, *args, **kwargs):
        raise NotImplementedError()


class SingletonService(metaclass=Singleton):
    pass


class State(SingletonService):
    def __init__(self, *args, **kwargs):
        self._state = self.init_state(*args, **kwargs)

    @property
    @abstractmethod
    def state(self):
        """should return the state value"""

    @state.setter
    @abstractmethod
    def state(self, value):
        """should update the state value"""

    @abstractmethod
    def init_state(self, *args, **kwargs):
        """should return the state initial value"""

    @abstractmethod
    def query(self, *args, **kwargs):
        """should query the state to get specific value"""

    @abstractmethod
    def insert(self, *args, **kwargs):
        """should query the state to get specific value"""

    @abstractmethod
    def update(self, *args, **kwargs):
        """should query the state to get specific value"""

    @abstractmethod
    def remove(self, *args, **kwargs):
        """should remove an item from the state"""

    def reset_state(self, *args, **kwargs):
        self._state = self.init_state(*args, **kwargs)


class Event(metaclass=ABCMeta):
    def __init__(self):
        self.extractor = DataExtractor()

    @property
    @abstractmethod
    def args_names(self) -> list:
        """must return a set of arguments names"""

    @property
    @abstractmethod
    def args_types(self) -> list:
        """must return a set of arguments types"""

    def get_data(self, values: list):
        return self.extractor.extract(self.args_names, self.args_types, values)
