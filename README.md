# java9k
Java Node 9000 - Big Brother is watching

This is a project to provide automated logging of coffee at the ARL:UT
java node

General idea: Raspberry pi reading a badge readers, logs when a badge
is swiped as a cup of coffee consumed


## badge readers
HID6005BGB00, HID ProxPro reader. Only reads the 'new' ARL badges

GE 940-W reader, see 460157001K_94x-97x_Readers.pdf for data sheet

Looks like the old reader interferes with the new reader when they are operated close to each other.

The new reader/badges output a 26 bit id while the old one outputs a 42 bit one.


## weigand interface to badge readers
power; POE converter: TP-Link TL-POE10R ->

Pinout of RPi adapter card:

RPI	Adapter
-	gnd to card reader
-	+12 output to card reader
+5	-
+5	+5 input from PoE adapter
gnd	gnu from PoE adapter
Tx	-
Rx	-
#18	PWM output to BRB LED
gnd	gnd (for BRB LED)
#23	D0 from card reader
#24	D1 from card reader
gnu	gnd to BRB switch
#25	to BRB switch
CE0	-
CE1	-

## 2/3/16
Dusting this project off after 18 months of so…

To make the device work better when a simple badge swipe doesn’t work,
 I purchased a 7” touchscreen that mates with the RPi’s display connector.

Looks like the recommended API/frameworks is Kivy:
http://kivypie.mitako.eu/kivy-gallery.html

Looks like I can develop the UI app on any OS with Kivy.


## 2/4/16
Details about the 7" touchscreen
https://www.raspberrypi.org/blog/the-eagerly-awaited-raspberry-pi-display/
http://forums.pimoroni.com/t/official-7-raspberry-pi-touch-screen-faq/959

overall dims: 194mm x 110mm x 20mm (including standoffs) (7.63
adding in rpi: ...x 40mm

back wide mounting holes: 126mm x 66mm
LCD metal housing on back: 100.5mm x 161mm x 5mm (not including raised screw mounts)
display front dims: 193mm x 110mm

800x480 ~ 155 x 86 mm = .19 x .175 mm dot pitch

a 13.3 mm square should be 70 px wide x 76 px tall

Badge reader: 121mm x 73mm x 23mm

## 2/10/16
Created a github repo for this beast as I am starting to write code...
