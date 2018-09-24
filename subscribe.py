import logging
import logging.config
import settings
from solclient import solclient

logger = logging.getLogger(__name__)


#
# main()
#
def main():
    logging.config.dictConfig(settings.LOGGING_SUBSCRIBE)

    logging.debug('initializing solClient...')
    solclient.solClient_initialize(initialLogLevel=solclient.SOLCLIENT_LOG_DEBUG)
    logging.info('solClient initialized')

    logging.debug('creating solClient context...')
    context_p = solclient.solClient_opaqueContext_pt()
    contextFuncInfo = solclient.SOLCLIENT_CONTEXT_CREATEFUNC_INITIALIZER
    solclient.solClient_context_create(
        solclient.SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD,
        context_p,
        contextFuncInfo
    )
    logging.info('solClient context created')

    logging.debug('creating solClient session...')
    sessionProps = {
        solclient.SOLCLIENT_SESSION_PROP_HOST: settings.SOLACE_HOST,
        solclient.SOLCLIENT_SESSION_PROP_VPN_NAME: settings.SOLACE_VPN,
        solclient.SOLCLIENT_SESSION_PROP_USERNAME: settings.SOLACE_USERNAME,
    }
    session_p = solclient.solClient_opaqueSession_pt()
    sessionFuncInfo = solclient.SOLCLIENT_SESSION_CREATEFUNC_INITIALIZER
    solclient.solClient_session_create(
        sessionProps,
        context_p,
        session_p,
        sessionFuncInfo
    )
    logging.info('solClient session created')


if __name__ == '__main__':
    main()

