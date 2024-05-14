import logging
import sys

logger = logging.getLogger('labyrinth')     # set log name as labyrinth
logger.setLevel(logging.INFO)

# Create a handler for logging to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)