"""⚙️ Opciones and automatic fights in batches (D-114).

[ES] Pruebas de ⚙️ Opciones y las peleas automáticas: la pantalla tiene 4 botones como mucho y lo que se cambia queda
guardado; el menú de abajo suma ⚙️ Opciones (6 como mucho) y /opciones la abre. Con ✋ Manual (lo de siempre) el lote se
corta en la pelea. Con ⚔️ Automática el héroe pelea solo: si gana, el lote sigue; si pierde o su vida queda bajo el límite,
el lote se corta; el resumen cuenta las peleas y el bot avisa una sola vez por lote (también con el chat cerrado). Las
pociones solo se usan si se permite. El Guardián y las defensas del campamento nunca van solos. Cazar en lote cuesta 2 ⚡ por
presa y se corta bien. Los héroes guardados antes cargan con las opciones por defecto. Ningún texto falta.
"""

from conftest import make_hero
from engine.combat import choose_action, make_combat
from engine.hero import Hero, hero_stats
from test_boss import _to_lair
from test_camps import place
from test_hunt import wild
from test_raids import camp_at_level, open_raid

MINUTE = 60


def ids(view):
    return [a.id for a in view.actions]


def max_hp(service, hero):
    return hero_stats(service._kit(hero), hero.level)["max_hp"]


def ready(service, account="test:1", level=1, auto=True, hp=1.0, **extra):
    """A hero in a wild zone next to the Claro, with full energy, its life at `hp` of the max and ⚔️ automatic fights."""
    make_hero(service, account, "Lyra")
    x, y = wild(service)
    place(service, account, x, y, level=level, **extra)
    hero = service._load(account)
    hero.hp = max(1, int(max_hp(service, hero) * hp))
    service._save(hero)
    if auto:
        service.act(account, "opt:fights")
        assert service._load(account).options["fights"] == "auto"
    return hero


def pushes_for(service, account):
    return [view for acc, view in service.tick() if acc == account]


def run_batch(service, clock, account, minutes, steps):
    """Advance the clock one step at a time, calling tick() like the bot does; return the pushes for the account."""
    out = []
    for _ in range(steps):
        clock.advance(minutes * MINUTE)
        out += pushes_for(service, account)
    return out


def fake_play_out(result, hp=None, calls=None):
    """A stand-in for engine.combat.auto.play_out with a fixed outcome (and, optionally, life left as a share of the max)."""
    def play(state, hero, class_def, ctx, *, attentive=True, use_items=True, max_rounds=None, on_hit=None):
        if calls is not None:
            calls.append(use_items)
        state["outcome"] = result
        state["log"] = []
        if result == "victory":
            state["enemy"]["hp"] = 0
        if result == "defeat":
            hero.hp = 0
        if hp is not None:
            hero.hp = max(1, int(hero_stats(class_def, hero.level)["max_hp"] * hp))
        return 1
    return play


# ---------------------------------------------------------------- the screen, the menu and the command

def test_options_screen_has_four_buttons_and_toggles_persist(service):
    make_hero(service)
    view = service.act("test:1", "options")
    assert view.kind == "options" and len(view.actions) <= 4
    assert ids(view) == ["opt:fights", "opt:retreat", "opt:potions", "home"]
    assert view.actions[0].label == "☑️ Peleas automáticas"            # D-178: gray check = off (✋ manual)
    assert "30 %" in view.actions[1].label and view.actions[2].label == "✅ Pociones"   # green check = on
    assert "✅ activo" in "\n".join(view.body)
    view = service.act("test:1", "opt:fights")
    assert view.actions[0].label == "✅ Peleas automáticas" and view.notice
    assert service.store.get("hero", "test:1")["options"]["fights"] == "auto"
    for expected in (50, 70, 30):                       # 30 → 50 → 70 → 30 (D-119: 30 by default)
        view = service.act("test:1", "opt:retreat")
        assert f"{expected} %" in view.actions[1].label
        assert service.store.get("hero", "test:1")["options"]["retreat"] == expected
    view = service.act("test:1", "opt:potions")
    assert view.actions[2].label == "☑️ Pociones" and service.store.get("hero", "test:1")["options"]["potions"] is False
    again = service.act("test:1", "options")               # saved: the screen reads it back
    assert again.actions[0].label == "✅ Peleas automáticas" and again.actions[2].label == "☑️ Pociones"
    assert service.act("test:1", "opt:nothing").kind == "options"      # an unknown option changes nothing
    assert service.act("test:1", "home").kind == "zone"
    assert not service.texts.missing


