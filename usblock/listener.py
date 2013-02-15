import os
import sys
import dbus
import signal
import gobject
import subprocess
from dbus.mainloop.glib import DBusGMainLoop

from .registrar import Device
from .logger import logger


def queryYesNo(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif cmp(default, "yes") == 0:
        prompt = " [Y/n] "
    elif cmp(default, "no") == 0:
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


class Listener(object):
    def __init__(self, registrar):
        self.registrar = registrar
        self._add_device = False
        self._device_udi = None
        self._adding_device = False

    def add_device(self):
        self._adding_device = True

    def list_devices(self):
        devices = self.registrar.devices
        if not devices:
            print "There are currently no registered devices."
            return

        print "These are the currently registered devices:"
        for num, device in enumerate(devices, start=1):
            print ("%d) Label: %s\n\t ID: %s" %
                  (num, device.label, device.uuid))

    def listen(self):
        '''Starts listening for inserted devices
        '''

    def _register_device(self, device):
        if device.uuid in [d.uuid for d in self.registrar.devices]:
            print ("Device %s with ID %s already registered." %
                  (device.label, device.uuid))
            if not queryYesNo("Would you like to add another device?"):
                return False
            else:
                print "Please insert another device."
            return True

        print ("You are about to add device %s with ID %s." %
              (device.label, device.uuid))

        if not queryYesNo("Is this OK?"):
            return False

        self.registrar.add_device(device)

        print "Device added successfully."
        return False


class LinuxListener(Listener):
    def __init__(self, registrar):
        super(LinuxListener, self).__init__(registrar)
        self._loop = None
        self._xlock_pid = 0

    def listen(self):
        '''Starts listening for inserted devices
        '''
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        hal_manager_obj = bus.get_object(
            "org.freedesktop.Hal",
            "/org/freedesktop/Hal/Manager")

        hal_manager = dbus.Interface(hal_manager_obj,
                                     "org.freedesktop.Hal.Manager")

        hal_manager.connect_to_signal("DeviceAdded", self._add_event)
        hal_manager.connect_to_signal("DeviceRemoved", self._remove_event)

        self._loop = gobject.MainLoop()
        self._loop.run()

    def _get_device(self, udi):
        '''Check if device is a volume and return it if it is
        '''
        bus = dbus.SystemBus()
        device_obj = bus.get_object("org.freedesktop.Hal", udi)
        device = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")
        if device.QueryCapability("volume"):
            uuid = device.GetProperty("block.storage_device").split('/')[-1]
            size = device.GetProperty("volume.size")
            label = device.GetProperty("volume.label")
            return Device(uuid, size, label)
        return None

    def _add_event(self, udi):
        '''Called when a device is added. Performs validation
        '''
        device = self._get_device(udi)
        if device is None:
            return
        logger.debug("Device insertion detected %s %s" %
                     (device.label, device.uuid))

        if self._adding_device is True:
            if not self._register_device(device):
                self._loop.quit()
                return False
            return True

        if self.registrar.verify_device(device):
            logger.debug("Device verified OK")
            self._device_udi = udi
            if self._xlock_pid != 0:
                logger.debug("Unlocking.")
                os.kill(self._xlock_pid, signal.SIGTERM)
                self._xlock_pid = 0

    def _remove_event(self, udi):
        '''Called when device removed. Starts xlock if not already
        running
        '''
        if self._xlock_pid != 0:
            return

        if udi == self._device_udi:
            logger.debug("Device matches. Locking screen.")
            xlock_proc = subprocess.Popen(['/usr/bin/xlock', '-mode', 'blank'])
            self._xlock_pid = xlock_proc.pid


class MacListener(Listener):
    def __init__(self):
        raise Exception("MacListener not yet implemented")


class WinListener(Listener):
    def __init__(self):
        raise Exception("WinListener not yet implemented")
