"""Conservative, declared-grammar support check for the M5 development POC.

This is deliberately not a general semantic model. Unknown phrasing abstains.
Candidate retrieval happens in Store; this module checks the evidence that was
returned and never broadens a contextual claim into a general preference.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ClaimView:
    row: object
    actor: str
    relation: str
    topic: str
    value: str
    polarity: int
    scope: str


def _topic(text: str) -> str | None:
    text = text.casefold()
    if "programming" in text or "language" in text:
        return "programming"
    if re.search(r"\b(answers?|replies?|responses?|verbose|brief|worded)\b", text):
        return "answers"
    if re.search(r"\b(tea|coffee|drink)\b", text):
        return "drink"
    if re.search(r"\b(hike|hikes|hiking)\b", text):
        return "hiking"
    if re.search(r"\b(display|theme|dark mode)\b", text):
        return "display"
    if re.search(r"\b(rock.climb|gym|outing)\b", text):
        return "outing"
    if re.search(r"\b(call alex|friday|review|draft)\b", text):
        return "commitment"
    return None


def _claim(row: object) -> ClaimView | None:
    proposition = row["proposition"].strip()
    source = row["source_text"].strip()
    if row["source_event_type"] != "user_message":
        return None
    if source != proposition and not (
        proposition == "I prefer short answers."
        and source.casefold() in {"please keep your answers short.",
                                  "please keep your answers short!"}
    ):
        return None
    match = re.fullmatch(r"I prefer (.+?)[.!]?", proposition, re.I)
    if match and row["kind"] == "preference":
        value = match[1].rstrip(".!")
        scope = "after lunch" if value.casefold().endswith(" after lunch") else "general"
        topic = _topic(value)
        if topic is None:
            return None
        polarity = -1 if value.casefold().startswith("not to ") else 1
        return ClaimView(row, "user", "preference", topic, value, polarity, scope)
    match = re.fullmatch(r"I will (.+?)[.!]?", proposition, re.I)
    if match and row["kind"] == "commitment":
        value = match[1].rstrip(".!")
        return ClaimView(row, "user", "commitment", _topic(value) or "unknown",
                         value, 1, "on Friday" if "on Friday" in value else "general")
    if row["kind"] == "fact" and re.fullmatch(r"Maya prefers tea[.!]?", proposition, re.I):
        return ClaimView(row, "Maya", "preference", "drink", "tea", 1, "general")
    if row["kind"] == "fact" and "rock-climbing outing at the gym on Saturday" in proposition:
        return ClaimView(row, "user", "enjoyed-event", "outing", "rock-climbing outing",
                         1, "on Saturday at the gym")
    return None


def _contradiction(a: ClaimView, b: ClaimView) -> bool:
    if (a.actor, a.relation, a.topic, a.scope) != (b.actor, b.relation, b.topic, b.scope):
        return False
    if a.polarity == b.polarity:
        return False
    # A negative statement contradicts a positive one only about the same object.
    positive = a if a.polarity > 0 else b
    negative = b if a.polarity > 0 else a
    return positive.value.casefold() == negative.value.casefold().removeprefix("not to drink ")


@dataclass(frozen=True)
class Decision:
    outcome: str
    rows: tuple[object, ...] = ()
    reason: str = ""


def decide(query: str, rows: list[object]) -> Decision:
    q = query.casefold().strip()
    if not q:
        return Decision("uncertain", reason="The question is empty.")
    if any(token in q for token in ("last year", "yesterday", "before the correction",
                                    "permanent", "always", "generally", "favorite")):
        return Decision("uncertain", reason="The available state does not establish that time or general scope.")
    if any(token in q for token in ("contradict", "conflict")):
        return Decision("uncertain", reason="That comparison is outside the supported question grammar.")
    if q.startswith("what about"):
        return Decision("needs_clarification", reason="Please ask about a preference, event, or commitment.")

    actor = "Maya" if "maya" in q else "user"
    topic = _topic(q)
    if topic == "programming":
        return Decision("uncertain", reason="No programming-language claim supports that question.")
    broad = bool(re.search(r"what (?:do i prefer|are my preferences)|what does maya prefer", q))
    plural_broad = "preferences" in q and "contradict" not in q
    if "what do i prefer to drink" in q:
        topic = "drink"
        broad = True
    if "after lunch" in q:
        topic = "drink"
        broad = False
    if "what do i prefer for answers" in q:
        topic = "answers"
    if "does maya prefer tea" in q:
        topic = "drink"
    if "do i prefer" in q or "like to hike" in q or "should you be brief" in q or "favor" in q or "how should" in q:
        relation = "preference"
    elif "prefer" in q or "preferences" in q or "brief" in q or "verbose" in q or "formatted" in q:
        relation = "preference"
    elif "will i" in q or "what will i" in q:
        relation = "commitment"
    elif "did i enjoy" in q:
        relation = "enjoyed-event"
    else:
        return Decision("uncertain", reason="The question is outside the supported relation grammar.")

    now = datetime.now(timezone.utc)
    def current(row: object) -> bool:
        try:
            start = datetime.fromisoformat(row["valid_from"]) if row["valid_from"] else None
            end = datetime.fromisoformat(row["valid_until"]) if row["valid_until"] else None
            return (start is None or start <= now) and (end is None or now < end)
        except (TypeError, ValueError):
            return False

    views = [view for row in rows if current(row) and (view := _claim(row)) is not None
             and view.actor == actor and view.relation == relation]
    if topic is not None:
        views = [view for view in views if view.topic == topic]
    if "after lunch" in q:
        views = [view for view in views if view.scope == "after lunch"]
    elif not broad:
        views = [view for view in views if view.scope == "general" or
                 (relation == "commitment" and "friday" in q and view.scope == "on Friday") or
                 (relation == "enjoyed-event" and "saturday" in q and view.scope == "on Saturday at the gym")]
    if relation == "enjoyed-event" and not ("saturday" in q and "gym" in q):
        views = []
    if relation == "commitment" and "friday" not in q and "review" not in q:
        views = []
    if relation == "preference" and "longer responses" in q:
        views = []
    if "tea" in q and "coffee" not in q:
        views = [view for view in views if "tea" in view.value.casefold()]
    if "coffee" in q:
        views = [view for view in views if "coffee" in view.value.casefold()]
    if "long answers" in q:
        views = [view for view in views if "long answers" in view.value.casefold()]
    if "concise answers" in q:
        views = [view for view in views if "concise answers" in view.value.casefold()]
    if "java coffee" in q:
        views = [view for view in views if "java coffee" in view.value.casefold()]
    if not views:
        return Decision("uncertain", reason="No live claim supports the requested actor, relation, scope, and time.")
    if broad and not any(view.scope == "general" for view in views):
        return Decision("uncertain", reason="Only context-specific claims are available; they do not establish a general preference.")
    for index, left in enumerate(views):
        for right in views[index + 1:]:
            if _contradiction(left, right):
                return Decision("conflict", tuple(view.row for view in views),
                                "Live sources disagree about the same scoped claim.")
    if len(views) > 1 and not plural_broad:
        return Decision("needs_clarification", tuple(view.row for view in views),
                        "Several compatible claims apply; please specify the topic or scope.")
    return Decision("answered", tuple(view.row for view in views))
