"""Telegram rendering respects limits. [ES] Prueba de que el dibujo en Telegram respeta sus límites."""

from adapters.telegram.render import render_keyboard, render_text
from engine.messaging import Action, View


def test_render_limits_and_rows():
    view = View(kind="x", title="<T>", body=["a" * 5000], actions=[Action(id=f"a{i}", label=str(i)) for i in range(5)])
    text = render_text(view)
    assert len(text) <= 4096 and "&lt;T&gt;" in text
    keyboard = render_keyboard(view)
    assert [len(row) for row in keyboard.inline_keyboard] == [2, 2, 1]
