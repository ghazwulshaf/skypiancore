import csv
import os
import pandas as pd
import schedule
import time
from datetime import datetime
import pymongo

class DataCtrl():
    def __init__(self):
        """
        SENSOR
        sensor 1: TDS -> pH
        sensor 2: pH -> TDS
        sensor 3: water temp
        sensor 4: water level ->  air temp
        sensor 5: humidity
        sensor 6: air temp -> heat index
        sensor 7: heat index -> water level
        """
        self.DataSensor = ['0', '0', '0', '0', '0', '0', '0']
        self.AcMsg = "#A#0#0#"

        self.xList = []

        self.y1List = []
        self.y2List = []
        self.y3List = []
        self.y4List = []
        self.y5List = []
        self.y6List = []
        self.y7List = []

        self.iter = 0

        #csv file
        self.filename = "data_sensor.csv"
        """
        HEADER: Timestamp, Year, Month, Day, Hour, Minute, pH, TDS, Humidity, Heat Index, Water Temp, Air Temp, Fert Level
        """
        self.header = [
            "Timestamp",
            "Year",
            "Month",
            "Day",
            "Hour",
            "Minute",
            "pH",
            "TDS",
            "Humidity",
            "Heat Index",
            "Water Temp",
            "Air Temp",
            "Fert Level"
        ]

        #region global colors control

        #button bg color
        self.clr_btn = "#f0f0f0"

        #graphs
        self.clr_gp1 = "red"
        self.clr_gp2 = "green"
        self.clr_gp3 = "blue"
        self.clr_gp4 = "purple"

        #endregion global colors control

        #sensors name
        self.nm_s1 = "pH"
        self.nm_s2 = "TDS"
        self.nm_s3 = "Humidity"
        self.nm_s4 = "Heat Index"
        self.nm_s5 = "Water Temp"
        self.nm_s6 = "Air Temp"
        self.nm_s7 = "Fert Level"

        #sensors index --> change this value to syncronous the variabel with serial data sensors
        self.Sensors = {
            1: 0, # 1 pH
            2: 1, # 0 TDS
            3: 4, # 4 Humidity
            4: 5, # 6 Heat Index
            5: 2, # 2 Water Temp
            6: 3, # 5 Air Temp
            7: 6, # 3 Fert/Water Level
        }

        #sensors color
        self.clr_s1 = "purple"
        self.clr_s2 = "green"
        self.clr_s3 = "lightblue"
        self.clr_s4 = "orange"
        self.clr_s5 = "blue"
        self.clr_s6 = "red"
        self.clr_s7 = "green"

        #graphs name
        self.nm_gp1 = "pH"
        self.nm_gp2 = "Humidity"
        self.nm_gp3 = "Tds"
        self.nm_gp4 = "Temp"

        #graphs state controler
        self.stt_gp1 = "OFF"
        self.stt_gp2 = "OFF"
        self.stt_gp3 = "OFF"
        self.stt_gp4 = "OFF"

        #actuators name
        self.nm_ac1 = "Aktuator 1"
        self.nm_ac2 = "Aktuator 2"
        self.nm_fert = "Fert"

        #actuators state
        self.stt_ac1 = "OFF"
        self.stt_ac2 = "OFF"
        self.stt_fert = "OFF"

        #actuators value
        self.val_ac1 = 0
        self.val_ac2 = 0
        self.val_fert = 0

        #actions name
        self.nm_act1 = "State"
        self.nm_act2 = "Harvest"
        self.nm_act3 = "Exit"

        #actions state
        self.stt_act1 = "AUTO"

        #data control
        self.RowMsg = ""
        self.msg = []
    
    def DataStream(self):
        try:
            schedule.every(1).minutes.do(self.StoreData)
            schedule.every(5).minutes.do(self.PublishData)

            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            print(e)
    
    def DecodeMsg(self):
        # temp = self.RowMsg.decode("ascii")
        temp = str(self.RowMsg[0:len(self.RowMsg)].decode("utf-8"))
        self.msg = temp.split(",")
        # if len(temp) > 0:
        #     self.msg = temp.split("@")
        #     self.msg.remove("")
        #     self.DataSensor = self.msg
        #     for i in range(len(self.DataSensor)):
        #         self.DataSensor[i] = float(self.DataSensor[i])
        try:
            for i in range(len(self.msg)):
                self.DataSensor[i] = float(self.msg[i])
        except Exception as e:
            print(e)

    def CheckData(self):
        if os.path.exists(self.filename):
            # with open(self.filename, 'r') as csvfile:
            #     # datas = csv.reader(csvfile)
            #     datas = csvfile.readlines()
            #     for data in datas[-1800:]:
            #         data = data.strip()
            #         data = data.split(',')
            #         self.xList.append(int(data[0]))
            #         self.y1List.append(float(data[1]))
            #         self.y2List.append(float(data[2]))
            #         self.y3List.append(float(data[3]))
            #         self.y4List.append(float(data[4]))
            #         self.y5List.append(float(data[5]))
            #         self.y6List.append(float(data[6]))
            #         self.y7List.append(float(data[7]))
            #     lastdata = data
            #     # lastdata = lastdata.split(",")
            #     self.iter = int(lastdata[0])
            #     self.iter += 2
            pass
        else:
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.header)
                writer.writeheader()

    def StoreData(self):
        datas = self.DataSensor
        current_time = datetime.now()
        dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
        tm_year = current_time.year
        tm_month = current_time.month
        tm_day = current_time.day
        tm_hour = current_time.hour
        tm_minute = current_time.minute
        
        val_s1 = datas[self.Sensors[1]]
        val_s2 = datas[self.Sensors[2]]
        val_s3 = datas[self.Sensors[3]]
        val_s4 = datas[self.Sensors[4]]
        val_s5 = datas[self.Sensors[5]]
        val_s6 = datas[self.Sensors[6]]
        val_s7 = datas[self.Sensors[7]]

        dict = {
                "Timestamp": dt_string,
                "Year": tm_year,
                "Month": tm_month,
                "Day": tm_day,
                "Hour": tm_hour,
                "Minute": tm_minute,
                "pH": val_s1,
                "TDS": val_s2,
                "Humidity": val_s3,
                "Heat Index": val_s4,
                "Water Temp": val_s5,
                "Air Temp": val_s6,
                "Fert Level": val_s7
            }
        
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.header)
            writer.writerow(dict)
    
    def PublishData(self):
        datas = self.DataSensor
        current_time = datetime.now()
        dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
        myclient = pymongo.MongoClient("mongodb://userroot:3sdgd237xd@103.195.142.180:27017/?authMechanism=DEFAULT")
        mydb = myclient["skypianSGH"]
        mycol = mydb["skypianSensor"]

        ph = datas[self.Sensors[1]]
        tds = datas[self.Sensors[2]]
        hum = datas[self.Sensors[3]]
        heat = datas[self.Sensors[4]]
        wtemp = datas[self.Sensors[5]]
        atemp = datas[self.Sensors[6]]
        level = datas[self.Sensors[7]]

        mydict = {
            "time":dt_string,
            "ph": ph,
            "tds":tds,
            "water temperature":wtemp,
            "air temperature":atemp,
            "humidity": hum,
            "heat index":heat,
        }

        x = mycol.insert_one(mydict)

    def ReadData(self):
        df = pd.read_csv(self.filename)

        current_time = datetime.now()
        dateToday = current_time.day

        # datas = df.tail(120)

        datas = df[df["Day"] == dateToday]

        hour = datas["Hour"]
        minute = datas["Minute"]

        self.xList = []
        for i in range(len(datas)):
            x = float(hour[i]) + (float(minute[i]) / 60.0)
            self.xList.append(x)
        
        self.y1List = datas["pH"]
        self.y2List = datas["TDS"]
        self.y3List = datas["Humidity"]
        self.y4List = datas["Heat Index"]
        self.y5List = datas["Water Temp"]
        self.y6List = datas["Air Temp"]
        self.y7List = datas["Fert Level"]
    
    def DeleteData(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        else:
            print("The file is not exist")

    def SetActuatorMsg(self):
        self.AcMsg = "#A#{}#{}#".format(self.val_ac1, self.val_ac2)

if __name__ == "__main__":
    DataCtrl()