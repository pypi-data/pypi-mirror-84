import logging
from datetime import datetime


class LoggerSetter(object):
    @classmethod
    def set_logger(cls, logger_type="default"):
        SETTERS[logger_type].set_logger()


class LoggingLoggerSetter(LoggerSetter):
    @classmethod
    def set_logger(cls, logger_type="default"):
        SETTERS[logger_type] = cls
        now = datetime.now()
        curr_time = now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        logging.basicConfig(filename=f"./logs/{curr_time}",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler())


SETTERS = {
    "default": LoggingLoggerSetter
}
