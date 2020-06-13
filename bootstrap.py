from concurrent.futures import _base
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread
from time import sleep
from typing import Iterable

from flask import Flask, Response, current_app, request
from requests import get as http_get

from node import ResponseLevel, inverse_response_level, SimpleNode

PORT_APP = dict()


def create_application(app_name: str, dependencies=None):
    dependencies = [] if dependencies is None else dependencies
    app_name = app_name.replace(',', '_')

    app = Flask(app_name)
    app.__response_level = ResponseLevel.NORMAL
    app.__dependencies = dependencies
    app.__executor = ThreadPoolExecutor(max_workers=16)

    # check dependencies must run asynchronously
    def check_dependencies(visited: str, dependencies: Iterable[str], executor: _base.Executor) -> bool:
        visited_set = set(visited.split(','))
        filtered_dep = filter(lambda x: PORT_APP[int(x.split(':')[1])] not in visited_set, dependencies)

        futures = []
        for target in filtered_dep:
            get_url = f'http://{target}/?from={visited}'
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
    def __init__(self, name, dependencies=None):
        dependencies = [] if dependencies is None else dependencies
        self.app = create_application(name, dependencies)

    def start(self, host='127.0.0.1', port=5000):
        # With Multi-Threading Apps, YOU CANNOT USE DEBUG! Though you can sub-thread.
        th = Thread(target=lambda: self.app.run(host, port, debug=False, threaded=True))
        th.start()


def bootstrap(graph=None, names=None):
    """
    Constructs startrable POCNode, and return the list of nodes
    @param graph:
        A dependency graph that looks like:{v:{v1,v2}}
        v: node number
        v1,v2: node numbers that influence node v
        if v has no dependent nodes, {v:{}}
    @return:
        Startable Node list
    """
    # for (port, name) in zip(ports, names):
    #     PORT_APP[port] = name

    if graph is None:
        graph = {}
    if names is None:
        names = {}

    host = '127.0.0.1'
    name_and_address = []
    dependencies = dict()
    for k, v in graph.items():
        node_name = "app" + str(k)
        port = 5000 + int(k)
        address = host + ':' + str(port)
        name_and_address.append((node_name, address))
        dependencies[node_name] = []
        for dependent in v:
            if k == dependent:
                continue
            dependencies[node_name].append(host + ':' + str(5000 + int(dependent)))
        if len(dependencies[node_name]) == 0:
            SimpleNodeStartable(node_name).start(port=port)
        else:
            SimpleNodeStartable(node_name, dependencies[node_name]).start(port=port)
        PORT_APP[port] = node_name

    # create Node
    nodes = []
    for ele in name_and_address:
        name = ele[0]
        port = ele[1].split(":")[1]
        port = int(port)
        nodes.append(SimpleNode(name, host, port))

    # return [node_list]
    return nodes


if __name__ == '__main__':
    graph = {
        1: {2, 3},
        2: {4},
        3: {},
        4: {}
    }
    names = {
        1: 'app1',
        2: 'app2',
        3: 'app3',
        4: 'app4',
    }
    nodes = bootstrap(graph, names)

    # for ele in nodes:
    #     assert(ele.ping())
    # # direct releationship
    # nodes[1].set_response_level(ResponseLevel.TERMINATED) # terminate node 2
    # assert not nodes[0].ping()
    # # recover
    # nodes[1].resurrect()
    # assert nodes[0].ping()
    # # indirect relationship
    # nodes[3].set_response_level(ResponseLevel.TERMINATED)  # terminate node 4
    # assert not nodes[0].ping()

    # graph = construct_random_graph()
    # nodes = bootstrap(graph)
    # for ele in nodes:
    #     assert ele.ping()
