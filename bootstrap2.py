import time
from concurrent.futures import _base
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread
from time import sleep
from typing import Iterable

from flask import Flask, Response, current_app, request
from requests import get as http_get

from node import ResponseLevel, inverse_response_level


PORT_APP = dict()


def create_application(app_name: str, dependencies=None):
    dependencies = [] if dependencies is None else dependencies
    app_name = app_name.replace(',', '_')

    app = Flask(app_name)
    app.__response_level = ResponseLevel.NORMAL
    app.__dependencies = dependencies
    app.__executor = ThreadPoolExecutor(max_workers=16)

    # check dependencies should run asynchronously
    def check_dependencies(visited: str, dependencies: Iterable[str], executor: _base.Executor) -> bool:
        visited_set = set(visited.split(','))
        filtered_dep = filter(lambda x: PORT_APP[int(x.split(':')[1])] not in visited_set, dependencies)

        # futures = []
        # for target in filtered_dep:
        #     get_url = f'http://{target}/?from={visited}'
        #     future = executor.submit(lambda: http_get(get_url))
        #     futures.append((get_url, future))
        #
        # for (get_url, future) in futures:
        #     result = future.result()
        #     is_ok = result.status_code == 200
        #     if not is_ok:
        #         return False

        for target in filtered_dep:
            get_url = f'http://{target}/?from={visited}'
            response = http_get(get_url)
            is_ok = response.status_code == 200
            if not is_ok:
                return False

        return True

    @app.route('/', methods=['GET'])
    @app.route('/ping', methods=['GET'])
    def ping():
        visited = request.args.get('from')
        updated_visited = current_app.name + ('' if visited is None else (',' + visited))

        response_level = current_app.__response_level
        if response_level == ResponseLevel.NORMAL:
            dependencies_ok = check_dependencies(updated_visited, current_app.__dependencies, current_app.__executor)
            message, code = ('OK', 200) if dependencies_ok else ('UNHEALTHY', 500)
            return Response(message, code)

        elif response_level == ResponseLevel.TERMINATED:
            return Response('UNHEALTHY', 500)

        else:
            sleep(5.0)
            dependencies_ok = check_dependencies(updated_visited, current_app.__dependencies, current_app.__executor)
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


def create_load_balancer(app_name: str, dependencies=None):
    dependencies = [] if dependencies is None else dependencies
    app_name = app_name.replace(',', '_')

    app = Flask(app_name)
    app.__response_level = ResponseLevel.NORMAL
    app.__dependencies = dependencies
    app.__executor = ThreadPoolExecutor(max_workers=16)

    # check dependencies should run asynchronously
    def check_dependencies(visited: str, dependencies: Iterable[str], executor: _base.Executor) -> bool:
        visited_set = set(visited.split(','))
        filtered_dep = filter(lambda x: PORT_APP[int(x.split(':')[1])] not in visited_set, dependencies)

        # futures = []
        # for target in filtered_dep:
        #     get_url = f'http://{target}/?from={visited}'
        #     future = executor.submit(lambda: http_get(get_url))
        #     futures.append((get_url, future))
        #
        # for (get_url, future) in futures:
        #     result = future.result()
        #     is_ok = result.status_code == 200
        #     if not is_ok:
        #         return False

        for target in filtered_dep:
            get_url = f'http://{target}/?from={visited}'
            response = http_get(get_url)
            is_ok = response.status_code == 200
            if is_ok:
                return True

        return False

    @app.route('/', methods=['GET'])
    @app.route('/ping', methods=['GET'])
    def ping():
        visited = request.args.get('from')
        updated_visited = current_app.name + ('' if visited is None else (',' + visited))

        response_level = current_app.__response_level
        if response_level == ResponseLevel.NORMAL:
            dependencies_ok = check_dependencies(updated_visited, current_app.__dependencies, current_app.__executor)
            message, code = ('OK', 200) if dependencies_ok else ('UNHEALTHY', 500)
            return Response(message, code)

        elif response_level == ResponseLevel.TERMINATED:
            return Response('UNHEALTHY', 500)

        else:
            sleep(5.0)
            dependencies_ok = check_dependencies(updated_visited, current_app.__dependencies, current_app.__executor)
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


