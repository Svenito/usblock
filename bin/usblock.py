#!/usr/bin/env python

"""
    USBLock: manage xlock via usbkeys
    Copyright (C) 2013  Sven Steinbauer <sven@unlogic.co.uk>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    See accompanying file GPL3.txt
"""


import os
import sys
import signal
from daemonize import Daemonize
from argparse import ArgumentParser

from usblock import listener
from usblock import registrar
from usblock import logger

# TODO Set CONFDIR based on OS
CONFDIR = os.path.expanduser(os.path.join('~', '.config', 'usblock'))
PIDFILE = os.path.join(CONFDIR, 'lock.pid')
LOGFILE = os.path.join(CONFDIR, 'usblock.log')
CONFFILE = os.path.join(CONFDIR, 'conf')
__version__ = "0.1"


def get_running_instances():
    '''Get the pid from the pidfile and return it.
    Return 0 if no pidfile found
    '''
    try:
        with open(PIDFILE) as pidfile:
            usblock_pid = pidfile.readline()
            return usblock_pid
    except IOError:
        return 0


def run_listener(options):
    '''Setup registrar and listener and run as needed
    by options
    '''
    logger.setup_logging(options.debug_level)

    reg = registrar.Registrar(CONFFILE)
    reg.load_config()

    listen = listener.LinuxListener(reg)

    if options.remove_device:
        listen.remove_device()
        return

    if options.list_devices:
        listen.list_devices()
        return

    if options.add_device:
        listen.add_device()
        listen.listen()
        return

    if options.foreground:
        listen.listen()
    else:
        if get_running_instances() > 0:
            print "USBlock is already running"
            sys.exit(0)

        to_file = LOGFILE
        file_handle = logger.setup_logging(options.debug_level, to_file)

        daemon = Daemonize(app="usblock",
                           pid=PIDFILE,
                           action=listen.listen,
                           keep_fds=[file_handle.stream.fileno()])
        daemon.start()


if __name__ == '__main__':
    usage = """%s V%s [options]\n
            Lock and unlock your desktop using a USB stick as a key
            """ % (os.path.basename(sys.argv[0]), __version__)

    parser = ArgumentParser(usage=usage)
    parser.add_argument("-a", "--add-device",
                        action="store_true",
                        dest="add_device",
                        help="Add the next aded device")
    parser.add_argument("-f", "--foreground",
                        action="store_true",
                        dest="foreground",
                        help="Run in foreground")
    parser.add_argument("-l", "--list",
                        action="store_true",
                        dest="list_devices",
                        help="List registered devices and exit")
    parser.add_argument("-r", "--remove",
                        action="store_true",
                        dest="remove_device",
                        help="Remove a registered device")
    parser.add_argument("--stop",
                        action="store_true",
                        dest="stop_lock",
                        help="Stop a running daemon")
    parser.add_argument("--pid",
                        action="store_true",
                        dest="pid",
                        help="Show pid of running daemon")
    parser.add_argument("-d", "--debug",
                        action="store",
                        dest="debug_level",
                        default=0,
                        help="Set debug level")
    # TODO expand on the help a little

    args = parser.parse_args()
    if args.stop_lock or args.pid:
        pid = get_running_instances()
        if pid > 0:
            if args.pid:
                print "There is an instance of USBlock running with PID: ", pid
            if args.stop_lock:
                os.kill(int(pid), signal.SIGTERM)
            sys.exit(0)
        else:
            print "No running USBlock processes."
            sys.exit(0)

    run_listener(args)
