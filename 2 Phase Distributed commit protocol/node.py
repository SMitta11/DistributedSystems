import sqlite3 as lite
import sys
from vars import NodeState

class DB:
    def __init__(self, node_name):
        self.table = "data_table"
        try:
            self.conn = lite.connect(node_name + ".db")
            self.cur = self.conn.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS "+self.table+"(key INT PRIMARY KEY, value TEXT)")
            self.conn.commit()        
        except lite.Error as e:
            print("Error", e)
            sys.exit()

    def set_value(self, key, value):
        self.cur.execute("INSERT OR REPLACE INTO "+self.table+" VALUES(?,?)", (key, value))
        self.commit()

    def get_value(self,key):
        self.cur.execute("SELECT value FROM "+self.table+" WHERE KEY = ?", key)
        return str(self.cur.fetchone())
    
    def delete(self,key):
        self.cur.execute("DELETE FROM "+self.table+" WHERE KEY = ?", key)
        self.commit()  

    def commit(self):
        self.conn.commit()

class Node:
    def __init__(self, port):
        self.port = port
        self.node_name = "node"+str(self.port)
        self.db = DB(self.node_name)

    def __save_log(self, data):
        with open(self.node_name + ".log", "a+") as file:
            file.write(data)
            file.flush()
        
    def recover(self):
        last_line = ""
        self.file = open(self.node_name + ".log", "r+")
        for line in self.file:
            last_line = line
        param = last_line.split(" ")

        if str(param[-1]) == "Commit\n" or str(param[-1]) == "Abort\n":
            self.file.write(" Do not need to recover")
            return True
        action = param[1]

        if action == "put":
            self.file.write(" Recover save function")
        elif action == "get":
            self.file.write(" Recover get function")
            self.db.get_value(param[2])
        elif action == "del":
            self.file.write(" Recover delete function")
            self.db.delete(param[2])

        self.file = open(self.node_name + ".log", "a+")
        self.file.write(" Commit\n")
        self.file.flush()
        self.isRecover = 0
        return 1

    def get(self, key):
        print(self.node_name)
        self.__save_log("Get for key -" + key + "\n")
        try:
            return self.db.get_value(key)
        except Exception as e:
            print(e)
        
    def put(self, key, value):
        if self.decide(key):
            self.__save_log("Save for key -" + key + " : " + value+ "\n")
            if key != NodeState.FAILED.value:
                try:
                    self.db.set_value(key, value)
                    self.__save_log("Status for Key - " + key + " => " )
                    return True
                except lite.Error as e:
                    print(e)
            else:
                self.isRecover = 1
                return self.isRecover
        return False

    def remove(self, key):
        if self.decide(key):
            self.__save_log("Delete for key -" + key+ "\n")
            if key != NodeState.FAILED.value:
                try:
                    self.db.delete(key)
                    return True
                except Exception as e:
                    print(e)
        return False

    def decide(self, key):
        if key == NodeState.REMOVED.value or key == NodeState.INITIAL.value:
            return False
        return True

    def commit(self):
        try:
            self.db.commit()
            self.__save_log(" Commit "+ "\n")
            return True
        except lite.Error as e:
            print(e)

    def abort(self):
        self.__save_log(" Abort "+ "\n")
        return True