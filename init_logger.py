import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(file_name):
    # Ensure the logging directory exists
    log_dir = 'logging'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure the logger
    logger = logging.getLogger(file_name)
    
    # Only add handler if the logger doesn't already have handlers
    if not logger.handlers:
        log_file = os.path.join(log_dir, f'{file_name}.log')
        max_log_size = 5 * 1024 * 1024  # 5 MB
        backup_count = 3

        handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    return logger