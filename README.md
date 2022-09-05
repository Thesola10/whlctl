# Warthog Lights Control

This Python module and command line tool control the lights on Thrustmaster's Warthog HOTAS throttle box.

Largely based on the [reverse-engineering] work done by mfranz

## How to use

Once installed, this tool provides a Python module and a command-line tool, both named `whlctl`.

### Command line tool

```sh
whlctl 0        # Turn off backlight
whlctl 5        # Turn backlight up to max brightness
whlctl 3 -l 1,5 # Turn lights 1 and 5 up to brightness 3/5
whlctl 1 -l 0,5 # Turn backlight and light 5 up to brightness 1/5
```

Omitting the `-l` flag will default to adjusting the backlight, and turn off all other lights.

### Python API

```python
import whlctl

whlctl.find_throttle()  # -> "/dev/hidrawN" or FileNotFoundError
whlctl.write_leds(backlight=True, leds=[True,True,True,True,True], brightness=5)
                        # -> None or FileNotFoundError (see find_throttle)
```

#### `find_throttle()`
Takes no argument and returns the HID node for the Thrustmaster Warthog throttle (`044f:0404`), or raises a `FileNotFoundError` if the device isn't found.  
This function is cached.

#### `write_leds(backlight: bool, leds: list[bool], brightness: int)`
The `leds` list must contain 5 booleans which designate, in order, the five circular lights from top to bottom. `True` means the light is to be powered on at the given brightness, `False` means it should be powered off.  
`brightness` is expressed between 0 and 5.  
Returns nothing, implicitly calls `find_throttle()` and thus can fail with `FileNotFoundError` as above. It can also hit a permission error if the current user has no write permission to the device node.

[reverse-engineering]: https://web.archive.org/web/20121029171225/http://members.aon.at/mfranz/warthog.html
