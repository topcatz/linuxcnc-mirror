import linuxcnc

import hal
import glib
import time

import inspect

v = 0
s = linuxcnc.command()

def on_button1_pressed(gtkobj, date=None):
    global s
    print dir(s)
    gtkobj.set_label("hello")