class SimpleNodeStartable(object):
    def __init__(self, name, dependencies=None, load_balancer=False):
        dependencies = [] if dependencies is None else dependencies
        if load_balancer:
            self.app = create_load_balancer(name, dependencies)
        else:
            self.app = create_application(name, dependencies)

    def start(self, host='127.0.0.1', port=5000):
        # With Multi-Threading Apps, YOU CANNOT USE DEBUG! Though you can sub-thread.
        th = Thread(target=lambda: self.app.run(host, port, debug=False, threaded=True))
        th.start()


def bootstrap(graph=None):
    if graph is None:
        graph = {}

    host = '127.0.0.1'
    name_and_address = []
    dependencies = dict()

    for node, node_dependencies in graph.items():
        node_name = "app" + str(node)
        port = 5000 + int(node)
        address = host + ':' + str(port)
        name_and_address.append((node_name, address))
        dependencies[node_name] = []

        for dep in node_dependencies:
            if node == dep:
                continue
            dependencies[node_name].append(host + ':' + str(5000 + int(dep)))

        if len(dependencies[node_name]) == 0:
            SimpleNodeStartable(node_name).start(port=port)
        else:
            SimpleNodeStartable(node_name, dependencies[node_name]).start(port=port)

        PORT_APP[port] = node_name

    time.sleep(1)
    print(f'''
!!!!!!!!!!!!!!!!!!!!!!!!!!
!! BOOTSTRAP SUCCESSFUL !!
!!!!!!!!!!!!!!!!!!!!!!!!!!
''')
    for (node_name, address) in name_and_address:
        name = node_name
        port = address.split(":")[1]
        port = int(port)
        print(f'[INFO] {name} is running on {host} (PORT: {port})')

def bootstrap2(graph=None, replication=1):
    if graph is None:
        graph = {}

    host = '127.0.0.1'
    name_and_address = []
    dependencies = dict()

    # assign port for each node
    port_counter = 1
    LB_PORT = dict()
    for node, node_dependencies in graph.items():
        LB_PORT[node] = 5000 + port_counter
        port_counter += 1

    for node, node_dependencies in graph.items():
        replica_ports = []
        for rep in range(replication):
            node_name = "app" + str(node) + f'_{rep}'
            port = 5000 + port_counter
            port_counter += 1
            replica_ports.append(port)

            address = host + ':' + str(port)
            name_and_address.append((node_name, address))
            dependencies[node_name] = []

            for dep in node_dependencies:
                if node == dep:
                    continue
                lb_port = LB_PORT[dep]
                dependencies[node_name].append(host + ':' + str(lb_port))

            if len(dependencies[node_name]) == 0:
                SimpleNodeStartable(node_name).start(port=port)
            else:
                SimpleNodeStartable(node_name, dependencies[node_name]).start(port=port)

            PORT_APP[port] = node_name

        transformed_loc = [f'{host}:{x}' for x in replica_ports]
        node_name = "LB" + str(node)
        port = LB_PORT[node]
        address = host + ':' + str(port)
        name_and_address.append((node_name, address))

        SimpleNodeStartable(node_name, transformed_loc, True).start(port=port)
        PORT_APP[port] = node_name


    time.sleep(1)
    print(f'''
!!!!!!!!!!!!!!!!!!!!!!!!!!
!! BOOTSTRAP SUCCESSFUL !!
!!!!!!!!!!!!!!!!!!!!!!!!!!
''')
    for (node_name, address) in name_and_address:
        name = node_name
        port = address.split(":")[1]
        port = int(port)
        print(f'[INFO] {name} is running on {host} (PORT: {port})')


if __name__ == '__main__':
    # graph = {
    #     1: {2, 3},
    #     2: {4},
    #     3: {},
    #     4: {}
    # }
    graph = {
        1: {2},
        2: {}
    }
    bootstrap2(graph, 1)
