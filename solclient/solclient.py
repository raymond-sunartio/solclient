from ctypes import *
import inspect
import logging

logger = logging.getLogger(__name__)

#
# The solclient library
#
_solClient = windll("./solclient-7.5.0.7/bin/Win64/libsolclient.dll")

#
# typedef void  *solClient_opaqueContext_pt;   /**< An opaque pointer to a processing Context. */
# typedef void  *solClient_opaqueSession_pt;   /**< An opaque pointer to a Session. */
# typedef void  *solClient_opaqueFlow_pt;      /**< An opaque pointer to a Flow. */
# typedef void  *solClient_opaqueMsg_pt;       /**< An opaque pointer to a message. */
# typedef void  *solClient_opaqueContainer_pt; /**< An opaque pointer to a container (such as a map or stream). */
# typedef void  *solClient_opaqueDatablock_pt; /**< An opaque pointer to a data block. */
# typedef void  *solClient_opaqueTransactedSession_pt;      /**< An opaque pointer to a Transacted Session. */
# typedef void  **solClient_opaquePointer_pt;   /**< An opaque pointer to a pointer */
#
solClient_opaqueContext_pt = c_void_p
solClient_opaqueSession_pt = c_void_p
solClient_opaqueFlow_pt = c_void_p
solClient_opaqueMsg_pt = c_void_p
solClient_opaqueContainer_pt = c_void_p
solClient_opaqueDatablock_pt = c_void_p
solClient_opaqueTransactedSession_pt = c_void_p
solClient_opaquePointer_pt = POINTER(c_void_p)

#
# #if defined (SOLCLIENT_CONST_PROPERTIES)
#   typedef const char ** solClient_propertyArray_pt;  /**< pointer to an array of string pointers for properties */
# #else
#   typedef char ** solClient_propertyArray_pt;        /**< pointer to an array of string pointers for properties */
# #endif
#
solClient_propertyArray_pt = POINTER(c_char_p)

#
#  typedef enum solClient_returnCode
#  {
#    SOLCLIENT_OK = 0,           /**< The API call was successful. */
#    SOLCLIENT_WOULD_BLOCK = 1,  /**< The API call would block, but non-blocking was requested. */
#    SOLCLIENT_IN_PROGRESS = 2,  /**< An API call is in progress (non-blocking mode). */
#    SOLCLIENT_NOT_READY = 3,    /**< The API could not complete as an object is not ready (for example, the Session is not connected). */
#    SOLCLIENT_EOS  = 4,         /**< A getNext on a structured container returned End-of-Stream. */
#    SOLCLIENT_NOT_FOUND = 5,    /**< A get for a named field in a MAP was not found in the MAP. */
#    SOLCLIENT_NOEVENT = 6,      /**< solClient_context_processEventsWait returns this if wait is zero and there is no event to process */
#    SOLCLIENT_INCOMPLETE = 7,   /**< The API call completed some, but not all, of the requested function. */
#    SOLCLIENT_ROLLBACK = 8,     /**< solClient_transactedSession_commit returns this when the transaction has been rolled back. */
#    SOLCLIENT_FAIL = -1         /**< The API call failed. */
#  } solClient_returnCode_t;     /**< The type for API return codes. */
#
solClient_returnCode_t = int
(
    SOLCLIENT_FAIL,
    SOLCLIENT_OK,
    SOLCLIENT_WOULD_BLOCK,
    SOLCLIENT_IN_PROGRESS,
    SOLCLIENT_NOT_READY,
    SOLCLIENT_EOS,
    SOLCLIENT_NOT_FOUND,
    SOLCLIENT_NOEVENT,
    SOLCLIENT_INCOMPLETE,
    SOLCLIENT_ROLLBACK
) = map(solClient_returnCode_t, range(-1, 9, 1))

