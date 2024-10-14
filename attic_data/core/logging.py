import os
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(name)s: %(message)s"))
logger.addHandler(console_handler)

# Log to a file
os.makedirs(os.path.join(os.getcwd(), "logs"), exist_ok=True)
os.remove(os.path.join(os.getcwd(), "logs", "attic_data.log"))

file_handler = logging.FileHandler(os.path.join(os.getcwd(), "logs", "attic_data.log"))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
