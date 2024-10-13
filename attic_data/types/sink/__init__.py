from typing import Any


class Sink:
    def __init__(self):
        pass

    def dump_to_location(self, location: str, data: Any):
        raise NotImplementedError
