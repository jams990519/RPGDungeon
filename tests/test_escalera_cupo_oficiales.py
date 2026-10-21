"""The settlement ladder, first slice (D-253, D-122; how it was applied: D-327, 0.51): one cap per stage, officers who accept
members, who stops playing frees the place, and the castle's 40 active members.

[ES] Pruebas de la 1.ª parte jugable de la escalera del asentamiento (D-253, confirmada por el dueño el 17-oct-2026; cómo se
aplicó: D-327, provisional):
- un solo cupo por etapa (campamento 10, aldea 15, pueblo 25, ciudad 40, castillo 50), que nunca baja de lo que el
  campamento tenía antes del parche (el piso "cap_floor"), con las 🛖 Cabañas encima, sin sacar a nadie si sobran miembros; el
  nivel del gremio ya no suma; ⏫ Siguiente nivel dice cuántos caben al subir;
- quien espera lugar en el gremio entra solo cuando el cupo sube (al pasar de etapa y el día del parche, D-323);
- los 🤝 asistentes son los oficiales: un asistente acepta o rechaza una solicitud y un miembro común no; antes del campamento,
  un oficial del gremio acepta y un miembro común no;
- quien no juega recibe el aviso a los 25 días y libera su lugar a los 30 (nunca el fundador); si juega después del aviso, la
  cuenta vuelve a empezar; nadie sale por días de antes del parche (tampoco quien no tiene marca de juego); al salir conserva
  su héroe y sus cosas, lo que dio queda, deja de ser asistente, entra quien espera y puede volver a pedir entrar;
- el paso a castillo pide "👥 Activos esta semana: N de 40" y la 🌙 Noche de prueba, 10 vencedores distintos;
- ❓ Dudas y los avisos se leen bien en los dos idiomas.
Archivo: tests/test_escalera_cupo_oficiales.py · Módulo: M9 Frontera y Fundación, M15 Social · Prueba: engine/service/ladder.py
(_base_cap_at, _cap_floor_sweep, _idle_tick, _castle_active_row), engine/service/game.py (_members_cap, _castle_needs,
_lvlup_view, _level_up, _answer_join) y engine/service/gremio.py (_camp_members_view, _gremio_answer, _tell_waiting_room).
"""

from conftest import make_hero
from engine.social import guilds as guild_rules
from test_camps import old_camp_at, place
from test_guilds import join, set_level

KEY = "6:0"
HOUR = 3600.0
DAY = 24 * HOUR


def text(view):
    return "\n".join([view.notice or ""] + list(view.body))


def camp(service):
    return service.store.get("camp", KEY)


def camp_with(service, *names, level=1):
    """An old camp at 6:0 founded by Lyra (test:1), of `level`, with the given members (test:2, test:3…) at its center."""
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    set_level(service, level)
    for n, name in enumerate(names, 2):
        make_hero(service, f"test:{n}", name)
        join(service, f"test:{n}")
        place(service, f"test:{n}", 6, 0)
    service.tick()


def wait(service, *accounts):
    """Put these heroes in the camp's waiting line (D-294), in this order."""
    data = camp(service)
    for account in accounts:
        data.setdefault("waiting", []).append(account)
        service.store.put("camp_wait", account, {"camp": KEY})
    service.store.put("camp", KEY, data)


def ghosts(service, n):
    """Fill the camp with n more members that never play (ids only: the cap counts them)."""
    data = camp(service)
    data["members"] += [f"ghost:{i}" for i in range(n)]
    service.store.put("camp", KEY, data)


def add_guild(service, level):
    service.store.put("guild", KEY, {"name": "Lobos Grises", "camp": KEY, "founder_id": "test:1", "level": level,
                                     "progress": {k: 0 for k in guild_rules.COUNTERS}, "created": 0.0})


def by(out, account, title=None):
    return [v for acc, v in out if acc == account and v.kind == "gremio_news" and (title is None or v.title == title)]


# ---------------------------------------------------------------- 👥 one cap per stage (D-253.1)


