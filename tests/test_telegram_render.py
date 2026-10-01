"""Telegram rendering respects limits. [ES] Prueba de que el dibujo en Telegram respeta sus límites."""

from adapters.telegram.render import render_keyboard, render_text
from engine.messaging import Action, View


def test_render_limits_and_rows():
    view = View(kind="x", title="<T>", body=["a" * 5000], actions=[Action(id=f"a{i}", label=str(i)) for i in range(5)])
    text = render_text(view)
    assert len(text) <= 4096 and "&lt;T&gt;" in text
    keyboard = render_keyboard(view)
    assert [len(row) for row in keyboard.inline_keyboard] == [2, 2, 1]


def test_clean_token():
    from adapters.telegram.bot import TOKEN_RE, clean_token
    good = "8786913287:AAH" + "x" * 32
    for raw in (good, f" {good} ", f'"{good}"', f"TELEGRAM_BOT_TOKEN={good}"):
        assert clean_token(raw) == good and TOKEN_RE.match(clean_token(raw))
