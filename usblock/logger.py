import logging

logger = logging.getLogger("usblock")


def setup_logging(level, to_file=""):
    if level > 5:
        level = 5

    level *= 10
    logger.setLevel(level)

    # create console handler and set level to debug
    if to_file:
        h = logging.FileHandler(to_file)
    else:
        h = logging.StreamHandler()
    h.setLevel(level)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - "
                                  "%(levelname)s -%(message)s")
    # add formatter to ch
    h.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(h)