def test_bottom_menu_and_command(service):
    make_hero(service)
    menu = service.menu()
    assert len(menu) <= 6 and menu[-1].id == "options" and menu[-1].label == "⚙️ Opciones"
    assert service.commands()["/opciones"] == "options"
    assert service.act("test:1", service.commands()["/opciones"]).kind == "options"


def test_telegram_bottom_keyboard_fits_six_buttons(service):
    from adapters.telegram.bot import menu_keyboard
    keyboard = menu_keyboard(service)
    assert [len(row) for row in keyboard.keyboard] == [2, 2, 2]        # 3 short rows on a phone (D-117: 📖 Historia is the 6th)
    assert keyboard.keyboard[-1][-1].text == "⚙️ Opciones"


def test_options_can_change_during_a_batch_but_not_in_combat(service, clock):
    ready(service, auto=False)
    service.act("test:1", "do:explore:5")
    assert service.act("test:1", "options").kind == "options"          # busy exploring: still allowed
    assert service.act("test:1", "opt:fights").kind == "options"
    assert service._load("test:1").activity is not None
    hero = service._load("test:1")
    eid = next(e for e, d in service.content.enemies.items() if not d.get("boss"))
    service.store.put("combat", "test:1", make_combat(eid, service.content.enemies[eid], 1, service._kit(hero), 1))
    assert service.act("test:1", "options").kind == "combat"           # mid-fight, nothing else


