"""Security (D-345): the anti-flood guard of the Telegram bot, no reports chat without its variable, and no server data in
the repository.

[ES]
Para qué sirve: comprueba las protecciones de D-345 (25-oct-2026, intento de ataque): el freno FloodGuard (más de
FLOOD_MAX_UPDATES en FLOOD_WINDOW_SECONDS se ignora y el aviso sale como mucho una vez por minuto), que sin
RPG_REPORTS_CHAT_ID no hay chat de informes (el número ya no está en el código) y que el repositorio, que es público, no
tiene tokens de Telegram, claves ni identificadores de Railway.
Lo que prueba: adapters/telegram/bot.py (FloodGuard, report_chats) y todos los archivos del repositorio.
Si falla: alguien subió un dato del servidor o cambió el freno; ver D-345 en diseno/00-vision/decisiones.md.
"""

from __future__ import annotations

import asyncio
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace

from adapters.telegram import bot as tg

ROOT = Path(__file__).resolve().parents[1]


class FakeClock:
    def __init__(self) -> None:
        self.t = 1000.0

    def __call__(self) -> float:
        return self.t


def test_the_guard_lets_a_normal_player_through_and_stops_a_flood(service):
    clock = FakeClock()
    guard = tg.FloodGuard(service, now=clock)
    assert all(guard.allow(7) for _ in range(tg.FLOOD_MAX_UPDATES))        # up to the cap: all in
    assert not guard.allow(7)                                               # one more inside the window: dropped
    assert guard.allow(8)                                                   # other players are not touched
    clock.t += tg.FLOOD_WINDOW_SECONDS + 0.1                                # the window slides: in again
    assert guard.allow(7)


def test_the_slow_down_notice_goes_at_most_once_a_minute(service):
    clock = FakeClock()
    guard = tg.FloodGuard(service, now=clock)
    assert guard.should_notice(7) and not guard.should_notice(7)
    clock.t += tg.FLOOD_NOTICE_SECONDS
    assert guard.should_notice(7)


def test_a_dropped_update_never_reaches_the_handler(service):
    clock = FakeClock()
    guard = tg.FloodGuard(service, now=clock)
    calls = []

    async def handler(event, data):
        calls.append(event)
        return "ok"

    answers = []

    class Button(SimpleNamespace):
        async def answer(self, text=None, show_alert=False):
            answers.append((text, show_alert))

    user = SimpleNamespace(id=42, language_code="es")
    event = Button(from_user=user)
    for _ in range(tg.FLOOD_MAX_UPDATES + 3):
        asyncio.run(guard(handler, event, {}))
    assert len(calls) == tg.FLOOD_MAX_UPDATES
    assert len(answers) == 3                                                # every dropped button is answered (no spinner)
    texts = [text for text, alert in answers if text]
    assert len(texts) == 1 and "rápido" in texts[0]                         # the notice once, in the player's language


def test_no_reports_chat_without_its_variable(monkeypatch):
    monkeypatch.delenv("RPG_REPORTS_CHAT_ID", raising=False)
    tg._reports_chat[0] = None
    assert tg.report_chats() == []
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", "-1001234567890")
    assert tg.report_chats() == [-1001234567890, -1234567890]


def test_the_repository_has_no_secrets_nor_server_ids():
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    token = re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_-]{30,}\b|sk-ant-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|github_pat_\w{20,}")
    railway = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
    found = []
    for name in files:
        path = ROOT / name
        if not path.is_file() or path.suffix in (".png", ".jpg", ".pdf", ".sqlite3", ".pyc"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if token.search(text):
            found.append(f"{name}: token or key")
        for match in railway.findall(text):
            if name.startswith("tests/") and match.startswith("00000000"):
                continue
            found.append(f"{name}: uuid {match[:8]}…")
    assert not found, found
