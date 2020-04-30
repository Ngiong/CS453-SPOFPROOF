from node import SimpleNode

# TODO: if it is possible, we might want to be able to automatically start the microservice environment
# This is just an example to bootstrap the microservice


def bootstrap():
    parent1 = SimpleNode(name='parent 1', ip_address='localhost', port=3887)
    parent1.start()

    parent2 = SimpleNode(name='parent 2', ip_address='localhost', port=3888)
    parent2.start()

    dependant = SimpleNode(name='dependant', ip_address='localhost', port=3889)
    dependant.set_dependencies([parent1, parent2])

    dependant.start()


if __name__ == '__main__':
    bootstrap()