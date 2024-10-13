import os
from typing import Any, override

from . import Sink


class FileSink(Sink):
    def __init__(self):
        super().__init__()

    @override
    def dump_to_location(self, file_path: str, data: Any):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Serialize the data
        serialized_data = str(data)

        # Write the data to the file
        with open(file_path, "w") as f:
            f.write(serialized_data)
