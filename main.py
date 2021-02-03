import os
import time
import pathlib
import xml.etree.ElementTree as ET
from datetime import datetime
local_project = str(pathlib.Path(__file__).parent.parent)


##############################
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

def scroll_screen_down_to_up(serialNb):
    size = device_size(serialNb)
    time.sleep(0.5)
    os.popen("adb shell input touchscreen swipe " + str(size["x"]/2) + " " + str(size["y"]-100) + " "
             + str(size["x"]/2) + " " + str(size["y"]/2-100))

def scroll_screen_up_to_down(serialNb):
    size = device_size(serialNb)
    time.sleep(0.5)
    os.popen("adb shell input touchscreen swipe " + str(size["x"]/2) + " " + str(size["y"]/2-100) + " "
             + str(size["x"]/2) + " " + str(size["y"]-100))

def scroll_screen_right_to_left(serialNb):
    size = device_size(serialNb)
    time.sleep(0.6)
    os.popen("adb -s "+serialNb+" shell input touchscreen swipe " + str(size["x"]-100) + " " + str(size["y"]/2) + " "
             + str(size["x"]/3) + " " + str(size["y"]/2))

def scroll_screen_left_to_right(serialNb):
    size = device_size(serialNb)
    time.sleep(0.6)
    os.popen("adb -s "+serialNb+" shell input touchscreen swipe " + str(size["x"]/3) + " " + str(size["y"]/2) + " "
             + str(size["x"]-100) + " " + str(size["y"]/2))

def press_home(serialNb):
    os.popen("adb -s "+serialNb+" shell input keyevent 3")
    time.sleep(0.3)


def tap(serialNb, x, y):
    os.popen("adb -s "+serialNb+" shell input tap " + str(x) + " " + str(y))

def devices_list():
    os.popen("adb shell screencap -p /sdcard/screen.png").read()



def screenCap(serialNb):
    time.sleep(0.4)
    start_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.popen("adb shell screencap -p /sdcard/screen.png").read()

    os.popen("adb -s " + serialNb + " pull /sdcard/screen.png " + "\"" + local_project +
             "\\Screenshot_"+start_time_str+".png"+"\"").read()

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

def get_dump_screen(serialNb):
    os.popen("adb -s "+serialNb+" shell mkdir /sdcard/log_auto/").read()
    os.popen("adb -s "+serialNb+" shell uiautomator dump /sdcard/log_auto/dump.xml").read()
    time.sleep(0.3)
    print(os.popen("adb -s "+serialNb+" pull /sdcard/log_auto/dump.xml " + "\""+local_project+"\"").read())


##############################


def main():
    serial = input("Serial Number: ")

    get_dump_screen(serial)
    press_home(serial)


    ###### Abrindo menu de aplicações ######
    Gval = get_bound_screen("content-desc", "Aplicativos")
    while Gval == {}:
        press_home(serial)
        get_dump_screen(serial)
        Gval = get_bound_screen("content-desc", "Aplicativos")

    tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])

    ###### Abrindo o app de configurações ######
    get_dump_screen(serial)
    Gval = get_bound_screen("text", "Ajustes")
    while Gval  == {}:
        scroll_screen_right_to_left(serial)
        get_dump_screen(serial)
        Gval = get_bound_screen("text", "Ajustes")

    tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])

    ###### Abrindo a opção de Sistema ######
    Gval = get_bound_screen("text", "Sistema")
    while Gval == {}:
        scroll_screen_down_to_up(serial)
        get_dump_screen(serial)
        Gval = get_bound_screen("text", "Sistema")

    tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])

    ###### Abrindo a opção de informações do device ######
    Gval = get_bound_screen("text", "Sobre o telefone")
    while Gval == {}:
        scroll_screen_down_to_up(serial)
        get_dump_screen(serial)
        Gval = get_bound_screen("text", "Sobre o telefone")

    tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])

    screenCap(serial)

    get_dump_screen(serial)
    Gval = get_bound_screen("text", "Spotify")
    while Gval  == {}:
        get_dump_screen(serial)
        Gval = get_bound_screen("text", "Spotify")

    tap(serial, Gval["v3"]["x"], Gval["v3"]["y"])


main()


#LMX430UOAUR4LRWWTG