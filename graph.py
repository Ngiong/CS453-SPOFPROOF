import pydot
import os
import threading
import time
from poc.poc import POCNode
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import webbrowser as web


#create graph object
class Node_Graph():
    name = ''
    G = None
    target_node = ""

    def __init__(self, name ): 
        self.name = name
        self.G = pydot.Dot(graph_type="digraph")
        self.G.set_size("9,15\!")
        self.G.set_dpi(100)
        
        self.G.write_png("./init.png")
        img = mpimg.imread('./init.png')
        #X = [[1]]# sample 2D array
        self.figure= plt.imshow(img, aspect=1)  #, aspect='auto'
        #plt.axis("scaled")
        #plt.axis("off")
        plt.ion()
        self.gui_thread = threading.Thread(target=self.show_matplot)


    def set_target_node(self, node):

        # get current target_node and reset color
        if self.target_node != "":
            current = self.G.get_node(self.target_node)
            print(current)
            current[0].set_style("None")

        graph_node = self.G.get_node(node.name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("red")

        self.target_node = node.name

    def set_edge_color(self, src, dest, color):
        edge = self.G.get_edge(src.name, dest.name)
        print(edge)
        if len(edge) > 0:
            print("change edge color")
            edge[0].set_color(color)

    def add_node(self, node):
        self.G.add_node(pydot.Node(node.name))

    def add_edge(self, node1, node2):
        edge = pydot.Edge(node1.name, node2.name)  #, color="blue"
        self.G.add_edge(edge)

    def save_graph(self, path):
        if not path.endswith("./pic.png"):
            path += ".png"
        self.G.write_png(path)

    def show_matplot(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print("called")
            img = mpimg.imread('./pic.png')
            #self.figure.set_data(img)
            plt.figure(img)
            plt.show()
            plt.pause(0.001)
            #print("plotted")     
        #print("Stopping as you wish.")   
     


    def gui_thread_start(self):
        self.gui_thread.start()
        #threading.Thread(target=self.show_matplot).start()

    def gui_thread_stop(self):
        self.gui_thread.do_run = False
        self.gui_thread.join()


def testing(): 
    web.open(os.path.dirname(os.path.realpath(__file__))+"/Spoofproof.html")
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
    #graph.gui_thread_start()
    time.sleep(2)
    graph.set_target_node(node2)
    graph.save_graph("./pic.png")
    time.sleep(2)

    graph.add_edge(node2,node3)
    graph.save_graph("./pic.png")
    time.sleep(2)

    graph.set_edge_color(node2,node3,"green")
    graph.save_graph("./pic.png")
    time.sleep(2)

    #graph.gui_thread_stop()
if __name__ == '__main__':
    testing()