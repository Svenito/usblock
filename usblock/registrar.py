import errno
import os
import ConfigParser
from collections import namedtuple

from .logger import logger

Device = namedtuple("Device", ["uuid", "size", "label"])


class Registrar(object):
    '''Handles reading and writing device details to the
    config file'''
    def __init__(self, path=""):
        self.devices = []

        self._path = path
        self._config = None

    def load_config(self):
        '''Read the config file and get all listed
        devices.
        '''
        self._create_conf_dir()
        self._config = ConfigParser.ConfigParser()
        opened_files = self._config.read(self._path)
        if not len(opened_files):
            try:
                file_handle = open(self._path, "w+")
                file_handle.close()
                os.chmod(self._path, 0600)
            except IOError:
                raise Exception("Failed to open %s for writing." %
                                self._path)
        else:
            self._set_values()

    def write_config(self):
        '''Write all current devices stored in memory to config file
        '''
        # Start with a clean config and just dump everything
        logger.debug("Write out config file")
        del self._config
        self._config = ConfigParser.ConfigParser()

        for num, device in enumerate(self.devices, start=1):
            section_name = "device%d" % num
            self._config.add_section(section_name)
            self._config.set(section_name, "deviceid", device.uuid)
            self._config.set(section_name, "devicesize", device.size)
            self._config.set(section_name, "devicelabel", device.label)

        with open(self._path, "w") as config_fh:
            self._config.write(config_fh)

    def add_device(self, device):
        '''Adds a device to the list and writes the new config
        '''
        self.devices.append(device)
        self.write_config()

    def verify_device(self, device):
        '''Checks supplied device against known devices. Returns
        True if a match is found, False otherwise
        '''
        if device.uuid not in [d.uuid for d in self.devices]:
            return False

        if str(device.size) not in [d.size for d in self.devices]:
            return False

        return True

    def _create_conf_dir(self):
        '''Create a config dir. Raise Exception if unable to
        create it
        '''
        try:
            os.makedirs(os.path.dirname(self._path))
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise Exception("Unable to create config dir %s %s" %
                                (self._path, os.strerror(err.errno)))

    def _set_values(self):
        '''Set up devices for current config
        '''
        if not len(self._config.sections()):
            return

        for section in self._config.sections():
            device = Device(self._config.get(section, "deviceid"),
                            self._config.get(section, "devicesize"),
                            self._config.get(section, "devicelabel"))
            self.devices.append(device)
