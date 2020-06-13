from abc import ABC, abstractmethod
from node import INode, ResponseLevel
import sys
sys.path.append("poc/")
from poc.poc import POCNode
from poc.bootstrap_flask import POCNodeStartable, PORT_APP
import random

# TODO: if it is possible, we might want to be able to automatically start the microservice environment
# This is just an example to bootstrap the microservice


class IStartable(ABC):
    @abstractmethod
    def start(self):
        pass

# TODO: IMPORTANT! THIS CODE DESIGN IS TERRIBLY WRONG. Please refer to the PoC in poc directory.
class SimpleNodeStartable(INode, IStartable):
    dependencies = []

    def __str__(self):
        pass

    def ping(self):
        pass

    def set_response_level(self, response_level: ResponseLevel):
        pass

    def get_name(self):
        pass

    def set_dependencies(self, node):
        self.dependencies = ['{}:{}'.format(x.ip_address, x.port) for x in node]

    def start(self):
        # TODO: when called, this method will start the webserver on specified ip_address & port
        pass


def bootstrap(graph:{}):
    """
    Constructs startrable POCNode, and return the list of nodes
    @param graph:
        A dependency graph that looks like:{v:{v1,v2}}
        v: node number
        v1,v2: node numbers that influence node v
        if v has no dependent nodes, {v:{}}
    @return:
        True if the function f is nonzero polynomial, False otherwise.
    """
    host = '127.0.0.1'
    name_and_address = []
    dependencies = dict()
    for k,v in graph.items():
        node_name = "app"+str(k)
        port = 5000 + int(k)
        address = host + ':' + str(port)
        name_and_address.append((node_name, address))
        dependencies[node_name] = []
        for dependent in v:
            if k == dependent:
                continue
            dependencies[node_name].append(host+':'+str(5000+int(dependent)))
        if len(dependencies[node_name]) == 0:
            POCNodeStartable(node_name).start(port=port)
        else:
            POCNodeStartable(node_name, dependencies[node_name]).start(port=port)
        PORT_APP[port] = node_name

    # create Node
    nodes = []
    for ele in name_and_address:
        name = ele[0]
        port = ele[1].split(":")[1]
        port = int(port)
        nodes.append(POCNode(name, host, port))

    # return [node_list]
    return nodes


def construct_random_graph():
    N = random.randint(1,1000)
    graph = {}
    for i in range(N):
        dependencies = []
        for j in range(N):
            if j == i:
                continue
            if round(random.random()) == 0:
                dependencies.append(j)
        graph[i] = dependencies
    return graph
if __name__ == '__main__':
    # graph = {1:{2,3},2:{4},3:{},4:{}}
    # nodes = bootstrap(graph)
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

    graph = construct_random_graph()
    nodes = bootstrap(graph)
    for ele in nodes:
        assert ele.ping()