#
#  typedef enum solClient_log_level
#  {
#    SOLCLIENT_LOG_EMERGENCY = 0, /**< This level is not used by the API. */
#    SOLCLIENT_LOG_ALERT = 1,     /**< This level is not used by the API. */
#    SOLCLIENT_LOG_CRITICAL = 2,  /**< A serious error that can make the API unusable. */
#    SOLCLIENT_LOG_ERROR = 3,     /**< An unexpected condition within the API that can affect its operation. */
#    SOLCLIENT_LOG_WARNING = 4,   /**< An unexpected condition within the API that is not expected to affect its operation. */
#    SOLCLIENT_LOG_NOTICE = 5,    /**< Significant informational messages about the normal operation of the API. These messages are never output in the normal process of sending or receiving a message from the appliance. */
#    SOLCLIENT_LOG_INFO = 6,      /**< Informational messages about the normal operation of the API. These might include information related to sending or receiving messages from the appliance. */
#    SOLCLIENT_LOG_DEBUG = 7      /**< Debugging information generally useful to API developers (very verbose). */
#  } solClient_log_level_t;       /**< Type for log levels. */
#
solClient_log_level_t = c_int
(
    SOLCLIENT_LOG_EMERGENCY,
    SOLCLIENT_LOG_ALERT,
    SOLCLIENT_LOG_CRITICAL,
    SOLCLIENT_LOG_ERROR,
    SOLCLIENT_LOG_WARNING,
    SOLCLIENT_LOG_NOTICE,
    SOLCLIENT_LOG_INFO,
    SOLCLIENT_LOG_DEBUG
) = map(solClient_log_level_t, range(8))

#
# #define SOLCLIENT_LOG_DEFAULT_FILTER (SOLCLIENT_LOG_NOTICE) /**< Default log filter level. */
#
SOLCLIENT_LOG_DEFAULT_FILTER = SOLCLIENT_LOG_NOTICE

