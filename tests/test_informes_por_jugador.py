"""The player report every 3 hours, card by card with each player's @, and the light telemetry behind it (D-341, D-344).

[ES] Pruebas de lo que pidió el dueño el 24-oct-2026 ("los promedios de jugadores activos con más detalles, quiénes son, con su
arroba, y cuál es el tipo de contenido que más hacen... cuánto juegan y juntan, eso lo quiero por jugador"; "como un reporte
constante de base de datos, para evitar que el servidor se sobrecargue") y de sus respuestas: cada 3 horas, un .txt y un .csv,
el servidor guarda solo 3 días y van todos los que jugaron en 24 h:
- cada botón y cada texto cuenta una vez, por tipo de contenido; minutos con botón y sesiones (pausa de más de 15 minutos);
- nada se escribe por botón: los contadores van al almacén como mucho una vez por minuto;
- las unidades que entran de verdad al recolectar y al despellejar, las peleas, la experiencia y las monedas;
- un informe por tramo de 3 horas, uno solo después de un apagón, y el que no salió se reemplaza (sin avalancha);
- tarjetas con el @ (o "sin @"), el .csv con una fila por jugador, quién dejó de venir, la malla de la 0.62.2 si existe;
- se borra lo suyo de más de 3 días y nunca lo de los jugadores ni el "market_log" del mercado;
- el bot manda los dos archivos y, si falla el segundo, no repite el primero; medir nunca corta una jugada.
Archivo: tests/test_informes_por_jugador.py · Módulo: M20 Administración y telemetría · Prueba: engine/service/telemetry.py
(tracked, action_category, typed_category, TelemetryMixin), adapters/reports.py (due, generate, pending, mark_sent, build,
prune, malla_lines) y adapters/telegram/bot.py (send_reports).
"""

import asyncio
import csv
import io

import pytest
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import SendDocument
from conftest import make_hero
from test_solo_privado import FakeBot

from adapters import reports
from adapters.telegram import bot as tg
from engine.core import MemoryStore
from engine.service import GameService
from engine.service import telemetry
from engine.service.telemetry import KEEP_SECONDS, SLOT_SECONDS, action_category, typed_category

HOUR = 3600


class CountingStore(MemoryStore):
    """A memory store that counts the writes to each namespace."""

    def __init__(self):
        super().__init__()
        self.puts = {}

    def put(self, namespace, key, value):
        self.puts[namespace] = self.puts.get(namespace, 0) + 1
        super().put(namespace, key, value)


def to_slot_start(clock, offset=60):
    """Move the clock to `offset` seconds after the start of the next 3-hour slot."""
    clock.advance(SLOT_SECONDS - clock.now() % SLOT_SECONDS + offset)


def window(service, hours=24, this_slot=False):
    """Every account's counts of the last `hours` (or only of the slot the clock is in), after writing them."""
    service.flush_telemetry()
    now = service.clock.now()
    since = now - now % SLOT_SECONDS if this_slot else now - hours * HOUR
    return service.telemetry_window(since, now + SLOT_SECONDS)


def meadow(service, account="test:1", x=0, y=-1):
    """Put the hero out in the meadow (0, -1), where there is prey."""
    hero = service._load(account)
    hero.x, hero.y = x, y
    hero.remember(x, y)
    service._save(hero)


def fight(service, account="test:1"):
    service.act(account, "explore_menu")
    service.act(account, "hunt")
    service.act(account, "prey")
    for _ in range(60):
        if service.store.get("combat", account) is None:
            break
        service.act(account, "atk")


def test_buttons_and_texts_count_once_by_kind_of_content(service):
    make_hero(service)
    service.act("test:1", "explore_menu")
    service.act("test:1", "gather")
    service.act("test:1", "mkt")
    service.act("test:1", "home")
    service.text("test:1", "/stats")                 # text() calls act() inside: one count, the button's kind
    service.text("test:1", "/ir 1 0")
    service.text("test:1", "hola a todos")           # loose text: a message to the guild
    service.text("test:1", "/minero")                # a profession's screen
    rec = window(service)["test:1"]
    cats = rec["cats"]
    assert cats["explore"] == 1 and cats["gather"] == 1 and cats["market"] == 1 and cats["hero"] == 1
    assert cats["travel"] == 1 and cats["social"] == 1 and cats["craft"] == 1
    assert rec["actions"] == sum(cats.values())
    assert action_category("do:chop:10") == "gather" and action_category("fish") == "gather"
    assert action_category("guide") == "quests" and action_category("guides") == "menus"
    assert action_category("dgo") == "dungeon" and action_category("upact:muralla") == "camp"
    assert action_category("nuevo_boton_que_no_existe") == "menus"
    assert typed_category("/v02") == "market" and typed_category("/r3") == "craft" and typed_category("/rc2") == "explore"
    assert typed_category("/saludar Bram") == "social" and typed_category("/palabra_rara") == "menus"


