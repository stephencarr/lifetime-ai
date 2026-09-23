from datetime import datetime, timezone
from io import StringIO

from lifetime_ai.chat import ChatRuntime, RuleBasedLocalExtractor
from lifetime_ai.store import Store
from lifetime_ai.terminal import TerminalChat


def test_terminal_chat_is_presentable_and_exercises_lifecycle(tmp_path):
    inputs = StringIO(
        "I prefer concise answers\n"
        ":state\n"
        "? What do I prefer?\n"
        ":correct claim:chat-fake I prefer detailed answers\n"
        ":help\n"
        ":quit\n"
    )
    output = StringIO()
    with Store(tmp_path / "terminal.sqlite") as store:
        # Seed a stable id so the command parser and correction path are tested
        # without depending on random UUID output from the interactive send path.
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        chat.send("I prefer concise answers", datetime(2026, 9, 23, tzinfo=timezone.utc),
                  "chat-fake")
        TerminalChat(chat, inputs, output).run()

    rendered = output.getvalue()
    assert "LIFETIME AI // LOCAL MEMORY" in rendered
    assert "source:chat-fake" in rendered
    assert "[answered]" in rendered
    assert ":correct ITEM TEXT" in rendered
    assert "bye // state remains on disk" in rendered


def test_terminal_keeps_running_after_bad_correction(tmp_path):
    output = StringIO()
    with Store(tmp_path / "terminal.sqlite") as store:
        chat = ChatRuntime(store, RuleBasedLocalExtractor())
        TerminalChat(chat, StringIO(":correct missing I prefer tea\n:quit\n"), output).run()
    assert "[error] state item does not exist" in output.getvalue()
    assert "bye // state remains on disk" in output.getvalue()
