"""Draw a neutral View as a Telegram message with inline buttons.

[ES]
Para qué sirve: convertir una vista del motor en texto de Telegram (HTML) y un
teclado de botones de 2 por fila (o las filas que pida la vista, D-189), respetando los límites de Telegram.
Documento de diseño: diseno/01-plataforma/telegram.md; web-y-multiplataforma.md §3.2
Módulo: adaptador de Telegram (M19 del lado del cliente)
Depende de: engine.messaging (View, Action), aiogram (tipos de teclado)
Lo usan: adapters/telegram/bot.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Texto de 4.096 caracteres como máximo; callback_data de 64 bytes como máximo.
    2. No inventa información: solo dibuja lo que trae la vista.
Si cambias esto, revisa:
    - Bot: adapters/telegram/bot.py
    - Pruebas: tests/test_telegram_render.py
"""

from __future__ import annotations

import html

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from engine.messaging import View

MAX_TEXT = 4096
BOT_USERNAME: list[str] = [""]  # set by bot.py at startup (for invite links)
MAX_CALLBACK = 64


def render_text(view: View) -> str:
    """HTML text for a view, truncated to Telegram's limit. [ES] Qué hace: arma el texto del mensaje. La llaman: el bot. Si cambia, afecta: cómo se ve todo en Telegram."""
    parts: list[str] = []
    if view.notice:
        parts.append(f"<i>{html.escape(view.notice)}</i>")
        parts.append("")
    parts.append(f"<b>{html.escape(view.title)}</b>")
    parts.extend(html.escape(line) for line in view.body)
    if view.meta.get("invite_code") and BOT_USERNAME[0]:
        parts.append(f"🔗 https://t.me/{BOT_USERNAME[0]}?start=ref_{view.meta['invite_code']}")
    text = "\n".join(parts)
    if len(text) > MAX_TEXT:
        text = text[: MAX_TEXT - 1] + "…"
    return text


MAX_ROW = 8                     # Telegram shows at most 8 inline buttons in one row


def render_keyboard(view: View) -> InlineKeyboardMarkup | None:
    """Inline keyboard: the view's layout first (D-189), then 2 buttons per row.

    [ES] Qué hace: arma los botones. Si la vista trae "layout" (por ejemplo [5, 1] en las pantallas de cantidad, D-189), las
    primeras filas llevan esa cantidad de botones (como mucho 8, el tope de Telegram): así los botoncitos de cantidad van uno
    al lado del otro y el de volver ocupa una fila entera. El resto, de 2 en 2. La llaman: el bot. Si cambia, afecta: la
    disposición de los botones (tests/test_telegram_render.py)."""
    if not view.actions:
        return None
    buttons = []
    for action in view.actions:
        data = action.id.encode("utf-8")[:MAX_CALLBACK].decode("utf-8", "ignore")
        label = action.label if action.enabled else f"🚫 {action.label}"
        buttons.append(InlineKeyboardButton(text=label, callback_data=data))
    rows: list[list[InlineKeyboardButton]] = []
    for size in view.layout:
        if not buttons:
            break
        size = max(1, min(int(size), MAX_ROW))
        rows.append(buttons[:size])
        buttons = buttons[size:]
    for button in buttons:
        if rows and len(rows[-1]) < 2 and len(rows) > len(view.layout):
            rows[-1].append(button)
        else:
            rows.append([button])
    return InlineKeyboardMarkup(inline_keyboard=rows)