#
#  typedef enum solClient_session_event
#  {
#    SOLCLIENT_SESSION_EVENT_UP_NOTICE = 0,              /**< The Session is established. */
#    SOLCLIENT_SESSION_EVENT_DOWN_ERROR = 1,             /**< The Session was established and then went down. */
#    SOLCLIENT_SESSION_EVENT_CONNECT_FAILED_ERROR = 2,   /**< The Session attempted to connect but was unsuccessful. */
#    SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR = 3,     /**< The appliance rejected a published message. */
#    SOLCLIENT_SESSION_EVENT_SUBSCRIPTION_ERROR = 4,     /**< The appliance rejected a subscription (add or remove). */
#    SOLCLIENT_SESSION_EVENT_RX_MSG_TOO_BIG_ERROR = 5,   /**< The API discarded a received message that exceeded the Session buffer size. */
#    SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT = 6,        /**< The oldest transmitted Persistent/Non-Persistent message that has been acknowledged. */
#    SOLCLIENT_SESSION_EVENT_ASSURED_PUBLISHING_UP = 7,  /**< Deprecated -- see notes in solClient_session_startAssuredPublishing. The AD Handshake (that is, Guaranteed Delivery handshake) has completed for the publisher and Guaranteed messages can be sent. */
#    SOLCLIENT_SESSION_EVENT_ASSURED_CONNECT_FAILED = 8, /**< Deprecated -- see notes in solClient_session_startAssuredPublishing. The appliance rejected the AD Handshake to start Guaranteed publishing. Use ::SOLCLIENT_SESSION_EVENT_ASSURED_DELIVERY_DOWN instead. */
#    SOLCLIENT_SESSION_EVENT_ASSURED_DELIVERY_DOWN = 8,  /**< Guaranteed Delivery publishing is not available. The guaranteed delivery capability on the session has been disabled by some action on the appliance. */
#    SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_ERROR = 9,   /**< The Topic Endpoint unsubscribe command failed. */
#    SOLCLIENT_SESSION_EVENT_DTE_UNSUBSCRIBE_ERROR = SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_ERROR,  /**< Deprecated name; ::SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_ERROR is preferred */
#    SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK = 10,     /**< The Topic Endpoint unsubscribe completed. */
#    SOLCLIENT_SESSION_EVENT_DTE_UNSUBSCRIBE_OK = SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK,    /**< Deprecated name; ::SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK is preferred */
#    SOLCLIENT_SESSION_EVENT_CAN_SEND =            11,   /**< The send is no longer blocked. */
#    SOLCLIENT_SESSION_EVENT_RECONNECTING_NOTICE = 12,   /**< The Session has gone down, and an automatic reconnect attempt is in progress. */
#    SOLCLIENT_SESSION_EVENT_RECONNECTED_NOTICE =  13,   /**< The automatic reconnect of the Session was successful, and the Session was established again. */
#    SOLCLIENT_SESSION_EVENT_PROVISION_ERROR =     14,   /**< The endpoint create/delete command failed. */
#    SOLCLIENT_SESSION_EVENT_PROVISION_OK    =     15,   /**< The endpoint create/delete command completed. */
#    SOLCLIENT_SESSION_EVENT_SUBSCRIPTION_OK =     16,   /**< The subscribe or unsubscribe operation has succeeded. */
#    SOLCLIENT_SESSION_EVENT_VIRTUAL_ROUTER_NAME_CHANGED = 17, /**< The appliance's Virtual Router Name changed during a reconnect operation. This could render existing queues or temporary topics invalid. */
#    SOLCLIENT_SESSION_EVENT_MODIFYPROP_OK   =     18,   /**< The session property modification completed. */
#    SOLCLIENT_SESSION_EVENT_MODIFYPROP_FAIL   =   19,   /**< The session property modification failed. */
#    SOLCLIENT_SESSION_EVENT_REPUBLISH_UNACKED_MESSAGES = 20  /**< After successfully reconnecting a disconnected session, the SDK received an unknown publisher flow name response when reconnecting the GD publisher flow. If configured to auto-retry (See ::SOLCLIENT_SESSION_PROP_GD_RECONNECT_FAIL_ACTION.) this event is generated to indicate how many unacknowledged messages are retransmitted on success. As the publisher state has been lost on failover, receiving this event may indicate that some messages have been duplicated in the system.*/
#  } solClient_session_event_t;                          /**< Type for Session events. */
#
solClient_session_event_t = c_int
(
    SOLCLIENT_SESSION_EVENT_UP_NOTICE,
    SOLCLIENT_SESSION_EVENT_DOWN_ERROR,
    SOLCLIENT_SESSION_EVENT_CONNECT_FAILED_ERROR,
    SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR,
    SOLCLIENT_SESSION_EVENT_SUBSCRIPTION_ERROR,
    SOLCLIENT_SESSION_EVENT_RX_MSG_TOO_BIG_ERROR,
    SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT,
    SOLCLIENT_SESSION_EVENT_ASSURED_PUBLISHING_UP,
    SOLCLIENT_SESSION_EVENT_ASSURED_DELIVERY_DOWN,
    SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_ERROR,
    SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK,
    SOLCLIENT_SESSION_EVENT_CAN_SEND,
    SOLCLIENT_SESSION_EVENT_RECONNECTING_NOTICE,
    SOLCLIENT_SESSION_EVENT_RECONNECTED_NOTICE,
    SOLCLIENT_SESSION_EVENT_PROVISION_ERROR,
    SOLCLIENT_SESSION_EVENT_PROVISION_OK,
    SOLCLIENT_SESSION_EVENT_SUBSCRIPTION_OK,
    SOLCLIENT_SESSION_EVENT_VIRTUAL_ROUTER_NAME_CHANGED,
    SOLCLIENT_SESSION_EVENT_MODIFYPROP_OK,
    SOLCLIENT_SESSION_EVENT_MODIFYPROP_FAIL,
    SOLCLIENT_SESSION_EVENT_REPUBLISH_UNACKED_MESSAGES
) = map(solClient_session_event_t, range(21))

