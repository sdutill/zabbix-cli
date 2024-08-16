from __future__ import annotations

from typing import List
from typing import Optional

from zabbix_cli.models import TableRenderable


class AcknowledgeEventResult(TableRenderable):
    """Result type for `acknowledge_event` command."""

    event_ids: List[str] = []
    close: bool = False
    message: Optional[str] = None


class AcknowledgeTriggerLastEventResult(AcknowledgeEventResult):
    """Result type for `acknowledge_trigger_last_event` command."""

    trigger_ids: List[str] = []