def test_a_button_in_a_fight_is_fighting(service):
    make_hero(service)
    meadow(service)
    fight(service)
    rec = window(service)["test:1"]
    assert rec["cats"]["fight"] >= 3 and rec["won"] + rec["lost"] + rec["fled"] == 1


def test_active_minutes_and_sessions(service, clock):
    make_hero(service)
    to_slot_start(clock)
    service.act("test:1", "home")
    clock.advance(30)
    service.act("test:1", "hero")                    # the same minute
    clock.advance(5 * 60)
    service.act("test:1", "home")                    # 5 minutes later: the same session
    clock.advance(20 * 60)
    service.act("test:1", "home")                    # after 20 minutes: a new session
    rec = window(service, this_slot=True)["test:1"]
    assert rec["active_minutes"] == 3 and rec["sessions"] == 2 and rec["actions"] == 4


def test_nothing_is_written_per_button_only_once_a_minute(content, clock):
    store = CountingStore()
    service = GameService(content, store, clock, world_seed=12345)
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    store.puts.clear()
    for _ in range(25):
        service.act("test:1", "home")
        service.act("test:2", "hero")
    service.tick()
    assert store.puts.get("telemetry", 0) == 0       # still in memory
    clock.advance(61)
    service.tick()
    assert store.puts.get("telemetry", 0) == 2       # one record per account
    service.act("test:1", "home")
    service.tick()
    assert store.puts.get("telemetry", 0) == 2       # less than a minute since the last write
    clock.advance(61)
    service.tick()
    assert store.puts.get("telemetry", 0) == 3       # only the account that changed


def test_a_restart_keeps_counting_and_the_session_goes_on(content, clock):
    store = MemoryStore()
    first = GameService(content, store, clock, world_seed=12345)
    make_hero(first)
    to_slot_start(clock)
    first.act("test:1", "home")
    first.flush_telemetry()
    second = GameService(content, store, clock, world_seed=12345)    # the bot restarted
    clock.advance(5 * 60)
    second.act("test:1", "hero")
    rec = window(second, this_slot=True)["test:1"]
    assert rec["actions"] == 2 and rec["sessions"] == 1


def test_units_gathered_are_the_ones_that_enter_the_backpack(service, clock):
    make_hero(service)
    before = dict(service._load("test:1").backpack)
    service.act("test:1", "gather")
    service.act("test:1", "do:gather:3")
    for _ in range(90):
        clock.advance(60)
        service.tick()
    after = service._load("test:1").backpack
    entered = {k: after.get(k, 0) - before.get(k, 0) for k in after if after.get(k, 0) > before.get(k, 0)}
    rec = window(service)["test:1"]
    assert entered and rec["items"] == entered        # gathering without the profession learned: still counted
    assert rec["gather_steps"] == 3 and rec["timed"].get("gather", 0) > 0 and rec["xp"] > 0


def test_fights_skins_xp_and_coins(service):
    make_hero(service)
    meadow(service)
    hero = service._load("test:1")
    gold, xp = hero.gold, hero.xp
    for _ in range(4):
        fight(service)
    hero = service._load("test:1")
    rec = window(service)["test:1"]
    assert rec["won"] >= 1 and rec["xp"] == hero.xp - xp
    assert rec["coins_in"] - rec["coins_out"] == hero.gold - gold
    skins = {"carne", "piel"} & set(hero.backpack)
    assert all(rec["items"].get(item) == hero.backpack[item] for item in skins)


