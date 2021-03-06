from ctypes import *
import inspect
import logging
import os

from solclient import _solClient

__author__ = 'Raymond Sunartio'

logger = logging.getLogger(__name__)

#
# typedef unsigned char  solClient_uint8_t;          /**< 8-bit unsigned integer type. */
# typedef signed char    solClient_int8_t;           /**< 8-bit signed integer type. */
# typedef unsigned short solClient_uint16_t;         /**< 16-bit unsigned integer type. */
# typedef short          solClient_int16_t;          /**< 16-bit signed integer type. */
# typedef unsigned char  solClient_bool_t;           /**< Boolean type (non-zero is true, 0 is false) .*/
#
# #if UINT_MAX == 0xffffffff
#   typedef int solClient_int32_t;                   /**< 32-bit signed integer type. */
#   typedef unsigned int solClient_uint32_t;         /**< 32-bit unsigned integer type. */
# #elif ULONG_MAX == 0xffffffff
#   typedef long solClient_int32_t;                  /**< 32-bit signed integer type. */
#   typedef unsigned long solClient_uint32_t;        /**< 32-bit unsigned integer type. */
# #else
# #   error Problem with 32-bit types.
# #endif
#
solClient_uint8_t = c_ubyte
solClient_int8_t = c_byte
solClient_uint16_t = c_ushort
solClient_int16_t = c_short
solClient_uint32_t = c_uint
solClient_int32_t = c_int
solClient_uint64_t = c_ulonglong
solClient_int64_t = c_longlong
solClient_bool_t = c_bool
solClient_wchar_t = c_wchar

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
solClient_returnCode_t = c_int32
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
solClient_log_level_t = c_int32
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
solClient_session_event_t = c_int32
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
solClient_flow_event_t = c_int32
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
solClient_rxMsgCallback_returnCode_t = c_int32
(
     SOLCLIENT_CALLBACK_OK,
     SOLCLIENT_CALLBACK_TAKE_MSG
) = map(solClient_rxMsgCallback_returnCode_t, range(2))

#
# #define SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM        (0x02) /**< The subscribe/unsubscribe call blocks until a confirmation is received. @see @ref blocking-context "Threading Effects on Blocking Modes" for more information about setting subscribe flags in the Context thread.*/
# #define SOLCLIENT_SUBSCRIBE_FLAGS_RX_ALL_DELIVER_TO_ONE (0x04) /**< This flag, when present in a subscription ADD request, overrides the deliver-to-one property in a message (see ::solClient_msg_setDeliverToOne()) - If the Topic in the message matches, it is delivered to clients with ::SOLCLIENT_SUBSCRIBE_FLAGS_RX_ALL_DELIVER_TO_ONE set, in addition to any one client that is subscribed to the Topic without this override. */
# #define SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY   (0x08) /**< For the @ref topic-dispatch "topic dispatch" feature, this flag indicates the subscription should only be added to the dispatch table and should not be added to the appliance. */
# #define SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM       (0x10) /**< Requests a confirmation for the subscribe/unsubscribe operation. This bit is implied by ::SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM. If ::SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM is not set when this flag is set, then a confirmation event will be issued through the Session event callback procedure. */
#
SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM = 2
SOLCLIENT_SUBSCRIBE_FLAGS_RX_ALL_DELIVER_TO_ONE = 4
SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY = 8
SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM = 16

#
# #ifdef WIN32
#   typedef SOCKET solClient_fd_t;    /**< Type for a file descriptor. */
# #else
#   typedef int solClient_fd_t;       /**< Type for a file descriptor. */
# #endif
#
solClient_fd_t = c_int32

