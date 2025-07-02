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

def log_func_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.info(f"Calling function: {func.__name__} with args: {args} and kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logging.info(f"Function {func.__name__} returned: {result}")
            return result
        except Exception as e:
            logging.exception(f"Exception in function {func.__name__}: {e}")
            raise
    return wrapper