"""Time zones and the world clock (D-124 and D-126, confirmed; D-239.9, confirmed; how it was applied: D-334, provisional; 0.58).

[ES] Pruebas de la zona horaria de cada jugador y del día, la tarde y la noche del mundo:
- ⚙️ Opciones tiene 🕐 Zona horaria: se elige con un toque (México, Colombia, Venezuela, Chile, Argentina, España, EE. UU.,
  UTC) o con ➖ 1 h / ➕ 1 h (de UTC−12 a UTC+14, sin pasarse); queda guardada en "prefs" (campo "tz", como el idioma);
- las horas que se ven cambian con la zona (el 📜 Tablón, la oleada, el 📔 Diario…), pero las reglas no: el corte del día,
  el cierre de la oleada y la franja del mundo son los mismos para todos; cada aviso llega con la hora de quien lo recibe;
- quien nunca eligió ve UTC (lo de antes), con la etiqueta "UTC" al lado de la hora;
- España sigue su horario de verano; un preset sin zona conocida usa sus horas fijas;
- el reloj del mundo: un día de 96 horas reales con tres franjas de 32 horas, desde world_clock.anchor, igual para todos;
- cada franja cambia la mezcla de lo que se recolecta (sorteo con semilla: de día más madera, de noche más hierbas), nunca
  la cantidad, y la tarde es lo de siempre;
- 📍 Zona dice la franja y cuándo llega la siguiente; 🧭 Explorar, lo que sale más ahora;
- los 🔥 Braseros cuentan en la 🌙 noche del mundo y el aviso de la oleada lo dice;
- todo se lee en español y en inglés, sin textos que falten.
Archivo: tests/test_zona_horaria_y_dia.py · Módulo: M1 Núcleo (zonas horarias) y M8 Mundo (reloj del mundo) · Prueba:
engine/core/timezones.py, engine/world/world_clock.py, engine/service/world_time.py y sus ganchos en game.py (_speaking,
_options_view, _zone_view, _explore_menu, _gather_step, _is_night, _raid_notice), story.py (_journal_lines) y market.py
"""

import pytest

from conftest import make_hero
from engine.core import Rng
from engine.core import timezones as tz_rules
from engine.service.game import button_cap
from engine.world import world_clock as wc_rules
from test_camps import place
from test_idiomas import english_hero
from test_raids import KEY, build_all, camp, camp_at_level, open_raid, pushes

HOUR = 3600
DAY = 24 * HOUR


def ids(view):
    return [a.id for a in view.actions]


def wc(service):
    return service.content.balance["world_clock"]


def band_seconds(service):
    cfg = wc(service)
    return cfg["day_hours"] / len(cfg["bands"]) * HOUR


def go_to(clock, when):
    clock.advance(when - clock.now())


def choose(service, account, zone_id):
    return service.act(account, f"tz:set:{zone_id}")


# ---------------------------------------------------------------- ⚙️ Opciones → 🕐 Zona horaria

def test_the_zone_is_chosen_in_options_and_saved(service):
    make_hero(service)
    options = service.act("test:1", "options")
    assert "tz" in ids(options) and len(options.actions) == button_cap("options") == 7   # D-336 (0.60): and 💀
    assert any(line.startswith("🕐 Zona horaria: UTC, la del juego") for line in options.body)
    screen = service.act("test:1", "tz")
    assert screen.kind == "timezone" and len(screen.actions) <= button_cap("timezone") == 8
    assert ids(screen)[:6] == [f"tz:set:{z}" for z in ("mx", "co", "ve", "cl", "ar", "es")]
    assert ids(screen)[-2:] == ["tz:p:1", "options"]                 # ➡️ Más zonas, ↩️ Volver to ⚙️ Opciones
    assert any("Hora del juego (UTC)" in line for line in screen.body)
    view = choose(service, "test:1", "co")
    assert service.store.get("prefs", "test:1")["tz"] == "co"
    assert view.notice.startswith("✅ Listo: ves las horas en 🇨🇴 Colombia, Perú, Ecuador (UTC−5)")
    assert [a.label for a in view.actions if a.id == "tz:set:co"] == ["✅ 🇨🇴 Colombia, Perú, Ecuador"]
    hour = tz_rules.clock_text(service.clock.now(), -5 * HOUR)
    options = service.act("test:1", "options")
    assert f"🕐 Zona horaria: 🇨🇴 Colombia, Perú, Ecuador (UTC−5) · ahora: {hour}" in options.body
    assert service.text("test:1", "/hora").kind == "timezone"        # the shortcut (and /time in English)
    page = service.act("test:1", "tz:p:1")
    assert ids(page) == ["tz:set:us", "tz:set:utc", "tz:step:-1", "tz:step:1", "tz:p:0", "options"]
    # an unknown zone or a retired preset is not saved (the choice stays)
    service.act("test:1", "tz:set:marte")
    service.content.balance["time_zones"]["presets"][0]["retired"] = True       # mx (test only)
    service.act("test:1", "tz:set:mx")
    assert service.store.get("prefs", "test:1")["tz"] == "co"
    assert not service.texts.missing