#
#  typedef solClient_uint32_t solClient_fdEvent_t;              /**< A mask of events that can be requested for a file descriptor. */
#  typedef solClient_uint32_t solClient_subscribeFlags_t;       /**< A set of \ref subscribeflags "flags"  that can be provided to solClient_session_topicSubscribeExt() and solClient_session_topicUnsubscribeExt(). */
#  typedef solClient_uint32_t solClient_session_responseCode_t; /**< An error response code that is returned with Session events. */
#  typedef solClient_uint64_t solClient_msgId_t;                /**< A unique msgId assigned to each Persistent and Non-Persistent message. */
#  typedef solClient_uint32_t solClient_modifyPropFlags_t;      /**< A set of \ref modifypropflags "flags" that can be provided to a solClient_session_modifyClientInfo() call. */
#
solClient_fdEvent_t = solClient_uint32_t
solClient_subscribeFlags_t = solClient_uint32_t
solClient_session_responseCode_t = solClient_uint32_t
solClient_msgId_t = solClient_uint64_t
solClient_modifyPropFlags_t = solClient_uint32_t

#
# #define SOLCLIENT_SESSION_PROP_HOST                          "SESSION_HOST"     /**< The IP address (or host name) to connect to. @ref host-list "Multiple entries" (up to ::SOLCLIENT_SESSION_PROP_MAX_HOSTS) are allowed, separated by commas. @ref host-entry "The entry for the SOLCLIENT_SESSION_PROP_HOST property should provide a protocol, host, and port". See @ref host-list "Configuring Multiple Hosts for Redundancy and Failover" for a discussion of Guaranteed Messaging considerations. May be set as an environment variable (See @ref SessionProps). Default: ::SOLCLIENT_SESSION_PROP_DEFAULT_HOST */
# #define SOLCLIENT_SESSION_PROP_VPN_NAME                      "SESSION_VPN_NAME"    /**< The name of the Message VPN to attempt to join when connecting to an appliance running SolOS-TR. Default: ::SOLCLIENT_SESSION_PROP_DEFAULT_VPN_NAME */
# #define SOLCLIENT_SESSION_PROP_USERNAME                      "SESSION_USERNAME" /**< The username required for authentication. Default: ::SOLCLIENT_SESSION_PROP_DEFAULT_USERNAME */
# #define SOLCLIENT_SESSION_PROP_PASSWORD                      "SESSION_PASSWORD" /**< The password required for authentication. May be set as an environment variable (See @ref SessionProps). Default: ::SOLCLIENT_SESSION_PROP_DEFAULT_PASSWORD */
#
SOLCLIENT_SESSION_PROP_HOST = 'SESSION_HOST'
SOLCLIENT_SESSION_PROP_VPN_NAME = 'SESSION_VPN_NAME'
SOLCLIENT_SESSION_PROP_USERNAME = 'SESSION_USERNAME'
SOLCLIENT_SESSION_PROP_PASSWORD = 'SESSION_PASSWORD'
SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME = 'SESSION_AUTHENTICATION_SCHEME'
SOLCLIENT_SESSION_PROP_KRB_SERVICE_NAME = 'SESSION_KRB_SERVICE_NAME'


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
if os.name == 'nt':
    solClient_session_eventCallbackFunc_t = WINFUNCTYPE(c_int, solClient_opaqueSession_pt, solClient_session_eventCallbackInfo_pt, c_void_p)
    solClient_flow_eventCallbackFunc_t = WINFUNCTYPE(c_int, solClient_opaqueFlow_pt, solClient_flow_eventCallbackInfo_pt, c_void_p)
    solClient_context_fdCallbackFunc_t = WINFUNCTYPE(c_int, solClient_opaqueContext_pt, solClient_fd_t, solClient_fdEvent_t, c_void_p)
    solClient_session_rxMsgCallbackFunc_t = WINFUNCTYPE(solClient_rxMsgCallback_returnCode_t, solClient_opaqueSession_pt, solClient_opaqueMsg_pt, c_void_p)
    solClient_flow_rxMsgCallbackFunc_t = WINFUNCTYPE(solClient_rxMsgCallback_returnCode_t, solClient_opaqueFlow_pt, solClient_opaqueMsg_pt, c_void_p)
    solClient_context_registerFdFunc_t = WINFUNCTYPE(solClient_returnCode_t, c_void_p, solClient_fd_t, solClient_fdEvent_t, solClient_context_fdCallbackFunc_t, c_void_p)
    solClient_context_unregisterFdFunc_t = WINFUNCTYPE(solClient_returnCode_t, c_void_p, solClient_fd_t, solClient_fdEvent_t)
