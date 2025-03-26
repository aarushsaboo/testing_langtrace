import os
import sys
import logging
from datetime import datetime

def setup_logging():
    log_dir = 'performance_logs'
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join(log_dir, 'ai_assistant_full_log.txt'), mode='a')
        ]
    )

    return log_dir