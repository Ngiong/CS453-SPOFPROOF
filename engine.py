from node import INode


class SPOFProofEngine:
    nodes = dict()
    dependency_found = []

    def set_nodes(self, inodes: [INode]):
        for inode in inodes:
            self.nodes[inode.get_name()] = inode

    def run_test(self):
        # TODO: implementation of chaotic testing
        # TODO: kill a node, check all other, if it has dependency, add to dependency found
        pass

    def print_dependency(self):
        # TODO: print/display the dependency graph
        pass