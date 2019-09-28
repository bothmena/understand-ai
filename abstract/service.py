from abc import ABCMeta, abstractmethod
from abstract.singleton import Singleton


class Service(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, *args, **kwargs):
        raise NotImplementedError()


class SingletonService(metaclass=Singleton):
    pass
