import os
import logging
import logging.config

# TODO: tests


def configure_only_console(logger_name, level=logging.NOTSET):

    cfg = {
        'version': 1,
        'loggers': {

            # '': {  # root logger
            #     'level': 'NOTSET',
            #     'handlers': [
            #         'notset_console_handler',
            #         'notset_time_rotating_file_handler',
            #     ],
            # },

            logger_name: {
                'level': level,
                'propagate': False,
                'handlers': 'console_handler',
            },
        },

        'handlers': {
            'console_handler': {
                'level': level,
                'formatter': 'generic',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },

            # 'notset_rotating_file_handler': {
            #     'level': 'NOTSET',
            #     'formatter': 'generic',
            #     'class': 'logging.handlers.RotatingFileHandler',
            #     'filename': 'info.log',
            #     'mode': 'a',
            #     'maxBytes': 7000000,
            #     'backupCount': 10
            # },

            # 'notset_time_rotating_file_handler': {
            #     'level': file_level,
            #     'formatter': 'generic',
            #     'class': 'logging.handlers.TimedRotatingFileHandler',
            #     'filename': os.path.join(directory, '%s.time.log' % logger_name),
            #     'when': 'midnight',
            #     'backupCount': 10
            # },

            # 'critical_mail_handler': {
            #     'level': 'CRITICAL',
            #     'formatter': 'generic',
            #     'class': 'logging.handlers.SMTPHandler',
            #     'mailhost': 'localhost',
            #     'fromaddr': 'critical.watch.dog@app.domain.com',
            #     'toaddrs': ['admin1@app.domain.com', 'admin2@app.domain.com'],
            #     'subject': 'Watchdog: critical error in application'
            # }
        },

        'formatters': {
            'generic': {
                'format': '%(asctime)s %(levelname)s:  %(message)s'
            }
        },

    }

    logging.config.dictConfig(cfg)


class Message(object):
    def __init__(self, text, level, logger_names):
        self.text = text
        self.level = level
        self.logger_names = logger_names


class AbstractMessage(object):
    level = None
    logger_names = []

    def __init__(self, text):
        self.text = text


class NoSetMessage(AbstractMessage):
    level = logging.NOTSET


class DebugMessage(AbstractMessage):
    level = logging.DEBUG


class InfoMessage(AbstractMessage):
    level = logging.INFO


class WarningMessage(AbstractMessage):
    level = logging.WARNING


class ErrorMessage(AbstractMessage):
    level = logging.ERROR


class CriticalMessage(AbstractMessage):
    level = logging.CRITICAL


def before(message_generator):
    def decorator(f):
        def wrapper(*args, **kwargs):
            message = message_generator(f, *args, **kwargs)
            log(message)
            result = f(*args, **kwargs)
            return result
        return wrapper
    return decorator


def after(message_generator):
    def decorator(f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            message = message_generator(result, f, *args, **kwargs)
            log(message)
            return result
        return wrapper
    return decorator


def log(message):
    for logger_name in message.logger_names:
        logger = logging.getLogger(logger_name)
        logger.log(message.level, message.text)

