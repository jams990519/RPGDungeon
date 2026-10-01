"""Guild of a player camp (D-97, provisional): founding, capacity per level, collective counters, castle.

[ES] Pruebas del gremio: lo crea el fundador en su campamento (con nombre único), sus miembros son los del
campamento, el cupo sale del nivel del gremio, los contadores suben al explorar, ganar peleas y recolectar,
sube cuando cumplen, el castillo pide gremio, los campamentos sin gremio siguen igual y ninguna pantalla pasa
de 4 botones.
"""

from collections import deque

from conftest import make_hero
from engine.combat import make_combat
from engine.core import FixedClock, MemoryStore
from engine.hero import Hero
from engine.service import GameService
from engine.social import guilds as guild_rules
from test_camps import found_at, place

HOUR = 3600


def ids(view):
    return [a.id for a in view.actions]


def set_gold(service, account, gold):
    hero = service._load(account)
    hero.gold = gold
    service._save(hero)


def join(service, account, key="6:0"):
    """Put a hero in a camp straight in the store (the approval flow is tested in test_camps.py)."""
    camp = service.store.get("camp", key)
    camp["members"].append(account)
    service.store.put("camp", key, camp)
    hero = service._load(account)
    hero.camp = key
    service._save(hero)


def set_level(service, level, key="6:0"):
    camp = service.store.get("camp", key)
    camp["level"] = level
    service.store.put("camp", key, camp)


def new_guild(service, account="test:1", name="Lobos Grises"):
    set_gold(service, account, 100)
    ask = service.act(account, "guildnew")
    assert ask.kind == "name_guild" and ask.expects_text, ask.notice
    return service.text(account, name)


def win(service, account, enemy_id="lobo_ceniciento", seed=1):
    hero = service._load(account)
    edef = service.content.enemies[enemy_id]
    state = make_combat(enemy_id, edef, edef["level_min"], service._kit(hero), seed)
    state["outcome"] = "victory"
    service._end_combat(hero, state)
    service._save(hero)


def test_pure_rules():
    levels = [{"capacity": 4, "needs": {"explorations": 10, "victories": 5}},
              {"capacity": 6, "needs": {"explorations": 20}}, {"capacity": 9, "needs": {}}]
    assert [guild_rules.capacity(levels, n) for n in (1, 2, 3, 7)] == [4, 6, 9, 9]   # the last row holds above
    assert guild_rules.needs(levels, 3) == {} and guild_rules.needs(levels, 1) == {"explorations": 10, "victories": 5}
    guild = {"level": 1, "progress": {}}
    assert guild_rules.count(guild, {"explorations": 12, "victories": 0, "gathered": -3})
    assert guild["progress"] == {"explorations": 12}              # only positive amounts count
    assert not guild_rules.can_rise(guild, levels) and not guild_rules.rise(guild, levels)
    guild_rules.count(guild, {"victories": 5})
    assert guild_rules.rise(guild, levels)
    assert guild["level"] == 2 and guild["progress"] == {"explorations": 2, "victories": 0}   # the excess carries over
    guild["level"] = 3
    assert not guild_rules.can_rise(guild, levels)                # top level: nothing more to ask


