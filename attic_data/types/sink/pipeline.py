from typing import Any

from . import Sink


class SinkPipeline(Sink):
    def __init__(self, sinks: list[Sink]):
        self.sinks = sinks

    def dump_to_location(self, location: str, data: Any):
        for sink in self.sinks:
            sink.dump_to_location(location, data)
