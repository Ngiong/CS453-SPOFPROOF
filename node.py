from abc import ABC, abstractmethod
from enum import Enum
from requests import get as http_get
from threading import Thread


class ResponseLevel(Enum):
    NORMAL = 0 # node responding normally
    SLOW = 1 # node should give delay / have chance to not responding
    TERMINATED = 2 # node cannot respond


def inverse_response_level(level: int) -> ResponseLevel:
    if level == 0:
        return ResponseLevel.NORMAL
    if level == 1:
        return ResponseLevel.SLOW
    if level == 2:
        return ResponseLevel.TERMINATED
    raise ValueError("Level must be in {0,1,2}")


class INode(ABC):
    # Representation of microservices
    # Should use interface so that our project can be "extensible" for non-localhost
    @abstractmethod
    def __init__(self, name, ip_address, port):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def set_response_level(self, response_level: ResponseLevel):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_url(self, path):
        pass

    @abstractmethod
    def kill(self):
        pass

    @abstractmethod
    def resurrect(self):
        pass


class SimpleNode(INode):
    name = ''
    ip_address = ''
    port = 0

    def __init__(self, name='', ip_address='', port=0):
        self.name = name
        self.ip_address = ip_address
        self.port = port

    def __str__(self):
        return '({}, {}:{})'.format(self.name, self.ip_address, self.port)

    def get_name(self):
        return self.name

    def get_url(self, path='/'):
        return f'http://{self.ip_address}:{self.port}{path}'

    def ping(self) -> bool:
        response = http_get(self.get_url('/ping'))
        return response.status_code == 200

    def set_response_level(self, response_level: ResponseLevel):
        level = response_level.value
        response = http_get(self.get_url(f'/response/{level}'))
        return response.status_code == 200   

    def kill(self) -> bool:
        return self.set_response_level(ResponseLevel.TERMINATED)

    def resurrect(self) -> bool:
        return self.set_response_level(ResponseLevel.NORMAL)
