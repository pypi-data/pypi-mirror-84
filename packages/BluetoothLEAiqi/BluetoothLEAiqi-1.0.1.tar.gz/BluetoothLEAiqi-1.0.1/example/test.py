import time

import BluetoothLEAiqi


blue_watcher = ""
blue_gatt = ""

mydev = "E8F4F3395CBD"


#要连接的设备mac
connectid = mydev


'''
建立连接  状态回调

'''
def Ble_connect_create_handle(sender, stats):
    if stats < BluetoothLEAiqi.Connect_result.Connect_Send_OK.value:

        if stats == BluetoothLEAiqi.Connect_result.Connect_Notify_OK.value:
            print("connect ok")

        else:
            print("connect err", stats)
    else:
        print("blue send stats", stats)


def Ble_scan_handle(sender, par):
    print(par)
    if par[1] == connectid:
        blue_watcher.Bluetooth_Watch_Enable(False)
        print("find mibot")
        # 建立连接
        blue_gatt.bluetooth_connect_create(par[3])

'''

蓝牙连接状态监听

'''
def Ble_connect_stats_handle(sender, par):
    print(par)

    

'''

蓝牙接受数据监听

'''

def Ble_value_change_handle(sender, par):
    print("rev value len:",len(par))
    print(par[0])


def main():
    global  blue_watcher,blue_gatt

    print("BluetoothLEAiqi example")

    blue_watcher = BluetoothLEAiqi.Bluetooth_Watch_Init(Ble_scan_handle)

    blue_gatt=BluetoothLEAiqi.Bluetooth_Init(Ble_connect_stats_handle, Ble_connect_create_handle,Ble_value_change_handle)

    BluetoothLEAiqi.Bluetooth_Scan_Ctrl(blue_watcher,True)

    time.sleep(6)

    data = [0, 1, 2, 3]
    BluetoothLEAiqi.Bluetooth_Send(blue_gatt,data)

    # Bluetooth_Disconnect()
    time.sleep(2)

    while True:
        # bluetooth_send()
        time.sleep(10)
        # bluetooth_send()
        print("re send")



if __name__ == '__main__':
    main()