def test_a_report_every_3_hours_with_a_card_and_the_at_of_each_player(service, clock):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    service.set_handle("test:1", "@lyra")
    to_slot_start(clock)
    service.act("test:1", "explore_menu")
    service.act("test:1", "explore")
    service.act("test:2", "home")
    to_slot_start(clock, offset=30)
    assert reports.due(service)
    record = reports.generate(service)
    assert record["until"] - record["since"] == SLOT_SECONDS and record["until"] % SLOT_SECONDS == 0
    assert record["txt_name"].startswith("informe-jugadores-") and record["txt_name"].endswith("h.txt")
    assert record["csv_name"].startswith("datos-jugadores-") and record["csv_name"].endswith("h.csv")
    assert record["caption"].startswith("📊 Informe de jugadores · ") and record["caption"].endswith("UTC")
    text = record["txt"]
    assert "@lyra · Lyra · test:1" in text and "sin @ · Bram · test:2" in text
    assert text.index("@lyra · Lyra") < text.index("sin @ · Bram")      # the most active first
    assert "TARJETAS POR JUGADOR" in text and "PROMEDIOS POR JUGADOR ACTIVO" in text and "QUÉ HACEN MÁS" in text
    assert not reports.due(service)                  # built: waiting to go out
    reports.mark_sent(service, record["key"], "txt")
    assert reports.pending(service) is not None       # the .csv is still missing
    reports.mark_sent(service, record["key"], "csv")
    assert reports.pending(service) is None and not reports.due(service)
    clock.advance(SLOT_SECONDS)
    assert reports.due(service)


def test_after_a_downtime_only_one_report_covers_everything(service, clock):
    make_hero(service)
    to_slot_start(clock)
    record = reports.generate(service)
    reports.mark_sent(service, record["key"], "txt")
    reports.mark_sent(service, record["key"], "csv")
    clock.advance(4 * SLOT_SECONDS)                  # 12 hours with the bot off
    assert reports.due(service)
    late = reports.generate(service)
    assert late["since"] == record["until"] and late["until"] - late["since"] == 4 * SLOT_SECONDS
    assert "cubre desde el último que salió" in late["txt"]
    assert not reports.due(service)
    assert len(list(service.store.items("report_out"))) == 2


def test_a_report_that_did_not_go_out_is_replaced_not_piled_up(service, clock):
    make_hero(service)
    to_slot_start(clock)
    first = reports.generate(service)                # Telegram refuses it
    clock.advance(SLOT_SECONDS)
    second = reports.generate(service)
    assert second["since"] == first["since"] and service.store.get("report_out", first["key"]) is None
    assert reports.pending(service)["key"] == second["key"]


def test_the_csv_has_one_row_per_player_and_opens_with_accents(service, clock):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    service.set_handle("test:2", "@bram")
    service.act("test:1", "home")
    service.act("test:2", "hero")
    to_slot_start(clock)
    record = reports.generate(service)
    data = record["csv"]
    assert data.startswith("﻿")
    rows = list(csv.reader(io.StringIO(data.lstrip("﻿"))))
    header = rows[0]
    assert header == reports.csv_header() and len(rows) == 3 and all(len(r) == len(header) for r in rows)
    by_account = {r[0]: dict(zip(header, r)) for r in rows[1:]}
    assert by_account["test:2"]["arroba"] == "@bram" and by_account["test:1"]["heroe"] == "Lyra"
    assert int(by_account["test:2"]["botones_24h"]) >= 1 and "botones_recolectar_3h" in header


def test_who_stopped_coming_is_listed_with_their_at(service, clock):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    service.set_handle("test:2", "@bram")
    clock.advance(2 * 86400)                         # two days later only Lyra plays
    service.act("test:1", "home")
    to_slot_start(clock)
    text = reports.generate(service)["txt"]
    stopped = text.split("DEJARON DE VENIR")[1].split("\n\n")[0]
    assert "@bram · Bram" in stopped and "Lyra" not in stopped


