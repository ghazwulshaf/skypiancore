from tkinter import *
from tkinter import messagebox
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import numpy as np

# style.use("ggplot")

class RootGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Skypian")
        self.root.geometry("%dx%d" % (800, 480))
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        # self.root.attributes("-fullscreen", True)

class MasterGUI():
    def __init__(self, root, serial, data, gpio):
        self.root = root
        self.serial = serial
        self.data = data
        self.gpio = gpio

        self.padX = 20
        self.fontSize = 18

        self.GUI_COM()
        self.GUI_DATA()
        self.GUI_SENSOR()
        self.GUI_GRAPH()
        self.GUI_ACTUATOR()
        self.GUI_ACTION()

        self.publish()

    def GUI_COM(self):
        self.frm_com = LabelFrame(self.root, text="Com Manager", bg="white", padx=2, pady=2)

        self.lbl_com = Label(self.frm_com, text="Available Port(s): ", bg="white", anchor="w")
        self.lbl_bd = Label(self.frm_com, text="Baud Rate: ", bg="white", anchor="w")

        self.ComOptionMenu()
        self.BaudOptionMenu()

        self.btn_refresh = Button(self.frm_com, text="Refresh", width=10, command=self.refresh)
        self.btn_connect = Button(self.frm_com, text="Connect", width=10, command=self.connect, state="disabled")

    def ComOptionMenu(self):
        coms = ["-"]
        self.clicked_com = StringVar()
        self.clicked_com.set(coms[0])
        self.drop_com = OptionMenu(self.frm_com, self.clicked_com, *coms, command=self.connect_ctrl)
        self.drop_com.config(width=10)

    def BaudOptionMenu(self):
        bds = ["-",
               "300",
               "600",
               "1200",
               "2400",
               "4800",
               "9600",
               "14400",
               "19200",
               "28800",
               "38400",
               "56000",
               "57600",
               "115200",
               "128000",
               "256000"]
        self.clicked_bd = StringVar()
        self.clicked_bd.set(bds[0])
        self.drop_baud = OptionMenu(self.frm_com, self.clicked_bd, *bds, command=self.connect_ctrl)
        self.drop_baud.config(width=10)

    def connect_ctrl(self, widget):
        """Method to control connect button and get com and baudrate"""
        print()
        print("COM: " + self.clicked_com.get())
        print("Baud: " + self.clicked_bd.get())

        if "-" in self.clicked_com.get() or "-" in self.clicked_bd.get():
            self.btn_connect["state"] = "disable"
        else:
            self.btn_connect["state"] = "active"

    def refresh(self):
        self.serial.getCOMList()
        coms = self.serial.com_list

        print()
        print(self.serial.com_list)

        self.clicked_com.set(coms[0])
        self.drop_com.destroy()
        self.drop_com = OptionMenu(self.frm_com, self.clicked_com, *coms, command=self.connect_ctrl)
        self.drop_com.config(width=10)
        self.drop_com.grid(column=2, row=0, padx=self.padX)

    def connect(self):
        if self.btn_connect["text"] in "Connect":
            self.serial.SerialOpen(self)
            if self.serial.ser.status:
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disable"
                self.drop_com["state"] = "disable"
                self.drop_baud["state"] = "disable"
                InfoMsg = f"Successful UART connection using {self.clicked_com.get()}"
                messagebox.showinfo("showinfo", InfoMsg)

                self.frm_com.destroy()
                self.data.CheckData()
                self.start_stream()

                self.t2 = threading.Thread(name="t2", target=self.Animate, daemon=True)
                
                self.serial.t1.start()
                self.t2.start()
                self.data.t3.start()
            else:
                ErrorMsg = f"Failure to estabish UART connection using {self.clicked_com.get()}"
                messagebox.showerror("showerror", ErrorMsg)
        else:
            self.serial.SerialClose()
            self.stop_stream()
            InfoMsg = f"UART connection using {self.clicked_com.get()} is now closed"
            messagebox.showwarning("showinfo", InfoMsg)
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_com["state"] = "active"
            self.drop_baud["state"] = "active"

    # def auto_connect(self):
    #     self.serial.getCOMList()
    #     coms = self.serial.com_list
    #     self.serial.SerialOpen(self)

    #     if self.serial.ser.status:
    #         InfoMsg = f"Successful UART connection using {self.clicked_com.get()}"

    #         self.data.CheckData()
    #         self.start_stream()

    #         self.t2 = threading.Thread(name="t2", target=self.Animate, daemon=True)
            
    #         self.serial.t1.start()
    #         self.t2.start()
    #         self.data.t3.start()
    #     else:
    #         ErrorMsg = f"Failure to estabish UART connection using {self.clicked_com.get()}"
    #         messagebox.showerror("showerror", ErrorMsg)

    def start_stream(self):
        self.serial.t1 = threading.Thread(name="t1", target=self.serial.SerialDataStream, args=(self,), daemon=True)
        self.data.t3 = threading.Thread(name="t3", target=self.data.DataStream, daemon=True)

    def stop_stream(self):
        self.serial.t1.stop()

    def GUI_DATA(self):
        self.frm_data = Frame(self.root, bg="white")

        height = self.frm_data.winfo_height()
        width = self.frm_data.winfo_width()

        self.frm_data.rowconfigure([0,1,2,3,4,5], minsize=height/6, weight=1)
        self.frm_data.columnconfigure([0,1], minsize=width/2, weight=1)

    def GUI_SENSOR(self):
        self.frm_sensor = LabelFrame(self.frm_data, text="Sensors", labelanchor="n", bg="white", padx=2, pady=2)

        height = self.frm_sensor.winfo_height()
        width = self.frm_sensor.winfo_width()

        self.frm_sensor.rowconfigure([0,1,2], minsize=height/3, weight=1)
        self.frm_sensor.columnconfigure([0,1,2], minsize=width/3, weight=1)

        self.frm_s1 = LabelFrame(self.frm_sensor, text=self.data.nm_s1, labelanchor="n", bg="white", padx=2, pady=2)
        self.frm_s2 = LabelFrame(self.frm_sensor, text=self.data.nm_s2, labelanchor="n", bg="white", padx=2, pady=2)
        self.frm_s3 = LabelFrame(self.frm_sensor, text=self.data.nm_s3, labelanchor="n", bg="white", padx=2, pady=2)
        self.frm_s4 = LabelFrame(self.frm_sensor, text=self.data.nm_s4, labelanchor="n", bg="white", padx=2, pady=2)
        self.frm_s5 = LabelFrame(self.frm_sensor, text=self.data.nm_s5, labelanchor="n", bg="white", padx=2, pady=2)
        self.frm_s6 = LabelFrame(self.frm_sensor, text=self.data.nm_s6, labelanchor="n", bg="white", padx=2, pady=2)
        self.frm_s7 = LabelFrame(self.frm_sensor, text=self.data.nm_s7, labelanchor="n", bg="white")

        self.lbl_s1 = Label(self.frm_s1, text=self.data.DataSensor[self.data.Sensors[1]], font=("Arial", self.fontSize), bg="white", anchor="center")
        self.lbl_s2 = Label(self.frm_s2, text=self.data.DataSensor[self.data.Sensors[2]], font=("Arial", self.fontSize), bg="white", anchor="center")
        self.lbl_s3 = Label(self.frm_s3, text=self.data.DataSensor[self.data.Sensors[3]], font=("Arial", self.fontSize), bg="white", anchor="center")
        self.lbl_s4 = Label(self.frm_s4, text=self.data.DataSensor[self.data.Sensors[4]], font=("Arial", self.fontSize), bg="white", anchor="center")
        self.lbl_s5 = Label(self.frm_s5, text=self.data.DataSensor[self.data.Sensors[5]], font=("Arial", self.fontSize), bg="white", anchor="center")
        self.lbl_s6 = Label(self.frm_s6, text=self.data.DataSensor[self.data.Sensors[6]], font=("Arial", self.fontSize), bg="white", anchor="center")
        # self.lbl_s7 = Label(self.frm_s7, text=self.data.DataSensor[6], font=("Arial", self.fontSize), bg="white", anchor="center")
        
        dt_s7 = (float(self.data.DataSensor[self.data.Sensors[7]]) / 100.00) * self.frm_s7.winfo_height()
        self.frm_dt_s7 = Frame(self.frm_s7, bg="lightblue", height=dt_s7)

    def UpdateSensorText(self):
        self.lbl_s1["text"] = self.data.DataSensor[self.data.Sensors[1]]
        self.lbl_s2["text"] = self.data.DataSensor[self.data.Sensors[2]]
        self.lbl_s3["text"] = self.data.DataSensor[self.data.Sensors[3]]
        self.lbl_s4["text"] = self.data.DataSensor[self.data.Sensors[4]]
        self.lbl_s5["text"] = self.data.DataSensor[self.data.Sensors[5]]
        self.lbl_s6["text"] = self.data.DataSensor[self.data.Sensors[6]]
        # self.lbl_s7["text"] = self.data.DataSensor[6]

        dt_s7 = (float(self.data.DataSensor[self.data.Sensors[7]]) / 100.00) * self.frm_s7.winfo_height()
        self.frm_dt_s7["height"] = dt_s7

    def GUI_GRAPH(self):
        self.frm_graph = LabelFrame(self.frm_data, text="Graph", labelanchor="n", bg="white", padx=2, pady=2)

        height = self.frm_graph.winfo_height()
        width = self.frm_graph.winfo_width()

        self.frm_graph.rowconfigure([0,1,2,3,4], minsize=height/5, weight=1)
        self.frm_graph.columnconfigure(0, weight=1)

        self.frm_gp = Frame(self.frm_graph, bg="white", highlightbackground="grey", highlightthickness=1)
        self.frm_btn = Frame(self.frm_graph, bg="white")

        self.AddGraph()

        height_btn = self.frm_btn.winfo_height()
        width_btn = self.frm_btn.winfo_width()

        self.frm_btn.rowconfigure([0,1], minsize=height_btn/2, weight=1)
        self.frm_btn.columnconfigure([0,1], minsize=width_btn/2, weight=1)
        
        self.btn_gp1 = Button(self.frm_btn, text=self.data.nm_gp1, command=self.setGp1)
        self.btn_gp2 = Button(self.frm_btn, text=self.data.nm_gp2, command=self.setGp2)
        self.btn_gp3 = Button(self.frm_btn, text=self.data.nm_gp3, command=self.setGp3)
        self.btn_gp4 = Button(self.frm_btn, text=self.data.nm_gp4, command=self.setGp4)

    def AddGraph(self):
        self.fig = Figure(figsize=(3,2), dpi=80)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frm_gp)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def Animate(self):
        self.aniThreading = True
        while self.aniThreading:
            try:
                self.data.ReadData()
                self.ax.clear()
                if self.data.xList[-1] < 2:
                    self.ax.set_xlim([0, self.data.xList[-1]])
                else:
                    self.ax.set_xlim([(self.data.xList[-1] - 2), self.data.xList[-1]])
                self.setPlot()
                self.canvas.draw()
            except Exception as e:
                print(e)

    def setGp1(self):
        if self.data.stt_gp1 in "OFF":
            self.data.stt_gp1 = "ON"
            self.btn_gp1["bg"] = self.data.clr_gp1
        else:
            self.data.stt_gp1 = "OFF"
            self.btn_gp1["bg"] = self.data.clr_btn

    def setGp2(self):
        if self.data.stt_gp2 in "OFF":
            self.data.stt_gp2 = "ON"
            self.btn_gp2["bg"] = self.data.clr_gp2
        else:
            self.data.stt_gp2 = "OFF"
            self.btn_gp2["bg"] = self.data.clr_btn

    def setGp3(self):
        if self.data.stt_gp3 in "OFF":
            self.data.stt_gp3 = "ON"
            self.btn_gp3["bg"] = self.data.clr_gp3
        else:
            self.data.stt_gp3 = "OFF"
            self.btn_gp3["bg"] = self.data.clr_btn

    def setGp4(self):
        if self.data.stt_gp4 in "OFF":
            self.data.stt_gp4 = "ON"
            self.btn_gp4["bg"] = self.data.clr_gp4
        else:
            self.data.stt_gp4 = "OFF"
            self.btn_gp4["bg"] = self.data.clr_btn

    def setPlot(self):
        if self.data.stt_gp1 in "ON":
            self.plot1()
        if self.data.stt_gp2 in "ON":
            self.plot2()
        if self.data.stt_gp3 in "ON":
            self.plot3()
        if self.data.stt_gp4 in "ON":
            self.plot4()

    def plot1(self):
        self.ax.plot(self.data.xList, self.data.y1List, color = self.data.clr_s1)

    def plot2(self):
        self.ax.plot(self.data.xList, self.data.y3List, color = self.data.clr_s3)

    def plot3(self):
        self.ax.plot(self.data.xList, self.data.y2List, color = self.data.clr_s2)

    def plot4(self):
        self.ax.plot(self.data.xList, self.data.y5List, color = self.data.clr_s5)
        self.ax.plot(self.data.xList, self.data.y6List, color = self.data.clr_s6)

    def GUI_ACTUATOR(self):
        self.frm_actuator = LabelFrame(self.frm_data, text="Actuators", labelanchor="n", bg="white", padx=2, pady=2)

        height = self.frm_actuator.winfo_height()
        width = self.frm_actuator.winfo_width()

        self.frm_actuator.rowconfigure(0, weight=1)
        self.frm_actuator.columnconfigure([0,1,2], minsize=width/3, weight=1)

        self.btn_ac1 = Button(self.frm_actuator, text=(self.data.nm_ac1 + ": " + self.data.stt_ac1), command=self.turnAc1, state=DISABLED)
        self.btn_ac2 = Button(self.frm_actuator, text=(self.data.nm_ac2 + ": " + self.data.stt_ac2), command=self.turnAc2, state=DISABLED)
        self.btn_fert = Button(self.frm_actuator, text=(self.data.nm_fert + ": " + self.data.stt_fert), command=self.turnFert, state=DISABLED)

    def turnAc1(self):
        if self.data.stt_ac1 in "OFF":
            self.gpio.TurnAc1()
            self.data.stt_ac1 = "ON"
            self.data.val_ac1 = 1
            self.data.SetActuatorMsg()
            self.btn_ac1["text"] = self.data.nm_ac1 + ": " + self.data.stt_ac1
            self.btn_ac1["bg"] = "grey"
        else:
            self.gpio.TurnAc1Off()
            self.data.stt_ac1 = "OFF"
            self.data.val_ac1 = 0
            self.data.SetActuatorMsg()
            self.btn_ac1["text"] = self.data.nm_ac1 + ": " + self.data.stt_ac1
            self.btn_ac1["bg"] = self.data.clr_btn

    def turnAc2(self):
        if self.data.stt_ac2 in "OFF":
            self.gpio.TurnAc2()
            self.data.stt_ac2 = "ON"
            self.data.val_ac2 = 1
            self.btn_ac2["text"] = self.data.nm_ac2 + ": " + self.data.stt_ac2
            self.btn_ac2["bg"] = "grey"
        else:
            self.gpio.TurnAc2Off()
            self.data.stt_ac2 = "OFF"
            self.data.val_ac2 = 0
            self.btn_ac2["text"] = self.data.nm_ac2 + ": " + self.data.stt_ac2
            self.btn_ac2["bg"] = self.data.clr_btn

    def turnFert(self):
        if self.data.stt_fert in "OFF":
            self.gpio.TurnFert()
            self.data.stt_fert = "ON"
            self.data.val_fert = 1
            self.btn_fert["text"] = self.data.nm_fert + ":" + self.data.stt_fert
            self.btn_fert["bg"] = "grey"
        else:
            self.gpio.TurnFertOff()
            self.data.stt_fert = "OFF"
            self.data.val_fert = 0
            self.btn_fert["text"] = self.data.nm_fert + ":" + self.data.stt_fert
            self.btn_fert["bg"] = self.data.clr_btn

    def GUI_ACTION(self):
        self.frm_action = LabelFrame(self.frm_data, text="Actions", labelanchor="n", bg="white", padx=2, pady=2)

        height = self.frm_action.winfo_height()
        width = self.frm_action.winfo_width()

        self.frm_action.rowconfigure([0,1], minsize=height/2, weight=1)
        self.frm_action.columnconfigure([0,1], minsize=width/2, weight=1)

        self.btn_act1 = Button(self.frm_action, text=(self.data.nm_act1 + ": " + self.data.stt_act1), command=self.turnAct1)
        self.btn_act2 = Button(self.frm_action, text=self.data.nm_act2, command=self.harvest)
        self.btn_act3 = Button(self.frm_action, text=self.data.nm_act3, command=self.exit)

    def turnAct1(self):
        if self.data.stt_act1 in "AUTO":
            self.data.stt_act1 = "MANUAL"
            self.btn_act1["text"] = self.data.nm_act1 + ": " + self.data.stt_act1
            self.btn_act1["bg"] = "grey"
            self.btn_ac1["state"] = "active"
            self.btn_ac2["state"] = "active"
            self.btn_fert["state"] = "active"
        else:
            self.data.stt_act1 = "AUTO"
            self.btn_act1["text"] = self.data.nm_act1 + ": " + self.data.stt_act1
            self.btn_act1["bg"] = self.data.clr_btn
            self.btn_ac1["state"] = "disabled"
            self.btn_ac2["state"] = "disabled"
            self.btn_fert["state"] = "disabled"

    def harvest(self):
        dlg_harvest = messagebox.askyesno(title='Harvest?', message='Are you sure you want to reset data?', parent=self.root, icon='warning')
        if dlg_harvest:
            self.data.DeleteData()
            self.data.CheckData()

    def exit(self):
        dlg_exit = messagebox.askyesno(title="Exit?", message="Are you sure you want to close GUI?", parent=self.root, icon="warning")
        if dlg_exit:
            self.root.destroy()

    def publish(self):
        #region Com GUI
        self.frm_com.pack(anchor="w", padx=5, pady=5)

        self.lbl_com.grid(column=1, row=0)
        self.drop_com.grid(column=2, row=0, padx=self.padX)

        self.lbl_bd.grid(column=3, row=0)
        self.drop_baud.grid(column=4, row=0, padx=self.padX)

        self.btn_refresh.grid(column=5, row=0, padx=2)
        self.btn_connect.grid(column=6, row=0, padx=2)
        #endregion Com GUI

        #region Data GUI
        self.frm_data.pack(fill="both", expand=True, padx=5, pady=5)

        #region Sensor GUI
        self.frm_sensor.grid(row=0, column=0, rowspan=5, sticky="news", padx=2, pady=2)

        self.frm_s1.grid(row=0, column=0, sticky="news", padx=2, pady=2)
        self.frm_s2.grid(row=0, column=1, sticky="news", padx=2, pady=2)
        self.frm_s3.grid(row=1, column=0, sticky="news", padx=2, pady=2)
        self.frm_s4.grid(row=1, column=1, sticky="news", padx=2, pady=2)
        self.frm_s5.grid(row=2, column=0, sticky="news", padx=2, pady=2)
        self.frm_s6.grid(row=2, column=1, sticky="news", padx=2, pady=2)
        self.frm_s7.grid(row=1, column=2, rowspan=2, sticky="news", padx=2, pady=2)

        self.lbl_s1.pack(fill="both", expand="true")
        self.lbl_s2.pack(fill="both", expand="true")
        self.lbl_s3.pack(fill="both", expand="true")
        self.lbl_s4.pack(fill="both", expand="true")
        self.lbl_s5.pack(fill="both", expand="true")
        self.lbl_s6.pack(fill="both", expand="true")
        # self.lbl_s7.pack(fill="both", expand="true")
        self.frm_dt_s7.place(anchor="sw", relwidth=1, relx=0, rely=1)
        #endregion Sensor GUI

        #region Graph GUI
        self.frm_graph.grid(row=0, column=1, rowspan=5, sticky="news", padx=2, pady=2)

        self.frm_gp.grid(row=0, column=0, rowspan=4, sticky="news", padx=2, pady=2)
        self.frm_btn.grid(row=4, column=0, sticky="news")

        self.btn_gp1.grid(row=0, column=0, sticky="news", padx=2, pady=2)
        self.btn_gp2.grid(row=0, column=1, sticky="news", padx=2, pady=2)
        self.btn_gp3.grid(row=1, column=0, sticky="news", padx=2, pady=2)
        self.btn_gp4.grid(row=1, column=1, sticky="news", padx=2, pady=2)
        #endregion Graph GUI

        #region Actuator GUI
        self.frm_actuator.grid(row=5, column=0, sticky="news", padx=2, pady=2)

        self.btn_ac1.grid(row=0, column=0, sticky="news", padx=2, pady=2)
        self.btn_ac2.grid(row=0, column=1, sticky="news", padx=2, pady=2)
        self.btn_fert.grid(row=0, column=2, sticky="news", padx=2, pady=2)
        #endregion Actuator GUI

        #region Action GUI
        self.frm_action.grid(row=5, column=1, sticky="news", padx=2, pady=2)

        self.btn_act1.grid(row=0, column=0, rowspan=2, sticky="news", padx=2, pady=2)
        self.btn_act2.grid(row=0, column=1, sticky="news", padx=2, pady=2)
        self.btn_act3.grid(row=1, column=1, sticky="news", padx=2, pady=2)
        #endregion Action GUI
        #endregion Data GUI

if __name__ == "__main__":
    RootGUI()
    MasterGUI()