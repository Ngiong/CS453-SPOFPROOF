from engine import SPOFProofEngine
from node import SimpleNode


def main():
    parent1 = SimpleNode(name='parent 1', ip_address='localhost', port=3887)
    parent2 = SimpleNode(name='parent 2', ip_address='localhost', port=3888)
    dependant = SimpleNode(name='dependant', ip_address='localhost', port=3889)

    engine = SPOFProofEngine()
    engine.set_nodes([parent1, parent2, dependant])
    engine.run_test()
    engine.print_dependency()


if __name__ == '__main__':
    main()