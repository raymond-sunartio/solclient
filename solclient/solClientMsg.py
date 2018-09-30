from ctypes import *
import logging

from solclient import _solClient
from solclient.solClient import *
from solclient.solClient import _logAndRaiseError

__author__ = 'Raymond Sunartio'

logger = logging.getLogger(__name__)


#
# solClient_dllExport solClient_returnCode_t
# solClient_msg_dump(
#     solClient_opaqueMsg_pt  msg_p,
#     char                   *buffer_p,
#     size_t                  bufferSize
# );
#
def solClient_msg_dump(msg_p, buffer_p, bufferSize):
    _solClient.solClient_msg_dump.restype = solClient_returnCode_t
    _solClient.solClient_msg_dump.argtypes = [
        solClient_opaqueMsg_pt,
        c_char_p,
        c_size_t
    ]
    if _solClient.solClient_msg_dump(msg_p, buffer_p, bufferSize) != SOLCLIENT_OK:
        _logAndRaiseError()


#
# solClient_dllExport solClient_returnCode_t
# solClient_msg_getBinaryAttachmentPtr(solClient_opaqueMsg_pt msg_p,
#                              solClient_opaquePointer_pt bufPtr_p,
#                              solClient_uint32_t         *size_p);
#
def solClient_msg_getBinaryAttachmentPtr(msg_p, bufPtr_p, size_p):
    _solClient.solClient_msg_getBinaryAttachmentPtr.restype = solClient_returnCode_t
    _solClient.solClient_msg_getBinaryAttachmentPtr.argtypes = [
        solClient_opaqueMsg_pt,
        solClient_opaquePointer_pt,
        solClient_uint32_t
    ]
    if _solClient.solClient_msg_getBinaryAttachmentPtr(msg_p, byref(bufPtr_p), byref(size_p)) != SOLCLIENT_OK:
        _logAndRaiseError()
