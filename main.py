import os
import time
import pathlib
import xml.etree.ElementTree as ET
from datetime import datetime
local_project = str(pathlib.Path(__file__).parent.parent)


#Get Device's size
def device_size(serialNb):
    val = os.popen("adb -s "+serialNb+" shell wm size").read()
    if val.find("device not found") == -1:
        if val.find("\n") > -1:
            val = val.split("\n")
            for x in val:
                if x.find("Override") > -1:
                    val = x

            if str(type(val)) == "<class 'list'>":
                val = val[0]
                val = val.split(":")
                new_val = val[1].split("x")
                size = {}
                size["x"] = int(new_val[0].replace(" ", "").replace("\n", ""))
                size["y"] = int(new_val[1].replace(" ", "").replace("\n", ""))
                return size
        return False
    else:
        return False

#Do Scroll to Down
def scroll_screen_down_to_up(serialNb):
    size = device_size(serialNb)
    time.sleep(0.5)
    os.popen("adb -s "+serialNb+" shell input touchscreen swipe " + str(size["x"]/2) + " " + str(size["y"]-100) + " "
             + str(size["x"]/2) + " " + str(size["y"]/2-100))

#Do Scroll to up
def scroll_screen_up_to_down(serialNb):
    size = device_size(serialNb)
    time.sleep(0.5)
    os.popen("adb -s "+serialNb+" shell input touchscreen swipe " + str(size["x"]/2) + " " + str(size["y"]/2-100) + " "
             + str(size["x"]/2) + " " + str(size["y"]-100))

#Do Scroll to Right
def scroll_screen_right_to_left(serialNb):
    size = device_size(serialNb)
    time.sleep(0.6)
    os.popen("adb -s "+serialNb+" shell input touchscreen swipe " + str(size["x"]-100) + " " + str(size["y"]/2) + " "
             + str(size["x"]/3) + " " + str(size["y"]/2))

#Do Scroll to Left
def scroll_screen_left_to_right(serialNb):
    size = device_size(serialNb)
    time.sleep(0.6)
    os.popen("adb -s "+serialNb+" shell input touchscreen swipe " + str(size["x"]/3) + " " + str(size["y"]/2) + " "
             + str(size["x"]-100) + " " + str(size["y"]/2))

#Press Home Button
def press_home(serialNb):
    os.popen("adb -s "+serialNb+" shell input keyevent 3")
    time.sleep(0.3)

#give a touch in local X Y
def tap(serialNb, x, y):
    os.popen("adb -s "+serialNb+" shell input tap " + str(x) + " " + str(y))


#give Devices List
def devices_list():
    values = os.popen("adb devices").read()
    values = values.split("\n")
    values.pop(0)
    devicesSerial = []
    if len(values) > 2:
        for element in values:
            if element != "":
                element = element.split("\t")
                if len(element) > 1:
                    element.pop(1)
                devicesSerial.append(element[0])
        return devicesSerial
    else:
        return devicesSerial


#Do Screenshot
def screenCap(serialNb):
    time.sleep(1)
    start_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    arq_name = "Screenshot_"+start_time_str+".png"
    os.popen("adb -s "+serialNb+" shell screencap -p /sdcard/screen.png").read()

    os.popen("adb -s " + serialNb + " pull /sdcard/screen.png " + "\"" + local_project +"\\"+arq_name+"\"").read()

#Get local for press
def get_bound_screen(attr, value):
    time.sleep(0.4)
    tree = ET.parse("C:\\Dev_Py\\Find_Element_in_screen\\dump.xml")
    root = tree.getroot()
    root.find("node").find("text")
    bounds=[]
    for x in root.iter('node'):
        if x.attrib[attr] == value:
            val = x.get('bounds')
            val = val.split("][")

            for subVals in val:
                new_val = subVals.replace(" ", "").replace("[","").replace("]","")
                new_val = new_val.split(",")
                bounds.append(new_val)
    if bounds:
        dict_bounds = {"v1": {}}
        dict_bounds["v1"]["x"] = int(bounds[0][0])
        dict_bounds["v1"]["y"] = int(bounds[0][1])
        dict_bounds["v2"] = {}
        dict_bounds["v2"]["x"] = int(bounds[1][0])
        dict_bounds["v2"]["y"] = int(bounds[1][1])
        dict_bounds["v3"] = {}
        dict_bounds["v3"]["x"] = ( int(bounds[1][0])+int(bounds[0][0]) )/2
        dict_bounds["v3"]["y"] = ( int(bounds[1][1])+int(bounds[0][1]) )/2
        return dict_bounds
    else:
        return {}

#Get XML with UI Hierarchy
def get_dump_screen(serialNb):
    os.popen("adb -s "+serialNb+" shell mkdir /sdcard/log_auto/").read()
    os.popen("adb -s "+serialNb+" shell uiautomator dump /sdcard/log_auto/dump.xml").read()
    time.sleep(0.3)
    print(os.popen("adb -s "+serialNb+" pull /sdcard/log_auto/dump.xml " + "\""+local_project+"\"").read())

#Auxiliar Function for Step by Step
def do_scroll(command,serial):
    if command == "SDU":
        scroll_screen_down_to_up(serial)
    elif command == "SUD":
        scroll_screen_up_to_down(serial)
    elif command == "SLR":
        scroll_screen_left_to_right(serial)
    elif command == "SRL":
        scroll_screen_right_to_left(serial)
    elif command == "HM":
        press_home(serial)

#Loop for shearch bounds of 
def loop_for_find(attr, name, serial, scroll_Command):
    get_dump_screen(serial)
    Gval = get_bound_screen(attr, name)
    while Gval == {}:
        do_scroll(scroll_Command.upper(), serial)
        get_dump_screen(serial)
        Gval = get_bound_screen(attr, name)

    return Gval


def main():
    print("Devices List: ")
    print(devices_list())
    print("\n")
    serial = input("Serial Number: ")

    get_dump_screen(serial)
    press_home(serial)




if __name__ == '__main__':
    main()




################ TESTE LG-K40 ################

    # ###### Abrindo menu de aplicações ######
    # Gval = loop_for_find("content-desc", "Aplicativos", serial, "HM")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # ###### Abrindo o app de configurações ######
    # Gval = loop_for_find("text", "Ajustes", serial, "SRL")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # ###### Abrindo a opção de Sistema ######
    # Gval = loop_for_find("text", "Sistema", serial, "SDU")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # ###### Abrindo a opção de informações do device ######
    # Gval = loop_for_find("text", "Sobre o telefone", serial, "SDU")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # screenCap(serial)



################ Samsung Espanhol ################
    # get_dump_screen(serial)
    # press_home(serial)
    #
    # scroll_screen_down_to_up(serial)
    # Gval = loop_for_find("text", "Ajustes", serial, "SRL")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # Gval = loop_for_find("text", "Acerca del teléfono", serial, "SDU")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # screenCap(serial)

################ Samsung English ################
    # scroll_screen_down_to_up(serial)
    # Gval = loop_for_find("text", "Settings", serial, "SRL")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # Gval = loop_for_find("text", "About phone", serial, "SDU")
    # tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])
    #
    # screenCap(serial)