elif os.name == 'posix':
    solClient_session_eventCallbackFunc_t = CFUNCTYPE(c_int, solClient_opaqueSession_pt, solClient_session_eventCallbackInfo_pt, c_void_p)
    solClient_flow_eventCallbackFunc_t = CFUNCTYPE(c_int, solClient_opaqueFlow_pt, solClient_flow_eventCallbackInfo_pt, c_void_p)
    solClient_context_fdCallbackFunc_t = CFUNCTYPE(c_int, solClient_opaqueContext_pt, solClient_fd_t, solClient_fdEvent_t, c_void_p)
    solClient_session_rxMsgCallbackFunc_t = CFUNCTYPE(solClient_rxMsgCallback_returnCode_t, solClient_opaqueSession_pt, solClient_opaqueMsg_pt, c_void_p)
    solClient_flow_rxMsgCallbackFunc_t = CFUNCTYPE(solClient_rxMsgCallback_returnCode_t, solClient_opaqueFlow_pt, solClient_opaqueMsg_pt, c_void_p)
    solClient_context_registerFdFunc_t = CFUNCTYPE(solClient_returnCode_t, c_void_p, solClient_fd_t, solClient_fdEvent_t, solClient_context_fdCallbackFunc_t, c_void_p)
    solClient_context_unregisterFdFunc_t = CFUNCTYPE(solClient_returnCode_t, c_void_p, solClient_fd_t, solClient_fdEvent_t)


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

    def __init__(self, regFdFunc_p=solClient_context_registerFdFunc_t(0), unregFdFunc_p=solClient_context_unregisterFdFunc_t(0), user_p=None):
        self.regFdFunc_p = regFdFunc_p
        self.unregFdFunc_p = unregFdFunc_p
        self.user_p = user_p


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

    def __init__(self, regFdInfo):
        self.regFdInfo = regFdInfo


#
# #define SOLCLIENT_CONTEXT_CREATEFUNC_INITIALIZER {{NULL, NULL, NULL}}
#
SOLCLIENT_CONTEXT_CREATEFUNC_INITIALIZER = solClient_context_createFuncInfo_t(
    regFdInfo=solClient_context_createRegisterFdFuncInfo_t()
)


#
#  typedef struct solClient_session_createRxCallbackFuncInfo
#  {
#    void *callback_p;
#    void *user_p;
#  } solClient_session_createRxCallbackFuncInfo_t;
#
class solClient_session_createRxCallbackFuncInfo_t(Structure):
    _fields_ = [
        ('callback_p', c_void_p),
        ('user_p', c_void_p)
    ]

    def __init__(self, callback_p=None, user_p=None):
        self.callback_p = callback_p
        self.user_p = user_p


#
#  typedef struct solClient_session_createEventCallbackFuncInfo
#  {
#    solClient_session_eventCallbackFunc_t callback_p;
#    void *user_p;
#  } solClient_session_createEventCallbackFuncInfo_t;
#
class solClient_session_createEventCallbackFuncInfo_t(Structure):
    _fields_ = [
        ('callback_p', solClient_session_eventCallbackFunc_t),
        ('user_p', c_void_p)
    ]

    def __init__(self, callback_p=solClient_session_eventCallbackFunc_t(0), user_p=None):
        self.callback_p = callback_p
        self.user_p = user_p


#
#  typedef struct solClient_session_createRxMsgCallbackFuncInfo
#  {
#    solClient_session_rxMsgCallbackFunc_t callback_p;
#    void *user_p;
#  } solClient_session_createRxMsgCallbackFuncInfo_t;
#
class solClient_session_createRxMsgCallbackFuncInfo_t(Structure):
    _fields_ = [
        ('callback_p', solClient_session_rxMsgCallbackFunc_t),
        ('user_p', c_void_p)
    ]

    def __init__(self, callback_p=solClient_session_rxMsgCallbackFunc_t(0), user_p=None):
        self.callback_p = callback_p
        self.user_p = user_p


