=======
USBLock
=======

Copyright (C) 2013  Sven Steinbauer http://www.unlogic.co.uk

[![Build Status](https://travis-ci.org/Svenito/usblock.png?branch=master)](https://travis-ci.org/Svenito/usblock)

USBlock is a Python script that will lock and unlock your linux box using any 
old USB storage device as a key.

** NOTE **
V0.1 only works on Linux. OS X and Windows will have to wait a little.

Installation
============

Install with `pip install usblock` or run `sudo python ./setup.py install` 
from the directory you downloaded USBLock into.

See `requirements.txt` for a list of required Python modules.

Non Python dependencies
=======================

Linux
-----

You will need `dbus` and `python-dbus` as well as `hal`. These should all be 
available via your package manager. See below why `python-dbus` is listed here.

OS X
----

On OSX you will need to install `pyobjc` which takes two steps

  $> pip install pyobjc-core
  $> pip install pyobjc

Known Issues
============

* I've had some devices not mount on external USB ports (like on a Mac keyboard
or hub). DBus does not register the device insertion and so USBLock cannot
lock or unlock your machine. Try a different memory stick or USB port.

* On linux you need dbus installed. `pip install dbus-python` doesn't work, so 
you may have to install it via your system's package manager or from source.

See this Stackoverflow post for more information

http://stackoverflow.com/questions/13365697/install-python-dbus-in-virtualenv

Thanks for the patches
======================

Joel Semar, Natan L

