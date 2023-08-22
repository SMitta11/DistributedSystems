import rpyc
import threading
import time
import os


#establish a connection to server

class DropboxClient:
    def __init__(self,files_client=[],last_check_time=0):
        
        self.files_client = os.listdir("./FolderClient/")
        self.last_check_time = time.time()

    #File upload
    def upload(self,filename):

        try:
            filename_path = "./FolderClient/" + filename
            with open(filename_path,"rb") as file:
                data = file.read()
                response = connection.root.upload(filename,data)
                if response is True:
                    print(f"file {filename} uploaded successfully")
                else:
                    print("File not uploaded")
        except:
            print("File not found,enter correct filename")

    # #file delete
    def delete(self,filename):
        try:
            output = connection.root.delete(filename)
            if output is True:
                print(f"file {filename} deleted successfully")
            else:
                print("Deletion not successful , provide correct details")
        except:
            print("Deletion not successful , provide correct details")



    def track_updated_files(self):

        modified_files = []
        try:
            for file_name in self.files_client:
                file_path = os.path.join("./FolderClient/", file_name)
                if os.path.getmtime(file_path) > self.last_check_time - 10:
                    modified_files.append(file_name)
                filtered_modified_files = [file for file in modified_files if file != '.DS_Store']

            for filename in modified_files:
                self.upload(filename)
        except FileNotFoundError:
            print("File is not present to upload")

    def track_all_server_files(self):
       
        files_server = connection.root.retrieve_file_names()
        dict = {}
        for i,val in enumerate(self.files_client):
            dict[val] = i
 
        #creating a list to store files which are at server side but not at client side
        to_be_deleted_files = []

        #adding files to delete from server in list
        for file_s in files_server:
            if file_s not in dict:
                to_be_deleted_files.append(file_s)
    

        #calling delete function for files
        for filename in to_be_deleted_files:
            self.delete(filename)
        


if __name__ == "__main__":
    connection = rpyc.connect('localhost', 18811)
    
    while True:
        dropbox = DropboxClient() 
        dropbox.track_updated_files()
        dropbox.track_all_server_files()
        time.sleep(10)










