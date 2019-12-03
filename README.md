# pixelpi
This project has been forked from [marian42](https://github.com/marian42/pixelpi), this readme has also been extensively copied from there.

Games and Animations on 16x16 LEDs

![16x16 LED matrix](https://github.com/Oftatkofta/pixelpi/blob/master/readme/my_gameFrame.jpg)

This is a collection of python scripts that run animations and games on a 16x16 matrix of WS2812B LEDs (aka Neopixel).
The project is inspired by and compatible to Jeremy Williams' [Game Frame](http://ledseq.com).

The code has also been ported to Python 3.


## Hardware

Since I'm cheap I only buy what I absolutely have to. One of those things was laser cut cardboard inserts, because it is impossible to get right by hand (I tried...a lot). My original plan was to manually cut the PVC board for this, but it has to be completely straight, otherwise it just looks bad. The grid design .pdf file is available in the /readme directory of the repo.

![Laser cut grid](https://github.com/Oftatkofta/pixelpi/blob/master/readme/laser_cut_grid.jpg)

- 300 LEDs, WS2812B, 60/m, 330 NOK (37 €)
- Frame found in dumpster and cut to size -free
- 30x30 cm 3 mm MDF board found in dumpster -free
- Raspberry Pi2 Model B, 299 NOK (33€)
- Power Supply 5V 25A 125W, 171 NOK (19 €), a modified ATX-PSU will also do.
- Wifi-dongle, 100 NOK (11 €)
- Laser cut 1.4 mm white cardboard for the grid from RazorLAB, 412 NOK (46 €)
- Level shifter, 11 NOK (1 €)
- White PVC board for diffuser/screen,  129 NOK (14 €)
- eBoy animation pack from www.ledseq.com, 86 NOK (10 $)
- Wire, solder, hot glue, capacitors, etc
- PiJuice HAT 54.98 GBP 

UPDATE 2019

I have made a nice wooden frame from oak.

![Nice wooden frame](https://github.com/Oftatkofta/pixelpi/blob/python3/readme/wood_frame.jpg)


### LED strips

I recommend you use [this tutorial](https://learn.adafruit.com/neopixels-on-raspberry-pi/overview) to set up the LED hardware.
Make sure you install [rpi_ws281x](https://github.com/jgarff/rpi_ws281x.git) as explained in the tutorial.

Then copy this repository somewhere to the SD card, copy your animations to the sd card and run a script.

You can edit the `Screen.py` file to default to the LED strip settings you used in the neopixel tutorial (especially pin and brightness).

### LED layout

The `Screen.py` script expects your LED strip to be laid out like this:

```
<- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <-
-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->
<- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <-
-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->
...
```

Although there is now the possibility to hard code a different rotation in screen.py.



![LED layout](https://github.com/Oftatkofta/pixelpi/blob/master/readme/top_LEDs.jpg)

If you have a different setup, you can edit the `Screen.py` file to translate the 16x16 matrix on your LED strip.

Power is running through copper pins tying two strips together on the front and out on to the back side.

![GameFrame back](https://github.com/Oftatkofta/pixelpi/blob/master/readme/back_power_and_data.jpg)

## Software

To set up the software, clone this repository on your Raspberry Pi. Rename the file `config.ini.example` to `config.ini`.
Make sure, the neopixel, pillow(PIL), noise (for fire module), and Pygame libraries are installed.
This project uses Python 3.

### Animations
Place your animations in a folder called `animations` in the repository. For each animation, a file `/animations/animation_name/0.bmp` should exist.

Here are the [Eboy animations](http://ledseq.com/product/game-frame-sd-files/) and a [forum for fan-made Game Frame animations](http://ledseq.com/forums/forum/game-frame/game-frame-art/).

Take a look at the files `example_animation.py` and `example_cycle.py` to display single or multiple animations.

### Gamepad
The current gamepad code probably only works with my logitech gamepad. I'm planning to make more generic gamepad support. Until then, you need to edit the `gamepad.py` file and make it work with your gamepad.

### Menu
The file `menu.py` provides a visual menu to select from the available modules such as animations and games. For me, this is the default way of using the LED screen. You need a gamepad for this to work.

### Virtual hardware
You can test all software without a Raspberry Pi, Gamepad or LED matrix. To do so, set up the software as described above and edit the `config.ini` file. Set `virtualhardware` to true. Try to run `menu.py`, a window with a simulated screen should open. Note that this requires `pygame` which you may need to install.

### Updates to original pixelpi

- text scrolling module
- PNG images
- PIL/Pillow backend for image handling
- automatic image resizing
- a new funky 24-hour clock module with a binary representation (pictured above)
- horizontal animation images
- [Langton's Ant](https://en.wikipedia.org/wiki/Langton%27s_ant) Module
- a 3x7 monospaced font for text and numbers
- FPS test

###TODO's:
- automatic animation loading from sprite sheets
- animated .GIFs
- "panning" large images
- "next bus timer"
- Conway's game of life
- web interface
- something cool you suggest?

