from logging import getLogger, StreamHandler, INFO, Formatter, Logger
from sys import stdout

from helix_events_sdk.event_writer import EventWriter
from helix_events_sdk.events.audit import AuditEvent
from helix_events_sdk.schemas.audit import Audit
from helix_events_sdk.schemas.audit_enums import AuditAction, AuditActionType, ResourceType
from helix_events_sdk.schemas.source import Source


def test_can_send_event(caplog) -> None:  # type: ignore
    caplog.set_level(INFO)
    event = AuditEvent(
        Source.BWELLBACKEND,
        Audit(
            patient_id="1",
            user_id="1",
            user_role="Patient",
            ip_address="192.168.1.1",
            action=AuditAction.READ,
            action_type=AuditActionType.VIEW,
            accessed_resource=ResourceType.DIAGNOSES
        )
    )

    event_writer = EventWriter(get_logger())
    event_writer.write_event(event=event)


def get_logger() -> Logger:
    logger = getLogger(__name__)
    stream_handler: StreamHandler = StreamHandler(stdout)
    stream_handler.setLevel(level=INFO)
    # noinspection SpellCheckingInspection
    formatter: Formatter = Formatter(
        '%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(lineno)d - %(funcName)s: %(message)s'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
