#!/usr/bin/env python

import argparse
import RPi.GPIO as gpio
import time
from numpy import array


class Weigand:
    """ Class to read a raspberry Pi's GPIO lines #18 & #23
    as a Weigand interface from a ID card reader"""
    def __init__(self, debug=False):
        self.buff = []
        self.trx = []
        self.debug = debug
        self.bit_time = 1e-3 # seconds per bit

        gpio.setmode(gpio.BCM)
        self.D0 = 23
        self.D1 = 24
        gpio.setup(self.D0, gpio.IN) # D0
        gpio.setup(self.D1, gpio.IN) # D1
        gpio.add_event_detect(self.D0, gpio.FALLING)
        gpio.add_event_detect(self.D1, gpio.FALLING)
        gpio.add_event_callback(self.D0, self.d0_callback)
        gpio.add_event_callback(self.D1, self.d1_callback)


    def d0_callback(self, channel):
        """ Called when a zero bit is received"""
        self.remove_previous()
        self.buff.append(0)
        self.trx.append(time.time())

    def d1_callback(self, channel):
        """ Called when a one bit is received"""
        self.remove_previous()
        self.buff.append(1)
        self.trx.append(time.time())

    def remove_previous(self):
        if len(self.trx) > 0 and time.time() - self.trx[-1] > 5*self.bit_time:
            if self.debug:
                print "Timeout from reader."
            self.buff = []
            self.trx = []

    def get_id(self):
        id = 0L
        if len(self.trx) == 0 or time.time() - self.trx[-1] < 5*self.bit_time:
            return id
        if self.debug:
            trx = array(self.trx)
            dtrx = trx[1:]-trx[0:-1]
            print "buff:", len(self.buff), self.buff
            print "mean dt={:.3} ms".format(1000*dtrx.mean())
        d = array(self.buff)
        pe = sum(d[1:13]) & 0x1
        po = sum(d[13:-1]) & 0x1
        if pe == d[0] and po != d[-1]:
            id = d[0] + 0L
            for b in d[1:]:
                id <<= 1
                id |= b
        else:
            if self.debug:
                print "Parity error"
        self.buff = []
        self.trx = []
        return id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tests reading id card data.")
    parser.add_argument("-d", "--debug", dest='debug', action='count',
                        help="Increase debug output")
    args = parser.parse_args()

    stinkin = Weigand(debug=args.debug>0)

    try:
        while True:
            id = stinkin.get_id()
            if id != 0:
                print "id:{:x}".format(id)
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        gpio.cleanup()       # clean up GPIO on CTRL+C exit
