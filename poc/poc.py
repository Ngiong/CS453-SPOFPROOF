from threading import Thread
from time import sleep

from flask import Flask, Response, current_app
from requests import get as http_get

from bootstrap import IStartable
from node import INode, ResponseLevel, inverse_response_level


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


def create_application(app_name):
    app = Flask(app_name)
    app.__response_level = ResponseLevel.NORMAL

    @app.route('/', methods=['GET'])
    @app.route('/ping', methods=['GET'])
    def ping():
        response_level = current_app.__response_level
        if response_level == ResponseLevel.NORMAL:
            return Response('OK', 200)
        elif response_level == ResponseLevel.TERMINATED:
            return Response('UNHEALTHY', 500)
        else:
            sleep(5.0)
            return Response('OK', 200)

    @app.route('/response/<level>', methods=['GET'])
    def set_response_level(level):
        try:
            level = int(level)
            response_level = inverse_response_level(level)
            current_app.__response_level = response_level
            return 'OK'
        except ValueError as e:
            return str(e)

    return app


class POCNodeStartable(object):
    def __init__(self, name):
        self.app = create_application(name)
        self.name = name

    def start(self, host='localhost', port=5000):
        # With Multi-Threading Apps, YOU CANNOT USE DEBUG! Though you can sub-thread.
        th = Thread(target=lambda: self.app.run(host, port, debug=False, threaded=True))
        th.start()

    dependencies = []

    def set_dependencies(self, node):
        self.dependencies = ['{}:{}'.format(x.ip_address, x.port) for x in node]


def main():
    app1 = POCNodeStartable('app1')
    app1.start(port=5000)

    app2 = POCNodeStartable('app2')
    app2.start(port=5001)

    node1 = POCNode('app1', 'localhost', 5000)
    assert node1.ping()

    assert node1.set_response_level(ResponseLevel.TERMINATED)
    assert not node1.ping()

    assert node1.set_response_level(ResponseLevel.SLOW)
    assert node1.ping()


if __name__ == '__main__':
    main()