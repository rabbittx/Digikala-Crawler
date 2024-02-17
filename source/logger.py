
import logging

# TODO add  a proper logger to this module.
def setup_logger():
    """
     Setup logger for the application.

     Returns:
         Logger object
        
    """
    logger = logging.getLogger("DigikalaCrawler")
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Add formatter to console handler
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    return logger

def web_setup_logger():
    logger = logging.getLogger("DigikalaCrawler")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    file_handler = logging.FileHandler(r'archive\logs\web_crawler_logs.log',encoding='utf-8-sig')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger