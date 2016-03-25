#!/usr/bin/env python
""" Module to read a raspberry Pi's GPIO lines #18 & #23
 as a Weigand interface from a ID card reader"""

import argparse
import RPi.GPIO as gpio
import time
from numpy import array

gpio.setmode(gpio.BCM)

D0 = 23
D1 = 24
gpio.setup(D0, gpio.IN) # D0
gpio.setup(D1, gpio.IN) # D1

buff=[]
trx=[]

def d0_callback(chan):
    """ Called when a zero bit is received"""
    global buff,trx
    buff.append(0)
    trx.append(time.time())

def d1_callback(chan):
    """ Called when a one bit is received"""
    global buff,trx
    buff.append(1)
    trx.append(time.time())

gpio.add_event_detect(D0, gpio.FALLING)
gpio.add_event_detect(D1, gpio.FALLING)
gpio.add_event_callback(D0, d0_callback)
gpio.add_event_callback(D1, d1_callback)

def get_id(num_bits=40, debug=False):
    """ Returns (facory_code,card_id) decoded from a card reader. The older HID
    readers seem to have 40 bit cards while the newer ones seem to be 24."""
    global buff,trx
    buff=[]
    trx=[]
    while len(buff) < num_bits:
        time.sleep(0.02)
        if len(trx) > 0:
            dt = time.time() - trx[-1]
            if dt > 0.05:
                if (debug):
                    print "timeout"
                break
    if (debug):
        trx = array(trx)
        dtrx = trx[1:]-trx[0:-1]
        print "buff:", len(buff), buff
        print "mean dt={:.3} ms".format(1000*dtrx.mean())

    fc=0
    id=0
    if len(buff) == num_bits:
        d=array(buff)
        pe=sum(d[1:13]) & 0x1
        po=sum(d[13:-1]) & 0x1
        if pe == d[0] and po != d[-1]:
            d_fc = d[1:9]
            d_id = d[9:-2]

            fc=d_fc[0];
            for b in d_fc[1:]:
                fc <<= 1
                fc |= b
            id=d_id[0]
            for b in d_id[1:]:
                id <<= 1
                id |= b
        else:
            if (debug):
                print "Parity error"

    return (fc, id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tests reading id card data.")
    parser.add_argument("-d", "--debug", dest='debug', action='count',
                        help="Increase debug output")
    parser.add_argument("-b", "--bits", dest='bits', default=40,
                         help="Number of bits expected in a card")
    args = parser.parse_args()
    
    try:
        while True:
            (fc,id) = get_id(num_bits=args.bits, debug=args.debug>0)
            print "fc:{:x} id:{:x}".format(fc, id)
    except KeyboardInterrupt:
        gpio.cleanup()       # clean up GPIO on CTRL+C exit
