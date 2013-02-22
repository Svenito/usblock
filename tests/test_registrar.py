import os
import nose
from nose.tools import *

from usblock import registrar

CONFIG_FILE = "./test.conf"
CONFIG_CONTENTS = ("[device1]\n"
                   "devicelabel = TEST\n"
                   "devicesize = 249500160\n"
                   "deviceid = storage")


def setup_func():
    with open(CONFIG_FILE, 'w') as f:
        f.write(CONFIG_CONTENTS)


def teardown_func():
    os.unlink(CONFIG_FILE)


@with_setup(setup_func, teardown_func)
def test_load_config():
    r = registrar.Registrar(CONFIG_FILE)
    r.load_config()

    eq_(len(r.devices), 1)
    eq_(r.devices[0].uuid, "storage")
    eq_(r.devices[0].size, "249500160")
    eq_(r.devices[0].label, "TEST")


def test_write_config():
    r = registrar.Registrar(CONFIG_FILE)
    d = registrar.Device("new", "12345", "label")

    # Writes automatically
    r.add_device(d)

    new_r = registrar.Registrar(CONFIG_FILE)
    new_r.load_config()

    eq_(len(r.devices), 1)
    eq_(r.devices[0].uuid, "new")
    eq_(r.devices[0].size, "12345")
    eq_(r.devices[0].label, "label")
    os.unlink(CONFIG_FILE)


@with_setup(setup_func, teardown_func)
def test_validate():
    r = registrar.Registrar(CONFIG_FILE)
    r_blank = registrar.Registrar(CONFIG_FILE)
    r.load_config()

    d = registrar.Device("storage", "249500160", "TEST")
    d_fail = registrar.Device("stoadrage", "2495500160", "3TEST")

    assert(r.verify_device(d))
    assert(not r.verify_device(d_fail))
    assert(not r_blank.verify_device(d))

