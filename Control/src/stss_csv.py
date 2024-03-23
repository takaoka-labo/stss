import csv
import datetime

class csv_manager:
    def __init__(self):
        self.cell_ID = []
        self.serial_ID = []
        self.tool_name = []
        self.tool_size = []
        self.manage_data = []
        
    def get_state(self):
        with open('state.csv', 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                self.cell_ID.append(row[0])
                self.serial_ID.append(row[1])
                self.tool_name.append(row[2])
                self.tool_size.append(row[3])
        return self.cell_ID, self.serial_ID, self.tool_name, self.tool_size
    
    def get_manage(self):
        with open('manage.csv', 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                self.manage_data.append(row)
        return self.manage_data
    
    def withdraw(self, input_number, username):#input_numberは取り出す工具のシリアルID
        for i in range(len(self.serial_ID)):
            if self.serial_ID[i] == input_number:  
                self.serial_ID[i] = -1
                self.tool_name[i] = "none"
                self.tool_size[i] = "none"
                for row in self.manage_data:
                    if row[0] == input_number:
                        row[4] = username
                        row[3] = "using" 
        return self.serial_ID, self.tool_name, self.tool_size, self.manage_data
    
    def deposite(self, string, username):
        for i in range(len(self.cell_ID)):
            if self.serial_ID[i] == "-1" :
                self.serial_ID[i] = string    
                for row in self.manage_data:
                    if row[0] == string:
                        row[4] = username
                        row[3] = 1 #machine_ID #とりあえず今は1
        return self.serial_ID, self.manage_data
    
    def update_state(self):
        with open('state.csv', 'w', newline='') as f:
            csv_writer = csv.writer(f)
            for i in range(len(self.cell_ID)) :
                csv_writer.writerow(self.cell_ID[i], self.serial_ID[i], self.tool_name[i], self.tool_size[i])
        return self.cell_ID, self.serial_ID, self.tool_name, self.tool_size
    
    def update_manage(self):
        with open('manage.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(self.manage_data)
        return self.manage_data
    
    def log(self, string):
        current_time = datetime.datetime.now()
        with open('log.csv', 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([string, current_time,])
        return current_time

