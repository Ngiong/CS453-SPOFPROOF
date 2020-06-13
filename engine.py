from node import INode, ResponseLevel
import sys
sys.path.append("poc")
from poc.poc import POCNode
from poc.bootstrap_flask import POCNodeStartable, PORT_APP


class SPOFProofEngine:
    nodes = dict()
    dependency_found = dict()

    def set_nodes(self, inodes: [INode]):
        for inode in inodes:
            self.nodes[inode.get_name()] = inode

    def run_test(self):
        for node_name in self.nodes:
            other_nodes = self.nodes.copy()
            other_nodes.pop(node_name, None)

            # Kill a node
            curr_node = self.nodes[node_name]
            curr_node.kill()

            # Ping every remaining node
            for node in other_nodes:
                # If ping doesnt work, then this has dependency
                if not other_nodes[node].ping():
                    if node in self.dependency_found and (node_name not in self.dependency_found[node]):
                        self.dependency_found[node].append(node_name)
                    elif node not in self.dependency_found:
                        self.dependency_found[node] = [node_name]

            # Resurrect the node
            curr_node.resurrect()

    def run_repeated_test(self, n_tests=10):
        for i in range(n_tests):
            self.run_test()

    def print_dependency(self):
        print(self.dependency_found)

def main():
    # Adding the boostrap part
    app1 = POCNodeStartable('app1')
    app1.start(port=5000)

    app2 = POCNodeStartable('app2', ['127.0.0.1:5000'])
    app2.start(port=5001)

    app3 = POCNodeStartable('app3', ['127.0.0.1:5001'])
    app3.start(port=5002)

    app4 = POCNodeStartable('app4', ['127.0.0.1:5001'])
    app4.start(port=5003)

    app5 = POCNodeStartable('app5', ['127.0.0.1:5000', '127.0.0.1:5002'])
    app5.start(port=5004)

    names = ['app1', 'app2', 'app3', 'app4', 'app5']
    ports = [5000, 5001, 5002, 5003, 5004]

    for (port, name) in zip(ports, names):
        PORT_APP[port] = name

    #----------------------------------------------
    # Test if the NodeStartable is running correctly
    # node1 = POCNode('app1', '127.0.0.1', 5000)
    # assert node1.ping()

    # assert node1.set_response_level(ResponseLevel.TERMINATED)
    # assert not node1.ping()

    # assert node1.set_response_level(ResponseLevel.SLOW)
    # assert node1.ping()

    # # Check dependency
    # node2 = POCNode('app2', '127.0.0.1', 5001)
    # node1.set_response_level(ResponseLevel.NORMAL)
    # assert node2.ping()

    # node1.set_response_level(ResponseLevel.TERMINATED)
    # assert not node2.ping()
    # print("Test success")
    # node1.resurrect()

    # Initialize node for test
    node1 = POCNode('app1', '127.0.0.1', 5000)
    node2 = POCNode('app2', '127.0.0.1', 5001)
    node3 = POCNode('app3', '127.0.0.1', 5002)
    node4 = POCNode('app4', '127.0.0.1', 5003)
    node5 = POCNode('app5', '127.0.0.1', 5004)

    nodes = [node1, node2, node3, node4, node5]

    for node in nodes:
        assert node.ping()

    # Test the engine
    engine = SPOFProofEngine()
    engine.set_nodes(nodes)
    engine.run_test()
    engine.print_dependency()

if __name__ == '__main__':
    main()