import pydot
import os

from poc import POCNode


#create graph object
class Node_Graph():
    name = ''
    G = None
    target = ""

    def __init__(self, name ): 
        self.name = name
        self.G = pydot.Dot(graph_type="digraph")

    def set_target_node(self, node):

        # get current target and reset color
        if self.target != "":
            current = self.G.get_node(self.target)
            print(current)
            current[0].set_style("None")

        graph_node = self.G.get_node(node.name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("red")

        self.target = node.name

    def add_node(self, node):
        self.G.add_node(pydot.Node(node.name))

    def add_edge(self, node1, node2):
        edge = pydot.Edge(node1.name, node2.name)
        self.G.add_edge(edge)

    def save_graph(self, path):
        if not path.endswith(".png"):
            path += ".png"
        self.G.write_png(path)

def testing(): 
    print("Hello world")
    graph = Node_Graph("testgraph")
    node1 = POCNode('app1', '127.0.0.1', 5000)
    node2 = POCNode('app2', '127.0.0.1', 5001)
    node3 = POCNode('app3', '127.0.0.1', 5002)

    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    graph.set_target_node(node1)
    graph.add_edge(node1,node2)
    graph.save_graph("./pic")
    graph.set_target_node(node2)
    graph.save_graph("./pic2.png")




if __name__ == '__main__':
    testing()