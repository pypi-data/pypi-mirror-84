import logging
import logging.handlers
import os
import datetime

_logger = logging.getLogger('')
_logger.setLevel(logging.INFO)  # or use logging.basicConfig( level=logging.DEBUG )

_default_formatter = logging.Formatter('%(asctime)-6s: %(levelname)-8s [%(name)s:%(lineno)d] - %(message)s')


def get_logger(name):
    return logging.getLogger(name)


def set_log_level(level=logging.INFO):
    _logger.setLevel(level)


def log_to_console(formatter=_default_formatter):
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)


# rotating log files: https://pymotw.com/3/logging/
# think of handlers as logging channels/destinations to pipe out msgs
def log_to_file(filename, log_dir=None, file_size=9000000, backups=10,
                formatter=_default_formatter):
    if not log_dir:
        log_dir = os.getcwd()

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if log_dir.endswith('/'):
        log_dir = log_dir[:-1]  # remove last / to make it consistent

    now = datetime.datetime.now()
    filename = filename + "-%04d%02d%02d-%02d.%02d.%02d.log" % \
                          (now.year, now.month, now.day, now.hour, now.minute, now.second)

    file_handler = logging.handlers.RotatingFileHandler(log_dir + '/' + filename,
                                                        maxBytes=file_size, backupCount=backups)
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)

    _logger.info("logging setup for %s in %s ...", filename, log_dir)

    # return the handler in case caller wants to remove this later
    return file_handler


def remover_handler(handler: logging.Handler):
    _logger.removeHandler(handler)
    return _logger.handlers


def get_handlers():
    return _logger.handlers
