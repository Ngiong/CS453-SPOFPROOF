from graph import GraphVisualizer
from node import INode, SimpleNode


class SPOFProofEngine:
    nodes = dict()
    dependency_found = dict()

    def set_nodes(self, inodes: [INode]):
        for inode in inodes:
            self.nodes[inode.get_name()] = inode

    def run_test(self, n_tests=1, sim_mode=False):
        viz = GraphVisualizer(enabled=sim_mode)
        viz.draw_initialize(node_names=self.nodes.keys())

        for target_node_name in self.nodes:
            other_nodes = self.nodes.copy()
            other_nodes.pop(target_node_name, None)

            # Kill a node
            curr_node = self.nodes[target_node_name]
            curr_node.kill()
            viz.draw_target(target_node_name)

            # Ping every remaining node
            for other_node in other_nodes:

                # If ping doesnt work, then this has dependency
                other_inode = other_nodes[other_node]
                has_dependency = False
                viz.draw_edge_test(other_node, target_node_name)

                for i in range(n_tests):
                    is_healthy = other_inode.ping()
                    has_dependency |= not is_healthy
                    if has_dependency:
                        break

                if has_dependency:
                    viz.draw_dependency(other_node, target_node_name)
                    if other_node in self.dependency_found:
                        self.dependency_found[other_node].append(target_node_name)
                    elif other_node not in self.dependency_found:
                        self.dependency_found[other_node] = [target_node_name]

            # Resurrect the node
            curr_node.resurrect()

        # Viz on complete
        viz.draw_complete_test()

    def print_dependency(self):
        print(self.dependency_found)


def main():
    # Initialize node for test
    node1 = SimpleNode('app1', '127.0.0.1', 5001)
    node2 = SimpleNode('app2', '127.0.0.1', 5002)
    node3 = SimpleNode('app3', '127.0.0.1', 5003)
    node4 = SimpleNode('app4', '127.0.0.1', 5004)

    nodes = [node1, node2, node3, node4]

    for node in nodes:
        node.resurrect()

    # Nodes OK?
    for node in nodes:
        assert node.ping()

    # Test the engine
    engine = SPOFProofEngine()
    engine.set_nodes(nodes)
    engine.run_test(n_tests=10, sim_mode=True)
    engine.print_dependency()


if __name__ == '__main__':
    main()
