from abc import ABCMeta, abstractmethod, abstractproperty
from abstract.singleton import Singleton


class Service(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, *args, **kwargs):
        raise NotImplementedError()


class SingletonService(metaclass=Singleton):
    pass


class State(SingletonService, metaclass=ABCMeta):

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

    def reset_state(self, *args, **kwargs):
        self.state = self.init_state(*args, **kwargs)