def test_founder_creates_the_guild_at_the_camp(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    view = service.act("test:1", "claro")
    assert view.kind == "player_camp" and ids(view) == ["grow", "guild", "home"]
    screen = service.act("test:1", "guild")
    assert screen.kind == "guild" and ids(screen) == ["guildnew", "rename", "claro"]
    assert any("Lyra" in line and "activo" in line for line in screen.body)
    member = service.act("test:2", "guild")                       # a member sees it, but cannot create it
    assert ids(member) == ["leave", "claro"]
    assert "fundador" in service.act("test:2", "guildnew").notice
    place(service, "test:1", 7, 0, backpack={})                    # the founder away from the camp: only looks
    away = service.act("test:1", "guild")
    assert ids(away) == ["home"]
    assert service.act("test:1", "guildnew").kind == "guild" and service.store.get("guild", "6:0") is None
    place(service, "test:1", 6, 0)
    set_gold(service, "test:1", 10)                               # the fee: 50 bronze
    assert "monedas" in service.act("test:1", "guildnew").notice
    set_gold(service, "test:1", 100)
    service.act("test:1", "guildnew")
    assert service.text("test:1", "x").kind == "name_guild"       # too short: asked again
    view = service.text("test:1", "Lobos Grises")
    guild = service.store.get("guild", "6:0")
    assert guild["name"] == "Lobos Grises" and guild["level"] == 1 and guild["founder_id"] == "test:1"
    assert view.kind == "guild" and "Lobos Grises" in view.notice and "guildnew" not in ids(view)
    assert service._load("test:1").gold == 100 - service.content.balance["guild"]["found_coins"]
    news = [v for acc, v in service.tick() if acc == "test:2"]
    assert news and news[0].kind == "guild_news" and "Lobos Grises" in news[0].body[0]
    camp_view = service.act("test:2", "claro")
    assert any("Lobos Grises" in line for line in camp_view.body)  # the camp screen names its guild
    assert service.act("test:1", "guildnew").kind == "guild"      # one guild per camp
    assert service.store.get("guild", "6:0")["name"] == "Lobos Grises"


def test_cancel_and_moving_away_found_nothing(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    set_gold(service, "test:1", 100)
    service.act("test:1", "guildnew")
    assert service.act("test:1", "guild").kind == "guild"          # ❌ Cancelar goes back to the guild screen
    service.text("test:1", "Lobos Grises")                         # a later text founds nothing
    assert service.store.get("guild", "6:0") is None
    assert service._load("test:1").gold == 100


def test_guild_names_are_unique(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    found_at(service, "test:2", -6, 0)
    new_guild(service, "test:1", "Lobos Grises")
    set_gold(service, "test:2", 100)
    service.act("test:2", "guildnew")
    view = service.text("test:2", "lobos grises")                  # same name without case: taken
    assert view.kind == "name_guild" and service.store.get("guild", "-6:0") is None
    assert service.text("test:2", "Campo 1 6").kind == "guild"     # a camp's name is fine for a guild
    assert service.store.get("guild", "-6:0")["name"] == "Campo 1 6"


def test_members_cap_follows_the_guild_level(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    camp = service.store.get("camp", "6:0")
    assert service._members_cap(camp) == 2                         # old formula without a guild at level 1
    new_guild(service)
    levels = service.content.balance["guild"]["levels"]
    assert service._members_cap(camp) == levels[0]["capacity"] == 4   # the guild only adds room
    for n, name in ((2, "Bram"), (3, "Cora"), (4, "Dara")):
        make_hero(service, f"test:{n}", name)
        join(service, f"test:{n}")
    make_hero(service, "test:5", "Eric")
    place(service, "test:5", 6, 0)
    view = service.act("test:5", "askjoin")                        # 4 of 4: full until the guild rises
    assert "lleno" in view.notice and "gremio" in view.notice
    assert "test:5" not in service.store.get("camp", "6:0").get("requests", [])
    guild = service.store.get("guild", "6:0")
    guild["level"] = 2
    service.store.put("guild", "6:0", guild)
    assert service._members_cap(camp) == levels[1]["capacity"] == 6
    service.act("test:5", "askjoin")
    asks = [v for acc, v in service.tick() if acc == "test:1" and v.kind == "camp_join"]
    service.act("test:1", asks[0].actions[0].id)
    assert "test:5" in service.store.get("camp", "6:0")["members"]
    assert any("5 de 6" in line for line in service.act("test:1", "claro").body)


def test_creating_a_guild_never_kicks_anyone(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    set_level(service, 4)                                          # old cap 8
    for n in range(2, 7):
        make_hero(service, f"test:{n}", f"Miembro{chr(64 + n)}")
        join(service, f"test:{n}")
    new_guild(service)                                             # guild level 1 gives 4: the cap stays 8
    camp = service.store.get("camp", "6:0")
    assert len(camp["members"]) == 6 and service._members_cap(camp) == 8
    assert all(service._load(f"test:{n}").camp == "6:0" for n in range(2, 7))
    for n in (7, 8):
        make_hero(service, f"test:{n}", f"Miembro{chr(64 + n)}")
        join(service, f"test:{n}")
    make_hero(service, "test:9", "Zora")
    place(service, "test:9", 6, 0)
    assert "lleno" in service.act("test:9", "askjoin").notice     # 8 of 8


def test_counters_rise_with_exploring_winning_and_gathering(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    service.act("test:1", "claim:7:0")                             # territory: no fights while we count
    new_guild(service)
    place(service, "test:1", 7, 0, backpack={}, energy=50)
    service.act("test:1", "do:explore:3")
    clock.advance(3 * 10 * 60 + 5)
    service.view("test:1")
    done = service.store.get("guild", "6:0")["progress"]["explorations"]
    assert 1 <= done <= 3 and done == 50 - service._load("test:1").energy    # 1 exploration per energy spent
    place(service, "test:1", 7, 0, backpack={})                    # drop the finds: count only what is gathered
    service.act("test:1", "do:gather:2")
    clock.advance(2 * 8 * 60 + 5)
    service.view("test:1")
    gathered = sum(service._load("test:1").backpack.values())
    progress = service.store.get("guild", "6:0")["progress"]
    assert gathered > 0 and progress["gathered"] == gathered
    win(service, "test:1")
    win(service, "test:1", seed=2)
    assert service.store.get("guild", "6:0")["progress"]["victories"] == 2
    win(service, "test:2")                                         # not a member: counts for nobody
    assert service.store.get("guild", "6:0")["progress"]["victories"] == 2
    join(service, "test:2")
    win(service, "test:2")
    assert service.store.get("guild", "6:0")["progress"]["victories"] == 3
    place(service, "test:2", 6, 0)
    service.act("test:2", "leave")                                 # leaving the camp = leaving the guild
    win(service, "test:2")
    assert service.store.get("guild", "6:0")["progress"]["victories"] == 3


def test_the_guild_rises_when_the_members_meet_its_needs(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    new_guild(service)
    service.tick()
    levels = service.content.balance["guild"]["levels"]
    need = levels[0]["needs"]
    view = service.act("test:2", "guild")
    assert "guildup" not in ids(view)
    assert any(f"0/{need['explorations']}" in line for line in view.body)
    assert "no cumplen" in service.act("test:2", "guildup").notice
    guild = service.store.get("guild", "6:0")
    guild["progress"] = {k: n for k, n in need.items()}
    guild["progress"]["explorations"] += 5
    service.store.put("guild", "6:0", guild)
    place(service, "test:1", 7, 0)                                 # away from the camp: told to go back
    away = service.act("test:1", "guild")
    assert "guildup" not in ids(away) and any("Vuelve al campamento" in line for line in away.body)
    view = service.act("test:2", "guild")                          # any member at the camp can do it
    assert ids(view)[0] == "guildup" and len(view.actions) <= 4
    view = service.act("test:2", "guildup")
    guild = service.store.get("guild", "6:0")
    assert guild["level"] == 2 and guild["progress"]["explorations"] == 5 and guild["progress"]["victories"] == 0
    assert str(levels[1]["capacity"]) in view.notice
    news = [v for acc, v in service.tick() if acc == "test:1"]
    assert news and news[0].kind == "guild_news"


def test_no_castle_without_a_guild_that_is_ready(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    cfg = service.content.balance["guild"]
    castle = next(s["from_level"] for s in service.content.balance["camps"]["stages"] if s["id"] == "castillo")
    set_level(service, castle - 1)
    camp = service.store.get("camp", "6:0")
    camp["trial_won"] = True                                       # the Noche de prueba is its own gate (D-99, test_raids.py)
    service.store.put("camp", "6:0", camp)
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999}, chests=99)   # 🪎 chests pay from level 6 (D-92)
    view = service.act("test:1", "grow")                           # no guild: blocked, and the screen says why
    assert view.kind == "camp_grow" and not any(a.id.startswith("claim:") for a in view.actions)
    assert any("castillo" in line for line in view.body) and len(view.actions) <= 4
    service.act("test:1", "claim:7:0")
    assert service.store.get("camp", "6:0")["level"] == castle - 1
    new_guild(service)
    guild = service.store.get("guild", "6:0")
    guild["level"] = cfg["castle_min_level"]
    service.store.put("guild", "6:0", guild)
    for n in range(2, cfg["castle_min_members"]):                  # one member short
        make_hero(service, f"test:{n}", f"Miembro{chr(64 + n)}")
        join(service, f"test:{n}")
    assert not any(a.id.startswith("claim:") for a in service.act("test:1", "grow").actions)
    service.act("test:1", "claim:7:0")
    assert service.store.get("camp", "6:0")["level"] == castle - 1
    make_hero(service, "test:99", "Ultimo")
    join(service, "test:99")
    camp = service.store.get("camp", "6:0")
    assert len(camp["members"]) == cfg["castle_min_members"] and all(ok for _, ok in service._castle_needs(camp))
    view = service.act("test:1", "grow")
    claims = [a.id for a in view.actions if a.id.startswith("claim:")]
    assert claims
    service.act("test:1", claims[0])
    assert service.store.get("camp", "6:0")["level"] == castle
    assert service._castle_needs(service.store.get("camp", "6:0")) == []   # a castle keeps growing freely


def test_camps_without_a_guild_behave_as_before(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    cfg = service.content.balance["camps"]
    for level in (1, 3, 7):
        set_level(service, level)
        camp = service.store.get("camp", "6:0")
        assert service._members_cap(camp) == cfg["members_base"] + (level - 1) * cfg["members_per_level"]
        assert service._castle_needs(camp) == []
    set_level(service, 1)
    view = service.act("test:1", "grow")
    assert not any("castillo" in line for line in view.body)       # growing below the castle asks nothing new
    service.act("test:1", "claim:7:0")
    assert service.store.get("camp", "6:0")["level"] == 2
    set_level(service, 9)                                          # an old castle keeps growing without a guild
    hero = service._load("test:1")
    hero.chests = 99                                               # 🪎 chests pay from level 6 (D-92)
    service._save(hero)
    service.act("test:1", "claim:6:1")
    assert service.store.get("camp", "6:0")["level"] == 10
    make_hero(service, "test:2", "Bram")
    win(service, "test:1")                                         # no guild: nothing is counted anywhere
    assert list(service.store.items("guild")) == []


def test_member_lines_show_when_each_one_last_played(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    join(service, "test:2")
    service.act("test:2", "hero")                                  # Bram presses a button now
    clock.advance(2 * HOUR)
    view = service.act("test:1", "guild")
    lines = [line for line in view.body if line.startswith("• ")]
    assert lines[0].startswith("• Lyra") and "👑" in lines[0] and "activo ahora" in lines[0]
    assert "Bram" in lines[1] and "activo hace 2 h" in lines[1]
    clock.advance(3 * 24 * HOUR)
    assert any("Bram" in line and "hace 3 días" in line for line in service.act("test:1", "guild").body)


def test_gremio_command_and_no_camp(service):
    make_hero(service, "test:1", "Lyra")
    assert service.commands()["/gremio"] == "guild"
    view = service.act("test:1", "guild")
    assert view.kind == "zone" and "campamento" in view.notice
    assert service.act("test:1", "guildup").kind == "zone"
    assert service.act("test:1", "guildnew").kind == "zone"


def test_every_guild_screen_keeps_four_buttons(content):
    """Crawl every button from the camp screen, as founder and as member, with and without a guild."""

    def build(role, with_guild, path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        make_hero(service, "test:1", "Lyra")
        make_hero(service, "test:2", "Bram")
        found_at(service, "test:1", 6, 0)
        set_level(service, 3)                                      # the pantry button too: 4 on the camp screen
        join(service, "test:2")
        place(service, "test:2", 6, 0)
        if with_guild:
            new_guild(service)
            guild = service.store.get("guild", "6:0")
            guild["progress"] = dict(service.content.balance["guild"]["levels"][0]["needs"])
            service.store.put("guild", "6:0", guild)
        account = "test:1" if role == "founder" else "test:2"
        view = service.act(account, "claro")
        for action in path:
            view = service.act(account, action)
        return service, view

    for role in ("founder", "member"):
        for with_guild in (False, True):
            seen, queue = set(), deque([[]])
            while queue:
                path = queue.popleft()
                service, view = build(role, with_guild, path)
                assert len(view.actions) <= 4, (role, with_guild, path, view.kind, ids(view))
                assert not service.texts.missing, (path, service.texts.missing)
                key = (view.kind, tuple(ids(view)))
                if key in seen or len(path) >= 3:
                    continue
                seen.add(key)
                for action_id in ids(view):
                    if not action_id.startswith(("claim:", "go:", "goto:")):
                        queue.append(path + [action_id])
            assert any(kind == "guild" for kind, _ in seen), (role, with_guild)


def test_old_heroes_and_camps_load(service):
    """Camps and heroes saved before the guild existed keep working (no new field is required)."""
    make_hero(service, "test:1", "Lyra")
    service.store.put("camp", "0:3", {"name": "Viejo", "founder": "Lyra", "founder_id": "test:1",
                                       "members": ["test:1"], "relations": {}, "asked": [], "x": 0, "y": 3})
    hero = Hero.from_dict(service.store.get("hero", "test:1"))
    hero.camp, hero.x, hero.y = "0:3", 0, 3
    service.store.put("hero", "test:1", hero.to_dict())
    view = service.act("test:1", "claro")
    assert view.kind == "player_camp" and "guild" in ids(view)
    assert service.act("test:1", "guild").kind == "guild"
