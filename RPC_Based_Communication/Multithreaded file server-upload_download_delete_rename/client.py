import rpyc
import threading



class MultithreadedFileClient:

    #File upload
    def upload(self):

        filename_path = input("Enter file name and path to upload: ")
        #filepath = "./FolderClient/" + filename

        filename = filename_path.split("/")[-1]

        print(f"File {filename} upload is processing....")
        try:
            with open(filename_path,"rb") as file:
                data = file.read()
                response = connection.root.upload(filename,data)
                if response is True:
                    print(f"file {filename} uploaded successfully")
                else:
                    print("File not uploaded")
        except:
            print("File not found,enter correct filename")

        

    #File download
    def download(self):

        filename = input("Enter the filename to download:")
        print(f"File {filename} download is processing....")
        try:

            file_content, file_status = connection.root.download(filename)
            
            #print(file_content,"file_content",file_status,"status")
            if file_status == "False":
                print("Enter correct details,file not present")

            else:
                if file_content is not None:
                    filepath = "./FolderClient/" + filename
                    with open(filepath,"wb") as file:
                        file.write(file_content)
                        print(f"File '{filename}' downloaded successfully")
                else:
                    print("Enter correct details,file not present")
        except:
            print("File not present to download.Enter correct details")


    #file delete
    def delete(self):

        filename = input("Enter the filename to delete : ")
        print(f"File {filename} deletion is processing....")
        try:
            output = connection.root.delete(filename)
            if output is True:
                print(f"file {filename} deleted successfully")
            else:
                print("Deletion not successful , provide correct details")
        except:
            print("Deletion not successful , provide correct details")
    

    #File Rename
    def rename(self):
        filename_old = str.strip(input("Enter the filename to rename : "))
        filename_new = str.strip(input("Enter the new name for file :"))

        print(f"File {filename_old} rename is processing....")
    
        if len(filename_new) == 0 or len(filename_old) == 0:
            print("File name not provided,provide correct details")
        else:
            try:
                output = connection.root.rename(filename_old,filename_new)
                if output is True:
                    print(f"file {filename_old} is successfully renamed to {filename_new}")
                else:
                    print("Rename not successful, provide correct details")
            except:
                print("Rename not successful, provide correct details")

if __name__ =="__main__":
    #establish a connection to server
    connection = rpyc.connect('localhost', 18811)

    while True:
        choice = input("\n\nEnter 1 to upload file :\nEnter 2 to download file\nEnter 3 to delete file\nEnter 4 to rename file\nEnter 0 to exit\n\nGive your choice of selection: \n")
        mfc = MultithreadedFileClient()
        if choice == "0":
            break
        if choice == "1":
            mfc.upload()
        elif choice == "2":
            mfc.download()
        elif choice == "3":
            mfc.delete()
        elif choice == "4":
            mfc.rename()


        else:
            print("Invalid choice.")