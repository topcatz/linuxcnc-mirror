#!/usr/bin/env python
#
# Copyright (C) 2013 Sebastian Kuzminsky
#
# This is a userspace, non-realtime component that interfaces the control
# box of a Scorbot ER-3 robot arm to the LinuxCNC HAL.
#

import hal
import serial
import time

def serial_write(data):
    print "serial write: [%s]" % data
    serial.write(data)
    #time.sleep(0.1)

def serial_read(num_bytes):
    data = serial.read(num_bytes)
    print "serial read: [%s]" % data
    return data


port = '/dev/ttyS0'
serial = serial.serial_for_url(
    port,
    9600,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_TWO,
    rtscts = False,
    xonxoff = False,
    timeout = 1
)

# disable "interrupts" from the Scorbot ER-3
serial_write('X')


h = hal.component("scorbot-er-3")
h.setprefix("scorbot-er-3")

# create pins, initialize robot
old_motor_pos_cmd = [None] * 8
old_motor_max_vel = [None] * 8
for joint in range(0, 8):
    h.newpin('joint%d.limit-sw' % joint, hal.HAL_BIT, hal.HAL_OUT)
    h.newpin('joint%d.motor-pos-cmd' % joint, hal.HAL_S32, hal.HAL_IN)
    h.newpin('joint%d.motor-max-vel' % joint, hal.HAL_S32, hal.HAL_IN)

    h['joint%d.motor-pos-cmd' % joint] = 0
    old_motor_pos_cmd[joint] = 0

    h['joint%d.motor-max-vel' % joint] = 1  # slowest speed
    old_motor_max_vel[joint] = 1

    serial_write('%dV%d' % (joint+1, h['joint%d.motor-max-vel' % joint]))

h.ready()


# main loop
while True:
    print "top of main loop"
    for joint in range(0, 8):
        if h['joint%d.motor-pos-cmd' % joint] != old_motor_pos_cmd[joint]:
            delta = h['joint%d.motor-pos-cmd' % joint] - old_motor_pos_cmd[joint]
            print "joint %d moved to %d (commanding move of %d)" % (joint, h['joint%d.motor-pos-cmd' % joint], delta)
            serial_write('%dm%d\n\r' % (joint+1, delta))
            old_motor_pos_cmd[joint] = h['joint%d.motor-pos-cmd' % joint]

        if h['joint%d.motor-max-vel' % joint] != old_motor_max_vel[joint]:
            print "joint %d new max vel %d" % (joint, h['joint%d.motor-max-vel' % joint])
            serial_write('%dv%d\n' % (joint+1, h['joint%d.motor-max-vel' % joint]))
            old_motor_max_vel[joint] = h['joint%d.motor-max-vel' % joint]

        serial_write('%dl' % (joint+1))

    data = serial_read(8)
    for joint in range(0, 8):
        l = data[joint:joint+1]
        if l != None:
            h['joint%d.limit-sw' % joint] = bool(int(l))

    time.sleep(0.1)

