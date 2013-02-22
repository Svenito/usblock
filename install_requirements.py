from __future__ import unicode_literals, print_function

import sys
import os


def get_requirements_file_path():
    """Returns the absolute path to the correct requirements file."""
    directory = os.path.dirname(__file__)

    requirements_file = 'requirements.txt'

    return os.path.join(directory, requirements_file)


def main():
    requirements_file = get_requirements_file_path()
    print('Installing requirements from %s' % requirements_file)
    os.system('pip install -r %s --use-mirrors' % requirements_file)


if __name__ == '__main__':
    main()
