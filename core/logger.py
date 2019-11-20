import logging
import os
import stat
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
import coloredlogs

class GroupWriteRotatingFileHandler(TimedRotatingFileHandler):
    def _open(self):
        # Rotate the file first.
        f = super()._open()

        # Add group write to the current permissions.
        try:
            currMode = os.stat(self.baseFilename).st_mode
            os.chmod(self.baseFilename, currMode | stat.S_IWGRP)
        except Exception:
            pass
        return f


def load_configuration():
    # load .env file
    APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path=dotenv_path)

    log_file = os.getenv('LOG_FILE_PATH')
    dictConfig({
        'version': 1.0,
        'formatters': {
            'default': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s - %(levelname)-s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'class': 'logging.Formatter',
                'format': "%(asctime)s - %(levelname)-s - %(pathname)s - %(funcName)s - %(lineno)d - ""%(message)s",  # noqa
                'datefmt': "%Y-%m-%d %H:%M:%S"
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': log_file,
                'when': 'midnight',
                'backupCount': 30
            }
        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': False
    })


load_configuration()

logger = logging.getLogger('default')
coloredlogs.install(logger=logger)
