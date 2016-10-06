# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 14:15:25 2016

@author: Aman Priyadarshi
@handle: amaneureka
"""

import csv
import time
import subprocess
from random import randint
from datetime import datetime
from pyxhook import HookManager

DATABASE = "data.csv"
FUNNY_FILE = "funnymessages.txt"
words_dictionary = {}
index=0
ignore_keys = ["Control_R", "Control_L", "Shift_L", "Shift_R", "Caps_Lock", "Alt_L", "Alt_R"]
allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
current_buffer = ""

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

def StartService():
    with open(FUNNY_FILE, "r") as myfile:
        global funnymessages
        funnymessages = myfile.readlines()          
    for key, val in csv.reader(open(DATABASE)):
        words_dictionary[key] = val
    hm.start()

def StopService():
    w = csv.writer(open(DATABASE, "w+"))
    for key, val in words_dictionary.items():
        w.writerow([key, val])
    hm.cancel()

def Handle_Keyboard_Event(event):
    global current_buffer
    global index
    _key = event.Key
    if _key in ignore_keys:
        return
    if _key=="BackSpace" and current_buffer:
        current_buffer=current_buffer[:(index - 1)] + current_buffer[index:]
        index = index - 1
    elif _key=="Left" and index!=0:
        index = index - 1
    elif _key=="Right" and len(current_buffer)!=index:
        index = index + 1
    elif _key=="End" or _key=="KP_End":
        index=len(current_buffer)
    elif ( _key=="Delete" or _key=="KP_Delete" ) and len(current_buffer)!=index:
        current_buffer = current_buffer[:index] + current_buffer[( index + 1 ):]
    elif allowed_characters.find(_key) != -1:
        current_buffer = current_buffer[:index] + _key + current_buffer[index:]
        index = index + 1
    else:
        current_buffer = current_buffer.lower()
        if current_buffer in words_dictionary:
            sendmessage("{0} `{1}`?".format(funnymessages[randint(0,len(funnymessages)-1)], current_buffer))
        current_buffer = ""
        index=0

#Keyboard Hookup settings
hm = HookManager()
hm.HookKeyboard()
hm.KeyUp = Handle_Keyboard_Event

def WriteScreen(message):
    print "[{0}]:\t{1}".format(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), message)

def Handle_User():
    global current_buffer
    cmd = str(raw_input()).strip().lower()
    current_buffer = "" #empty up buffer
    if cmd == "close":
        StopService()
        return False
    else:
        args = cmd.split(' ')
        if args[0] == "add":
            new_word = args[1]
            if new_word in words_dictionary:
                WriteScreen("Already exist!")
            else:
                words_dictionary[new_word] = True
        elif args[0] == "enable":
            new_word = args[1]
            if new_word in words_dictionary:
                words_dictionary[new_word] = True
            else:
                WriteScreen("No such word exist!")
        elif args[0] == "disable":
            new_word = args[1]
            if new_word in words_dictionary:
                words_dictionary[new_word] = False
            else:
                WriteScreen("No such word exist!")
    return True

StartService()
while Handle_User():
    continue
WriteScreen("Closed!")
