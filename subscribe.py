import logging
import logging.config
import settings
from solclient import solclient

logger = logging.getLogger(__name__)


#
# messageReceiveCallback
#
def messageReceiveCallback(opaqueSession_p, msg_p, user_p):
    logger.debug('messageReceiveCallback called')


#
# eventCallback
#
def eventCallback(opaqueSession_p, eventInfo_p, user_p):
    eventInfo = eventInfo_p.contents
    lastErrorInfo = solclient.solClient_getLastErrorInfo()
    subCodeStr = solclient.solClient_subCodeToString(lastErrorInfo.subCode)
    logger.debug('eventCallback called: sessionEvent={}, subCode={}, info_p={}'.format(
        eventInfo.sessionEvent,
        subCodeStr,
        eventInfo.info_p
    ))
    return 0


#
# main()
#
def main():
    logging.config.dictConfig(settings.LOGGING_SUBSCRIBE)

    logger.debug('initializing solClient...')
    solclient.solClient_initialize(initialLogLevel=solclient.SOLCLIENT_LOG_DEBUG)
    logger.info('solClient initialized')

    logger.debug('creating solClient context...')
    context_p = solclient.solClient_opaqueContext_pt()
    contextFuncInfo = solclient.SOLCLIENT_CONTEXT_CREATEFUNC_INITIALIZER
    solclient.solClient_context_create(
        solclient.SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD,
        context_p,
        contextFuncInfo
    )
    logger.info('solClient context created')

    logger.debug('creating solClient session...')
    sessionProps = {
        solclient.SOLCLIENT_SESSION_PROP_HOST: settings.SOLACE_HOST,
        solclient.SOLCLIENT_SESSION_PROP_VPN_NAME: settings.SOLACE_VPN,
        solclient.SOLCLIENT_SESSION_PROP_USERNAME: settings.SOLACE_USERNAME,
    }
    session_p = solclient.solClient_opaqueSession_pt()
    sessionFuncInfo = solclient.SOLCLIENT_SESSION_CREATEFUNC_INITIALIZER
    sessionFuncInfo.rxMsgInfo.callback_p = solclient.solClient_session_rxMsgCallbackFunc_t(messageReceiveCallback)
    sessionFuncInfo.eventInfo.callback_p = solclient.solClient_session_eventCallbackFunc_t(eventCallback)
    solclient.solClient_session_create(
        sessionProps,
        context_p,
        session_p,
        sessionFuncInfo
    )
    logger.info('solClient session created')

    logger.debug('connecting solClient session...')
    solclient.solClient_session_connect(session_p)
    logger.info('solClient session connected')

    logger.debug('disconnecting solClient session...')
    solclient.solClient_session_disconnect(session_p)
    logger.info('solClient session disconnected')

    logger.debug('cleaning up solClient...')
    solclient.solClient_cleanup()
    logger.info('solClient cleaned up')


if __name__ == '__main__':
    main()