#
#  typedef enum solClient_flow_event
#  {
#    SOLCLIENT_FLOW_EVENT_UP_NOTICE = 0,            /**< The Flow is established. */
#    SOLCLIENT_FLOW_EVENT_DOWN_ERROR = 1,           /**< The Flow was established and then disconnected by the appliance, likely due to operator intervention. The Flow must be destroyed. */
#    SOLCLIENT_FLOW_EVENT_BIND_FAILED_ERROR = 2,    /**< The Flow attempted to connect but was unsuccessful. */
#    SOLCLIENT_FLOW_EVENT_REJECTED_MSG_ERROR = 3,   /**< This event is deprecated and will never be raised. */
#    SOLCLIENT_FLOW_EVENT_SESSION_DOWN       = 4,   /**< The Session for the Flow was disconnected. The Flow will rebound automatically when the Session is reconnected.*/
#    SOLCLIENT_FLOW_EVENT_ACTIVE             = 5,   /**< The flow has become active */
#    SOLCLIENT_FLOW_EVENT_INACTIVE           = 6    /**< The flow has become inactive */
#  } solClient_flow_event_t;                        /**< Type for Flow events. */
#
solClient_flow_event_t = c_int
(
     SOLCLIENT_FLOW_EVENT_UP_NOTICE,
     SOLCLIENT_FLOW_EVENT_DOWN_ERROR,
     SOLCLIENT_FLOW_EVENT_BIND_FAILED_ERROR,
     SOLCLIENT_FLOW_EVENT_REJECTED_MSG_ERROR,
     SOLCLIENT_FLOW_EVENT_SESSION_DOWN,
     SOLCLIENT_FLOW_EVENT_ACTIVE,
     SOLCLIENT_FLOW_EVENT_INACTIVE
) = map(solClient_flow_event_t, range(7))

#
#  typedef enum solClient_rxMsgCallback_returnCode {
#    SOLCLIENT_CALLBACK_OK       = 0, /**< Normal return - the message is destroyed by the API upon return. */
#    SOLCLIENT_CALLBACK_TAKE_MSG = 1  /**< The application is keeping the rxMsg, and it must not be released or reused by the API .*/
#  } solClient_rxMsgCallback_returnCode_t;
#
solClient_rxMsgCallback_returnCode_t = c_int
(
     SOLCLIENT_CALLBACK_OK,
     SOLCLIENT_CALLBACK_TAKE_MSG
) = map(solClient_rxMsgCallback_returnCode_t, range(2))

#
# #ifdef WIN32
#   typedef SOCKET solClient_fd_t;    /**< Type for a file descriptor. */
# #else
#   typedef int solClient_fd_t;       /**< Type for a file descriptor. */
# #endif
#
solClient_fd_t = c_int

#
#  typedef solClient_uint32_t solClient_fdEvent_t;              /**< A mask of events that can be requested for a file descriptor. */
#  typedef solClient_uint32_t solClient_subscribeFlags_t;       /**< A set of \ref subscribeflags "flags"  that can be provided to solClient_session_topicSubscribeExt() and solClient_session_topicUnsubscribeExt(). */
#  typedef solClient_uint32_t solClient_session_responseCode_t; /**< An error response code that is returned with Session events. */
#  typedef solClient_uint64_t solClient_msgId_t;                /**< A unique msgId assigned to each Persistent and Non-Persistent message. */
#  typedef solClient_uint32_t solClient_modifyPropFlags_t;      /**< A set of \ref modifypropflags "flags" that can be provided to a solClient_session_modifyClientInfo() call. */
#
solClient_fdEvent_t = c_ulong
solClient_subscribeFlags_t = c_ulong
solClient_session_responseCode_t = c_ulong
solClient_msgId_t = c_ulonglong
solClient_modifyPropFlags_t = c_ulong


#
#  typedef struct solClient_session_eventCallbackInfo
#  {
#    solClient_session_event_t sessionEvent;         /**< The Session event that has occurred. */
#    solClient_session_responseCode_t responseCode;  /**< A response code that is returned for some events, otherwise zero. */
#    const char *info_p;                             /**< Except for ::SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT (see Detailed Description above), a pointer to a NULL-terminated string providing further information about the event, when available. This pointer is never NULL */
#    void       *correlation_p;                      /**< Application-supplied correlation pointer where applicable. Used when acknowledging or rejecting Guaranteed messages, in responses to any function calls that pass a correlationTag that will be returned in a Session Event. */
#  } solClient_session_eventCallbackInfo_t, *solClient_session_eventCallbackInfo_pt; /**< A pointer to ::solClient_session_eventCallbackInfo structure of information returned with a Session event. */
#
class solClient_session_eventCallbackInfo_t(Structure):
    _fields_ = [
        ('sessionEvent', solClient_session_event_t),
        ('responseCode', solClient_session_responseCode_t),
        ('info_p', c_char_p),
        ('correlation_p', c_void_p)
    ]
solClient_session_eventCallbackInfo_pt = POINTER(solClient_session_eventCallbackInfo_t)


