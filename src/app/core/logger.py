"""
@file:          core/logger.py
@description:   Logging Configuration
@date:          21 April 2026
@author:        Kalpan Shah
@version:       1.0.0
"""
import os
import logging
import sys
from pythonjsonlogger.json import JsonFormatter

from app.core.config import base_settings, ENV


def setup_logging():
    # 1. Define Formats
    json_format = '%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s'
    #  %(process)d %(env)s
    json_formatter = JsonFormatter(
        json_format,
        static_fields={
            "env": base_settings.Environment.name
        },
        datefmt='%Y-%m-%dT%H:%M:%SZ'  # ISO 8601
    )
    text_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # 2. Configure the ROOT logger
    # This ensures everything (including FastAPI internal logs) goes to stdout as JSON
    root_logger = logging.getLogger()

    if base_settings.Environment == ENV.DEV:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Shared STDOUT Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    root_logger.addHandler(console_handler)

    # 3. Specific Service Configuration Helper
    def add_service_file_handler(service_name: str, filename: str):
        # Note: Temperary file handler - Remove once log aggregator is up
        service_logger = logging.getLogger(service_name)
        file_handler = logging.FileHandler(os.path.join(os.getcwd(), 'logs', filename))
        # Seperate log file by service.
        file_handler.setFormatter(logging.Formatter(text_format))
        # make sure logs write debug level
        service_logger.setLevel(logging.DEBUG)
        service_logger.addHandler(file_handler)

    # create directory if not exists
    if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
        os.makedirs(os.path.join(os.getcwd(), 'logs'))

    # Initialize specific service files
    add_service_file_handler("posts", "posts.log")
    add_service_file_handler("users", "users.log")
    add_service_file_handler("auth", "auth.log")