def test_one_cap_per_stage_ten_to_fifty(service):
    camp_with(service)
    assert service.content.balance["camps"]["members_by_stage"] == {"campamento": 10, "aldea": 15, "pueblo": 25,
                                                                     "ciudad": 40, "castillo": 50}
    assert camp(service)["cap_floor"] == 2                       # the old count of a level-1 camp, kept as its floor
    for level, cap in ((1, 10), (2, 10), (3, 15), (4, 15), (5, 25), (6, 25), (7, 40), (8, 40), (9, 50)):
        set_level(service, level)
        assert service._members_cap(camp(service)) == cap, level
    hero = service._load("test:1")                               # a camp founded after the patch: no old cap to keep
    service._create_camp(hero, 12, 0, "Nueva Roca")
    service._save(hero)
    fresh = service.store.get("camp", "12:0")
    assert fresh["cap_floor"] == 0 and service._members_cap(fresh) == 10


def test_a_camp_never_gets_less_room_than_before_and_the_guild_no_longer_adds(service):
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    set_level(service, 3)                                        # aldea: 15 now...
    add_guild(service, 6)                                        # ...but its guild of level 6 gave 20 before the patch
    assert "cap_floor" not in camp(service) and service._members_cap(camp(service)) == 20     # never less, not even a second
    service.tick()                                               # the first tick keeps it as the floor (D-64)
    assert camp(service)["cap_floor"] == 20 and service._members_cap(camp(service)) == 20
    add_guild(service, 8)                                        # the guild's level no longer adds room (30 before)
    assert service._members_cap(camp(service)) == 20
    set_level(service, 5)                                        # pueblo: 25
    assert service._members_cap(camp(service)) == 25
    record = service._upgrades(KEY)                              # 🛖 Cabañas still add on top
    record["built"]["cabanas"] = 0.0
    service.store.put("upgrades", KEY, record)
    assert service._members_cap(camp(service)) == 27


def test_more_members_than_the_cap_nobody_leaves_and_nobody_new_gets_in(service):
    camp_with(service)
    ghosts(service, 11)                                          # 12 members in a camp of 10
    service.tick()
    assert len(camp(service)["members"]) == 12 and service._camp_room(camp(service)) == 0
    make_hero(service, "test:9", "Ivo")
    place(service, "test:9", 6, 0)
    view = service.act("test:9", "askjoin")
    assert "está lleno" in view.notice and "test:9" not in (camp(service).get("requests") or [])


def test_next_level_says_how_many_fit_when_the_stage_changes(service):
    camp_with(service, level=2)
    view = service.act("test:1", "lvlup")
    assert "Al subir: 👥 caben 15 (hoy 10)" in text(view)
    set_level(service, 1)
    view = service.act("test:1", "lvlup")
    assert "👥 El cupo (10) crece al pasar a la etapa siguiente" in text(view)


# ---------------------------------------------------------------- ⏳ the waiting line gets in when the cap rises (D-323)


def level_up(service, to):
    """Everything the next level asks is there: its works built and its materials given; Lyra taps ⏫ Subir."""
    record = service._upgrades(KEY)
    for uid in service._lvlup_works(to):
        record["built"][uid] = 0.0
    record["levelup"] = {"to": to, "given": service._lvlup_need(to - 1), "chests": 0}
    service.store.put("upgrades", KEY, record)
    return service.act("test:1", "lvlgo")


def test_who_waits_gets_in_when_the_camp_reaches_a_new_stage(service):
    camp_with(service, level=2)
    ghosts(service, 9)                                           # 10 of 10
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cora")
    wait(service, "test:2", "test:3")
    service.tick()
    assert camp(service)["waiting"] == ["test:2", "test:3"]
    view = level_up(service, 3)                                  # aldea: 15
    assert "Caben 15 miembros" in text(view)
    data = camp(service)
    assert data["level"] == 3 and data["members"][-2:] == ["test:2", "test:3"] and not data["waiting"]
    assert service._load("test:2").camp == KEY and service._load("test:3").camp == KEY


