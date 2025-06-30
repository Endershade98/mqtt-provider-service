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

setup_logging()

def log_func_calls(func, logging_level=logging.INFO):
    """Decorator to log function calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.log(logging_level, f"Calling function: {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.log(logging_level, f"Function {func.__name__} returned: {result}")
        return result
    return wrapper

