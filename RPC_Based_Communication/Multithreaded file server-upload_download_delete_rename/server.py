import rpyc #imported rpyc library
from rpyc.utils.server import ThreadedServer #imported "threadedserver" clas from rpyc library
import os

@rpyc.service

class MultithreadedFileServer(rpyc.Service):

    #Upload file 
    @rpyc.exposed
    def upload(self,filename,data):
        
        file_path = "./FolderServer/" + filename
        try:
            with open(file_path,"wb") as file:
                file.write(data)
            return True
                
        except FileNotFoundError:
            return "File is not present to upload.Enter correct details"


    #Download file
    @rpyc.exposed
    def download(self,filename):

        if len(filename) == 0:
            return "File name not provided,provide correct details"
        

      
        try:
            file_path = "./FolderServer/" +  filename
            if os.path.exists(file_path):
                with open(file_path,"rb") as file:
                    file_content = file.read()
                    #print(file_content,"FILE CONTENT")
                if file_content is not None:
                    return file_content, True
                else:
                    
                    return None, False
            else:
                return None, False
        except FileNotFoundError:
            return None, False
        except:
            return None, False
    
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
    
    #Rename file
    @rpyc.exposed
    def rename(self,filename_old,filename_new):

        if len(filename_new) == 0 or len(filename_old) == 0:
            return "File name not provided,provide correct details"
        
        try:
            file_path_old = "./FolderServer/" + filename_old
            file_path_new = "./FolderServer/" + filename_new
            #print(file_path_old,file_path_new,"ee")
            if os.path.exists(file_path_old):
                os.rename(file_path_old,file_path_new)
                return True
            else:
                return False
            
        except FileNotFoundError:
            return False
            
        except:
            return False
    
            


if __name__ == '__main__':         
    print('starting server')
    server = ThreadedServer(MultithreadedFileServer, port=18811)
    server.start()