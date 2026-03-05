
import os
import logging

logger = None
LOG_PATH = f"/scratch/work/{os.environ.get('USER', '')}/.ondemand/slurm_monitor/log.log"

def get_logger() -> logging.Logger:
    global logger
    if logger is not None:
        return logger
    logger = logging.getLogger("slurm_monitor")
    logger.setLevel(logging.INFO)
    os.path.dirname(LOG_PATH) and os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    # Avoid duplicate file handlers for the same file
    if not any(isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', None) == LOG_PATH for h in logger.handlers):
        file_handler = logging.FileHandler(LOG_PATH)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    # Always add a console handler if not present
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

# Usage:
# from logger import get_logger
# logger = get_logger("/path/to/logfile.log")
