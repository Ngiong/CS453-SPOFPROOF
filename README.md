# CS453-SPOFPROOF
SPOF-PROOF is a chaotic testing tool to detect Single-Point-of-Failure in Microservice architecture.

See the [Pitching Slide](https://docs.google.com/presentation/d/1qoFa3NXIqOvbzcUKHA8MI9WaSup0UFfhF0olwBJRhIo/edit)

## Using SPOFPROOF

SPOFPROOF aim for general usage by organizations. Here are the steps to use SPOFPROOF:

### 1. Create user-custom Node class
the Node class need to be created according to organization needs. The class need to be put in the `node.py` file. 
The INode class show the abstraction of what should be included in the class. Here are the methods that need to be implemented

`__init__(self, name, ip_address, port)` function is used to initiate the node. At the very least, it should contain the node name, ip address, port. 

`__str__(self)`  function is used to print the node name, ip address and the port.

`ping(self)` function is used to the ping the node and get its response status.

`get_name(self)` function is used to get the name of the node.

`get_url(self, path)` function is used to get the url of the node with the given path

`set_response_level(self, response_level: ResponseLevel)` function is used to set/change the response level of a node.

`kill(self)` function is used to kill a node, usually by setting its response level to 2 (TERMINATED)

`resurrect(self)` function is used to turn a node on, usually by setting its reponse level 0 (NORMAL)

The class `SimpleNode` in the same file is an example on how to implement the class.

### 2. Set up the testing process
In the `main.py` file, list each of the nodes that are included in the network with its ip address and port using the user-custom node class that has been created before. For example: 

```
node1 = SimpleNode('app1', '127.0.0.1', 5001)
node2 = SimpleNode('app2', '127.0.0.1', 5002)
node3 = SimpleNode('app3', '127.0.0.1', 5003)
node4 = SimpleNode('app4', '127.0.0.1', 5004)
```

This is done assuming that the network of nodes is already running. If not, `bootstrap.py` can be used to run the nodes. To stimulate a network of nodes, add the list of nodes along with its dependencies in the bottom of part of the boostrap file. For example, 
```
graph = {
    1: {2, 3},
    2: {4},
    3: {},
    4: {}
}
bootstrap(graph)
```
means that there are 4 nodes where node 1 depends on node 2 and 3, while node 2 depends on node 4.
To run the bootstrap, use command `python3 bootstrap.py`. 

Then, create a SPOFProofEngine() object, set the node list using `set_nodes(nodes)` method. For example, 
`engine.set_nodes([node1, node2, node3, node4])` sets the nodes for the boostrap sample.
The engine can be run using `run_test(n_test, sim_mode)` method, where n_test is the number of tests that needs to be done and sim_mode is true if the simulation graph needs to be displayed and false otherwise. For example,
```
engine.run_test(n_tests=10, sim_mode=True)
```
means that the test need to be run 10 times, and at the end of the test, the graph should be displayed
.Using the resulting graph, SPOF detection can be performed.