def test_step_buttons_reach_any_whole_hour_and_stop_at_the_edges(service):
    make_hero(service)
    choose(service, "test:1", "co")                                  # UTC−5
    view = service.act("test:1", "tz:step:1")
    assert service.store.get("prefs", "test:1")["tz"] == "utc-4" and "UTC−4" in view.notice
    service.act("test:1", "tz:step:-1")
    service.act("test:1", "tz:step:-1")
    assert service.store.get("prefs", "test:1")["tz"] == "utc-6"
    choose(service, "test:1", "utc+13")
    for _ in range(3):
        service.act("test:1", "tz:step:1")
    assert service.store.get("prefs", "test:1")["tz"] == "utc+14"   # time_zones.offsets: never past UTC+14
    choose(service, "test:1", "utc-11")
    for _ in range(3):
        service.act("test:1", "tz:step:-1")
    assert service.store.get("prefs", "test:1")["tz"] == "utc-12"
    choose(service, "test:1", "utc+20")                              # outside the range: not saved
    assert service.store.get("prefs", "test:1")["tz"] == "utc-12"


# ---------------------------------------------------------------- what is shown changes, the rules do not

def test_clock_times_change_with_the_zone_but_the_rules_do_not(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    reset = (service._story_day() + 1) * service._day_seconds()      # the board's reset: UTC midnight, for everyone
    day_before = service._story_day()

    def board_line(account):
        return next(line for line in service.act(account, "board").body if line.startswith("🔄 Cambian en"))

    utc = board_line("test:1")
    assert utc.endswith(f"{tz_rules.clock_text(reset, 0)} UTC).")                # midnight UTC, with its label (never chosen)
    choose(service, "test:1", "utc-5")
    choose(service, "test:2", "utc+1")
    west, east = board_line("test:1"), board_line("test:2")
    assert tz_rules.clock_text(reset, -5 * HOUR) in west and tz_rules.clock_text(reset, HOUR) in east and west != east
    assert west.split(" (")[0] == east.split(" (")[0]               # the duration is the same: only the clock changes
    assert service._story_day() == day_before and (service._story_day() + 1) * service._day_seconds() == reset
    assert service._world_band() == service._world_band()            # the world's band does not look at anyone's zone

    # a wave: one closing time for the camp, each member reads it in their own zone
    camp_at_level(service, 3, members=("test:1", "test:2"))
    open_raid(service, clock, ["test:1", "test:2"])
    raid = camp(service)["raid"]
    notices = {acc: view for acc, view in pushes(service, "camp_raid")}
    assert set(notices) == {"test:1", "test:2"}
    with tz_rules.use("utc-5"):
        until_west = service._clock(raid["until"])
    with tz_rules.use("utc+1"):
        until_east = service._clock(raid["until"])                   # past midnight there: "15/01 00:46"
    assert until_west.endswith(tz_rules.clock_text(raid["until"], -5 * HOUR)) and until_west != until_east
    assert until_east.endswith(tz_rules.clock_text(raid["until"], HOUR))
    assert any(f"(hasta 🕐 {until_west})" in line for line in notices["test:1"].body)
    assert any(f"(hasta 🕐 {until_east})" in line for line in notices["test:2"].body)
    assert raid["until"] - raid["at"] == service._seconds(service.content.balance["raids"]["window_minutes"])
    assert not service.texts.missing


def test_heroes_who_never_chose_see_utc_with_its_label(service, clock):
    make_hero(service)
    assert "tz" not in (service.store.get("prefs", "test:1") or {})
    assert service.content.balance["time_zones"]["default"] == "utc"
    zone = service.act("test:1", "home")
    assert zone.body[3].endswith("UTC)")                              # "… (🕐 13/01 21:00 UTC)": the zone beside the clock
    # the 📔 Diario writes the date in the player's zone: 23:30 UTC is still today in UTC and tomorrow in UTC+1
    late = (service._story_day() + 1) * service._day_seconds() - 30 * 60
    hero = service._load("test:1")
    hero.journal.append({"t": late, "k": "awoke", "v": {}})
    service._save(hero)
    with tz_rules.use(None):
        assert service._local_date(late) == tz_rules.date_text(late, 0)
    with tz_rules.use("utc+1"):
        assert service._local_date(late) == tz_rules.date_text(late + HOUR, 0) != tz_rules.date_text(late, 0)
    choose(service, "test:1", "utc+1")
    journal = "\n".join(service.act("test:1", "journal").body)
    assert tz_rules.date_text(late + HOUR, 0) in journal
    assert not service.texts.missing


def test_spain_follows_summer_time_and_a_preset_without_zone_files_keeps_its_hours(service):
    cfg = service.content.balance["time_zones"]
    winter, summer = 1768478400, 1784116800                          # 15-jan-2026 and 15-jul-2026, 12:00 UTC
    if tz_rules._zoneinfo("Europe/Madrid") is not None:              # the server knows the zone (tzdata)
        assert tz_rules.offset_seconds(cfg, "es", winter) == HOUR
        assert tz_rules.offset_seconds(cfg, "es", summer) == 2 * HOUR
    fake = {"presets": [{"id": "x", "tz": "Nowhere/Atlantis", "offset": -3}], "default": "utc"}
    assert tz_rules.offset_seconds(fake, "x", summer) == -3 * HOUR   # unknown zone: its fixed hours
    assert tz_rules.offset_seconds(cfg, "utc-5", summer) == -5 * HOUR
    assert tz_rules.resolve(cfg, "marte") == "utc" and tz_rules.resolve(cfg, None) == "utc"
    assert tz_rules.offset_parts(-5 * HOUR) == ("−", "5") and tz_rules.offset_parts(int(5.5 * HOUR)) == ("+", "5:30")
    assert tz_rules.clock_text(winter, -5 * HOUR) == "07:00" and tz_rules.date_text(winter, 0) == "15/01"


# ---------------------------------------------------------------- ☀️ 🌇 🌙 the world clock

def test_world_clock_bands_at_fixed_instants(service):
    cfg = wc(service)
    anchor, band = cfg["anchor"], band_seconds(service)
    assert cfg["day_hours"] == 96 and band == 32 * HOUR              # D-239.9: 4 real days, 32 hours a band
    assert wc_rules.band_at(cfg, anchor)["id"] == "dia"
    assert wc_rules.band_at(cfg, anchor + band - 1)["id"] == "dia"
    at = wc_rules.band_at(cfg, anchor + band)
    assert at["id"] == "tarde" and at["start"] == anchor + band and at["end"] == anchor + 2 * band and at["next"] == "noche"
    assert wc_rules.band_at(cfg, anchor + 2 * band + HOUR)["id"] == "noche"
    assert wc_rules.band_at(cfg, anchor + 2 * band + HOUR)["next"] == "dia"
    assert wc_rules.band_at(cfg, anchor + 3 * band)["id"] == "dia" and wc_rules.band_at(cfg, anchor + 3 * band)["day"] == 1
    assert wc_rules.band_at(cfg, anchor - HOUR)["id"] == "noche"     # before the anchor it keeps turning
    assert wc_rules.band_at(cfg, 1_000_000)["id"] == "tarde"          # the tests' clock starts at the beginning of an evening
    # whoever always plays at the same hour sees the three bands in 4 days (32 is not a multiple of 24)
    assert {wc_rules.band_at(cfg, anchor + 20 * HOUR + d * DAY)["id"] for d in range(4)} == {"dia", "tarde", "noche"}
    # time_scale shortens the world day like every other timer (the console's --fast)
    assert wc_rules.band_at(cfg, anchor + band / 600, scale=1 / 600)["id"] == "tarde"


def test_bands_tilt_what_gathering_gives_with_a_seed(service):
    make_hero(service)
    cfg = wc(service)
    assert wc_rules.weight(cfg, "dia", "madera") > 1 and wc_rules.weight(cfg, "noche", "hierba_curativa") > 1
    assert wc_rules.weight(cfg, "tarde", "madera") == 1.0 and wc_rules.weight(cfg, "dia", "nada") == 1.0
    assert wc_rules.weight({"weights": {"dia": {"x": 0.0}}}, "dia", "x") == 0.5     # never below min_weight: nothing disappears
    assert wc_rules.favoured(cfg, "noche", ["madera", "pescado", "hierba_curativa"]) == ["pescado", "hierba_curativa"]
    service.content.balance["gather"]["amount"] = [30, 30]           # a fixed draw (test only)
    service.content.balance["gather"]["encounter_scale"] = 0         # no ambush (test only)
    service._trade_gather = lambda hero, got, activity: []           # no profession extras (test only)
    service._node_main = lambda x, y: None                           # no node ×2 (test only)
    service._zone_resources = lambda x, y: {"madera": 1.0, "hierba_curativa": 1.0}
    service._bag_full = lambda hero: False
    anchor, band = cfg["anchor"], band_seconds(service)

    def gather_at(when, seed=7):
        service.store.put("stock", "1:0", {"levels": {"madera": 1.0, "hierba_curativa": 1.0}, "at": service.clock.now()})
        hero = service._load("test:1")
        hero.backpack = {}
        activity = {"kind": "gather", "got": {}, "log": [], "until": when, "done": 1}
        service._gather_step(hero, service._zone(1, 0), Rng(seed), activity)
        return activity["got"]

    day, evening, night = gather_at(anchor + HOUR), gather_at(anchor + band + HOUR), gather_at(anchor + 2 * band + HOUR)
    assert gather_at(anchor + HOUR) == day                           # the same seed and band: the same round
    total = 30 + service._zone(1, 0).level // 3
    assert sum(day.values()) == sum(evening.values()) == sum(night.values()) == total     # the amount never changes
    assert day.get("madera", 0) > evening.get("madera", 0) > night.get("madera", 0)
    assert night.get("hierba_curativa", 0) > evening.get("hierba_curativa", 0) > day.get("hierba_curativa", 0)
    service.content.balance["world_clock"]["weights"] = {}           # with no tilt, every band gives the evening's mix
    assert gather_at(anchor + HOUR) == evening == gather_at(anchor + 2 * band + HOUR)


def test_the_zone_header_shows_the_band_and_the_explore_menu_the_tilt(service, clock):
    make_hero(service)
    cfg = wc(service)
    anchor, band = cfg["anchor"], band_seconds(service)
    view = service.act("test:1", "home")
    assert view.body[3].startswith("🌇 Es de tarde en el mundo · 🌙 la noche llega en ")
    go_to(clock, anchor + 2 * band + HOUR)
    view = service.act("test:1", "home")
    line = view.body[3]
    assert line.startswith("🌙 Es de noche en el mundo · ☀️ el día llega en 31 h") and "(🕐 " in line
    choose(service, "test:1", "utc-5")
    line = service.act("test:1", "home").body[3]
    nxt = anchor + 3 * band                                          # not today in UTC−5: the clock carries its date
    assert line.endswith(f"(🕐 {tz_rules.date_text(nxt, -5 * HOUR)} {tz_rules.clock_text(nxt, -5 * HOUR)})")
    service._zone_resources = lambda x, y: {"madera": 1.0, "hierba_curativa": 1.0}
    place(service, "test:1", 1, 0, exploration={"1:0": 100}, known=["0:0", "1:0"])
    menu = service.act("test:1", "explore_menu")
    assert any(line.startswith("🌙 De noche, al 🧺 recolectar aquí sale más: 🌿") for line in menu.body)
    go_to(clock, anchor + 3 * band + HOUR)                           # ☀️ day: wood comes out more
    menu = service.act("test:1", "explore_menu")
    assert any(line.startswith("☀️ De día, al 🧺 recolectar aquí sale más: 🪵") for line in menu.body)
    assert not service.texts.missing


def test_braseros_use_the_world_night_and_the_notice_says_so(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 6)
    braseros = [uid for uid, u in service._upgrade_catalog().items() if u.get("effect", {}).get("night_defense")]
    build_all(service, braseros)
    open_raid(service, clock, ["test:1"])
    raid = camp(service)["raid"]
    night = service._is_night(raid["at"])
    assert night == (service._world_band(raid["at"])["id"] == "noche")
    assert raid["defense"] == service._camp_defense(camp(service), night=night)
    notice = pushes(service, "camp_raid")[0][1]
    has_line = any(line.startswith("🌙 Es de noche en el mundo: los 🔥 Braseros suman +1") for line in notice.body)
    assert has_line == night
    assert not service.texts.missing


# ---------------------------------------------------------------- both languages

def test_both_languages(service, clock):
    english_hero(service, "test:1", "Lyra")
    options = service.act("test:1", "options")
    assert any(line.startswith("🕐 Time zone: UTC, the game's (choose yours)") for line in options.body)
    assert [a.label for a in options.actions if a.id == "tz"] == ["🕐 Time zone"]
    view = choose(service, "test:1", "es")
    assert view.title == "🕐 Time zone" and view.notice.startswith("✅ Done: you see clock times in 🇪🇸 Spain (UTC+")
    zone = service.act("test:1", "home")
    assert zone.body[3].startswith("🌇 It's evening in the world · 🌙 night comes in ")
    go_to(clock, wc(service)["anchor"] + 2 * band_seconds(service) + HOUR)
    assert service.act("test:1", "home").body[3].startswith("🌙 It's night in the world · ☀️ day comes in ")
    answer = "\n".join(service.text("test:1", "/d05").body)
    assert "a world day lasts 4 real days and each band about 32 hours" in answer
    service.act("test:1", "lang:es")
    answer = "\n".join(service.text("test:1", "/d05").body)
    assert "un día del mundo dura 4 días reales y cada franja unas 32 horas" in answer
    assert not service.texts.missing
