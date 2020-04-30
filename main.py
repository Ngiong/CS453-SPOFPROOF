from node import SimpleNode


def main():
    node = SimpleNode(name='Node1', ip_address='localhost', port='3888')
    print(node)


if __name__ == '__main__':
    main()