#
#  typedef struct solClient_session_createFuncInfo
#  {
#    solClient_session_createRxCallbackFuncInfo_t    rxInfo;
#    solClient_session_createEventCallbackFuncInfo_t eventInfo;
#    solClient_session_createRxMsgCallbackFuncInfo_t rxMsgInfo;
#  } solClient_session_createFuncInfo_t;
#
class solClient_session_createFuncInfo_t(Structure):
    _fields_ = [
        ('rxInfo', solClient_session_createRxCallbackFuncInfo_t),
        ('eventInfo', solClient_session_createEventCallbackFuncInfo_t),
        ('rxMsgInfo', solClient_session_createRxMsgCallbackFuncInfo_t)
    ]

    def __init__(self, rxInfo, eventInfo, rxMsgInfo):
        self.rxInfo = rxInfo
        self.eventInfo = eventInfo
        self.rxMsgInfo = rxMsgInfo


#
# #define SOLCLIENT_SESSION_CREATEFUNC_INITIALIZER {{NULL,NULL},{NULL,NULL},{NULL,NULL}}
#
SOLCLIENT_SESSION_CREATEFUNC_INITIALIZER = solClient_session_createFuncInfo_t(
    rxInfo=solClient_session_createRxCallbackFuncInfo_t(),
    eventInfo=solClient_session_createEventCallbackFuncInfo_t(),
    rxMsgInfo=solClient_session_createRxMsgCallbackFuncInfo_t()
)

#
# typedef enum solClient_destinationType
# {
#     SOLCLIENT_NULL_DESTINATION          = -1,
#     SOLCLIENT_TOPIC_DESTINATION         = 0,
#     SOLCLIENT_QUEUE_DESTINATION         = 1,
#     SOLCLIENT_TOPIC_TEMP_DESTINATION    = 2,
#     SOLCLIENT_QUEUE_TEMP_DESTINATION    = 3
# } solClient_destinationType_t;
#
solClient_destinationType_t = c_int32
(
    SOLCLIENT_NULL_DESTINATION,
    SOLCLIENT_TOPIC_DESTINATION,
    SOLCLIENT_QUEUE_DESTINATION,
    SOLCLIENT_TOPIC_TEMP_DESTINATION,
    SOLCLIENT_QUEUE_TEMP_DESTINATION
) = map(solClient_destinationType_t, range(-1, 4, 1))


#
# typedef struct solClient_destination
# {
#     solClient_destinationType_t         destType; /**< The type of destination. */
#     const char *                        dest;     /**< The name of the destination (as a NULL-terminated UTF-8 string). */
# } solClient_destination_t;
#
class solClient_destination_t(Structure):
    _fields_ = [
        ('destType', solClient_destinationType_t),
        ('dest', c_char_p)
    ]


