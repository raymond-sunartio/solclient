LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - [%(filename)s:%(lineno)d] - %(levelname)-8s - %(message)s',
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
            'filename': './logs/solClient.log',
            'maxBytes': 8192,
            'backupCount': 10,
            'encoding': 'utf8',
        },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': './logs/solClient.error.log',
            'maxBytes': 8192,
            'backupCount': 10,
            'encoding': 'utf8',
        },
    },
    'loggers': {
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'info_file_handler', 'error_file_handler'],
    },
}
