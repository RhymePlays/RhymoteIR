"""
RhymeConnect is a network easy connect library for ESP8266 projects using Micropython.
This library aims to make connecting ESP8266 easier.

You can either use it in a AP mode, or you could change the Router-Login-Credentials to make it connect to a router.
If the ESP cannot connect to a router, it'll host it's own network. You can change the creds for the self hosted network.
It'll always prefer connecting to a Router than hosting it's own.

Starting the module:
    >>> import rhymeConnect
    >>> rhymeConnect.start()

Setting Router Credentials:
    >>> import rhymeConnect
    >>> rhymeConnect.setRouter(ssid, password) #both as string

Setting Self-Host Credentials:
    >>> import rhymeConnect
    >>> rhymeConnect.setHostAP(ssid, password) #both as string
"""
__all__ = ["start", "setRouter", "setHostAP"]
__version__ = "1.0.0"
__author__ = "Isfar Tausif"


# Imports
import os, json, network


# Variables
saveDataFileName = "rhymeConnectSaveData.json"
rhymeConnectSaveData = {}
defaultParms = {
    "self_ssid": "RhymeConnect",
    "self_password": "RhymeConn1"
}

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)


# Functions
def saveDataExists():
    if (saveDataFileName in os.listdir()):
        return True
    else:
        return False
def writeSaveData():
    try:
        with open(saveDataFileName, "w") as f:
            f.write(json.dumps(rhymeConnectSaveData))
    except: pass
def readSaveData():
    global rhymeConnectSaveData
    try:
        with open(saveDataFileName, "r") as f:
            rhymeConnectSaveData = json.loads(f.read())
    except:
        rhymeConnectSaveData = {}


def hostAP():
    global rhymeConnectSaveData
    if saveDataExists():
        readSaveData()
        if ("self_ssid" in rhymeConnectSaveData) and ("self_password" in rhymeConnectSaveData):
            if sta_if.active()==True: sta_if.active(False)
            if ap_if.active()==False: ap_if.active(True)

            ap_if.config(essid=rhymeConnectSaveData["self_ssid"], password=rhymeConnectSaveData["self_password"], channel=11)
            #End of Code.
        else:
            rhymeConnectSaveData = {"self_ssid": defaultParms["self_ssid"], "self_password": defaultParms["self_password"]}
            writeSaveData()
            start()
    else:
        rhymeConnectSaveData = {"self_ssid": defaultParms["self_ssid"], "self_password": defaultParms["self_password"]}
        writeSaveData()
        start()


# Operations
def start():
    if saveDataExists():
        readSaveData()
        if ("router_ssid" in rhymeConnectSaveData) and ("router_password" in rhymeConnectSaveData):

            if ap_if.active()==True: ap_if.active(False)
            if sta_if.active()==False: sta_if.active(True)
            sta_if.connect(rhymeConnectSaveData["router_ssid"], rhymeConnectSaveData["router_password"])
            
            """PAUSE FOR A BIT IF ASYNC"""
            if sta_if.isconnected():
                pass
                #End of Code.
            else:
                hostAP()
        else:
            hostAP()
    else:
        hostAP()

def setRouter(ssid, password):
    rhymeConnectSaveData["router_ssid"] = str(ssid)
    rhymeConnectSaveData["router_password"] = str(password)
    writeSaveData()
    start()

def setHostAP(ssid, password):
    rhymeConnectSaveData["self_ssid"] = str(ssid)
    rhymeConnectSaveData["self_password"] = str(password)
    writeSaveData()
    start()