#
# typedef enum solClient_fieldType
# {
#     SOLCLIENT_BOOL      = 0,    /**< Boolean. */
#     SOLCLIENT_UINT8     = 1,    /**< 8-bit unsigned integer. */
#     SOLCLIENT_INT8      = 2,    /**< 8-bit signed integer. */
#     SOLCLIENT_UINT16    = 3,    /**< 16-bit unsigned integer. */
#     SOLCLIENT_INT16     = 4,    /**< 16-bit signed integer. */
#     SOLCLIENT_UINT32    = 5,    /**< 32-bit unsigned integer. */
#     SOLCLIENT_INT32     = 6,    /**< 32-bit signed integer. */
#     SOLCLIENT_UINT64    = 7,    /**< 64-bit unsigned integer. */
#     SOLCLIENT_INT64     = 8,    /**< 64-bit signed integer. */
#     SOLCLIENT_WCHAR     = 9,   /**< 16-bit unicode character. */
#     SOLCLIENT_STRING    = 10,   /**< Null terminated string, (ASCII or UTF-8). */
#     SOLCLIENT_BYTEARRAY = 11,   /**< Byte array. */
#     SOLCLIENT_FLOAT     = 12,   /**< 32-bit floating point number. */
#     SOLCLIENT_DOUBLE    = 13,   /**< 64-bit floating point number. */
#     SOLCLIENT_MAP       = 14,   /**< Solace Map (container class). */
#     SOLCLIENT_STREAM    = 15,   /**< Solace Stream (container class). */
#     SOLCLIENT_NULL      = 16,   /**< NULL field.*/
#     SOLCLIENT_DESTINATION = 17, /**< Destination field. */
#     SOLCLIENT_SMF       = 18,   /**< A complete Solace Message Format (SMF) message is encapsulated in the container. */
#     SOLCLIENT_UNKNOWN   = -1    /**< A validly formatted, but unrecognized, data type was received. */
# } solClient_fieldType_t;
#
solClient_fieldType_t = c_int32
(
    SOLCLIENT_UNKNOWN,
    SOLCLIENT_BOOL,
    SOLCLIENT_UINT8,
    SOLCLIENT_INT8,
    SOLCLIENT_UINT16,
    SOLCLIENT_INT16,
    SOLCLIENT_UINT32,
    SOLCLIENT_INT32,
    SOLCLIENT_UINT64,
    SOLCLIENT_INT64,
    SOLCLIENT_WCHAR,
    SOLCLIENT_STRING,
    SOLCLIENT_BYTEARRAY,
    SOLCLIENT_FLOAT,
    SOLCLIENT_DOUBLE,
    SOLCLIENT_MAP,
    SOLCLIENT_STREAM,
    SOLCLIENT_NULL,
    SOLCLIENT_DESTINATION,
    SOLCLIENT_SMF
) = map(solClient_fieldType_t, range(-1, 19, 1))


#
# typedef struct solClient_field {
#     solClient_fieldType_t       type;
#     solClient_uint32_t          length;
#     union {
#         solClient_bool_t        boolean;
#         solClient_uint8_t       uint8;
#         solClient_int8_t        int8;
#         solClient_uint16_t      uint16;
#         solClient_int16_t       int16;
#         solClient_uint32_t      uint32;
#         solClient_int32_t       int32;
#         solClient_uint64_t      uint64;
#         solClient_int64_t       int64;
#         solClient_wchar_t       wchar;
#         float                   float32;
#         double                  float64;
#         const char             *string;
#         solClient_uint8_t      *bytearray;
#         solClient_opaqueContainer_pt
#                                 map;
#         solClient_opaqueContainer_pt
#                                 stream;
#         solClient_destination_t dest;
#         solClient_uint8_t      *smf;
#         solClient_uint8_t      *unknownField;
#     } value;
# } solClient_field_t;
#
class solClient_field_t(Structure):
    class _value(Union):
        _fields_ = [
            ('boolean', solClient_bool_t),
            ('uint8', solClient_uint8_t),
            ('int8', solClient_int8_t),
            ('uint16', solClient_uint16_t),
            ('int16', solClient_int16_t),
            ('uint32', solClient_uint32_t),
            ('int32', solClient_int32_t),
            ('uint64', solClient_uint64_t),
            ('int64', solClient_int64_t),
            ('wchar', solClient_wchar_t),
            ('float32', c_float),
            ('float64', c_double),
            ('string', c_char_p),
            ('bytearray', POINTER(solClient_uint8_t)),
            ('map', solClient_opaqueContainer_pt),
            ('stream', solClient_opaqueContainer_pt),
            ('dest', solClient_destination_t),
            ('smf', POINTER(solClient_uint8_t)),
            ('unknownField', POINTER(solClient_uint8_t))
        ]
    _fields_ = [
        ('type', solClient_fieldType_t),
        ('length', solClient_uint32_t),
        ('value', _value)
    ]


#
#  typedef enum solClient_subCode
#  {
#    ...
#  } solClient_subCode_t;
#
solClient_subCode_t = c_int32


