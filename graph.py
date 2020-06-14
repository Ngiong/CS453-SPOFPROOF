import pydot
import threading
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# create graph object
class Node_Graph():
    name = ''
    G = None
    target_node = ""
    current_edge_test = None

    def __init__(self):
        self.G = pydot.Dot(graph_type="digraph")
        self.G.set_size("9,15\!")
        self.G.set_dpi(100)

        self.G.write_png("./__init.png")
        img = mpimg.imread('./__init.png')
        # X = [[1]]# sample 2D array
        self.figure = plt.imshow(img, aspect=1)  # , aspect='auto'
        # plt.axis("scaled")
        # plt.axis("off")
        plt.ion()
        self.gui_thread = threading.Thread(target=self.show_matplot)

    def set_target_node(self, node_name):
        # get current target_node and reset color
        if self.target_node != "":
            current = self.G.get_node(self.target_node)
            current[0].set_style("None")

        graph_node = self.G.get_node(node_name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("red")

        self.target_node = node_name

    def set_edge_color(self, src, dest, color):
        edge = self.G.get_edge(src, dest)
        if len(edge) > 0:
            # print("change edge color")
            edge[0].set_color(color)

    def add_node(self, node_name):
        self.G.add_node(pydot.Node(node_name))

    def add_edge(self, node1, node2):
        edge = pydot.Edge(node1, node2)  # , color="blue"
        self.G.add_edge(edge)

    def remove_edge(self, node1, node2):
        self.G.del_edge(node1, node2)

    def save_graph(self, path):
        if not path.endswith("./__pic.png"):
            path += ".png"
        self.G.write_png(path)

    def show_matplot(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            # print("called")
            img = mpimg.imread('./__pic.png')
            # self.figure.set_data(img)
            plt.figure(img)
            plt.show()
            plt.pause(0.001)
            # print("plotted")
        # print("Stopping as you wish.")

    def gui_thread_start(self):
        self.gui_thread.start()
        # threading.Thread(target=self.show_matplot).start()

    def gui_thread_stop(self):
        self.gui_thread.do_run = False
        self.gui_thread.join()


class GUI:
    target_img = './__pic.png'
    graph = Node_Graph()
    prev_edge_test = None

    def flush(self):
        self.graph.save_graph(self.target_img)
        time.sleep(2)

    def draw_initialize(self, node_names=None):
        if node_names is None:
            node_names = []

        for node_name in node_names:
            self.graph.add_node(node_name)

        self.flush()

    def draw_kill(self, node):
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


def testing():
    # print("Hello world")
    graph = Node_Graph()

    graph.add_node('app1')
    graph.add_node('app2')
    graph.add_node('app3')

    graph.set_target_node('app1')
    graph.add_edge('app1', 'app2')
    graph.save_graph("./__pic")

    # graph.gui_thread_start()
    time.sleep(2)

    graph.set_target_node('app2')
    graph.save_graph("./__pic.png")
    time.sleep(2)

    graph.add_edge('app2', 'app3')
    graph.save_graph("./__pic.png")
    time.sleep(2)

    graph.set_edge_color('app2', 'app3', "green")
    graph.save_graph("./__pic.png")
    time.sleep(2)


def testGUI():
    gui = GUI()
    gui.draw_initialize(['app1', 'app2', 'app3', 'app4'])

    gui.draw_kill('app1')
    gui.draw_edge_test('app2', 'app1')
    gui.draw_dependency('app2', 'app1')
    gui.draw_edge_test('app3', 'app1')
    gui.draw_edge_test('app4', 'app1')
    gui.draw_dependency('app4', 'app1')

    gui.draw_kill('app2')
    gui.draw_edge_test('app1', 'app2')
    gui.draw_dependency('app1', 'app2')
    gui.draw_edge_test('app3', 'app2')
    gui.draw_edge_test('app4', 'app2')
    gui.draw_dependency('app4', 'app2')


if __name__ == '__main__':
    testGUI()
    # testing()
