from tkinter import *
import tkinter as tk
import sys
from tkinter.font import Font
import serial
import urllib3
import continuous_threading
from os import write
from pdb import main
import serial
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *
import csv
import pandas as pd
from datetime import datetime
import schedule
import os
from time import sleep
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.dates as mdates
import serial.tools.list_ports
from tkinter import filedialog as fd
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import pymongo
# Creating tkinter window
root = Tk()
root.title('Selamat Datang di SHS')
#w,h=1280,1024
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.configure(bg='#FFFFFF')
root.config(cursor="none")
def scanport():
    portList=list(serial.tools.list_ports.comports())

    for port in portList:
        if "VID:PID=2341:0043" in port[0]\
            or "VID:PID=2341:0043" in port[1]\
            or "VID:PID=2341:0043" in port[2]:
            return port[0]
portdevice=scanport()
# Read Serial

ser = serial.Serial(portdevice, 115200)
vall = 0
def grafik1():
    # Figure Plotting
    headers = ['time','pH']
    df = pd.read_csv('/home/skypian/Desktop/skypianData/skypiancolection-dataPh.csv',names=headers)
    data=df.tail(288)
    plt.show()
    figure1 = plt.Figure(figsize=(9.4,4.5), dpi=50)
    ax1 = figure1.add_subplot(111)
    line1 = FigureCanvasTkAgg(figure1, root)
    line1.get_tk_widget().place(x=175, y=0)
    data = data[['pH']]
    data.plot(kind='line', legend=True, ax=ax1, marker='o', fontsize=15)
    data.rc('exes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))
    
    
def grafik3():
    # Figure Plotting
    headers = ['time','Humidity']
    df = pd.read_csv('/home/skypian/Desktop/skypianData/skypiancolection-dataHum.csv',names=headers)
    data=df.tail(288)
    plt.show()
    figure1 = plt.Figure(figsize=(9.4,4.5), dpi=50)
    ax1 = figure1.add_subplot(111)
    line1 = FigureCanvasTkAgg(figure1, root)
    line1.get_tk_widget().place(x=175, y=0)
    data = data[['Humidity']]
    data.plot(kind='line', legend=True, ax=ax1, marker='o', fontsize=15)
    data.rc('exes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))


def grafik2():
    headers = ['time','tds']
    df = pd.read_csv('/home/skypian/Desktop/skypianData/skypiancolection-dataTds.csv',names=headers)
    data=df.tail(288)
    plt.show()
    figure1 = plt.Figure(figsize=(9.4,4.5), dpi=50)
    ax1 = figure1.add_subplot(111)
    line1 = FigureCanvasTkAgg(figure1, root)
    line1.get_tk_widget().place(x=175, y=210)
    data = data[['tds']]
    data.plot(kind='line', legend=True, ax=ax1, marker='o', fontsize=15)
    data.rc('exes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))

def grafik4():
    headers = ['time','Wtr Temp','Air Temp']
    df = pd.read_csv('/home/skypian/Desktop/skypianData/skypiancolection-dataTemp.csv',names=headers)
    data=df.tail(288)
    plt.show()
    figure1 = plt.Figure(figsize=(9.4,4.5), dpi=50)
    ax1 = figure1.add_subplot(111)
    line1 = FigureCanvasTkAgg(figure1, root)
    line1.get_tk_widget().place(x=175, y=210)
    data = data[['Wtr Temp','Air Temp']]
    data.plot(kind='line', legend=True, ax=ax1, marker='o', fontsize=15)
    data.rc('exes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))

# set mode GPIO
GPIO.setmode(GPIO.BCM)

ledon = 17
ledblue = 27
ledred = 22

# GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledon, GPIO.OUT)
GPIO.setup(ledblue, GPIO.OUT)
GPIO.setup(ledred, GPIO.OUT)
GPIO.output(ledon, GPIO.HIGH)
GPIO.output(ledblue, GPIO.HIGH)
GPIO.output(ledred, GPIO.HIGH)
# a = 9
# b = 10
# sw=11
# GPIO.setup(a, GPIO.OUT)
# GPIO.setup(b, GPIO.OUT)
# GPIO.setup(sw, GPIO.OUT)
# GPIO.output(a, GPIO.HIGH)
# GPIO.output(b, GPIO.LOW)
# GPIO.output(ledon, GPIO.HIGH)
# GPIO.output(ledblue, GPIO.HIGH)
# GPIO.output(ledred, GPIO.HIGH)
# GPIO.output(sw, GPIO.HIGH)
def onled():
    global lamp
    lamp=1
    Label(root,  text="LED ON    ", fg="#568ADB", bg="#FFFFFF", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=5, y=450)
    GPIO.output(ledon, GPIO.LOW)
    GPIO.output(ledblue, GPIO.HIGH)
    GPIO.output(ledred, GPIO.HIGH)

def offled():
    global lamp
    lamp=0
    Label(root,  text="LED OFF  ", fg="#568ADB", bg="#FFFFFF", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=5, y=450)
    GPIO.output(ledon, GPIO.HIGH)
    GPIO.output(ledblue, GPIO.HIGH)
    GPIO.output(ledred, GPIO.HIGH)

def redled():
    global lamp
    lamp=2
    Label(root,  text="LED RED     ", fg="#568ADB", bg="#FFFFFF", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=5, y=450)
    GPIO.output(ledon, GPIO.HIGH)
    GPIO.output(ledblue, GPIO.HIGH)
    GPIO.output(ledred, GPIO.LOW)

def blueled():
    global lamp
    lamp=3
    Label(root,  text="LED BLUE", fg="#568ADB", bg="#FFFFFF", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=5, y=450)

    GPIO.output(ledon, GPIO.HIGH)
    GPIO.output(ledblue, GPIO.LOW)
    GPIO.output(ledred, GPIO.HIGH)

global air1
global air2
air1 = False
air2 = False
def pump():

    if ((tds1>100) and (tds1< 850)):
        GPIO.output(ledred, GPIO.LOW)
        sleep(15)
        GPIO.output(ledred, GPIO.HIGH)
    else:
        GPIO.output(a, GPIO.HIGH)
#     if ((tds2>50) and (tds2 < 550)):
#         GPIO.output(b, GPIO.HIGH)
#         sleep(5)
#         GPIO.output(b, GPIO.LOW)
#     else:
#         GPIO.output(b, GPIO.LOW)

def publish():
    try :
        now=datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        myclient = pymongo.MongoClient("mongodb://userroot:3sdgd237xd@103.195.142.180:27017/?authMechanism=DEFAULT")
        mydb = myclient["skypianSGH"]
        mycol = mydb["skypianSensor"]
        mydict = {	"time":dt_string,
                    "ph": ph1,
                   "tds":tds1,
                   "water temperature":tempair1,
                   "air temperature":tempudara,
                   "humidity": ph2,
                   "heat index":tds2,}

        x = mycol.insert_one(mydict)
    except :
        print("connection error")

def Update():
#readserial()
    # Setting TDS Manual
    #seleksipompa()
    data_log={}
    data_logPh={}
    data_logTds={}
    data_logTem={}
    data_logHum={}
    data_logHix={}
    now=datetime.now()
    waktu = int(now.strftime("%H"))
#     if ((waktu<22)and(waktu>4)):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_log['skypiancolection-data']=(dt_string, ph1, tds1, tempair1, tempudara, ph2,tds2)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                
    data_log['skypiancolection-dataPh']=(dt_string, ph1)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                
    data_log['skypiancolection-dataTds']=(dt_string,tds1)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                
    data_log['skypiancolection-dataTemp']=(dt_string,tempair1, tempudara)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                
    data_log['skypiancolection-dataHum']=(dt_string,ph2)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                
    data_log['skypiancolection-dataHix']=(dt_string,tds2)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
#     

# schedule.every(2).seconds.do(Update)
schedule.every(5).minutes.do(Update)
schedule.every(10).minutes.do(publish)

frameViewPh1 = Frame(root, bg="#FFFFFF", borderwidth=2, highlightcolor="#000000", height=60, width=80, relief='raised')
frameViewPh1.place(x=2, y=10)
frameViewTDS1 = Frame(root, bg="#FFFFFF", borderwidth=2, highlightcolor="#000000", height=60, width=80, relief='raised')
frameViewTDS1.place(x=2, y=75)
frameViewTA1 = Frame(root, bg="#FFFFFF", borderwidth=2, highlightcolor="#000000", height=60, width=80, relief='raised')
frameViewTA1.place(x=2, y=140)
frameViewTU1 = Frame(root, bg="#FFFFFF", borderwidth=2, highlightcolor="#000000", height=60, width=80, relief='raised')
frameViewTU1.place(x=2, y=205)

# Frame Realtime Menu Tangki 2
frameViewPh2 = Frame(root, bg="#FFFFFF", borderwidth=2, highlightcolor="#000000", height=60, width=80, relief='raised')
frameViewPh2.place(x=90, y=10)
frameViewTDS2 = Frame(root, bg="#FFFFFF", borderwidth=2, highlightcolor="#000000", height=60, width=80, relief='raised')
frameViewTDS2.place(x=90, y=75)
# frameViewTA2 = Frame(root, bg="#FFFFFF", borderwidth=2, highlightcolor="#000000", height=100, width=150, relief='raised')
# frameViewTA2.place(x=155, y=215)
# frameViewHUM2 = Frame(root, bg="#FFFFFF", borderwidth=4, highlightcolor="#000000", height=100, width=150, relief='raised')
# frameViewHUM2.place(x=155, y=330)
# Realtime
def Realtime():

# Frame Realtime Menu Tangki 1
    global p3
    ser_bytes = ser.readline()
    dataArray=[]
    dataArrayFloat=[]
    ser_bytes = str(ser_bytes[0:len(ser_bytes)].decode("utf-8"))
    dataArray = ser_bytes.split('@')
    try:
        for item in dataArray:
            dataArrayFloat.append(item)

        #vall = ser_bytes
        global ph1
        global ph2
        global tds1
        global tds2
        global tempair1
        global tempair2
        global tempudara
        global humidity
        global levelair1
        global leveair2
        ph1=float(dataArrayFloat[0])
        ph2=int(dataArrayFloat[4])
        tds1=int(dataArrayFloat[1])
        tds2=int(dataArrayFloat[5])
        tempair1=float(dataArrayFloat[2])
        #tempair2=float(dataArrayFloat[6])
        tempudara=float(dataArrayFloat[3])
        #humidity=float(dataArrayFloat[8])
        #levelair1=int(dataArrayFloat[9])
        leveair2=int(dataArrayFloat[6])

    except:
        print('reconect to sensor')
        Realtime()

        #Label(root, text="Lost Connection", fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '30', 'bold')).place(x=900, y=930)
    p3 = Label(root, text="         ", fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '18', 'bold')).place(x=0,y=90)
#     p4 = Label(root, text="         ", fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '25', 'bold')).place(x=170,y=140)

#     p1 = Label(root, text="       ", fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '25', 'bold')).place(x=10, y=35)
    p1 = Label(root, text=ph1, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '22', 'bold')).place(x=5, y=20)
#     p2 = Label(root, text="       ", fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '18', 'bold')).place(x=170,y=35)

    p2 = Label(root, text=ph2, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '25', 'bold')).place(x=100,y=20)
    p3 = Label(root, text=tds1, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '18', 'bold')).place(x=0,y=90)
    p4 = Label(root, text=tds2, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '25', 'bold')).place(x=100,y=90)
    p5 = Label(root, text=tempair1, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '20', 'bold')).place(x=0,y=160)
    #p6 = Label(root, text=tempair2, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '30', 'bold')).place(x=100,y=190)
    p7 = Label(root, text=tempudara, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '20', 'bold')).place(x=0,y=220)
    #p8 = Label(root, text=humidity, fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '30', 'bold')).place(x=170,y=350)
    #log['colection-data']=( ph1, ph2, tds1, tds2, tempair1, tempair2, tempudara, humidity, levelair1, leveair2)
