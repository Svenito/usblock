from distutils.core import setup

setup(
    name='USBLock',
    version='0.1.2',
    author='Sven Steinbauer',
    author_email='sven@unlogic.co.uk',
    packages=['usblock'],
    scripts=['bin/usblock'],
    url='http://pypi.python.org/pypi/USBLock',
    license='LICENSE.txt',
    description='Lock and unlock your desktop using a USB stick as a key.',
    long_description=open('README.txt').read(),
    install_required=[
        "daemonize==2.1.1",
        "argparse==1.1.1",
    ],
)
