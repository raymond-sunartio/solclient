import argparse
import logging
import logging.config
import settings
import time

from solclient import solClient
from solclient import solClientMsg

logger = logging.getLogger(__name__)


#
# messageReceiveCallback
#
def messageReceiveCallback(opaqueSession_p, msg_p, user_p):
    logger.debug('message received:')
    solClientMsg.solClient_msg_dump(msg_p, None, 0)
    return solClient.SOLCLIENT_CALLBACK_OK


#
# eventCallback
#
def eventCallback(opaqueSession_p, eventInfo_p, user_p):
    eventInfo = eventInfo_p.contents
    lastErrorInfo = solClient.solClient_getLastErrorInfo()
    subCodeStr = solClient.solClient_subCodeToString(lastErrorInfo.subCode)
    logger.debug('eventCallback called: sessionEvent={}, subCode={}, info_p={}'.format(
        eventInfo.sessionEvent,
        subCodeStr,
        eventInfo.info_p
    ))
    return solClient.SOLCLIENT_CALLBACK_OK


#
# main()
#
def main():
    logging.config.dictConfig(settings.LOGGING_SUBSCRIBE)

    parser = argparse.ArgumentParser(description='Subscribes to a solace topic.')
    parser.add_argument('topic', help='solace topic to subscribe to')
    args = parser.parse_args()
    logger.info('command line args=[{}]'.format(args))

    logger.debug('initializing solClient...')
    solClient.solClient_initialize()
    logger.info('solClient initialized')

    logger.debug('creating solClient context...')
    context_p = solClient.solClient_opaqueContext_pt()
    contextFuncInfo = solClient.SOLCLIENT_CONTEXT_CREATEFUNC_INITIALIZER
    solClient.solClient_context_create(
        solClient.SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD,
        context_p,
        contextFuncInfo
    )
    logger.info('solClient context created')

    logger.debug('creating solClient session...')
    sessionProps = {
        solClient.SOLCLIENT_SESSION_PROP_HOST: settings.SOLCLIENT_SESSION_PROP_HOST,
        solClient.SOLCLIENT_SESSION_PROP_VPN_NAME: settings.SOLCLIENT_SESSION_PROP_VPN_NAME,
        solClient.SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME: settings.SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME,
        solClient.SOLCLIENT_SESSION_PROP_KRB_SERVICE_NAME: settings.SOLCLIENT_SESSION_PROP_KRB_SERVICE_NAME,
    }
    session_p = solClient.solClient_opaqueSession_pt()
    sessionFuncInfo = solClient.SOLCLIENT_SESSION_CREATEFUNC_INITIALIZER
    sessionFuncInfo.rxMsgInfo.callback_p = solClient.solClient_session_rxMsgCallbackFunc_t(messageReceiveCallback)
    sessionFuncInfo.eventInfo.callback_p = solClient.solClient_session_eventCallbackFunc_t(eventCallback)
    solClient.solClient_session_create(
        sessionProps,
        context_p,
        session_p,
        sessionFuncInfo
    )
    logger.info('solClient session created')

    logger.debug('connecting solClient session...')
    solClient.solClient_session_connect(session_p)
    logger.info('solClient session connected')

    logger.debug('subscribing to solClient topic [{}]...'.format(args.topic))
    solClient.solClient_session_topicSubscribeExt(session_p, solClient.SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM, args.topic)
    logger.info('subscribed to solClient topic [{}]'.format(args.topic))

    while True:
        try:
            time.sleep(100)
        except KeyboardInterrupt:
            logger.debug("KeyboardInterrupt detected")
            break

    logger.debug('UNsubscribing to solClient topic [{}]...'.format(args.topic))
    solClient.solClient_session_topicUnsubscribeExt(session_p, solClient.SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM, args.topic)
    logger.info('UNsubscribed to solClient topic [{}]'.format(args.topic))

    logger.debug('disconnecting solClient session...')
    solClient.solClient_session_disconnect(session_p)
    logger.info('solClient session disconnected')

    logger.debug('cleaning up solClient...')
    solClient.solClient_cleanup()
    logger.info('solClient cleaned up')


if __name__ == '__main__':
    main()