#     print(auto)
#     if (auto==2):
#         if (lamp==0):
#             offled()
#         if (lamp==1):
#             onled()
#         if (lamp==2):
#             ledred()
#         if (lamp==3):
#             ledblue()
    if (auto==3):
        #schedule.every(5).seconds.do(pump)
#         schedule.every().day.at("07:00").do(pump)
#         schedule.every().day.at("14:00").do(pump)
#         schedule.every().day.at("18:00").do(pump)
#         #pump()
        schedule.every().day.at("07:00").do(blueled)
        schedule.every().day.at("07:02").do(offled)
        schedule.every().day.at("07:10").do(onled)
        schedule.every().day.at("07:15").do(offled)
        schedule.every().day.at("08:00").do(blueled)
        schedule.every().day.at("08:01").do(offled)
       
        
        schedule.every().day.at("09:30").do(onled)
        schedule.every().day.at("09:45").do(offled)
        schedule.every().day.at("10:15").do(onled)
        schedule.every().day.at("10:30").do(offled)
        schedule.every().day.at("11:15").do(onled)
        schedule.every().day.at("11:30").do(offled)
        schedule.every().day.at("12:15").do(onled)
        schedule.every().day.at("12:30").do(offled)#
        schedule.every().day.at("13:00").do(onled)
        schedule.every().day.at("13:20").do(offled)
        schedule.every().day.at("13:30").do(onled)
        schedule.every().day.at("13:50").do(offled)
        schedule.every().day.at("14:00").do(onled)
        schedule.every().day.at("14:20").do(offled)
        schedule.every().day.at("14:30").do(onled)
        schedule.every().day.at("14:50").do(offled)
        schedule.every().day.at("15:00").do(onled)
        schedule.every().day.at("15:20").do(offled)
        schedule.every().day.at("15:30").do(onled)
        schedule.every().day.at("15:50").do(offled)
        schedule.every().day.at("16:00").do(onled)
        schedule.every().day.at("16:20").do(offled)
        schedule.every().day.at("16:30").do(onled)
        schedule.every().day.at("16:50").do(offled)
        
        ######         seleksipompa()
    # Water Level

        # water level
