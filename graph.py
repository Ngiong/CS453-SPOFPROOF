import pydot
import os
import threading
import time
from poc.poc import POCNode
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


#create graph object
class Node_Graph():
    name = ''
    G = None
    target = ""

    def __init__(self, name ): 
        self.name = name
        self.G = pydot.Dot(graph_type="digraph")
        X = [[1],[1]]# sample 2D array
        self.figure= plt.imshow(X, aspect='auto')
        plt.axis("off")
        plt.ion()
        self.gui_thread = threading.Thread(target=self.show_matplot)


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
        edge = pydot.Edge(node1.name, node2.name, color="blue")
        self.G.add_edge(edge)

    def save_graph(self, path):
        if not path.endswith("./pic.png"):
            path += ".png"
        self.G.write_png(path)

    def show_matplot(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            print("called")
            img = mpimg.imread('./pic.png')
            self.figure.set_data(img)
            plt.show()
            plt.pause(0.001)
            print("plotted")     
        print("Stopping as you wish.")   
     


        

    def gui_thread_start(self):
        self.gui_thread.start()
        #threading.Thread(target=self.show_matplot).start()

    def gui_thread_stop(self):
        self.gui_thread.do_run = False
        self.gui_thread.join()


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
    graph.gui_thread_start()
    time.sleep(2)
    graph.set_target_node(node2)
    graph.save_graph("./pic.png")
    
    

    time.sleep(2)


    graph.gui_thread_stop()
if __name__ == '__main__':
    testing()