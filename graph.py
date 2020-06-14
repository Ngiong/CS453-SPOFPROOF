import pydot
import time


# create graph object
class Node_Graph():
    name = ''
    G = None
    target_node = ""
    source_node = ""
    colored_edges_dest = []

    def __init__(self):
        self.G = pydot.Dot(graph_type="digraph")
        self.G.set('splines', True)
        
    def set_source_node(self, node_name):
        # get current source_node and reset node and edge color
        if self.source_node != "":
            current = self.G.get_node(self.source_node)
            current[0].set_style("None")
            self.edge_color_normalization(self.source_node)
        graph_node = self.G.get_node(node_name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("blue")
        self.source_node = node_name

    def set_target_node(self, node_name):
        # get current target_node and reset color
        if self.target_node != "":
            current = self.G.get_node(self.target_node)
            # only reset color if it is not the source node
            if current[0].get_fillcolor() != "blue":
                current[0].set_style("None")

        graph_node = self.G.get_node(node_name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("red")

        self.target_node = node_name

    def set_edge_color(self, src, dest, color):
        edge = self.G.get_edge(src, dest)
        if len(edge) > 0:
            edge[0].set_color(color)
            if color != "black":
                self.colored_edges_dest.append(dest)

    def add_node(self, node_name, pos=None):
        if pos is None:
            self.G.add_node(pydot.Node(node_name))
        else:
            x, y = pos
            node = pydot.Node(node_name)
            node.set('pos', f'{x}, {y}!')
            self.G.add_node(node)

    def add_edge(self, node1, node2):
        edge = pydot.Edge(node1, node2)
        self.G.add_edge(edge)

    def remove_edge(self, node1, node2):
        self.G.del_edge(node1, node2)

    def save_graph(self, path, final=False):
        if not path.endswith("./__pic.png"):
            path += ".png"

        if final:
            if self.target_node != "":
                current = self.G.get_node(self.target_node)
                current[0].set_style("None")
            self.G.write(path, prog='dot', format='png')
        else:
            self.G.write(path, prog='neato', format='png')

    # getting called, when source node is changed
    def edge_color_normalization(self, src):
        for node in self.colored_edges_dest:
            self.set_edge_color(src,node,"black")
        self.colored_edges_dest = []

    # reset colors of source and target node
    def graph_build_finished(self):
        if self.source_node != "":
            self.edge_color_normalization(self.source_node)
            current = self.G.get_node(self.source_node)
            current[0].set_style("None")
        if self.target_node != "":
            current = self.G.get_node(self.target_node)
            current[0].set_style("None")


class GraphVisualizer:
    target_img = './__pic.png'
    graph = Node_Graph()
    prev_edge_test = None
    enabled = False

    def __init__(self, enabled=False):
        self.enabled = enabled

    def flush(self, final=False):
        if self.enabled or final:
            self.graph.save_graph(self.target_img, final)
            time.sleep(1.25)

    def draw_initialize(self, node_names=None):
        if node_names is None:
            node_names = []

        # positions = infer_positions(node_names)
        positions = []
        for idx, node_name in enumerate(node_names):
            x, y = (idx // 2) * 2, 2 if idx % 2 == 0 else 0
            positions.append((x, y))

        for idx, node_name in enumerate(node_names):
            self.graph.add_node(node_name, positions[idx])

        self.flush()

    def draw_target(self, node):
        if self.prev_edge_test is not None:
            u, v = self.prev_edge_test
            self.graph.remove_edge(u, v)

        self.graph.set_target_node(node)
        self.flush()

    def draw_edge_test(self, src, dest):
        if self.prev_edge_test is not None:
            u, v = self.prev_edge_test
            self.graph.remove_edge(u, v)

        self.graph.add_edge(src, dest)
        self.graph.set_edge_color(src, dest, "green")
        self.flush()
        self.prev_edge_test = (src, dest)

    def draw_dependency(self, src, dest):
        self.graph.set_edge_color(src, dest, "black")
        self.flush()
        self.prev_edge_test = None

    def draw_complete_test(self):
        if self.prev_edge_test is not None:
            u, v = self.prev_edge_test
            self.graph.remove_edge(u, v)
        self.flush(final=True)