#
#  typedef struct solClient_flow_eventCallbackInfo
#  {
#    solClient_flow_event_t flowEvent;         /**< The Session event that has occurred. */
#    solClient_session_responseCode_t responseCode;  /**< A response code that is returned for some events; otherwise zero. */
#    const char *info_p;                             /**< A pointer to a NULL-terminated string providing further information about the event, when available. This pointer is never NULL. */
#  } solClient_flow_eventCallbackInfo_t, *solClient_flow_eventCallbackInfo_pt; /**< A pointer to ::solClient_flow_eventCallbackInfo structure of information returned with a Session event. */
#
class solClient_flow_eventCallbackInfo_t(Structure):
    _fields_ = [
        ('flowEvent', solClient_flow_event_t),
        ('responseCode', solClient_session_responseCode_t),
        ('info_p', c_char_p)
    ]
solClient_flow_eventCallbackInfo_pt = POINTER(solClient_flow_eventCallbackInfo_t)

#
#  typedef void (*solClient_session_eventCallbackFunc_t) (solClient_opaqueSession_pt opaqueSession_p, solClient_session_eventCallbackInfo_pt eventInfo_p, void *user_p);
#  typedef void (*solClient_flow_eventCallbackFunc_t) (solClient_opaqueFlow_pt opaqueFlow_p, solClient_flow_eventCallbackInfo_pt eventInfo_p, void *user_p);
#  typedef void (*solClient_context_fdCallbackFunc_t) (solClient_opaqueContext_pt opaqueContext_p, solClient_fd_t fd, solClient_fdEvent_t events, void *user_p); /**< Callback prototype for FD events. */
#  typedef solClient_rxMsgCallback_returnCode_t
#  (*solClient_session_rxMsgCallbackFunc_t) (solClient_opaqueSession_pt opaqueSession_p, solClient_opaqueMsg_pt msg_p, void *user_p);
#  typedef solClient_rxMsgCallback_returnCode_t
#  (*solClient_flow_rxMsgCallbackFunc_t) (solClient_opaqueFlow_pt opaqueFlow_p, solClient_opaqueMsg_pt msg_p, void *user_p);
#  typedef solClient_returnCode_t (*solClient_context_registerFdFunc_t) (void *app_p, solClient_fd_t fd, solClient_fdEvent_t events, solClient_context_fdCallbackFunc_t callback_p, void *user_p);
#  typedef solClient_returnCode_t (*solClient_context_unregisterFdFunc_t) (void *app_p, solClient_fd_t fd, solClient_fdEvent_t events);
#
solClient_session_eventCallbackFunc_t = WINFUNCTYPE(c_int, solClient_opaqueSession_pt, solClient_session_eventCallbackInfo_pt, c_void_p)
solClient_flow_eventCallbackFunc_t = WINFUNCTYPE(c_int, solClient_opaqueFlow_pt, solClient_flow_eventCallbackInfo_pt, c_void_p)
solClient_context_fdCallbackFunc_t = WINFUNCTYPE(c_int, solClient_opaqueContext_pt, solClient_fd_t, solClient_fdEvent_t, c_void_p)
solClient_session_rxMsgCallbackFunc_t = WINFUNCTYPE(solClient_rxMsgCallback_returnCode_t, solClient_opaqueSession_pt, solClient_opaqueMsg_pt, solClient_opaqueMsg_pt, c_void_p)
solClient_flow_rxMsgCallbackFunc_t = WINFUNCTYPE(solClient_rxMsgCallback_returnCode_t, solClient_opaqueFlow_pt, solClient_opaqueMsg_pt, c_void_p)
solClient_context_registerFdFunc_t = WINFUNCTYPE(solClient_returnCode_t, c_void_p, solClient_fd_t, solClient_fdEvent_t, solClient_context_fdCallbackFunc_t, c_void_p)
solClient_context_unregisterFdFunc_t = WINFUNCTYPE(solClient_returnCode_t, c_void_p, solClient_fd_t, solClient_fdEvent_t)


