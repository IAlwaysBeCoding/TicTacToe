import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'TicTacToe'))


path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = ['funcy==1.6','rome==0.0.3']

setup(
    name='TicTacToe',
    version='0.0.2',
    description='TicTacToe',
    author='Erik Dominguez',
    author_email='erik.dominguez1003@gmail.com',
    packages=['tictactoe','tictactoe.hash','tictactoe.line'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite='test'
)

#package_data={'tictactoe': ['../VERSION']},
