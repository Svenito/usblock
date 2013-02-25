from distutils.core import setup

setup(
    name='USBLock',
    version='0.1.7',
    author='Sven Steinbauer',
    author_email='sven@unlogic.co.uk',
    maintainer='Sven Steinbauer',
    packages=['usblock'],
    scripts=['bin/usblock'],
    url='https://github.com/Svenito/usblock',
    license='GPL3',
    description='Lock and unlock your desktop using a USB stick as a key.',
    long_description=open('README.md').read(),
    requires=[
        "daemonize (==2.1.1)",
        "argparse (==1.2.1)",
    ],
)
