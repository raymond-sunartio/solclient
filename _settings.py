SOLCLIENT_SESSION_PROP_HOST = 'localhost:55555'
SOLCLIENT_SESSION_PROP_VPN_NAME = 'some_vpn'
#SOLCLIENT_SESSION_PROP_USERNAME = 'some_user'
#SOLCLIENT_SESSION_PROP_PASSWORD = 'some_pass'
#SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME = 'AUTHENTICATION_SCHEME_BASIC'
#SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME = 'AUTHENTICATION_SCHEME_CLIENT_CERTIFICATE'
SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME = 'AUTHENTICATION_SCHEME_GSS_KRB'
SOLCLIENT_SESSION_PROP_KRB_SERVICE_NAME = 'HOST'

LOGGING_SUBSCRIBE = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(name)s %(levelname)-8s %(asctime)s %(filename)s:%(lineno)d - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': './logs/subscribe.log',
            'maxBytes': 8192,
            'backupCount': 10,
            'encoding': 'utf8',
        },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': './logs/subscribe.error.log',
            'maxBytes': 8192,
            'backupCount': 10,
            'encoding': 'utf8',
        },
    },
    'loggers': {
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'info_file_handler', 'error_file_handler'],
    },
}