#     if (levelair1==1):
#         #GPIO.output(a, GPIO.LOW)
#         btn_WaterLevelt2f1 = Button(root, bg="#28DD75", state = DISABLED, borderwidth=1, width='7', height='5').place(x=5, y=740)
#         btn_WaterLevelt1f2 = Button(root, bg="#28DD75", state = DISABLED, borderwidth=1, width='7', height='4').place(x=5, y=840)
#     if (levelair1==0):
#         btn_WaterLevelt2f1 = Button(root, bg="#ffffff", state = DISABLED, borderwidth=1, width='7', height='5').place(x=5, y=740)
#         btn_WaterLevelt1f2 = Button(root, bg="#E59E57", state = DISABLED, borderwidth=1, width='7', height='4').place(x=5, y=840)
    if (leveair2==1):
        btn_WaterLevelt2f1 = Button(root, bg="#28DD75", state = DISABLED, borderwidth=1, width='7', height='5').place(x=90, y=160)
        btn_WaterLevelt1f2 = Button(root, bg="#28DD75", state = DISABLED, borderwidth=1, width='7', height='2').place(x=90, y=215)
    if (leveair2==0): 
        btn_WaterLevelt2f1 =Button(root, bg="#ffffff", state = DISABLED, borderwidth=1, width='7', height='5').place(x=90, y=160)
        btn_WaterLevelt1f2 = Button(root, bg="#E59E57", state = DISABLED, borderwidth=1, width='7', height='2').place(x=90, y=215)




    #def pompa1():
        #GPIO.output(9, GPIO.HIGH)
        #time.sleep(7)
        #GPIO.output(9, GPIO.LOW)

    #def pompa2():
        #GPIO.output(10, GPIO.HIGH)
        #time.sleep(7)
        #GPIO.output(10, GPIO.LOW)


    # Start realtime dashboard
    dataArray.clear()
    dataArrayFloat.clear()


