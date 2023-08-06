# -*- coding: utf-8 -*-
import inspect
import json
import logging
import traceback
from pathlib import Path


def print_exception(logger):
    def _inner(message=None, log_level="error", use_traceback=True):
        """
        To handle the printing of the exception message when one occurred. Particularly
        useful when catching errors and want to add debug information on the same
        time.
        """
        # set the available levels

        logging_function_dict = {
            "info": logger.info,
            "warning": logger.warning,
            "error": logger.error,
            "critical": logger.critical,
            "exception": logger.exception,
        }

        logging_function = logging_function_dict.get(log_level, logger.error)

        if use_traceback:
            # get the traceback
            trace = traceback.format_exc()
        else:
            trace = ""

        # if not message provided, get the traceback of errors to be a little more
        # useful for the developer
        if message is not None:
            mess = "\n".join([trace, message])
        else:
            # else use message provided by developer
            mess = trace

        # show error in the logger
        logging_function(mess)

        # return the message
        return mess

    return _inner


class OutflowLogger:
    """Setup automatically a logger instance using the name of the module where the logger module is imported

    This class avoids repeating this piece of code: `logger = logging.getLogger(__name__)`
     each time a logger is needed
    """

    @property
    def logger(self):
        calling_module = inspect.currentframe().f_back
        calling_module_name = calling_module.f_globals["__name__"]
        logger_instance = logging.getLogger(calling_module_name)
        logger_instance.print_exception = print_exception(logger_instance)
        return logger_instance

    @property
    def default_config(self):
        # get the default logger config
        with open(Path(__file__).parent / "config.json") as log_config_file:
            return json.load(log_config_file)
