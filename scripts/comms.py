#!/usr/bin/env python
import datetime
import socket
import std_msgs
import rospy

def formatMessage(data):
    result = "$"
    result = result+data
    checksum = 0
    for i in data:
        checksum = checksum ^ ord(i)
    result = result+"*"
    result = result+hex(checksum)[-2:]  # checksum
    result = result + '\r\n'
    return result


'''
state: a dictionary containing:
latitude (float)
latNS: (char)
longitude (float)
longEW: (char)
mode: (int) 1: teleop 2:auto 3:killed
AUVstat (int): basically always 1 because we have no AUV
'''
TEAMID = 'DESIG'


def sendHeartbeatMessage(state):
    k = datetime.datetime.now()
    message = 'RXHRB,'
    message = message+str(k.day)[0:2]+str(k.month)[0:2]+str(k.year)[0:2]+","
    message = message+str(k.hour)[0:2] + \
                          str(k.minute)[0:2]+str(k.second)[0:2]+","
    message = message+str(state['latitude'])+","+state['latNS'] + \
    ","+str(state['longitude'])+","+state['longEW']+","
    message = message+TEAMID+","
    message = message+str(state['mode'])+","
    message = message+str(state['AUVstat'])
    message=formatMessage(message)
    global s
    try:
        s.send(message)
    except Exception:
        print("message "+message+" not sent!")


'''DockSymMessage
state: a dictionary containing:
active_entrance_gate (int)
active_exit_gate (int)
light_buoy_active (char) N or Y
lignt_pattern (string)
'''


def sendExitGatesMessage(state):
    k = datetime.datetime.now()
    message = 'RXGAT,'
    message = message+str(k.day)[0:2]+str(k.month)[0:2]+str(k.year)[0:2]+","
    message = message+str(k.hour)[0:2] + \
    str(k.minute)[0:2]+str(k.second)[0:2]+","
    message = message+TEAMID+","
    message = message+str(state['active_entrance_gate'])+","
    message = message+str(state["active_exit_gate"])+","
    message = message+state["light_buoy_active"]+","
    message = message+state["light_pattern"]
    message = formatMessage(message)
    global s
    try:
        s.send(message)
    except Exception:
        print("message "+message+" not sent!")


'''
state: a dictionary containing:
lignt_pattern (string)
'''


def sendScanCodeMessage(state):
    k = datetime.datetime.now()
    message = 'RXCOD,'
    message = message+str(k.day)[0:2]+str(k.month)[0:2]+str(k.year)[0:2]+","
    message = message+str(k.hour)[0:2] + \
    str(k.minute)[0:2]+str(k.second)[0:2]+","
    message = message+TEAMID+","
    message = message+state["light_pattern"]
    message = formatMessage(message)
    global s
    try:
        s.send(message)
    except Exception:
        print("message "+message+" not sent!")


'''
state: a dictionary containing:
color (char)
shape (string)
'''


def sendDockSymMessage(state):
    k = datetime.datetime.now()
    message = 'RXDOK,'
    message = message+str(k.day)[0:2]+str(k.month)[0:2]+str(k.year)[0:2]+","
    message = message+str(k.hour)[0:2] + \
    str(k.minute)[0:2]+str(k.second)[0:2]+","
    message = message+TEAMID+","
    message = message+state["color"]+","
    message = message+state["shape"]
    message = formatMessage(message)
    global s
    try:
        s.send(message)
    except Exception:
        print("message "+message+" not sent!")


'''
state: a dictionary containing:
color (char)
shape (string)
'''


def sendDeliverMessage(state):
    k = datetime.datetime.now()
    message = 'RXDEL,'
    message = message+str(k.day)[0:2]+str(k.month)[0:2]+str(k.year)[0:2]+","
    message = message+str(k.hour)[0:2] + \
    str(k.minute)[0:2]+str(k.second)[0:2]+","
    message = message+TEAMID+","
    message = message+state["color"]+","
    message = message+state["shape"]
    message = formatMessage(message)
    global s
    try:
        s.send(message)
    except Exception:
        print("message "+message+" not sent!")


BUFFER_SIZE = 1024
s = 0


def conman_init(TCP_IP,TCP_PORT,TID):
    global s
    global TEAMID
    TEAMID=TID
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

if __name__=='__main__':
    conman_init('0.0.0.0',9999)
    # sendDeliverMessage({'color':'A','shape':'TRIAN','longitude':2,'longEW':'E','mode':3,'AUVstat':1})