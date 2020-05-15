# https://stackoverflow.com/questions/54115485/how-do-i-run-two-python-flask-applicationproject-on-server-in-parallel

import threading
from flask import Flask


def create_application(app_name):
    app = Flask(app_name)

    @app.route('/', methods=['GET'])
    @app.route('/ping', methods=['GET'])
    def hello():
        return 'Hello, World!' + ' from ' + app_name

    return app


class Application(object):
    def __init__(self, name):
        self.app = create_application(name)
        self.name = name

    def start(self, host='127.0.0.1', port=5000):
        # With Multi-Threading Apps, YOU CANNOT USE DEBUG! Though you can sub-thread.
        th = threading.Thread(
            target=lambda: self.app.run(host, port, debug=False, threaded=True))
        th.start()


if __name__ == '__main__':
    app = Application('app1')
    app.start(port=5000)

    app = Application('app2')
    app.start(port=5001)
