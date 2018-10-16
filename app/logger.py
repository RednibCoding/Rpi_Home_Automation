from logging import (
    DEBUG,
    Formatter,
    StreamHandler,
    getLogger as _getLogger,
)


LOG_FORMAT = '[%(levelname)s] (%(asctime)s) - PiController - %(message)s\n'


def getLogger():
    log = _getLogger('main')
    handler = StreamHandler()
    handler.setFormatter(Formatter(LOG_FORMAT))
    log.addHandler(handler)
    log.setLevel(DEBUG)
    return log
