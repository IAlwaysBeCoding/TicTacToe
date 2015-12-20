import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'TicTacToe'))


path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = ['requests==2.7.0', 'lxml==3.4.4']

setup(
    name='TicTacToe',
    version='0.0.1',
    description='TicTacToe',
    author='Erik Dominguez',
    author_email='erik.dominguez1003@gmail.com',
    packages=['tictactoe','tictactoe.hash'],
    include_package_data=True,
    install_requires=install_requires,
    test_suite='test'
)

#package_data={'tictactoe': ['../VERSION']},