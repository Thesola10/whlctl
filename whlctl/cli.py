#!/usr/bin/env python3

'''WartHog Lights ConTroL - Manage state and brightness of lights on the Thrustmaster Warthog

Usage:
    %s <brightness> [--lights=<lights>]

    Brightness is expressed 0 and 5.

Options:
    -h --help                       Show this message and exit.
    --version                       Show version.
    -l <lights>, --lights <lights>  Comma-separated list of lights to enable
                                    0 is the backlight, 1~5 are status LEDs
                                    from top to bottom. [default: 0]
'''

import os
import sys
import whlctl
from docopt import docopt

def main():
    args = docopt(__doc__ %sys.argv[0], version = f"WartHog Lights ConTroL v{whlctl.__version__}")

    try:
        br = int(args["<brightness>"])
    except:
        print(f"Error: '{args['<brightness>']}' is not a valid number.")
        return 1

    lis = [int(li) for li in args["--lights"].split(",")]

    if br < 0 or br > 5:
        print("Error: brightness must be between 0 and 5.")
        return 1
    if not all(el >= 0 and el <= 5 for el in lis):
        print("Error: light index out of range (0~5)")
        return 1

    try:
        whlctl.find_throttle()
        whlctl.write_leds(0 in lis, [(m in lis) for m in range(1,6)], int(args["<brightness>"]))
    except FileNotFoundError:
        print("Error: could not find Warthog controller. Make sure it is connected.")
        return 1
    except:
        print("Error: failed to set lights. Try running as root.")
        return 1

if __name__ == '__main__':
    main()