def test_old_heroes_load_with_the_default_options(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    del data["options"]
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.options == {}
    assert service._option(hero, "fights") == "manual" and service._option(hero, "retreat") == 30
    assert service._option(hero, "potions") is True
    hero.options = {"fights": "???", "retreat": 42}         # a value that no longer exists falls back too
    assert service._option(hero, "fights") == "manual" and service._option(hero, "retreat") == 30
    view = service.act("test:1", "options")
    assert view.actions[0].label.startswith("☑️")
    assert Hero.from_dict(service.store.get("hero", "test:1")).options == {}


# ---------------------------------------------------------------- batches: manual and automatic

def test_manual_mode_still_stops_the_batch_at_a_fight(service, clock):
    ready(service, auto=False)
    service.act("test:1", "do:explore:20")
    pushes = []
    for _ in range(20):
        clock.advance(10 * MINUTE)
        pushes += pushes_for(service, "test:1")
        if service.store.get("combat", "test:1"):
            break
    assert service.store.get("combat", "test:1") is not None          # the fight waits for the player
    assert service._load("test:1").activity is None
    assert len(pushes) == 1 and pushes[0].kind == "combat"
    assert "⚔️ Algo te interrumpió." in pushes[0].notice and "peleas automáticas" not in pushes[0].notice
    assert not service.texts.missing


def test_auto_mode_fights_and_the_batch_goes_on_with_one_push(service, clock):
    hero = ready(service, level=30)
    kills, energy = hero.kills, hero.energy
    view = service.act("test:1", "explore")
    assert any("tu héroe la pelea solo" in line for line in view.body)
    service.act("test:1", "do:explore:20")
    pushes = run_batch(service, clock, "test:1", 10, 22)
    hero = service._load("test:1")
    won = hero.kills - kills
    assert won >= 1 and service.store.get("combat", "test:1") is None and hero.activity is None
    assert len(pushes) == 1                                 # one message for the whole batch, not one per fight
    notice = pushes[0].notice
    assert "Exploraste 20 veces" in notice                  # the batch did not stop at the first fight
    assert f"{won} {'pelea automática' if won == 1 else 'peleas automáticas'}: {won} {'ganada' if won == 1 else 'ganadas'}" in notice
    assert "experiencia" in notice
    assert hero.energy < energy
    assert not service.texts.missing


def test_auto_fights_also_happen_with_the_chat_closed(service, clock):
    ready(service, level=30)
    service.act("test:1", "do:explore:20")
    clock.advance(5 * 3600)                                 # away: no tick, no button
    view = service.view("test:1")
    assert "peleas automática" in view.notice or "pelea automática" in view.notice
    assert "Exploraste 20 veces" in view.notice and service._load("test:1").activity is None


def test_auto_batch_stops_on_defeat(service, clock, monkeypatch):
    monkeypatch.setattr("engine.service.game.play_out", fake_play_out("defeat"))
    hero = ready(service, gold=1000)
    service.act("test:1", "do:hunt:10")                     # every prey is a fight
    pushes = run_batch(service, clock, "test:1", 16, 6)
    hero = service._load("test:1")
    assert hero.downed and hero.hp == 1 and hero.gold == 900 and hero.activity is None
    assert service.store.get("combat", "test:1") is None
    assert len(pushes) == 1 and "1 perdida" in pushes[0].notice and "te venció en una pelea automática" in pushes[0].notice
    assert hero.energy == 48                                # only the first prey was paid
    assert not service.texts.missing


def test_auto_batch_stops_when_life_drops_under_the_limit(service, clock, monkeypatch):
    monkeypatch.setattr("engine.service.game.play_out", fake_play_out("victory", hp=0.4))
    ready(service)
    service.act("test:1", "opt:retreat")                    # 30 → 50 (D-119: 30 by default)
    service.act("test:1", "do:hunt:10")
    pushes = run_batch(service, clock, "test:1", 16, 6)
    hero = service._load("test:1")
    assert hero.activity is None and not hero.downed and hero.kills == 1
    assert len(pushes) == 1 and "1 ganada" in pushes[0].notice and "por debajo del 50 %" in pushes[0].notice
    # With the limit at 30 %, the same fight lets the batch go on.
    monkeypatch.setattr("engine.service.game.play_out", fake_play_out("victory", hp=0.4))
    hero.hp = max_hp(service, hero)
    service._save(hero)
    service.act("test:1", "opt:retreat")
    service.act("test:1", "opt:retreat")                    # 50 → 70 → 30
    assert service._option(service._load("test:1"), "retreat") == 30
    service.act("test:1", "do:hunt:4")
    pushes = run_batch(service, clock, "test:1", 16, 3)
    assert service._load("test:1").kills == 3 and len(pushes) == 1 and "2 ganadas" in pushes[0].notice


def test_a_fight_with_life_already_low_waits_for_the_player(service, clock):
    ready(service, hp=0.01, downed=True)                    # downed: life comes back very slowly, it stays under 50 %
    service.act("test:1", "do:explore:20")
    pushes = []
    for _ in range(20):
        clock.advance(10 * MINUTE)
        pushes += pushes_for(service, "test:1")
        if service.store.get("combat", "test:1"):
            break
    assert service.store.get("combat", "test:1") is not None and service._load("test:1").activity is None
    assert len(pushes) == 1 and pushes[0].kind == "combat" and "no pelea solo" in pushes[0].notice


def test_a_stuck_auto_fight_is_left_without_reward_or_penalty(service, clock, monkeypatch):
    monkeypatch.setattr("engine.service.game.play_out", fake_play_out("fled"))
    hero = ready(service)
    gold, kills = hero.gold, hero.kills
    service.act("test:1", "do:hunt:4")
    pushes = run_batch(service, clock, "test:1", 16, 3)
    hero = service._load("test:1")
    assert hero.gold == gold and hero.kills == kills and not hero.downed and hero.activity is None
    assert len(pushes) == 1 and "1 sin terminar" in pushes[0].notice


def test_the_real_policy_finishes_every_fight(service):
    """play_out always ends: a win, a defeat or, after auto_fight.max_rounds, "fled"."""
    from engine.combat import play_out
    make_hero(service)
    hero = service._load("test:1")
    kit = service._kit(hero)
    for eid, edef in list(service.content.enemies.items())[:6]:
        hero.hp = max_hp(service, hero)
        state = make_combat(eid, edef, edef["level_min"], kit, 7)
        rounds = play_out(state, hero, kit, service.ctx, max_rounds=5)
        assert state["outcome"] in ("victory", "defeat", "fled") and rounds <= 5


# ---------------------------------------------------------------- potions

def test_policy_uses_belt_items_only_if_allowed(service):
    make_hero(service)
    hero = service._load("test:1")
    kit = dict(service._kit(hero))
    kit["abilities"] = [a for a in kit["abilities"] if a["kind"] != "heal"]     # no healing ability to pick first
    eid = next(e for e, d in service.content.enemies.items() if not d.get("boss"))
    state = make_combat(eid, service.content.enemies[eid], 1, kit, 3)
    full = max_hp(service, hero)
    hero.hp = int(full * 0.2)
    hero.belt = {"pocion_vida": 2, "venda": 1}
    assert choose_action(state, hero, kit, service.ctx, use_items=True) == {"type": "item", "item_id": "pocion_vida"}
    assert choose_action(state, hero, kit, service.ctx, use_items=False)["type"] != "item"
    hero.belt = {"venda": 1}                                # bandages only when attentive (the automatic fights are)
    assert choose_action(state, hero, kit, service.ctx, use_items=True) == {"type": "item", "item_id": "venda"}
    assert choose_action(state, hero, kit, service.ctx, attentive=False, use_items=True)["type"] != "item"
    hero.belt = {"pocion_vida": 1, "pocion_mayor": 1}       # missing 80 %: the big potion first
    assert choose_action(state, hero, kit, service.ctx)["item_id"] == "pocion_mayor"
    hero.hp = full                                          # full life: no item
    assert choose_action(state, hero, kit, service.ctx)["type"] != "item"


def test_the_potions_option_reaches_the_fight(service, clock, monkeypatch):
    calls = []
    monkeypatch.setattr("engine.service.game.play_out", fake_play_out("victory", calls=calls))
    ready(service)
    service.act("test:1", "do:hunt:4")
    run_batch(service, clock, "test:1", 16, 1)
    service.act("test:1", "stop")
    service.act("test:1", "opt:potions")
    service.act("test:1", "do:hunt:4")
    run_batch(service, clock, "test:1", 16, 1)
    assert calls[0] is True and calls[-1] is False


# ---------------------------------------------------------------- never alone

def test_the_guardian_and_raids_are_never_automatic(service, clock):
    make_hero(service)
    service.act("test:1", "opt:fights")
    _to_lair(service)
    view = service.act("test:1", "boss")
    assert view.kind == "combat" and service.store.get("combat", "test:1")["outcome"] is None
    hero = service._load("test:1")
    state = service.store.get("combat", "test:1")
    activity = {"kind": "explore", "done": 1, "log": [], "got": {}}
    lines = service._batch_fight(hero, activity, "!")       # even inside a batch it would wait for the player
    assert lines[-1] == "!" and service.store.get("combat", "test:1") == state and "fights" not in activity
    service.store.delete("combat", "test:1")
    eid = next(e for e, d in service.content.enemies.items() if not d.get("boss"))
    raid_state = make_combat(eid, service.content.enemies[eid], 1, service._kit(hero), 5)
    raid_state["raid"] = {"camp": "6:0", "at": 0}
    service.store.put("combat", "test:1", raid_state)
    assert service._batch_fight(hero, activity, "!")[-1] == "!" and service.store.get("combat", "test:1")["outcome"] is None


def test_defending_the_camp_is_a_manual_fight(service, clock):
    make_hero(service)
    camp_at_level(service, 5)
    service.act("test:1", "opt:fights")
    open_raid(service, clock, ("test:1",))
    view = service.act("test:1", "defend")
    assert view.kind == "combat" and service.store.get("combat", "test:1")["outcome"] is None


# ---------------------------------------------------------------- hunting in batches

def test_manual_hunting_stays_one_prey_at_a_time(service):
    hero = ready(service, auto=False)
    view = service.act("test:1", "hunt")
    assert view.actions[0].id == "prey" and "Buscar presa" in view.actions[0].label
    refused = service.act("test:1", "do:hunt:4")
    assert "⚙️ Opciones" in refused.notice and service._load("test:1").energy == hero.energy
    assert service._load("test:1").activity is None
    assert service.act("test:1", "prey").kind == "combat"           # one prey, fought by hand, as before


def test_auto_hunting_goes_in_batches_of_two_energy_per_prey(service, clock):
    hero = ready(service, level=30)
    kills = hero.kills
    view = service.act("test:1", "hunt")
    assert view.actions[0].label == "🏹 Cazar en lote" and len(view.actions) <= 4
    amounts = service.act("test:1", "prey")
    assert amounts.kind == "batch" and len(amounts.actions) <= 4 and amounts.title == "🏹 Cazar en lote"
    assert ids(amounts)[:2] == ["do:hunt:4", "do:hunt:10"] and "⚡ 4 · ⏱️ 32 min" == amounts.actions[0].label
    assert ids(service.act("test:1", "amt:hunt:1"))[-2:] == ["do:hunt:max", "amt:hunt:0"]
    started = service.act("test:1", "do:hunt:4")
    assert started.kind == "activity" and service._load("test:1").energy == 48     # the first prey is paid now
    assert service._load("test:1").activity["kind"] == "hunt" and service._load("test:1").activity["total"] == 2
    clock.advance(16 * MINUTE)
    assert pushes_for(service, "test:1") == []              # the first prey won: it goes on, silently
    assert service._load("test:1").energy == 46
    clock.advance(16 * MINUTE)
    pushes = pushes_for(service, "test:1")
    hero = service._load("test:1")
    assert hero.kills == kills + 2 and hero.activity is None and hero.energy == 46
    assert len(pushes) == 1 and "2 peleas automáticas: 2 ganadas" in pushes[0].notice
    assert not service.texts.missing


def test_hunting_batch_stops_properly(service, clock):
    ready(service, level=30, energy=3)
    view = service.act("test:1", "prey")
    assert ids(view) == ["do:hunt:max", "hunt"] and "Todo (2)" in view.actions[0].label
    service.act("test:1", "do:hunt:max")
    assert service._load("test:1").activity["total"] == 1 and service._load("test:1").energy == 1
    pushes = run_batch(service, clock, "test:1", 16, 2)
    assert len(pushes) == 1 and service._load("test:1").activity is None
    hero = service._load("test:1")
    hero.energy = 10
    service._save(hero)
    service.act("test:1", "do:hunt:10")
    stopped = service.act("test:1", "stop")                 # ❌ Detener gives the prey in progress back
    assert service._load("test:1").energy == 10 and service._load("test:1").activity is None
    assert stopped.kind == "hunt" and "Te detuviste" in stopped.notice
    hero = service._load("test:1")
    hero.hp = 1
    service._save(hero)
    low = service.act("test:1", "do:hunt:4")                # under the limit: it does not go out alone
    assert "por debajo del 30 %" in low.notice and service._load("test:1").energy == 10
    assert not service.texts.missing


def test_the_hunter_counts_as_present_in_the_zone(service, clock):
    ready(service, level=30)
    make_hero(service, "test:2", "Bram")
    x, y = wild(service)
    place(service, "test:2", x, y)
    service.act("test:1", "do:hunt:10")
    clock.advance(60 * MINUTE)                              # test:1 no longer pressed a button lately, but hunts there
    hero = service._load("test:1")
    hero.activity["until"] = clock.now() + 600              # keep it busy for this check
    service._save(hero)
    players = service._zone_players(x, y, exclude="test:2")
    assert any(p["id"] == "test:1" and p["activity"] == "🏹 cazando" for p in players)
