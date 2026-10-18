"""The team's feedback desk: one message per 💬 Feedback in the reports chat, with its type, priority and steps (D-275).

Pure functions: the engine keeps the notes (GameService.feedback_note / feedback_update), the Telegram bot posts the
message and turns the buttons below into an inline keyboard. Texts are for the team only, in Spanish (like reports.py).

[ES]
Para qué sirve: arma el mensaje de cada 💬 Feedback para el chat del equipo (pedido del dueño, 18-oct-2026: "que los
feedback vengan con el arroba, una descripción clasificada de acuerdo al tipo de problema y las notas del jugador para yo
darle prioridad. Dale botones de acción… hasta cerrar el feedback como que ya está resuelto"). Lleva el tipo que eligió el
jugador (🐞 Error, 💡 Idea, ⚖️ Balance, ❓ No se entiende, 💬 Otro), la prioridad (🔴 🟡 🟢), el paso (🆕 Nuevo → 👀 Visto →
✅ Aprobado → 🔧 En arreglo → ✔️ Resuelto, o ❌ Descartado), el @ del jugador, su héroe, nivel, clase, idioma, dónde estaba,
la versión del juego, su texto y quién tocó cada botón y cuándo.
Documento de diseño: diseno/01-plataforma/informes.md §1.1
Módulo: adaptador (M20 Telemetría y administración)
Depende de: nada (recibe la nota como dict; el número de cuenta "tg:<id>" lo interpreta solo para el enlace al jugador)
Lo usan: adapters/telegram/bot.py (send_reports, on_desk_button), tests/test_feedback_equipo.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (la nota vive en el espacio "feedback" del motor)
Reglas que nunca se rompen:
    1. Solo lo ve el equipo: no pasa por los archivos de idiomas (como el informe de jugadores).
    2. Los datos de un botón miden menos de 64 bytes (límite de Telegram): "fbo:<id>:<op>".
Si cambias esto, revisa: engine/service/game.py (feedback_update y los pasos FEEDBACK_NEXT), el bot y sus pruebas.
"""

from __future__ import annotations

import html
import time
from typing import Any

KIND = {"bug": "🐞 Error", "idea": "💡 Idea", "balance": "⚖️ Balance", "confusing": "❓ No se entiende", "other": "💬 Otro"}
PRIORITY = {"high": "🔴 Alta", "mid": "🟡 Media", "low": "🟢 Baja"}
STATUS = {"new": "🆕 Nuevo", "seen": "👀 Visto", "approved": "✅ Aprobado", "fixing": "🔧 En arreglo",
          "resolved": "✔️ Resuelto", "discarded": "❌ Descartado"}
NEXT_LABEL = {"seen": "👀 Visto", "approved": "✅ Aprobar", "fixing": "🔧 En arreglo", "resolved": "✔️ Resuelto"}
PREFIX = "fbo"


def _who(note: dict[str, Any]) -> str:
    """The player's @ (or a link to their chat when they have no @), then hero, level, class and language."""
    handle = note.get("handle") or ""
    account = str(note.get("account", ""))
    if handle:
        who = html.escape(handle)
    elif account.startswith("tg:"):
        who = f'<a href="tg://user?id={html.escape(account[3:])}">{html.escape(str(note.get("hero", "?")))}</a>'
    else:
        who = html.escape(account or "?")
    return (f"👤 {who} · {html.escape(str(note.get('hero', '?')))}, {html.escape(str(note.get('class_name', note.get('class', '?'))))}, "
            f"nivel {note.get('level', '?')}, {html.escape(str(note.get('lang', '?')))}")


def card(note: dict[str, Any]) -> str:
    """The desk message of one feedback note (HTML): type, priority, step, who, where, version, text and history.

    [ES]
    Qué hace: arma el mensaje del chat de informes de un feedback. Arriba el tipo, la prioridad y el paso, con su número
    (#fb12); después el @ del jugador y su héroe, dónde estaba y la versión; el texto del jugador; y al final quién tocó
    cada botón y cuándo (hora UTC). La llaman: el bot al mandarlo y cada vez que alguien toca un botón (edita el mensaje).
    Si cambia, afecta: lo que lee el equipo.
    """
    kind = KIND.get(note.get("kind", "other"), KIND["other"])
    lines = [f"<b>{kind}</b> · {PRIORITY.get(note.get('priority', 'low'), '')} · {STATUS.get(note.get('status', 'new'), '')}"
             f" · #fb{html.escape(str(note.get('id', '?')))}",
             _who(note)]
    where = note.get("where")
    extra = [f"📍 {html.escape(str(where))}" if where else "", f"v{html.escape(str(note['version']))}" if note.get("version") else ""]
    if any(extra):
        lines.append(" · ".join(part for part in extra if part))
    lines.append(f"💬 «{html.escape(str(note.get('text', '')))}»")
    history = note.get("history") or []
    if history:
        steps = [f"{_step_label(h)} — {html.escape(str(h.get('by', '?')))} {time.strftime('%d/%m %H:%M', time.gmtime(h.get('at', 0)))}"
                 for h in history[-6:]]
        lines.append("🗂️ " + " · ".join(steps))
    return "\n".join(lines)


def _step_label(entry: dict[str, Any]) -> str:
    op = entry.get("op", "")
    if op.startswith("p:"):
        return PRIORITY.get(op[2:], op)
    return STATUS.get(entry.get("status", ""), op)


def buttons(note: dict[str, Any]) -> list[list[tuple[str, str]]]:
    """The desk buttons as rows of (label, callback data): priority, then the next step and ❌; ↩️ Reabrir when closed.

    [ES]
    Qué hace: los botones del mensaje. Fila 1, la prioridad (la elegida lleva •). Fila 2, el paso siguiente (👀 Visto →
    ✅ Aprobar → 🔧 En arreglo → ✔️ Resuelto) y ❌ Descartar. Cerrado (✔️ o ❌): solo ↩️ Reabrir. La llama: el bot.
    Si cambia, afecta: qué puede hacer el equipo con cada feedback (engine: feedback_update).
    """
    fid = str(note.get("id", ""))
    status = note.get("status", "new")
    if status in ("resolved", "discarded"):
        return [[("↩️ Reabrir", f"{PREFIX}:{fid}:reopen")]]
    current = note.get("priority", "low")
    row1 = [(("• " if p == current else "") + label, f"{PREFIX}:{fid}:p:{p}") for p, label in PRIORITY.items()]
    nxt = {"new": "seen", "seen": "approved", "approved": "fixing", "fixing": "resolved"}.get(status)
    row2 = ([(NEXT_LABEL[nxt], f"{PREFIX}:{fid}:next")] if nxt else []) + [("❌ Descartar", f"{PREFIX}:{fid}:discard")]
    return [row1, row2]


def parse(data: str | None) -> tuple[str, str] | None:
    """"fbo:12:next" -> ("12", "next"); "fbo:12:p:high" -> ("12", "p:high"); anything else -> None."""
    parts = (data or "").split(":", 2)
    if len(parts) != 3 or parts[0] != PREFIX or not parts[1].isdigit() or not parts[2]:
        return None
    return parts[1], parts[2]
