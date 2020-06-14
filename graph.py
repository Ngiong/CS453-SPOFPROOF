import pydot
import os
import time
from poc.poc import POCNode
import webbrowser as web

#create graph object
class Node_Graph():
    name = ''
    G = None
    target_node = ""
    source_node = ""
    colored_edges_dest = []

    def __init__(self, name ): 
        self.name = name
        self.G = pydot.Dot(graph_type="digraph")

    def add_node(self, node):
        self.G.add_node(pydot.Node(node.name))

    def add_edge(self, node1, node2):
        edge = pydot.Edge(node1.name, node2.name)
        self.G.add_edge(edge)
    
    def del_edge(self, node1, node2):
        self.G.del_edge(node1.name,node2.name)

    def save_graph(self, path):
        if not path.endswith(".png"):
            path += ".png"
        self.G.write_png(path)

    def set_source_node(self, node):
        # get current source_node and reset node and edge color
        if self.source_node != "":
            current = self.G.get_node(self.source_node.name)
            current[0].set_style("None")
            self.edge_color_normalization(self.source_node)
        graph_node = self.G.get_node(node.name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("blue")
        self.source_node = node

    def set_target_node(self, node):
        # get current target_node and reset color
        if self.target_node != "":
            current = self.G.get_node(self.target_node)
            # only reset color if it is not the source node
            if current[0].get_fillcolor() != "blue":
                current[0].set_style("None")

        graph_node = self.G.get_node(node.name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("red")
        self.target_node = node.name

    def set_edge_color(self, src, dest, color):
        edge = self.G.get_edge(src.name, dest.name)
        if len(edge) > 0:
            edge[0].set_color(color)
            if color != "black":
                self.colored_edges_dest.append(dest)

    #getting called, when source node is changed
    def edge_color_normalization(self, src):
        for node in self.colored_edges_dest:
            self.set_edge_color(src,node,"black")
        self.colored_edges_dest = []

    def graph_build_finished(self):
        if self.source_node != "":
            self.edge_color_normalization(self.source_node)
            current = self.G.get_node(self.source_node.name)
            current[0].set_style("None")

        if self.target_node != "":
            current = self.G.get_node(self.target_node)
            current[0].set_style("None")



def testing(): 
    delay = 1
    web.open(os.path.dirname(os.path.realpath(__file__))+"/spofproof.html")
    graph = Node_Graph("testgraph")
    node1 = POCNode('app1', '127.0.0.1', 5000)
    node2 = POCNode('app2', '127.0.0.1', 5001)
    node3 = POCNode('app3', '127.0.0.1', 5002)
    node4 = POCNode('app4', '127.0.0.1', 5003)

    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    graph.add_node(node4)

    ### Source Node 1###
    ### EDGE 1###
    graph.set_source_node(node1)
    graph.set_target_node(node2)
    graph.add_edge(node1,node2)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.del_edge(node1, node2)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node3)
    graph.add_edge(node1,node3)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.set_edge_color(node1,node3,"green")
    graph.save_graph("./pic.png")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node4)
    graph.add_edge(node1,node4)

    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.del_edge(node1, node4)
    graph.save_graph("./pic")
    time.sleep(delay)

    ### Source Node 2###
    graph.set_source_node(node2)
    ### EDGE 1###
    graph.set_target_node(node1)
    graph.add_edge(node2,node1)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.set_edge_color(node2,node1,"green")
    graph.save_graph("./pic.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node3)
    graph.add_edge(node2,node3)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.del_edge(node2, node3)
    graph.save_graph("./pic")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node4)
    graph.add_edge(node2,node4)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.set_edge_color(node2,node4,"green")
    graph.save_graph("./pic.png")
    time.sleep(delay)

    ### Source Node 3###
    ### EDGE 1###
    graph.set_source_node(node3)
    graph.set_target_node(node1)
    graph.add_edge(node3,node1)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.del_edge(node3, node1)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node2)
    graph.add_edge(node3,node2)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.set_edge_color(node3,node2,"green")
    graph.save_graph("./pic.png")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node4)
    graph.add_edge(node3,node4)

    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.del_edge(node3, node4)
    graph.save_graph("./pic")
    time.sleep(delay)

    ### Source Node 4###
    graph.set_source_node(node4)
    ### EDGE 1###
    graph.set_target_node(node1)
    graph.add_edge(node4,node1)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.set_edge_color(node4,node1,"green")
    graph.save_graph("./pic.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node2)
    graph.add_edge(node4,node2)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.del_edge(node4, node2)
    graph.save_graph("./pic")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node3)
    graph.add_edge(node4,node3)
    graph.save_graph("./pic.png")
    time.sleep(delay)

    graph.set_edge_color(node4,node3,"green")
    graph.save_graph("./pic.png")
    time.sleep(delay)

    # finish raph building
    graph.graph_build_finished()
    graph.save_graph("./pic.png")


if __name__ == '__main__':
    testing()