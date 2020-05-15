from threading import Thread

from flask import Flask, current_app

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

    def ping(self):
        # TODO: when called, it will hit the ping API in the node
        # TODO: (cont.d) then node will ping all of its dependencies
        pass

    def set_response_level(self: ResponseLevel):
        # TODO: when called, it will hit the set response level API in the node
        pass


def create_application(app_name):
    app = Flask(app_name)
    app.__response_level = ResponseLevel.NORMAL

    @app.route('/', methods=['GET'])
    @app.route('/ping', methods=['GET'])
    def ping():
        response_level = current_app.__response_level
        return 'OK ' + str(response_level)

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


if __name__ == '__main__':
    main()