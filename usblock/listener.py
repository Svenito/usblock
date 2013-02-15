import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop


class Listener(object):
    def __init__(self):
        self._loop = None
        self._add_device = False

    def add_device(self):
        self._add_device = True

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

    def _get_device(self, udi):
        '''Check if device is a volume and return it if it is
        '''
        bus = dbus.SystemBus()
        device_obj = bus.get_object("org.freedesktop.Hal", udi)
        device = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")
        if device.QueryCapability("volume"):
            return device

    def _add_event(self, udi):
        '''Called when a device is added. Performs validation
        '''
        volume = self._get_device(udi)
        if volume is None:
            return

        # TODO Implement adddevice and kick of screen saver
        '''if self._add_device is True:
            self.addDevice(volume)
            return True

        if self.verifyDevice(volume) is True:
            logger.debug("Device accepted")
            self.device_udi = udi
            if self.xlock_pid != 0:
                os.kill(self.xlock_pid, signal.SIGTERM)
                self.xlock_pid = 0'''

    def _remove_event(self, udi):
        '''Called when a device is removed.
        '''
        pass


class LinuxListener(Listener):
    def __init__(self):
        super.__init__(LinuxListener, self)


class MacListener(Listener):
    def __init__(self):
        raise Exception("MacListener not yet implemented")


class WinListener(Listener):
    def __init__(self):
        raise Exception("WinListener not yet implemented")
