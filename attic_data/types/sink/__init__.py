from typing import Any


class Sink:
    def __init__(self):
        pass

    def dump_to_location(self, location: str, data: Any):
        raise NotImplementedError

    def dump_to_location_safe(self, location: str, data: Any):
        try:
            self.dump_to_location(location, data)
        except Exception as e:
            print(f"Failed to dump data: {e}")
            pass
