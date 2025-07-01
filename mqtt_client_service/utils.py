import logging
from functools import wraps
import paho.mqtt.client as mqtt

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("subscriber.log"),  # Log to a file
            logging.StreamHandler()  # Log to console
        ]
    )

# Initialize logging
logger = setup_logging()

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Calling function: {func.__name__} with args: {args} and kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.exception(f"Exception in function {func.__name__}: {e}")
            raise
    return wrapper