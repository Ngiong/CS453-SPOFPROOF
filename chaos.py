from node import INode


class ChaosTestingEngine:
    nodes = dict()
    dependency_found = []

    def add_node(self, inode: INode):
        self.nodes[inode.get_name()] = inode
        return self

    def run_test(self):
        # TODO: implementation of chaotic testing
        # TODO: kill a node, check all other, if it has dependency, add to dependency found
        pass

    def print_dependency(self):
        # TODO: print/display the dependency graph
        pass