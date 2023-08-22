import rpyc 
from rpyc.utils.server import ThreadedServer 
import os


@rpyc.service

class ComputationServer(rpyc.Service):
    
    @rpyc.exposed
    def addition(self,i,j):
        print(i,j)
        try:
            result = i + j
            return result
        except:
            return "Result not computed"

    @rpyc.exposed
    def sorting(self,arr):
        try:
            arr_new = arr.split(",")
            elements = [int(element) for element in arr_new]
            result = sorted(elements)
            return result
        except:
            return "Array should only contain numbers or result not sorted"

if __name__ == '__main__':
    print('starting server')
    server = ThreadedServer(ComputationServer, port=18811)
    server.start()
    print('server started')
        

