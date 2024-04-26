import logging
from datetime import datetime
def log_print(text):
    print(text)
    logging.info(f"{datetime.now()}: {text}")
    