def test_on_the_patch_day_who_waited_gets_in_with_the_new_cap(service):
    camp_with(service, "Bram")                                   # level 1: before the patch, room for 2 (full)
    make_hero(service, "test:3", "Cora")
    wait(service, "test:3")
    data = camp(service)
    data.pop("cap_floor")                                        # a camp the patch has not seen yet
    service.store.put("camp", KEY, data)
    service._cap_floors_set = service._waiting_swept = False     # as if the bot just started with 0.51
    service.tick()
    data = camp(service)
    assert data["cap_floor"] == 2 and "test:3" in data["members"] and service._load("test:3").camp == KEY


# ---------------------------------------------------------------- 🤝 officers accept members (D-253.4, D-269)


def test_an_officer_accepts_or_refuses_a_request_and_a_plain_member_cannot(service):
    camp_with(service, "Bram", "Cora")
    service.act("test:1", "ghelp:test:2")                        # Bram: 🤝 asistente, the camp's officer
    assert "Son los oficiales: aceptan gente" in text(service.act("test:1", "gmembers"))
    make_hero(service, "test:4", "Dax")
    make_hero(service, "test:5", "Eve")
    for account in ("test:4", "test:5"):
        place(service, account, 6, 0)
        service.tick()
        service.act(account, "askjoin")
    out = service.tick()
    assert [v for acc, v in out if acc == "test:2" and v.kind == "camp_join"]       # the request reaches the officer...
    assert not [v for acc, v in out if acc == "test:3" and v.kind == "camp_join"]   # ...not a plain member
    service.act("test:3", "join:6:0:test:4:y")                  # Cora, a plain member: nothing happens
    assert "test:4" not in camp(service)["members"] and "test:4" in camp(service)["requests"]
    service.act("test:2", "join:6:0:test:4:y")                  # Bram, the officer, accepts
    assert "test:4" in camp(service)["members"] and service._load("test:4").camp == KEY
    service.act("test:2", "join:6:0:test:5:n")                  # and refuses Eve
    assert "test:5" not in camp(service)["members"] and "test:5" not in camp(service)["requests"]
    refused = [v for acc, v in service.tick() if acc == "test:5" and v.kind == "camp_answer"]
    assert refused and "Roca Alta no te aceptó esta vez" in refused[0].body[0]


def test_before_the_camp_an_officer_of_the_guild_accepts_and_a_plain_member_cannot(service):
    from test_gremio_desde_el_inicio import join as gremio_join, new_gremio
    for n, name in ((1, "Lyra"), (2, "Bram"), (3, "Cora"), (4, "Dax")):
        make_hero(service, f"test:{n}", name)
    gid, _ = new_gremio(service)
    gremio_join(service, gid, "test:2")
    gremio_join(service, gid, "test:3")
    service.act("test:1", "goff:test:2")                         # Bram: ⭐ officer of the guild
    service.act("test:4", f"greq:{gid}")
    service.act("test:3", f"gans:{gid}:test:4:y")                # Cora, a plain member: nothing happens
    assert "test:4" not in service.store.get("gremio", gid)["members"]
    service.act("test:2", f"gans:{gid}:test:4:y")                # Bram, the officer, accepts
    assert "test:4" in service.store.get("gremio", gid)["members"]


# ---------------------------------------------------------------- 💤 who stops playing frees the place (D-253.3)


