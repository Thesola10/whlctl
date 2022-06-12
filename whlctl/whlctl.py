#!/usr/bin/env python3
# WartHog Light ConTroL (c) Karim Vergnes <me@thesola.io>
# Toggle the backlight and five LEDs on the Thrustmaster Warthog Throttle.
# Based on mfranz's work: https://web.archive.org/web/20121029171225/http://members.aon.at/mfranz/warthog.html

from glob import glob

import os
import functools

LED_BACKLIGHT = 0b00001000

LED_1 = 0b00000100  # Top
LED_2 = 0b00000010
LED_3 = 0b00010000
LED_4 = 0b00000001
LED_5 = 0b01000000  # Bottom

VENDOR  = '044f\n'
PRODUCT = '0404\n'

@functools.lru_cache
def find_throttle() -> str:
    for file in glob('/sys/class/input/js*/device'):
      with open(f"{file}/id/vendor", 'r') as fd:
        if fd.read() == VENDOR:
          with open(f"{file}/id/product", 'r') as fd2:
            if fd2.read() == PRODUCT:
              return f"/dev/{os.listdir(f'{file}/device/hidraw/')[0]}"
    raise FileNotFoundError("Did not find Warthog Throttle in USB devices")

def write_leds(backlight: bool, leds: list[bool], brightness: int):
    assert(brightness <= 0x5 and brightness >= 0x0)
    bmask = (LED_BACKLIGHT if backlight else 0) \
            | (LED_1       if leds[0] else 0) \
            | (LED_2       if leds[1] else 0) \
            | (LED_3       if leds[2] else 0) \
            | (LED_4       if leds[3] else 0) \
            | (LED_5       if leds[4] else 0)
    with open(find_throttle(), 'wb') as dev:
        dev.write(bytes([0x01, 0x06, bmask, brightness]))

if __name__ == '__main__':
    pass
