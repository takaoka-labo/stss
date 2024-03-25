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
        self.cell_ID.clear()
        self.serial_ID.clear()
        self.tool_name.clear() 
        self.tool_size.clear()
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
    
    def update_state(self):
        with open('state.csv', 'w', newline='') as f:
            csv_writer = csv.writer(f)
            for i in range(len(self.cell_ID)) :
                csv_writer.writerow([self.cell_ID[i], self.serial_ID[i], self.tool_name[i], self.tool_size[i]])
            print(self.cell_ID, self.serial_ID, self.tool_name, self.tool_size)
        self.cell_ID.clear()
        self.serial_ID.clear()
        self.tool_name.clear() 
        self.tool_size.clear()
            
    
    def update_manage(self):
        with open('manage.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(self.manage_data)
            print(self.manage_data)
        self.manage_data.clear()
    
    def update_withdraw(self, input_number, username):#input_numberは取り出す工具のシリアルID
        self.get_state()
        self.get_manage()
        for i in range(len(self.serial_ID)):
            if self.serial_ID[i] == input_number:  
                self.serial_ID[i] = -1
                self.tool_name[i] = "none"
                self.tool_size[i] = "none"
                for row in self.manage_data:
                    if row[0] == input_number:
                        row[4] = username
                        row[3] = "using" 
        self.update_state()
        self.update_manage()
        
    def search_vacant_cell(self):
        self.get_state()
        for i in range(len(self.cell_ID)):
            if self.serial_ID[i] == "-1":
                return i
        return -1
        
    def update_deposite(self, string):
        self.get_state()
        self.get_manage()
        for i in range(len(self.cell_ID)):
            if self.serial_ID[i] == "-1" :
                self.serial_ID[i] = string
                cell_id = i                                                                     #????????????????????
                for row in self.manage_data:
                    if row[0] == string:
                        #row[4] = username
                        row[3] = 1 #machine_ID #とりあえず今は1
                break
        self.update_state()
        self.update_manage()
    
    
    
    
    def log(self, string):
        current_time = datetime.datetime.now()
        with open('log.csv', 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([string, current_time,])
        return current_time

