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
    if _solClient.solClient_msg_dump(msg_p, buffer_p, bufferSize) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
# solClient_dllExport solClient_returnCode_t
# solClient_msg_getBinaryAttachmentMap(solClient_opaqueMsg_pt msg_p,
#                             solClient_opaqueContainer_pt     *map_p);
#
def solClient_msg_getBinaryAttachmentMap(msg_p, map_p):
    _solClient.solClient_msg_getBinaryAttachmentMap.restype = solClient_returnCode_t
    _solClient.solClient_msg_getBinaryAttachmentMap.argtypes = [
        solClient_opaqueMsg_pt,
        POINTER(solClient_opaqueContainer_pt)
    ]
    if _solClient.solClient_msg_getBinaryAttachmentMap(msg_p, map_p) != SOLCLIENT_OK.value:
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
    if _solClient.solClient_msg_getBinaryAttachmentPtr(msg_p, bufPtr_p, size_p) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
# solClient_dllExport solClient_returnCode_t
# solClient_container_getByteArray (solClient_opaqueContainer_pt container_p,
#                        solClient_uint8_t          *array_p,
#                        solClient_uint32_t         *arrayLength_p,
#                        const char                 *name);
#
def solClient_container_getByteArray(container_p, array_p, arrayLength_p, name):
    _solClient.solClient_container_getByteArray.restype = solClient_returnCode_t
    _solClient.solClient_container_getByteArray.argtypes = [
        solClient_opaqueContainer_pt,
        solClient_uint8_t,
        solClient_uint32_t,
        c_char_p
    ]
    if _solClient.solClient_container_getByteArray(container_p, array_p, arrayLength_p, name) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
# solClient_dllExport solClient_returnCode_t
# solClient_container_getString (solClient_opaqueContainer_pt container_p,
#                        char                       *string,
#                        size_t                      size,
#                        const char                 *name);
#
def solClient_container_getString(container_p, string, size, name):
    _solClient.solClient_container_getString.restype = solClient_returnCode_t
    _solClient.solClient_container_getString.argtypes = [
        solClient_opaqueContainer_pt,
        c_char_p,
        size_t,
        c_char_p
    ]
    if _solClient.solClient_container_getString(container_p, string, size, name) != SOLCLIENT_OK.value:
        _logAndRaiseError()
