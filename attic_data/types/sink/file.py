import os
from typing import Any, override

from attic_data.core.utils import with_retry

from . import Sink


class FileSink(Sink):
    base_path: str

    def __init__(self, base_path: str = "./"):
        super().__init__()
        self.base_path = os.path.join(os.getcwd(), base_path)

    @override
    @with_retry(3)
    def dump_to_location(self, file_path: str, data: Any):
        # Ensure the file path is absolute
        file_path = os.path.join(self.base_path, file_path)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Serialize the data
        serialized_data = str(data)

        # Write the data to the file
        with open(file_path, "w") as f:
            f.write(serialized_data)
