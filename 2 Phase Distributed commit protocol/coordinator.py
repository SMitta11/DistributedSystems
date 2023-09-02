from xmlrpc.client import ServerProxy
import random
import threading
from vars import Ports, NodeState

log_file = "coordinator.log"
class Coordinator:
    def __init__(self):
        self.nodes = []
        self.lock = threading.Lock()
        self.file = open(log_file, "a+")

    flag = False

    def recover(self):
        last_line = ""
        self.file = open(log_file, "r+")

        for line in self.file:
            last_line = line

        param = last_line.split(" ")
        print(param)

        if str(param[-1]) == "Commit\n" or str(param[-1]) == "Abort\n":
            print("Do not need to recover")
            return True

        action = param[1]
        print("action",action)
        self.lock.acquire()
        if action == "put":
            print("recover put func")
            self.commit()
            self.file.write(" Commit\n")
        elif action == "get":
            print("recover get func")
            self.get(param[2])
        elif action == "del":
            print("recover del func")
            self.remove(param[2])
        self.file.close()
        self.lock.release()
        
    def put(self, key, value):
        print("Lock acquired")
        self.lock.acquire()
        self.file = open(log_file, "a+")
        for node in self.nodes:
            
            try:
                flag = node.put(key, value)
                if flag:
                    print("Current status returned by node: yes" )
                elif not flag:
                    print("Current status returned by node: no")
                else:
                    print("Current status returned by node: " + str(flag))
                if flag == False:
                    self.abort()
                    self.file.write(" " + "Abort\n")
                    self.file.close()
                    self.lock.release()
                    print("Lock released")
                    return False
                elif key == NodeState.FAILED.value:
                    print("Node failed after responding, running recovery in next testcase")
                    self.file.write(" put" + " " + key + " " + value)                
            except Exception as e:
                print(e)

        if key != NodeState.INITIAL.value:
            if key != NodeState.FAILED.value:
                if key != NodeState.ABORTED.value:
                    self.commit()
                    self.file.write(" " + "Commit\n")
                else:
                                       
                    print("Coordinator updated to yes state and then crashed")
                    self.abort()
                    self.file.write(" " + "Abort\n")
        self.file.close()
        self.lock.release()
        print("Lock released")

    def get(self, key):
        print("calling get")
        self.file = open(log_file, "a+")
        self.file.write(" get " + key)

        random_num = random.randrange(0, len(self.nodes), 1)
        value = self.nodes[random_num].get(key)
        print("Get value %s", value)

        self.file.write(" Commit\n")
        self.commit()

    def remove(self, key):
        self.file = open(log_file, "a+")
        self.file.write(" del " + key)
        print("Lock acquired")

        self.lock.acquire
        for node in self.nodes:
            
            flag = False
            try:
                flag = node.remove(key)
                if flag:
                    print("Current status returned by node: yes" )
                elif not flag:
                    print("Current status returned by node: no")
                else:
                    print("Current status returned by node: " + str(flag))
            except Exception as e:
                print(e.args)
            if flag == False:
                self.abort()
                self.file.write(" Abort\n")
                return False
        self.commit()
        self.file.write(" Commit\n")
        self.file.close()
        self.lock.release
        print("Lock released")

    def decide(self, key):
        flag = False
        for node in self.nodes:
            flag ^= node.decide(key)  
        return flag

    def commit(self):
        print("Initiating commit on all nodes")
        for node in self.nodes:
            node.commit()

    def abort(self):
        print("Aborting transactions")
        for node in self.nodes:
            node.abort()
        print("Abort completed")

    def recover_nodes(self):
        for node in self.nodes:
            node.recover()


def main():
    print("\n")
    coordinator = Coordinator()
    all_ports = Ports().get()
    for port in all_ports:
        try:
            host = "http://localhost" + ":" + str(port)
            node_conn = ServerProxy(host)
            print("New connection for node - ",host)
            coordinator.nodes.append(node_conn)
        except:
            print("Some exception occured in setting up ServerProxy")
    print("\n")
    print("--------Testing new case--------")
    print("\n")
    print("Testcase name - Coordinator fail before sending prepare message ")
    coordinator.put(NodeState.INITIAL.value, "Testcase for "+ NodeState.INITIAL.name) 
    print("\n")
    print("--------Testing new case--------")
    print("\n")
    print("Testcase name - All cases are true, Testing ")
    coordinator.put(NodeState.COMMITTED.value, "Testcase for "+ NodeState.COMMITTED.name) 
    print("\n")
    print("--------Testing new case--------")
    print("\n")
    print("Testcase name - Coordinator will fail, Testing ")
    coordinator.put(NodeState.ABORTED.value, "Testcase for "+ NodeState.ABORTED.name)
    print("\n")
    print("--------Testing new case--------")
    print("\n")
    print("Testcase name - Nodes will fail before sending YES, Testing ")
    coordinator.remove(NodeState.REMOVED.value)  
    print("\n")
    print("--------Testing new case--------")
    print("\n")
    print("Testcase name - Nodes will fail after sending YES, Testing ")
    coordinator.put(NodeState.FAILED.value, "Testcase for "+ NodeState.FAILED.name) 
    print("\n")
    print("--------Testing new case--------")
    print("\n")
    print("Testcase name - Nodes will recover after crash and complete transaction ")
    coordinator.recover_nodes()
    coordinator.recover()

if __name__ == "__main__":
    main()
