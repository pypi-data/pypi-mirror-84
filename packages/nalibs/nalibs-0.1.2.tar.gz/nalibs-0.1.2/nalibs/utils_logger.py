#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging


def intialize_logging(debug):
    """
    Initialize the logging framework.
    """
    # Configure logging.
    root_logger = logging.getLogger()

    formater_base = '%(asctime)s [%(levelname)s]:[%(threadName)s] %(message)s'
    log_formatter = logging.Formatter(formater_base)
    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # Append the logs and overwrite once reached 1MB
    if debug:
        # print("Initialize log debug")
        root_logger.setLevel(logging.DEBUG)

        # Log to file
        # file_handler = RotatingFileHandler(
        #     config_base.LOG_FILE_PATH, maxBytes=1024 * 1024, backupCount=5, encoding=None, delay=0)
        # file_handler.setFormatter(log_formatter)

        root_logger.addHandler(console_handler)
        # root_logger.addHandler(file_handler)
    else:
        # print("Initialize log")
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)
        root_logger.propagate = False

    return root_logger
