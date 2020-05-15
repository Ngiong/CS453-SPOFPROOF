from requests import get as http_get

from node import INode, ResponseLevel
from poc.bootstrap_flask import POCNodeStartable


class POCNode(INode):
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
        response = http_get(self.get_url('/'))
        return response.status_code == 200

    def set_response_level(self, response_level: ResponseLevel) -> bool:
        level = response_level.value
        response = http_get(self.get_url(f'/response/{level}'))
        return response.status_code == 200


def main():
    app1 = POCNodeStartable('app1')
    app1.start(port=5000)

    app2 = POCNodeStartable('app2', ['127.0.0.1:5000'])
    app2.start(port=5001)

    # Test if the NodeStartable is running correctly
    node1 = POCNode('app1', '127.0.0.1', 5000)
    assert node1.ping()

    assert node1.set_response_level(ResponseLevel.TERMINATED)
    assert not node1.ping()

    assert node1.set_response_level(ResponseLevel.SLOW)
    assert node1.ping()

    # Check dependency
    node2 = POCNode('app2', '127.0.0.1', 5001)
    node1.set_response_level(ResponseLevel.NORMAL)
    assert node2.ping()

    node1.set_response_level(ResponseLevel.TERMINATED)
    assert not node2.ping()


if __name__ == '__main__':
    main()
