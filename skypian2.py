from GUI_Master import RootGUI, MasterGUI
from Serial_Master import SerialCtrl
from Data_Master import DataCtrl
from GPIO_Master import GPIOCtrl

serial = SerialCtrl()
data = DataCtrl()
gpio = GPIOCtrl()

GUI_ROOT = RootGUI()
GUI_MASTER = MasterGUI(GUI_ROOT.root, serial, data, gpio)

GUI_ROOT.root.mainloop()