#
#  typedef struct solClient_context_createRegisterFdFuncInfo
#  {
#    solClient_context_registerFdFunc_t regFdFunc_p;
#    solClient_context_unregisterFdFunc_t unregFdFunc_p;
#    void *user_p;
#  } solClient_context_createRegisterFdFuncInfo_t;
#
class solClient_context_createRegisterFdFuncInfo_t(Structure):
    _fields_ = [
        ('regFdFunc_p', solClient_context_registerFdFunc_t),
        ('unregFdFunc_p', solClient_context_unregisterFdFunc_t),
        ('user_p', c_void_p)
    ]


#
#  typedef struct solClient_context_createFuncInfo
#  {
#    solClient_context_createRegisterFdFuncInfo_t regFdInfo;
#  } solClient_context_createFuncInfo_t;
#
class solClient_context_createFuncInfo_t(Structure):
    _fields_ = [
        ('regFdInfo', solClient_context_createRegisterFdFuncInfo_t)
    ]

#
#  typedef enum solClient_subCode
#  {
#    ...
#  } solClient_subCode_t;
#
solClient_subCode_t = c_int


#
#  solClient_dllExport const char
#    *solClient_subCodeToString (solClient_subCode_t subCode);
#
def _solClient_subCodeToString(subCode):
    _solClient.solClient_subCodeToString.restype = c_char_p
    _solClient.solClient_subCodeToString.argtypes = [
        solClient_subCode_t
    ]
    return _solClient.solClient_subCodeToString(subCode)


#
#  typedef struct solClient_errorInfo
#  {
#    solClient_subCode_t subCode;                                              /**< A subcode indicating the type of error. */
#    solClient_session_responseCode_t responseCode;                            /**< A response code that is returned for some subcodes; otherwise zero. */
#    char errorStr[SOLCLIENT_ERRORINFO_STR_SIZE];                              /**< An information string for certain types of subcodes (empty string, if not used). */
#  } solClient_errorInfo_t, *solClient_errorInfo_pt; /**< A pointer to a ::solClient_errorInfo structure returned from ::solClient_getLastErrorInfo() .*/
#
def solClient_errorInfo_t(Structure):
    _fields_ = [
        ('subCode', solClient_subCode_t),
        ('responseCode', solClient_session_responseCode_t),
        ('errorStr', c_char_p)
    ]
solClient_errorInfo_pt = POINTER(solClient_errorInfo_t)


#
#  solClient_dllExport solClient_errorInfo_pt
#    solClient_getLastErrorInfo (void);
#
def _solClient_getLastErrorInfo():
    _solClient.solClient_getLastErrorInfo.restype = solClient_errorInfo_pt
    _solClient.solClient_getLastErrorInfo.argtypes = [
        c_int
    ]
    lastErrorInfo = _solClient.solClient_getLastErrorInfo().contents


#
# _logAndRaise
#   Log error and raise exception
#
def _logAndRaise():
    caller = inspect.stack()[1][3]
    lastErrorInfo = _solClient_getLastErrorInfo()
    errorStr = lastErrorInfo.errorStr
    subCodeStr = _solClient_subCodeToString(lastErrorInfo.subCode)
    errorMsg = 'Error encountered in {} - errorStr={}, subCode={}'.format(caller, errorStr, subCodeStr)
    logger.error(errorMsg)
    raise RuntimeError(errorMsg)


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_initialize (solClient_log_level_t initialLogLevel,
#                          solClient_propertyArray_pt props);
#
def solClient_initialize(initialLogLevel=SOLCLIENT_LOG_DEFAULT_FILTER, props=None):
    _solClient.solClient_initialize.restype = solClient_returnCode_t
    _solClient.solClient_initialize.argtypes = [
        solClient_log_level_t,
        solClient_propertyArray_pt
    ]
    if _solClient.solClient_initialize(initialLogLevel, props) != SOLCLIENT_OK:
        _logAndRaise()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_context_create (solClient_propertyArray_pt props,
#                              solClient_opaqueContext_pt * opaqueContext_p,
#                              solClient_context_createFuncInfo_t * funcInfo_p,
#                              size_t funcInfoSize);
#
def solClient_context_create(props, opaqueContext_p, funcInfo_p):
    _solClient.solClient_context_create.restype = solClient_returnCode_t
    _solClient.solClient_context_create.argtypes = [
        solClient_propertyArray_pt,
        POINTER(solClient_opaqueContext_pt),
        POINTER(solClient_context_createFuncInfo_t),
        c_size_t
    ]
    pass
