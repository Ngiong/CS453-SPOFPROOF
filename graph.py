import pydot
import os
import threading
import time
from poc.poc import POCNode

""" from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg """

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
        
        """ self.G.set_size("9,15\!")
        self.G.set_dpi(100)
        
        self.G.write_png("./init.png")
        img = mpimg.imread('./init.png')
        #X = [[1]]# sample 2D array
        self.figure= plt.imshow(img, aspect=1)  #, aspect='auto'
        #plt.axis("scaled")
        #plt.axis("off")
        plt.ion()
        self.gui_thread = threading.Thread(target=self.show_matplot) """


    def add_node(self, node):
        self.G.add_node(pydot.Node(node.name))

    def add_edge(self, node1, node2):
        edge = pydot.Edge(node1.name, node2.name)  #, color="blue"
        self.G.add_edge(edge)
    
    def del_edge(self, node1, node2):
        self.G.del_edge(node1.name,node2.name)

    def save_graph(self, path):
        if not path.endswith(".png"):
            path += ".png"
        self.G.write_png(path)

    def set_source_node(self, node):
        # get current source_node and reset node and edge color
        """ print("change source node")
        print(self.source_node)
        print(" to ", node) """
        if self.source_node != "":
            current = self.G.get_node(self.source_node.name)
            #print("current:", current, "style:", current[0].get_fillcolor())

            current[0].set_style("None")
            #print("DOO NORMALIZATION")
            self.edge_color_normalization(self.source_node)


        graph_node = self.G.get_node(node.name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("blue")

        self.source_node = node

    def set_target_node(self, node):
        # get current target_node and reset color
        if self.target_node != "":
            current = self.G.get_node(self.target_node)
            #print(current)
            #print("set target node current: ", current[0].get_fillcolor())
            # only reset color if it is not the source node
            if current[0].get_fillcolor() != "blue":
                current[0].set_style("None")

        graph_node = self.G.get_node(node.name)
        graph_node[0].set_style("filled")
        graph_node[0].set_fillcolor("red")

        self.target_node = node.name

    def set_edge_color(self, src, dest, color):
        #print("all edges")
        """ for e in self.G.get_edges():
            print(e)
        print("-----") """
        #print("set edge color: ", src, dest, color)
        edge = self.G.get_edge(src.name, dest.name)


        #print(edge)
        if len(edge) > 0:
            #print("change edge color")
            edge[0].set_color(color)
            #print(edge[0])
            if color != "black":
                #print("added to colored_edges", dest)
                self.colored_edges_dest.append(dest)

    #getting called, when source node is changed
    def edge_color_normalization(self, src):
        """ print("color normalization")
        print("src", type(src)) """
        for node in self.colored_edges_dest:
            #print("dest", type(node))

            #print(src, "-->",  node)
            self.set_edge_color(src,node,"black")
        self.colored_edges_dest = []

    def graph_build_finished(self):
        if self.source_node != "":
            self.edge_color_normalization(self.source_node)

    """ def show_matplot(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            #print("called")
            img = mpimg.imread('./pic.png')
            #self.figure.set_data(img)
            plt.figure(img)
            plt.show()
            plt.pause(0.001)
            #print("plotted")     
        #print("Stopping as you wish.")   """ 
     


    """ def gui_thread_start(self):
        self.gui_thread.start()
        #threading.Thread(target=self.show_matplot).start()

    def gui_thread_stop(self):
        self.gui_thread.do_run = False
        self.gui_thread.join() """


def testing(): 
    delay = 0
    web.open(os.path.dirname(os.path.realpath(__file__))+"/spofproof.html")
    print("Hello world")
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
    graph.save_graph("./pic1.png")
    #graph.gui_thread_start()
    time.sleep(delay)

    graph.del_edge(node1, node2)
    graph.save_graph("./pic2.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node3)
    graph.add_edge(node1,node3)
    graph.save_graph("./pic3.png")
    time.sleep(delay)

    graph.set_edge_color(node1,node3,"green")
    graph.save_graph("./pic4.png")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node4)
    graph.add_edge(node1,node4)

    graph.save_graph("./pic5.png")
    time.sleep(delay)

    graph.del_edge(node1, node4)
    graph.save_graph("./pic6")
    time.sleep(delay)

    ### Source Node 2###
    graph.set_source_node(node2)
    ### EDGE 1###
    graph.set_target_node(node1)
    graph.add_edge(node2,node1)
    graph.save_graph("./pic7.png")
    #graph.gui_thread_start()
    time.sleep(delay)

    graph.set_edge_color(node2,node1,"green")
    graph.save_graph("./pic8.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node3)
    graph.add_edge(node2,node3)
    graph.save_graph("./pic9.png")
    time.sleep(delay)

    graph.del_edge(node2, node3)
    graph.save_graph("./pic10")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node4)
    graph.add_edge(node2,node4)
    graph.save_graph("./pic11.png")
    time.sleep(delay)

    graph.set_edge_color(node2,node4,"green")
    graph.save_graph("./pic12.png")
    time.sleep(delay)

    ### Source Node 3###
    ### EDGE 1###
    graph.set_source_node(node3)
    graph.set_target_node(node1)
    graph.add_edge(node3,node1)
    graph.save_graph("./pic13.png")
    #graph.gui_thread_start()
    time.sleep(delay)

    graph.del_edge(node3, node1)
    graph.save_graph("./pic14.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node2)
    graph.add_edge(node3,node2)
    graph.save_graph("./pic15.png")
    time.sleep(delay)

    graph.set_edge_color(node3,node2,"green")
    graph.save_graph("./pic16.png")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node4)
    graph.add_edge(node3,node4)

    graph.save_graph("./pic17.png")
    time.sleep(delay)

    graph.del_edge(node3, node4)
    graph.save_graph("./pic18")
    time.sleep(delay)

    ### Source Node 4###
    graph.set_source_node(node4)
    ### EDGE 1###
    graph.set_target_node(node1)
    graph.add_edge(node4,node1)
    graph.save_graph("./pic19.png")
    #graph.gui_thread_start()
    time.sleep(delay)

    graph.set_edge_color(node4,node1,"green")
    graph.save_graph("./pic20.png")
    time.sleep(delay)

    ### EDGE 2###
    graph.set_target_node(node2)
    graph.add_edge(node4,node2)
    graph.save_graph("./pic21.png")
    time.sleep(delay)

    graph.del_edge(node4, node2)
    graph.save_graph("./pic22")
    time.sleep(delay)

    ### EDGE 3###
    graph.set_target_node(node4)
    graph.add_edge(node4,node3)
    graph.save_graph("./pic23.png")
    time.sleep(delay)

    graph.set_edge_color(node4,node3,"green")
    graph.save_graph("./pic24.png")
    time.sleep(delay)


    graph.graph_build_finished()
    graph.save_graph("./pic25.png")







    #graph.gui_thread_stop()
if __name__ == '__main__':
    testing()