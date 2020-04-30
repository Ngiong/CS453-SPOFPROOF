from abc import ABC, abstractmethod
from node import SimpleNode

# TODO: if it is possible, we might want to be able to automatically start the microservice environment
# This is just an example to bootstrap the microservice


class IStartable(ABC):
    @abstractmethod
    def start(self):
        pass


class SimpleNodeStartable(SimpleNode, IStartable):
    dependencies = []

    def set_dependencies(self, node):
        self.dependencies = ['{}:{}'.format(x.ip_address, x.port) for x in node]

    def start(self):
        # TODO: when called, this method will start the webserver on specified ip_address & port
        pass


def bootstrap():
    parent1 = SimpleNodeStartable(name='parent 1', ip_address='localhost', port=3887)
    parent1.start()

    parent2 = SimpleNodeStartable(name='parent 2', ip_address='localhost', port=3888)
    parent2.start()

    dependant = SimpleNodeStartable(name='dependant', ip_address='localhost', port=3889)
    dependant.set_dependencies([parent1, parent2])

    dependant.start()


if __name__ == '__main__':
    bootstrap()