def test_warned_at_25_days_released_at_30_never_the_founder(service, clock):
    camp_with(service, "Bram", "Cora")
    clock.advance(24 * DAY)
    service.act("test:3", "home")                                # Cora plays on day 24
    clock.advance(DAY + HOUR)
    out = service.tick()
    warned = by(out, "test:2", "💤 Tu lugar en el campamento")
    assert warned and "Si no juegas en 5 días, liberas tu lugar en Roca Alta" in warned[0].body[0]
    assert warned[0].actions[0].id == "guild"                    # any button keeps the place
    assert not by(out, "test:1", "💤 Tu lugar en el campamento") and not by(out, "test:3", "💤 Tu lugar en el campamento")
    assert "test:2" in camp(service)["members"] and set(camp(service)["idle_warned"]) == {"test:2"}
    members = service.act("test:1", "gmembers")                  # 👥 Miembros: the 💤 line and the mark on Bram
    assert any(line.startswith("/m") and "💤" in line and "Bram" in line for line in members.body)
    assert any("Quien no juega 30 días deja libre su lugar" in line for line in members.body)
    clock.advance(4 * DAY)
    assert not by(service.tick(), "test:2", "💤 Lugar liberado")   # day 29: still in
    clock.advance(DAY)
    out = service.tick()
    data = camp(service)
    assert "test:2" not in data["members"] and service._load("test:2").camp is None
    released = by(out, "test:2", "💤 Lugar liberado")
    assert released and "liberaste tu lugar en Roca Alta" in released[0].body[0]
    told = by(out, "test:1", "💤 Lugar liberado")
    assert told and "Bram" in told[0].body[0]
    assert "test:1" in data["members"] and "test:3" in data["members"]   # the founder never; Cora played on day 24
    clock.advance(30 * DAY)
    service.tick()
    assert "test:1" in camp(service)["members"]                  # 60 days without playing: the founder stays


def test_playing_after_the_warning_starts_the_count_again(service, clock):
    camp_with(service, "Bram")
    clock.advance(25 * DAY + HOUR)
    assert by(service.tick(), "test:2", "💤 Tu lugar en el campamento")
    clock.advance(2 * DAY)
    service.act("test:2", "home")                                # Bram plays
    clock.advance(3 * DAY + HOUR)
    service.tick()
    assert "test:2" in camp(service)["members"] and "test:2" not in (camp(service).get("idle_warned") or {})


def test_nobody_is_released_for_days_before_the_patch(service, clock):
    camp_with(service, "Bram", "Cora")
    data = service.store.get("hero", "test:2")
    data["seen_at"] = 0.0                                        # a hero saved before there was a mark of play
    service.store.put("hero", "test:2", data)
    data = camp(service)
    data.pop("idle_watch", None)                                 # a camp the patch has not scanned yet
    service.store.put("camp", KEY, data)
    service.store.delete("meta", "idle")
    clock.advance(40 * DAY)                                      # Bram and Cora last played 40 days before the patch
    out = service.tick()
    assert not by(out, "test:2") and not by(out, "test:3")
    assert {"test:2", "test:3"} <= set(camp(service)["members"])
    clock.advance(24 * DAY)
    assert not by(service.tick(), "test:2")                      # 24 days after the patch: nothing yet
    clock.advance(DAY + HOUR)
    assert by(service.tick(), "test:2", "💤 Tu lugar en el campamento")   # 25 days after the patch: the warning
    clock.advance(5 * DAY)
    service.tick()
    assert "test:2" not in camp(service)["members"] and "test:3" not in camp(service)["members"]


def test_who_leaves_keeps_everything_stops_being_an_officer_and_who_waits_gets_in(service, clock):
    camp_with(service, "Bram", "Cora")
    service.content.balance["camps"]["members_by_stage"]["campamento"] = 3     # a full camp of 3, for this test
    service.act("test:1", "ghelp:test:2")                        # Bram is an officer
    hero = service._load("test:2")
    hero.backpack["madera"] = 7
    hero.gold = 55
    service._save(hero)
    record = service._upgrades(KEY)
    record["gave"] = {"test:2": {"piedra": 12}}                  # what he gave to the camp's fund
    service.store.put("upgrades", KEY, record)
    make_hero(service, "test:4", "Dax")
    wait(service, "test:4")
    service.tick()
    assert camp(service)["waiting"] == ["test:4"]
    clock.advance(24 * DAY)
    service.act("test:3", "home")
    clock.advance(DAY + HOUR)
    service.tick()
    clock.advance(5 * DAY)
    service.tick()
    data = camp(service)
    assert "test:2" not in data["members"] and "test:2" not in (data.get("helpers") or [])
    assert "test:4" in data["members"] and not data.get("waiting")              # D-323: who waited got in
    hero = service._load("test:2")
    assert hero.camp is None and hero.backpack.get("madera") == 7 and hero.gold == 55
    assert service._upgrades(KEY)["gave"]["test:2"] == {"piedra": 12}          # what he gave stays in the camp
    assert service._gremio_free("test:2", hero)                                 # he can ask to join again
    service.content.balance["camps"]["members_by_stage"]["campamento"] = 10
    place(service, "test:2", 6, 0)
    service.act("test:2", "askjoin")
    assert "test:2" in camp(service)["requests"]


