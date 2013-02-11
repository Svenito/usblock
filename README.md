USBLock
-------

Copyright (C) 2013  Sven Steinbauer

USBlock is a Python script that will lock and unlock your linux box using any old USB storage device as
a key.

Dependencies
============

* Daemonize (pip install daemonize)
* dbus libraries
* xlock installed to /usr/bin

** NOTE **
V0.1 only works on Linux. OS X and Windows will have to wait a little.

Usage
=====

Before you launch USBLock for the first time you need to add your device to the list of registered
devices.
Run 

  usblock -a

and follow the onscreen prompts. When done you can confirm that the device was added by listing the known
devices with

  usblock -l

When you are satisfied run it with

  usblock

You can optionally set a logging level with -d[1-5] which will log to ~/.config/usblock/usblock.log

Once running you will need to insert or re-insert your USB device you registered earlier. Once you remove
it xlock should launch and your computer will be locked (you can unlock it with your usual password too).
When you re-insert your device, xlock will be stopped and you computer unlocked. Some WMs may require you 
to move your mouse/press a key to unblank the screen.

Run

  usblock -h

to see all available options.

