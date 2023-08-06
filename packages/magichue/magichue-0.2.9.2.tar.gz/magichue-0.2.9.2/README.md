# python-magichue

MagicHue (aka MagicHome) is a cheap smart led bulb that you can control hue/saturation/brightness and power over WiFi. They are available at Amazon or other online web shop.

I tested this library with RGB+WW+CW(v7), RGB(v8), RGB+WW(v8) bulbs.

# Example
Rainbow cross-fade.
```python
import time
import magichue


light = magichue.Light('192.168.0.20')  # change to your address

light.on = True
light.is_white = False
light.saturation = 1
light.brightness = 255

for hue in range(1000):
    light.hue = hue / 1000
    time.sleep(0.05)

```

# Installation
```
$ pip install magichue
```

# Usage
import magichue.
```python
import magichue

light = magichue.Light('192.168.0.20')
```

## Discover Bulbs on LAN
```python
from magichue import discover_bulbs

print(discover_bulbs())  # returns a list of bulb addresses
```

## Power State

### Getting Power Status
```python
print(light.on)  # => True if light is on else False
```

### Setting Light On/Off
```python
light.on = True
light.on = False
```

## Getting Color
This shows a tuple of current RGB:
```python
print(light.rgb)  # (255, 127, 63)
```
or access individually:
```python
print(light.r)  # 255
print(light.g)  # 127
print(light.b)  # 63
```

## White LEDs
If your bulbs support white LEDs, you can change the brightness (0-255) of white LEDs.

Enable the white led:
```python
light.is_white = True
```

**If white led is enabled, you can't change color of bulb!**  
You will need to disable it before you can change the color.

Disable the white led:
```python
light.is_white = False
```

### Warm White (ww)
```python
light.cw = 0
light.w = 255
```

### Cold White (cw)
```python
light.w = 0
light.cw = 255
```
 
## Setting Color

### Red, Green, Blue (RGB)
Assign all colors with a tuple of integers:
```python
light.rgb = (128, 0, 32)
```
or assign each color individually with an integer:
```python
light.r = 200
light.g = 0
light.b = 32
```

### Hue, Saturation, Brightness (HSB)
Hue and saturation are float values from 0 to 1.  
Brightness is a integer value from 0 to 255.
```python
light.hue = 0.3
light.saturation = 0.6
light.brightness = 255
```

### Note About Stripe Bulb
Stripe bulb doesn't seem to allow jumping to another color when you change color.

To disable the fading effect,
```python
light.rgb = (128, 0, 20)    # Fades to set color
light.allow_fading = False  # Set to True by default
light.rgb = (20, 0, 128)    # Jumps to set color
```

## Changing Modes
MagicHue bulb has built-in patterns.

Check current mode:
```python
print(light.mode)           # <Mode: NORMAL>
print(light.mode.name)      # 'NORMAL'
print(light.mode.value)     # 97
```

Set current mode:
```python
light.mode = magichue.RAINBOW_CROSSFADE
```

These are the built-in modes:
```text
RED_GRADUALLY
GREEN_GRADUALLY
BLUE_GRADUALLY
YELLOW_GRADUALLY
PURPLE_GRADUALLY
WHITE_GRADUALLY
BLUE_GREEN_GRADUALLY

RAINBOW_CROSSFADE
RED_GREEN_CROSSFADE
RED_BLUE_CROSSFADE
GREEN_BLUE_CROSSFADE

RAINBOW_STROBE
GREEN_STROBE
BLUE_STROBE
YELLOW_STROBE
BLUE_GREEN_STROBE
PURPLE_STROBE
WHITE_STROBE

RAINBOW_FLASH
NORMAL
```

### Changing The Speed of a Mode

The instance member `speed` is a float value from 0 to 1:
```python
light.speed = 0.5  # set speed to 50%
```

### Creating Custom Modes
You can create custom light flash patterns.

**Mode:**
```text
MODE_JUMP
MODE_GRADUALLY
MODE_STROBE
```

**Speed:** A float value 0 to 1.  
**Colors:** A list of RGB tuples. Max length of 17 tuples.

```python
from magichue import (
    CustomMode,
    MODE_JUMP,
)


# Creating Mode
mypattern1 = CustomMode(
    mode=MODE_JUMP,
    speed=0.5,
    colors=[
        (128, 0, 32),
        (100, 20, 0),
        (30, 30, 100),
        (0, 0, 50)
    ]
)

# Apply Mode
light.mode = mypattern1
```

---

Other features are in development.
