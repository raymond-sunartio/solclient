from ctypes import *
import os

#
# The solclient library
#
if os.name == 'nt':
    _solClient = windll.LoadLibrary(os.path.dirname(os.path.realpath(__file__)) + '/solclient-7.5.0.7/bin/Win64/libsolclient.dll')
elif os.name == 'posix':
    _solClient = cdll.LoadLibrary(os.path.dirname(os.path.realpath(__file__)) + '/solclient-7.5.0.7/lib/libsolclient.so')
else:
    raise RuntimeError('OS \'{}\' not supported'.format(os.name))
