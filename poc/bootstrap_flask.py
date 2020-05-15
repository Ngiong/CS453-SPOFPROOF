from concurrent.futures import _base
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread
from time import sleep
from typing import Iterable

from flask import Flask, Response, current_app, request
from requests import get as http_get

from node import ResponseLevel, inverse_response_level


def create_application(app_name, dependencies=None):
    dependencies = [] if dependencies is None else dependencies

    app = Flask(app_name)
    app.__response_level = ResponseLevel.NORMAL
    app.__dependencies = dependencies
    app.__executor = ThreadPoolExecutor(max_workers=16)

    # check dependencies must run asynchronously
    def check_dependencies(dependencies: Iterable[str], executor: _base.Executor) -> bool:
        futures = []
        for target in dependencies:
            get_url = f'http://{target}/'
            future = executor.submit(lambda: http_get(get_url))
            futures.append((get_url, future))

        for (get_url, future) in futures:
            result = future.result()
            is_ok = result.status_code == 200
            if not is_ok:
                return False

        return True

    @app.route('/', methods=['GET'])
    @app.route('/ping', methods=['GET'])
    def ping():
        response_level = current_app.__response_level
        if response_level == ResponseLevel.NORMAL:
            dependencies_ok = True
            if 'ping' in request.path:
                dependencies_ok = check_dependencies(current_app.__dependencies, current_app.__executor)
            message, code = ('OK', 200) if dependencies_ok else ('UNHEALTHY', 500)
            return Response(message, code)

        elif response_level == ResponseLevel.TERMINATED:
            return Response('UNHEALTHY', 500)

        else:
            sleep(5.0)
            dependencies_ok = True
            if 'ping' in request.path:
                dependencies_ok = check_dependencies(current_app.__dependencies, current_app.__executor)
            message, code = ('OK', 200) if dependencies_ok else ('UNHEALTHY', 500)
            return Response(message, code)

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
    def __init__(self, name, dependencies=None):
        dependencies = [] if dependencies is None else dependencies
        self.app = create_application(name, dependencies)

    def start(self, host='127.0.0.1', port=5000):
        # With Multi-Threading Apps, YOU CANNOT USE DEBUG! Though you can sub-thread.
        th = Thread(target=lambda: self.app.run(host, port, debug=False, threaded=True))
        th.start()


def main():
    N = 5
    names = ['app1','app2','app3','app4','app5']
    ports = [5000, 5001, 5002, 5003, 5004]
    edges = []

    # Complete graph
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            edges.append((i, j))

    sorted_edges = sorted(edges)
    adj_list = dict()
    for (u, v) in sorted_edges:
        adj_list[u] = [] if u not in adj_list else adj_list[u]
        adj_list[u] += [v]

    for i in range(N):
        name = names[i]
        port = ports[i]
        dependencies = [f'127.0.0.1:{ports[x]}' for x in adj_list[i]]

        app = POCNodeStartable(name, dependencies)
        app.start(port=port)


if __name__ == '__main__':
    main()