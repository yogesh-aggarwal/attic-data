from typing import Any, Callable
from attic_data.core.utils import with_retry

from . import Sink


class SinkPipeline(Sink):
    def __init__(self, sinks: list[Sink]):
        self.sinks = sinks

    def dump_to_location(self, location: str, data: Any):
        for sink in self.sinks:
            sink.dump_to_location(location, data)

    def dump_to_location_safe(self, location: str, data: Any):
        for sink in self.sinks:
            try:
                sink.dump_to_location(location, data)
            except:
                pass
