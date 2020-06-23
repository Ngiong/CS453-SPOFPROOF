
from engine import SPOFProofEngine
from node import SimpleNode


def main():
    node1 = SimpleNode('app1', '127.0.0.1', 5001)
    node2 = SimpleNode('app2', '127.0.0.1', 5002)
    node3 = SimpleNode('app3', '127.0.0.1', 5003)
    node4 = SimpleNode('app4', '127.0.0.1', 5004)

    for node in nodes:
        node.resurrect()

    for node in nodes:
        assert node.ping()

    engine = SPOFProofEngine()
    engine.set_nodes([node1, node2, node3, node4])
    engine.run_test(n_tests=10, sim_mode=True)
    engine.print_dependency()


if __name__ == '__main__':
    main()