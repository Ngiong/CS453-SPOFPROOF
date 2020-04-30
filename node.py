from abc import ABC, abstractmethod
from enum import Enum


class ResponseLevel(Enum):
    NORMAL = 0 # node responding normally
    SLOW = 1 # node should give delay / have chance to not responding
    TERMINATED = 2 # node cannot respond


class IStartable(ABC):
    @abstractmethod
    def start(self):
        pass


class INode(ABC):
    # Representation of microservices
    # Should use interface so that our project can be "extensible" for non-localhost
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def set_response_level(self: ResponseLevel):
        pass

    @abstractmethod
    def get_name(self):
        pass


class SimpleNode(INode, IStartable):
    name = ''
    ip_address = ''
    port = 0
    dependencies = []

    def __init__(self, name='', ip_address='', port=0):
        self.name = name
        self.ip_address = ip_address
        self.port = port

    def __str__(self):
        return '({}, {}:{})'.format(self.name, self.ip_address, self.port)

    def get_name(self):
        return self.name

    def set_dependencies(self, node):
        self.dependencies = ['{}:{}'.format(x.ip_address, x.port) for x in node]

    def start(self):
        # TODO: when called, this method will start the webserver on specified ip_address & port
        pass

    def ping(self):
        # TODO: when called, it will hit the ping API in the node
        # TODO: (cont.d) then node will ping all of its dependencies
        pass

    def set_response_level(self: ResponseLevel):
        # TODO: when called, it will hit the set response level API in the node
        pass
