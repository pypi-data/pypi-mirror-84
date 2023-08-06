from utils.logger_setter import LoggerSetter
from view.application.web_pipper_factory import FlaskPipperFactory
import logging


def run():
    LoggerSetter.set_logger()
    logging.info("Starting app...")
    app = FlaskPipperFactory.get_pipper()
    app.run()


if __name__ == '__main__':
    run()