#
#  solClient_dllExport const char
#    *solClient_subCodeToString (solClient_subCode_t subCode);
#
def solClient_subCodeToString(subCode):
    _solClient.solClient_subCodeToString.restype = c_char_p
    _solClient.solClient_subCodeToString.argtypes = [
        solClient_subCode_t
    ]
    return _solClient.solClient_subCodeToString(subCode)


#
# #define SOLCLIENT_ERRORINFO_STR_SIZE (256) /**< The maximum size of error string including terminating NULL character. */
#
SOLCLIENT_ERRORINFO_STR_SIZE = 256


#
#  typedef struct solClient_errorInfo
#  {
#    solClient_subCode_t subCode;                                              /**< A subcode indicating the type of error. */
#    solClient_session_responseCode_t responseCode;                            /**< A response code that is returned for some subcodes; otherwise zero. */
#    char errorStr[SOLCLIENT_ERRORINFO_STR_SIZE];                              /**< An information string for certain types of subcodes (empty string, if not used). */
#  } solClient_errorInfo_t, *solClient_errorInfo_pt; /**< A pointer to a ::solClient_errorInfo structure returned from ::solClient_getLastErrorInfo() .*/
#
class solClient_errorInfo_t(Structure):
    _fields_ = [
        ('subCode', solClient_subCode_t),
        ('responseCode', solClient_session_responseCode_t),
        ('errorStr', (c_char * SOLCLIENT_ERRORINFO_STR_SIZE))
    ]
solClient_errorInfo_pt = POINTER(solClient_errorInfo_t)


#
#  solClient_dllExport solClient_errorInfo_pt
#    solClient_getLastErrorInfo (void);
#
def solClient_getLastErrorInfo():
    _solClient.solClient_getLastErrorInfo.restype = solClient_errorInfo_pt
    return _solClient.solClient_getLastErrorInfo().contents


