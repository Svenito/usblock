import os

import sys
import dbus
import signal
import gobject
from dbus.mainloop.glib import DBusGMainLoop

from .registrar import Device


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
        self._device_uid = None

    def add_device(self):
        self._add_device = True

    def listen(self):
        '''Starts listening for inserted devices
        '''

    def _add_device(self, device):
        if device.uuid in [d.uuid for d in self.registrar.devices]:
            print ("Device %d with ID %s already registered." %
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
        print "Device added"
        device = self._get_device(udi)
        if device is None:
            return

        if self._add_device is True:
            if not self._add_device(device):
                self._loop.quit()
                return False
            return True

        if self.registrar.verify_device(device):
            self._device_udi = udi
            if self._xlock_pid != 0:
                os.kill(self._xlock_pid, signal.SIGTERM)
                self._xlock_pid = 0

    def _remove_event(self, udi):
        print "removed"

class MacListener(Listener):
    def __init__(self):
        raise Exception("MacListener not yet implemented")


class WinListener(Listener):
    def __init__(self):
        raise Exception("WinListener not yet implemented")
