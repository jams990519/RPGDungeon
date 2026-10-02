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



def test_a_view_layout_puts_small_amount_buttons_in_one_row():
    """D-189: an amount picker's layout [5, 1] gives one row of 5 small buttons and a wide back button; no layout, 2 per row."""
    from engine.messaging import Action, View
    from adapters.telegram.render import render_keyboard
    actions = [Action(id=f"do:explore:{n}", label=str(n)) for n in (5, 10, 20, 40)] + [Action(id="do:explore:max", label="Todo"),
                                                                                       Action(id="explore_menu", label="❌ Cancelar")]
    rows = render_keyboard(View(kind="batch", title="x", actions=actions, layout=[5, 1])).inline_keyboard
    assert [len(r) for r in rows] == [5, 1] and rows[1][0].text == "❌ Cancelar"
    rows = render_keyboard(View(kind="batch", title="x", actions=actions)).inline_keyboard
    assert [len(r) for r in rows] == [2, 2, 2]
    rows = render_keyboard(View(kind="batch", title="x", actions=actions + [Action(id="a", label="a")], layout=[5, 1])).inline_keyboard
    assert [len(r) for r in rows] == [5, 1, 1]
