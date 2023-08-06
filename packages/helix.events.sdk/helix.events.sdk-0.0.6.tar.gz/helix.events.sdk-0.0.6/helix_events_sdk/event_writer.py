from logging import Logger

from cloudevents.http import CloudEvent


class EventWriter:
    def __init__(self, logger: Logger):
        self._logger = logger

    def write_event(self, event: CloudEvent) -> None:
        self._logger.info("sending event")
        self._logger.info(event)
