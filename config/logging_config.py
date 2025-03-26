import os
import sys
import logging
from datetime import datetime

def setup_logging():
    log_dir = 'performance_logs'
    os.makedirs(log_dir, exist_ok=True)

    # Create a more comprehensive log format
    log_format = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
    
    # Configure logging to file with DEBUG level
    file_handler = logging.FileHandler(os.path.join(log_dir, 'ai_assistant_full_log.txt'), mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Configure console output with INFO level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))

    # Root logger configuration
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, console_handler]
    )

    return log_dir