#
# _logAndRaiseError
#   Log error and raise exception
#
def _logAndRaiseError():
    caller = inspect.stack()[1][3]
    lastErrorInfo = solClient_getLastErrorInfo()
    errorStr = lastErrorInfo.errorStr
    subCodeStr = solClient_subCodeToString(lastErrorInfo.subCode)
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
    if _solClient.solClient_initialize(initialLogLevel, props) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_context_create (solClient_propertyArray_pt props,
#                              solClient_opaqueContext_pt * opaqueContext_p,
#                              solClient_context_createFuncInfo_t * funcInfo_p,
#                              size_t funcInfoSize);
#
def solClient_context_create(props, opaqueContext_p, funcInfo_p, funcInfoSize):
    _solClient.solClient_context_create.restype = solClient_returnCode_t
    _solClient.solClient_context_create.argtypes = [
        solClient_propertyArray_pt,
        POINTER(solClient_opaqueContext_pt),
        POINTER(solClient_context_createFuncInfo_t),
        c_size_t
    ]
    if _solClient.solClient_context_create(props, opaqueContext_p, funcInfo_p, funcInfoSize) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_session_create (solClient_propertyArray_pt props,
#                              solClient_opaqueContext_pt opaqueContext_p,
#                              solClient_opaqueSession_pt * opaqueSession_p,
#                              solClient_session_createFuncInfo_t * funcInfo_p,
#                              size_t funcInfoSize);
#
def solClient_session_create(props, opaqueContext_p, opaqueSession_p, funcInfo_p, funcInfoSize):
    _solClient.solClient_session_create.restype = solClient_returnCode_t
    _solClient.solClient_session_create.argtypes = [
        solClient_propertyArray_pt,
        solClient_opaqueContext_pt,
        POINTER(solClient_opaqueSession_pt),
        POINTER(solClient_session_createFuncInfo_t),
        c_size_t
    ]
    if _solClient.solClient_session_create(props, opaqueContext_p, opaqueSession_p, funcInfo_p, funcInfoSize) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_session_connect (solClient_opaqueSession_pt opaqueSession_p);
#
def solClient_session_connect(opaqueSession_p):
    _solClient.solClient_session_connect.restype = solClient_returnCode_t
    _solClient.solClient_session_connect.argtypes = [
        solClient_opaqueSession_pt
    ]
    if _solClient.solClient_session_connect(opaqueSession_p) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_session_topicSubscribe (solClient_opaqueSession_pt opaqueSession_p,
#                                      const char *topicSubscription_p);
#
def solClient_session_topicSubscribe(opaqueSession_p, topicSubscription_p):
    _solClient.solClient_session_topicSubscribe.restype = solClient_returnCode_t
    _solClient.solClient_session_topicSubscribe.argtypes = [
        solClient_opaqueSession_pt,
        c_char_p
    ]
    if _solClient.solClient_session_topicSubscribe(opaqueSession_p, topicSubscription_p) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_session_topicSubscribeExt (
#                                      solClient_opaqueSession_pt opaqueSession_p,
#                                      solClient_subscribeFlags_t flags,
#                                      const char *topicSubscription_p);
#
def solClient_session_topicSubscribeExt(opaqueSession_p, flags, topicSubscription_p):
    _solClient.solClient_session_topicSubscribeExt.restype = solClient_returnCode_t
    _solClient.solClient_session_topicSubscribeExt.argtypes = [
        solClient_opaqueSession_pt,
        solClient_subscribeFlags_t,
        c_char_p
    ]
    if _solClient.solClient_session_topicSubscribeExt(opaqueSession_p, flags, topicSubscription_p) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_session_topicUnsubscribe (solClient_opaqueSession_pt opaqueSession_p,
#                                        const char *topicSubscription_p);
#
def solClient_session_topicUnsubscribe(opaqueSession_p, topicSubscription_p):
    _solClient.solClient_session_topicUnsubscribe.restype = solClient_returnCode_t
    _solClient.solClient_session_topicUnsubscribe.argtypes = [
        solClient_opaqueSession_pt,
        c_char_p
    ]
    if _solClient.solClient_session_topicUnsubscribe(opaqueSession_p, topicSubscription_p) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_session_topicUnsubscribeExt (solClient_opaqueSession_pt opaqueSession_p,
#                                        solClient_subscribeFlags_t flags,
#                                        const char *topicSubscription_p);
#
def solClient_session_topicUnsubscribeExt(opaqueSession_p, flags, topicSubscription_p):
    _solClient.solClient_session_topicUnsubscribeExt.restype = solClient_returnCode_t
    _solClient.solClient_session_topicUnsubscribeExt.argtypes = [
        solClient_opaqueSession_pt,
        solClient_subscribeFlags_t,
        c_char_p
    ]
    if _solClient.solClient_session_topicUnsubscribeExt(opaqueSession_p, flags, topicSubscription_p) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t
#    solClient_session_disconnect (solClient_opaqueSession_pt opaqueSession_p);
#
def solClient_session_disconnect(opaqueSession_p):
    _solClient.solClient_session_disconnect.restype = solClient_returnCode_t
    _solClient.solClient_session_disconnect.argtypes = [
        solClient_opaqueSession_pt
    ]
    if _solClient.solClient_session_disconnect(opaqueSession_p) != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
#  solClient_dllExport solClient_returnCode_t solClient_cleanup (void);
#
def solClient_cleanup():
    _solClient.solClient_cleanup.restype = solClient_returnCode_t
    if _solClient.solClient_cleanup() != SOLCLIENT_OK.value:
        _logAndRaiseError()


#
# solClient_dllExport extern const char *_solClient_contextPropsDefaultWithCreateThread[]; /* Do not use directly; use SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD */
# #define SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD ((solClient_propertyArray_pt )_solClient_contextPropsDefaultWithCreateThread) /**< Use with ::solClient_context_create() to create a Context in which the automatic Context thread is automatically created and all other properties are set with default values. */
#
SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD = pointer(c_char_p.in_dll(_solClient, '_solClient_contextPropsDefaultWithCreateThread'))
