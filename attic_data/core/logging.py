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
os.makedirs("logs", exist_ok=True)

log_filename = "attic_data.log"
log_file_path = os.path.join("logs", log_filename)
if os.path.exists(log_file_path):
    os.remove(log_file_path)

file_handler = logging.FileHandler(os.path.join("logs", log_filename))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