# ---------------------------------------------------------------- 🏰 the castle: 40 who played this week (D-253.2, D-122)


def test_the_castle_asks_for_40_who_played_this_week(service, clock):
    camp_with(service, "Bram", "Cora", level=8)
    add_guild(service, 5)
    service.act("test:2", "home")                               # the three of them play today
    service.act("test:3", "home")
    rows = service._lvlup_rows(camp(service), service._upgrades(KEY), service._load("test:1"))
    active = [(t, ok) for kind, t, ok in rows if "Activos esta semana" in t]
    assert active == [("👥 Activos esta semana: 3 de 40 (jugaron en los últimos 7 días)", False)]
    assert not any("miembros o más" in t for _, t, _ in rows)  # the old "10 members" line is gone
    service.content.balance["ladder"]["castle_active"] = 3
    rows = service._lvlup_rows(camp(service), service._upgrades(KEY), service._load("test:1"))
    assert [ok for _, t, ok in rows if "Activos esta semana" in t] == [True]
    clock.advance(8 * DAY)                                      # a week later only Lyra played
    view = service.act("test:1", "lvlup")
    assert "▫️ 👥 Activos esta semana: 1 de 3" in text(view)
    every = service.act("test:1", "lvlall")
    assert "3 miembros que jugaron en los últimos 7 días" in text(every) and "10 vencedores distintos" in text(every)
    set_level(service, 7)                                       # not on the step before the castle: no such line
    assert not [t for _, t, _ in service._lvlup_rows(camp(service), service._upgrades(KEY)) if "Activos" in t]


def test_the_trial_night_asks_for_10_different_winners(service):
    camp_with(service, "Bram", level=8)
    assert service.content.balance["raids"]["trial"]["min_wins"] == 10
    view = service._trial_view(service._load("test:1"), camp(service))
    assert "hacen falta 10 victorias de miembros distintos" in text(view)


# ---------------------------------------------------------------- ❓ Dudas and the two languages


def test_faq_and_notices_read_well_in_both_languages(service, clock):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")
    english_hero(service, "test:2", "Bram")
    join(service, "test:2")
    service.tick()
    clock.advance(25 * DAY + HOUR)
    out = service.tick()
    warned = by(out, "test:2")
    assert warned and "you free your place in Grey Rock" in warned[0].body[0]
    clock.advance(5 * DAY)
    out = service.tick()
    assert "you freed your place in Grey Rock" in by(out, "test:2")[0].body[0]
    assert "a place was freed in Grey Rock: Bram" in by(out, "test:1")[0].body[0]
    for lang in ("es", "en"):
        with service.texts.use(lang):
            values = service._faq_values()
            stages = service.texts.t("faq.d37.a", **values)
            castle = service.texts.t("faq.d42.a", **values)
            assert "{" not in stages + castle and "10 · 15 · 25 · 40 · 50" in stages and "30" in stages and "40" in castle
    assert values["members_stages"] == "10 · 15 · 25 · 40 · 50" and values["idle_days"] == 30 and values["idle_left"] == 5
    assert values["castle_active"] == 40 and values["trial_winners"] == 10
    assert not service.texts.fallbacks.get("en") and not service.texts.missing
