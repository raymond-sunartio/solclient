SOLACE_HOST = ''
SOLACE_VPN = ''
SOLACE_USERNAME = ''

LOGGING_SUBSCRIBE = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(name)s %(levelname)s %(asctime)s %(filename)s:%(lineno)d - %(message)s',
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
