from node import Node
from vars import Ports
from xmlrpc.server import SimpleXMLRPCServer
import threading

def run_server(port):
    try:
        print("Starting a node on port:", port)
        server = SimpleXMLRPCServer(("localhost", port))
        node = Node(port)
        server.register_instance(node)
        print("Node on port", port, "is listening...")
        server.serve_forever()
    except Exception as e:
        print("An error occurred on port", port, ":", e)

def main():
    all_ports = Ports().get()
    threads = []

    for port in all_ports:
        thread = threading.Thread(target=run_server, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
