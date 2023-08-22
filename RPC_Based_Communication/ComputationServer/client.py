import rpyc
import threading
import time


class ComputationClient:

    def __init__(self):
        self.result_async_addition = {}
        self.result_async_sort = {}
      
    #synchronous addition
    def sync_add(self,num1,num2):    
        result = connection.root.addition(num1,num2)
        print(f"Addition of {num1} and {num2} is {result}")
    

    #synchronous sort
    def sync_sort(self,arr):
        result = connection.root.sorting(arr)
        print(f"Sorted array is {result}")

    #asynchronous addition
    def async_add(self,num1,num2):
        print(f"Addition of {num1} and {num2} is processing in background..")

        addition_async = rpyc.async_(connection.root.addition)
        self.result_async_addition[num1,num2] = addition_async(num1, num2)
        print(f"Addition of {num1} and {num2} is {self.result_async_addition},do other operations and get results by entering appropriate choice")
        print(self.result_async_addition)


    #asynchronous sort
    def async_sort(self,arr):
        print(f"Sorting of {arr} is processing in background..")
        sorting_async = rpyc.async_(connection.root.sorting)
        self.result_async_sort[arr] = sorting_async(arr)
        print(f"Sorted array for input {arr} is {self.result_async_sort} ,do other operations and get results by entering appropriate choice")
    
    #show result addition
    def show_result_async_addition(self):
        if self.result_async_addition == {}:
            print("No asynchronous operation result available.")
        else:
            for key,result_add_async in self.result_async_addition.items():
                print(f"Asynchronous operation result for addition of {key} is {result_add_async.value}")
        self.result_async_addition = {}

    #show result sorting
    def show_result_async_sorting(self):
        if self.result_async_sort == {}:
            print("No asynchronous operation result available.")
        else:
            for key,result_sort_async in self.result_async_sort.items():
                print(f"Asynchronous operation result for sorting {key} is {result_sort_async.value}")
        self.result_async_sort = {}


if __name__ == "__main__":
    #establish a connection to server
    connection = rpyc.connect('localhost', 18811)   
    comp = ComputationClient()
    while(True):
        

        choice = input("\n\n\nEnter 1 for synchronous addition  \nEnter 2 for synchronous sort  \nEnter 3 for asynchronous addition  \nEnter 4 for asynchronous sort  \nEnter 5 to show asynchronous result for addition \nEnter 6 to show asynchronous result for sorting \nEnter 0 to exit\n\nGive your choice of selection: \n")

        if choice == "0":
            break
        if choice == "1":
            print("Enter numbers to perform addition:")
            num1 = int(input("Enter 1st number: "))
            num2 = int(input("Enter 2nd number: "))
            comp.sync_add(num1,num2)

        elif choice == "2":
            print("Enter array for sorting(separated by comma) : ")
            arr = input("Enter array")
            comp.sync_sort(arr)

        elif choice == "3":
            print("Enter numbers to perform addition:")
            num1 = int(input("Enter 1st number: "))
            num2 = int(input("Enter 2nd number: "))
            comp.async_add(num1,num2)
    
        elif choice == "4":
            print("Enter array for sorting(separated by comma) : ")
            arr = input("Enter array")
            comp.async_sort(arr)

        elif choice == "5":
            print("show all addition asynchronous operations result")
            comp.show_result_async_addition()

        elif choice == "6":
            print("show all sorting asynchronous operations result")
            comp.show_result_async_sorting()
      
    
        else:
            print("invalid choice")
        