def test_the_mail_section_shows_only_when_the_migration_left_its_record(service, clock):
    make_hero(service)
    to_slot_start(clock)
    # 0.62.2 runs once at start-up and always leaves its record: with nobody holding mail, one line says so
    assert "Nadie tenía piezas de malla" in reports.build(service).txt
    service.store.delete("migrations", "malla_to_leather")
    assert "MALLA CONVERTIDA" not in reports.build(service).txt and reports.malla_lines(service) == []
    service.store.put("migrations", "malla_to_leather", {
        "at": clock.now(), "version": "0.62.2", "other": {},
        "accounts": {"test:1": {"hero": "Lyra", "handle": "@lyra", "pieces": [["malla_1", "cuero_1"]]}}})
    text = reports.build(service).txt
    assert "MALLA CONVERTIDA EN CUERO" in text and "@lyra · Lyra · test:1: piezas 1" in text
    clock.advance(KEEP_SECONDS + 1)                  # only in the reports of the 3 days after the change
    assert reports.malla_lines(service) == []
    clock.advance(-(KEEP_SECONDS + 1))
    service.store.put("migrations", "malla_to_leather", {"accounts": "otro formato"})
    assert "otro formato" in "\n".join(reports.malla_lines(service))


def test_only_the_reports_own_data_older_than_3_days_is_deleted(service, clock):
    make_hero(service)
    service.act("test:1", "home")
    service.flush_telemetry()
    service.store.put("report_snap", str(int(clock.now() // 86400)), {"x": {}})     # a 0.33 daily photo
    service.store.put("reports", "players", {"day": 1, "at": clock.now()})
    service.store.put("market_log", "1", {"trades": 3})
    to_slot_start(clock)
    old = reports.generate(service)
    reports.mark_sent(service, old["key"], "txt")
    reports.mark_sent(service, old["key"], "csv")
    clock.advance(3 * 86400 + SLOT_SECONDS)
    service.act("test:1", "home")
    service.flush_telemetry()
    slots = [rec["slot"] for _, rec in service.store.items("telemetry")]
    assert slots and min(slots) * SLOT_SECONDS >= clock.now() - 3 * 86400 - SLOT_SECONDS
    new = reports.generate(service)
    assert service.store.get("report_out", old["key"]) is None and service.store.get("report_out", new["key"])
    assert list(service.store.items("report_snap")) == [] and service.store.get("reports", "players") is None
    assert service.store.get("market_log", "1") == {"trades": 3} and service._load("test:1") is not None


def test_measuring_never_breaks_a_move(service, monkeypatch):
    make_hero(service)

    def broken(action_id):
        raise RuntimeError("bug")
    monkeypatch.setattr(telemetry, "action_category", broken)
    view = service.act("test:1", "hero")
    assert view.kind == "hero" and service.telemetry_errors() == 1


@pytest.fixture
def reports_chat(monkeypatch):
    monkeypatch.setenv("RPG_REPORTS_CHAT_ID", "-1001234567890")
    tg._reports_chat[0] = None
    tg._report_failed_at[0] = float("-inf")


class CsvRefusingBot(FakeBot):
    """Accepts everything but the .csv document while `refuse_csv` is on."""

    refuse_csv = True

    async def __call__(self, method, request_timeout=None):
        if isinstance(method, SendDocument) and method.document.filename.endswith(".csv") and self.refuse_csv:
            raise TelegramBadRequest(method=method, message="Bad Request: file refused")
        return await super().__call__(method, request_timeout)


def test_the_bot_sends_both_files_and_never_repeats_the_one_that_went_out(service, clock, reports_chat):
    make_hero(service)
    service.act("test:1", "home")
    to_slot_start(clock)
    fake = CsvRefusingBot()
    asyncio.run(tg.send_reports(fake, service))
    sent = [c for c in fake.calls if isinstance(c, SendDocument)]
    assert [c.document.filename.endswith(".txt") for c in sent] == [True]
    assert sent[0].caption.startswith("📊 Informe de jugadores")
    tg._report_failed_at[0] = float("-inf")          # an hour later
    fake.refuse_csv = False
    fake.calls.clear()
    asyncio.run(tg.send_reports(fake, service))
    sent = [c for c in fake.calls if isinstance(c, SendDocument)]
    assert len(sent) == 1 and sent[0].document.filename.endswith(".csv")
    assert reports.pending(service) is None
    fake.calls.clear()
    asyncio.run(tg.send_reports(fake, service))      # nothing new until the next slot
    assert not [c for c in fake.calls if isinstance(c, SendDocument)]