Label(root, text='pH', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=5, y=4)
Label(root, text='Humidity', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=90, y=4)
Label(root, text='TDS', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=5, y=70)
Label(root, text='Heat Index', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=90, y=70)
Label(root, text='WtrTemp(°C)', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=5, y=140)
# Label(root, text='AirTemp2(°C)', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=157, y=230)
Label(root, text='AirTemp(°C)', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=5, y=205)
Label(root, text='Fert.Level', fg="#568ADB", bg="#FFFFFF", font=('IBM Plex Sans', '8', 'bold')).place(x=90, y=140)#

# Label(root, text="Fertilizer Level", fg="#568ADB", bg="#ffffff", anchor='w', font=('IBM Plex Sans', '22', 'bold')).place(x=5, y=700)

        # Water Level
#Label(root, text="   1                   2", fg="#000000", bg="#ffFFFF", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=5, y=930)

def harvest():
    file = '/home/skypian/Desktop/skypianData/skypiancolection-data.csv'
    if(os.path.exists(file) and os.path.isfile(file)):
#       os.remove(file)
      print("file deleted")
    else:
      print("file not found")
# 
#     frameViewGrafikAll = Frame(root, bg="#ffffff", height=1000, width=750, relief='raised')
#     frameViewGrafikAll.place(x=310, y=10)
# 
def menu():
    # Frame Setting
    frameViewGrafik = Frame(root, bg="#ffffff", height=420, width=470, relief='raised')
    frameViewGrafik.place(x=175, y=5)

    # Grafik 1
    btn_grafik1 = Button(root, bd=0, relief="raised", height = 1, width = 10, text="PH Graph", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#000000", borderwidth=2, activebackground="#28DD75", command=grafik1)
    btn_grafik1.place(x=650, y=10)
    #grafik1.1
    btn_grafik11 = Button(root, bd=0, relief="raised", height = 1, width = 10, text="Hum Graph", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#000000", borderwidth=2, activebackground="#28DD75", command=grafik3)
    btn_grafik11.place(x=650, y=50)

    # Grafik 2
    btn_grafik2 = Button(root, bd=0, relief="raised", height = 1, width = 10, text="TDS Graph", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#000000", borderwidth=2, activebackground="#FF8849", command=grafik2)
    btn_grafik2.place(x=650, y=90)

        # Grafik 2
    btn_grafik22 = Button(root, bd=0, relief="raised", height = 1, width = 10, text="Temp Graph", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#000000", borderwidth=2, activebackground="#FF8849", command=grafik4)
    btn_grafik22.place(x=650, y=130)

    # Harvest
    btn_grafik3 = Button(root, bd=0, relief="raised", height = 1, width = 10, text="Harvest", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#000000", borderwidth=2, activebackground="#FF0000", command=harvest)
    btn_grafik3.place(x=650, y=370)

    # Mode

    Label(root, text="Manual      ", fg="#568ADB", bg="#ffffff", anchor='w', font=('IBM Plex Sans', '12', 'bold')).place(x=650, y=190)
    btn_mode1 = Button(root, text="Manual", fg="#ffffff", bg="#9eb7e0", borderwidth=4, width='8',height = '2', font=('IBM Plex Sans', '15'), command=modeManual).place(x=650, y=210)
    btn_mode2 = Button(root, text="Otomatis", fg="#ffffff", bg="#9eb7e0", borderwidth=4, width='8', height = '2', font=('IBM Plex Sans', '15'), command=modeOtomatis).place(x=650, y=280)

# Setting LED

def SettingLED():
    #Label(root,  text="LED", fg="#568ADB", bg="#FFFFFF", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=5, y=450)
    OnLED = Button(root, bd=0, relief="raised", height = 2, width = 5, text="Act 1", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#FFFFFF", borderwidth=2, activebackground="#568ADB", command=onled)
    OnLED.place(x=0, y=280)
    OffLED = Button(root, bd=0, relief="raised", height = 2, width = 5, text="OFF", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#FFFFFF", borderwidth=2, activebackground="#D39139", command=offled)
    OffLED.place(x=85, y=280)
    BlueLED = Button(root, bd=0, relief="raised", text="Act 2", height = 2, width = 5, font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#FFFFFF", borderwidth=2, activebackground="#3978D3", command=blueled)
    BlueLED.place(x=0, y=345)
    RedLED = Button(root, bd=0, relief="raised", height = 2, width = 5, text="Fert", font="arial 15", bg="#9eb7e0", fg="#ffFFFF", activeforeground="#FFFFFF", borderwidth=2, activebackground="#F42C44", command=redled)
    RedLED.place(x=85, y=345)

auto=1
lamp=0;
#mode = BooleanVar(root, name = 'mod')
def modeManual():
    #offled()

    global auto
    auto=2
    Label(root, text="Manual      ", fg="#568ADB", bg="#ffffff", anchor='w', font=('IBM Plex Sans', '12', 'bold')).place(x=650, y=250)
    #GPIO.output(sw, GPIO.HIGH)
    #root.setvar(name = 'mod', value = True)
    #print(root.getvar(name = 'mod'))
    #Setting LED
    data_log={}
    now=datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_log['skypiancolection-mode']=(dt_string,auto)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
    SettingLED()
    menu()

def modeOtomatis():
    #offled()
    global auto
    auto=3
    Label(root, text="Automatic", fg="#568ADB", bg="#ffffff", anchor='w', font=('IBM Plex Sans', '12', 'bold')).place(x=650, y=190)
    #GPIO.output(sw, GPIO.LOW)
    #root.setvar(name = 'mod', value = False)
    #print(root.getvar(name = 'mod'))
    data_log={}
    now=datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data_log['skypiancolection-mode']=(dt_string,auto)
    for file, data in data_log.items():
            with open('/home/skypian/Desktop/skypianData/' + file + '.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
# 
#Label(root,  text="LED", fg="#568ADB", bg="#FFFFFF", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=5, y=450)
    OnLED = Button(root, bd=0, relief="raised", height = 2, width = 5, text="Act 1", font="arial 15", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#568ADB", state=DISABLED)
    OnLED.place(x=0, y=280)
    OffLED = Button(root, bd=0, relief="raised", height = 2, width = 5, text="OFF", font="arial 15", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#D39139", state=DISABLED)
    OffLED.place(x=85, y=280)
    BlueLED = Button(root, bd=0, relief="raised", text="Act 2", height = 2, width = 5, font="arial 15", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#3978D3", state=DISABLED)
    BlueLED.place(x=0, y=345)
    RedLED = Button(root, bd=0, relief="raised", height = 2, width = 5, text="Fert", font="arial 15", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#F42C44", state=DISABLED)
    RedLED.place(x=85, y=345)


# OnLED = Button(root, bd=0, relief="raised", height = 2, width = 6, text="ON", font="arial 24", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#568ADB", state=DISABLED)
#     OnLED.place(x=5, y=500)
#     OffLED = Button(root, bd=0, relief="raised", height = 2, width = 6, text="OFF", font="arial 24", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#D39139", state=DISABLED)
#     OffLED.place(x=165, y=500)
#     BlueLED = Button(root, bd=0, relief="raised", text="Blue", height = 2, width = 6, font="arial 24", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#3978D3", state=DISABLED)
#     BlueLED.place(x=5, y=600)
#     RedLED = Button(root, bd=0, relief="raised", height = 2, width = 6, text="Red", font="arial 24", bg="#99FFFF", fg="#000000", activeforeground="#FFFFFF", borderwidth=2, activebackground="#F42C44", state=DISABLED)
#     RedLED.place(x=165, y=600)

    #setting()

def seleksipompa():
    now = datetime.now()
    waktu = int(now.strftime("%H"))
    #print('waktunya adalah', waktu)
    #Label(root, text=waktu, fg="#000000", bg="#ffffff", anchor='w', font=('IBM Plex Sans', '20', 'bold')).place(x=10, y=10)
    if (waktu == 18):
        onled()
    if ((waktu > 21) or (waktu < 18)):
        offled()

    #setting()
# 
def setting():
    # Tampilan
    frameUtama = Frame(root, bg="#FFFFFF", height=900, width=700, relief='raised')
    frameUtama.place(x=310, y=0)

    image1 = image.open('/home/pi/mu_code/skypianimage.png')
    test = ImageTk.PhotoImage(image1)

    label1 = tkinter.label(image=test)
    label1.image = test

    label1.place(x = 300, y= 10)


   #gambar = PhotoImage(file="/home/pi/mu_code/skypianimage.png")
    #w1 = Label(frameUtama, image=gambar).pack(side="right")



# Creating menubar
menubar = Menu(root, bg='#868E8F',fg="#FFFFFF", activebackground='#A7ABAB')
menu2 = Menu(root)

# Adding File Menu and commands
file = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='EXIT   ', font=('IBM Plex Sans', '25'), menu = file)
file.add_command(label ='NO', font=('IBM Plex Sans', '25'))
file.add_command(label ='YES', font=('IBM Plex Sans', '25'), command = root.destroy)

# Adding Save History Menu and commands
#save = Menu(menubar, tearoff = 0)
#menubar.add_cascade(label ='Graph', font=('IBM Plex Sans', '24'), menu = save)
#save.add_command(label ='Show Graph', font=('IBM Plex Sans', '24'), command = menu)

# Tampilan Awal
#setting()
menu()
def restar():
    os.system("sudo reboot")
schedule.every().day.at("07:35").do(restar)
schedule.every().day.at("08:35").do(restar)
schedule.every().day.at("09:35").do(restar)
schedule.every().day.at("10:35").do(restar)
schedule.every().day.at("11:35").do(restar)
schedule.every().day.at("12:35").do(restar)
schedule.every().day.at("13:25").do(restar)
schedule.every().day.at("13:55").do(restar)
schedule.every().day.at("14:25").do(restar)
schedule.every().day.at("14:55").do(restar)
schedule.every().day.at("15:25").do(restar)
schedule.every().day.at("15:55").do(restar)
schedule.every().day.at("16:25").do(restar)
schedule.every().day.at("17:00").do(restar)
schedule.every().day.at("19:00").do(restar)
schedule.every().day.at("21:00").do(restar)
schedule.every().day.at("22:00").do(restar)
schedule.every().day.at("23:00").do(restar)
schedule.every().day.at("00:00").do(restar)
schedule.every().day.at("02:00").do(restar)
schedule.every().day.at("04:00").do(restar)
schedule.every().day.at("06:00").do(restar)
schedule.every().day.at("06:50").do(restar)










SettingLED()
# display Menu
root.config(menu = menubar)
modeOtomatis()
headers = ['time','status']
df = pd.read_csv('/home/skypian/Desktop/skypianData/skypiancolection-mode.csv',names=headers)
df = df.tail(1)
# # df.head(1)
run_modee = df[['status']]
print(run_modee)
# if(run_modee=='3'):
#     modeOtomatis()
# if(run_modee=='2'):
#     modeManual()
while True:
    root.update()
    Realtime()
#     headers = ['datetime','status']
#     df = pd.read_csv('/home/skypian/Desktop/skypiancolection-mode.csv',names=headers)
#     df = df.tail(1)
# #     run_mode=3
#     run_modee = df[['status']]
#     #print(run_modee)
#     if (run_modee=='3'):
#         modeOtomatis()
#     if (run_modee=='2'):
#         modeManual()
    schedule.run_pending()
    sleep(1)
#root.mainloop() 
