import logging

logger = logging.getLogger("usblock")


def setup_logging(level, to_file=""):
    level = int(level)
    if level > 5:
        level = 5

    level *= 10
    logger.setLevel(level)

    # create console handler and set level to debug
    if to_file:
        handler = logging.FileHandler(to_file)
    else:
        handler = logging.StreamHandler()
    handler.setLevel(level)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - "
                                  "%(levelname)s -%(message)s")
    # add formatter to ch
    handler.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(handler)
    return handler
