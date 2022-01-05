from logging.config import dictConfig
import logging
import os

if not os.path.exists("./logs"):
    os.mkdir("./logs")

dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        }
    },
    'handlers': {
        'myapp_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': './logs/my_app.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 1,
            'level': 'DEBUG',
            "encoding": "utf8",
            'formatter': 'standard'
        },
    },
    'loggers': {
        'simple': {
            'level': 'DEBUG',
            'handlers': ['myapp_handler']
        }
    },
})

logger = logging.getLogger("simple")
