import json
from typing import Any, override

from .file import FileSink


class JSONSink(FileSink):
    def __init__(self):
        super().__init__()

    @override
    def dump_to_location(self, file_path: str, data: dict[str, Any]):
        if not file_path.endswith(".json"):
            file_path = f"{file_path}.json"
        serialized_data = json.dumps(data, indent=4)
        super().dump_to_location(file_path, serialized_data)
