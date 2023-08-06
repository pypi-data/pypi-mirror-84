
import sys
import os

import clr


dll_path=os.path.split(os.path.realpath(__file__))[0]

sys.path.append(str(dll_path))


# install pythonnet
try :
   aiqi_blue=clr.AddReference('AIQI_Bluetooth_LIB')
except:

    print("please add AIQI_Bluetooth_LIB.ddl file ")
    sys.exit()


from AIQI_Bluetooth import  *
# from AIQI_Bluetooth import  *


'''
蓝牙数据发送 
参数：要发送的数组

'''

def Bluetooth_Send(gatt,send_buff):
    gatt.Aiqi_Bluetooth_Send(send_buff)


'''
蓝牙扫描控制
true is  scan open
false is scan false
'''

def Bluetooth_Scan_Ctrl(watch,enable):
    watch.Bluetooth_Watch_Enable(enable)


'''
蓝牙断开
参数1 要断开的gatt 实例

'''

def Bluetooth_Disconnect(gatt):
    gatt.Bluetooth_Disconnect()

'''

蓝牙发现初始化
参数 1 蓝牙扫描回调
返回值 蓝牙watcher 实例

'''
def Bluetooth_Watch_Init(watch_handle):
    print(aiqi_blue)
    global ble_watcher

    watch = Bluetooth_watcher()

    watch.Aiqi_ble_wachter_handle += watch_handle

    return watch

'''
蓝牙初始化
参数 1 蓝牙连接状态回调
参数 2 蓝牙建立过程回调
参数 3 蓝牙接收数据回调
返回值 gatt 实例
'''

def Bluetooth_Init(ble_stats_handle, create_stats_handle, char_ValueChanged_handle):
    print(aiqi_blue)
    global ble_watcher

    gatt = Bluetooth_gatt_class()
    gatt.Aiqi_Ble_connected_stats_handle += ble_stats_handle
    gatt.Aiqi_Characteristic_ValueChanged_handle += char_ValueChanged_handle
    gatt.Aiqi_Ble_connect_build_stats_handle += create_stats_handle
    return gatt





