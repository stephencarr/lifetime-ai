from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
import json


class EventType(str, Enum):
    USER_MESSAGE = "user_message"
    SYSTEM_MESSAGE = "system_message"
    OBSERVATION = "observation"


class StateKind(str, Enum):
    FACT = "fact"
    PREFERENCE = "preference"
    COMMITMENT = "commitment"
    PROSPECT = "prospect"


class StateStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: EventType
    text: str
    occurred_at: datetime
    metadata: dict[str, Any] | None = None

    def payload(self) -> str:
        return json.dumps(self.metadata or {}, sort_keys=True)


@dataclass(frozen=True)
class StateItem:
    item_id: str
    kind: StateKind
    proposition: str
    source_event_id: str
    source_type: EventType
    occurred_at: datetime
    status: StateStatus = StateStatus.ACTIVE
    confidence: float = 1.0
    sensitivity: str = "normal"
    valid_from: datetime | None = None
    valid_until: datetime | None = None


@dataclass(frozen=True)
class Transition:
    transition_id: str
    event_id: str
    item: StateItem
    operation: str = "upsert"
    reason: str = ""
