import rpyc 
from rpyc.utils.server import ThreadedServer 
import os


@rpyc.service

class DropboxServer(rpyc.Service):

    #Upload file 
    FolderServer = "./FolderServer/"
    @rpyc.exposed
    def upload(self,filename,data):
        try:
            file_path = "./FolderServer/" + filename
            with open(file_path,"wb") as file:
                file.write(data)
            return True
                
        except FileNotFoundError:
            return "File is not present to upload.Enter correct details"

       #delete file
    @rpyc.exposed
    def delete(self,filename):
        
        try:
            file_path = "./FolderServer/" + filename
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    #retrieve all files on server

    @rpyc.exposed
    def retrieve_file_names(self):
        try:
            
            files_server = os.listdir(DropboxServer.FolderServer)
            files_at_server = []
            for files in files_server:
                files_at_server.append(files)
                #print(files_at_server)
            return files_at_server
        except FileNotFoundError:
            return []



if __name__ == "__main__":
 
    print('starting server')
    server = ThreadedServer(DropboxServer, port=18811)
    server.start()
