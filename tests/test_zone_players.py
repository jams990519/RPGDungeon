"""Players in the zone (D-96, provisional): who else is here, what they do, and crossing paths while exploring.

[ES] Pruebas de ver a los otros jugadores de tu zona: dos héroes en la misma zona se ven con su actividad; quien se
fue o lleva más de presence.minutes sin tocar un botón (y no está ocupado ahí) no aparece; uno nunca se ve a sí
mismo; el tope de nombres con "… y N más"; la línea 👋 de cruzarse al explorar (y que no cambia ningún otro
resultado de la vuelta); y que 📍 Zona conserva sus botones.
"""

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.service import GameService

MIN = 60


def join(service, account, name):
    """Create a hero and press one button, so it counts as playing (Hero.seen_at) and is noted in its zone."""
    make_hero(service, account, name)
    return service.act(account, "home")


def players_block(view):
    return [line for line in view.body if line.startswith(("👥", "• "))]


def test_two_heroes_see_each_other_with_their_activity(service):
    join(service, "test:1", "Lyra")
    alone = service.act("test:1", "home")
    assert players_block(alone) == []                       # nobody else: nothing is shown (D-86)
    join(service, "test:2", "Bram")
    view = service.act("test:1", "home")
    block = players_block(view)
    assert block[0] == "👥 También en esta zona (1):"
    assert block[1] == "• Bram · 🏰 Guerrero · nv 1 · 🧍 por aquí"
    assert not any("Lyra" in line for line in block)        # never yourself
    service.act("test:2", "do:explore:5")                   # Bram starts exploring the Claro
    view = service.act("test:1", "home")
    assert "• Bram · 🏰 Guerrero · nv 1 · 🔎 explorando" in view.body
    busy = service.act("test:2", "home")                    # 📍 Zona while busy: the activity screen also lists who is here
    assert busy.kind == "activity" and "• Lyra · 🏰 Guerrero · nv 1 · 🧍 por aquí" in busy.body
    assert not any("Bram" in line for line in players_block(busy))


def test_zone_screen_keeps_its_buttons(service):
    join(service, "test:1", "Lyra")
    before = [a.id for a in service.act("test:1", "home").actions]
    join(service, "test:2", "Bram")
    view = service.act("test:1", "home")
    assert players_block(view)
    assert [a.id for a in view.actions] == before == ["go:n", "go:s", "go:e", "go:w"]


def test_idle_players_disappear_and_come_back_with_their_next_button(service, clock):
    join(service, "test:1", "Lyra")
    join(service, "test:2", "Bram")
    clock.advance(16 * MIN)                                 # Bram idle for longer than presence.minutes (15)
    view = service.act("test:1", "home")
    assert players_block(view) == []
    assert "test:2" not in service.store.get("presence", "0:0")["seen"]     # pruned on read
    service.act("test:2", "hero")                           # any button brings him back
    assert any(line.startswith("• Bram") for line in players_block(service.act("test:1", "home")))


def test_busy_hero_stays_listed_with_the_chat_closed(service, clock):
    join(service, "test:1", "Lyra")
    join(service, "test:2", "Bram")
    service.act("test:2", "do:gather:20")                   # 20 × 8 min in the Claro, no more buttons
    clock.advance(40 * MIN)
    service.tick()
    view = service.act("test:1", "home")
    assert "• Bram · 🏰 Guerrero · nv 1 · 🪓 recolectando" in view.body


def test_hero_who_left_is_not_listed_and_appears_where_he_arrived(service, clock):
    join(service, "test:1", "Lyra")
    join(service, "test:2", "Bram")
    service.act("test:2", "go:n")
    view = service.act("test:1", "home")
    assert "• Bram · 🏰 Guerrero · nv 1 · 🚶 de paso" in view.body          # on his way out
    clock.advance(10 * MIN)
    service.tick()                                          # arrives at (0, 1) with the chat closed
    assert service.store.get("hero", "test:2")["y"] == 1
    assert "test:2" not in service.store.get("presence", "0:0")["seen"]
    assert "test:2" in service.store.get("presence", "0:1")["seen"]
    assert players_block(service.act("test:1", "home")) == []


def test_cap_shows_the_first_names_and_how_many_more(service, clock):
    join(service, "test:0", "Lyra")
    names = ["Bram", "Cira", "Dano", "Eda", "Fio", "Gus", "Hela"]
    for n, name in enumerate(names, start=1):
        clock.advance(1)
        join(service, f"test:{n}", name)
    cap = service.content.balance["presence"]["max_listed"]
    block = players_block(service.act("test:0", "home"))
    assert block[0] == f"👥 También en esta zona ({len(names)}):"
    listed = [line for line in block[1:] if not line.startswith("• …")]
    assert len(listed) == cap
    assert block[-1] == f"• … y {len(names) - cap} más"
    assert listed[0].startswith("• Hela")                   # most recently seen first


def run_batch(service, clock, account, steps):
    """Advance step by step and collect the notices pushed to this account."""
    notices = []
    for _ in range(steps):
        clock.advance(10 * MIN)
        notices += [v.notice or "" for acc, v in service.tick() if acc == account]
    return "\n".join(notices)


def test_crossing_paths_while_exploring(service, clock):
    join(service, "test:1", "Lyra")
    service.content.balance["presence"]["cross_chance"] = 1.0
    service.act("test:1", "do:explore:5")
    alone = run_batch(service, clock, "test:1", 8)
    assert "🔎 Exploraste" in alone and "👋" not in alone   # nobody in the zone: nobody to cross

    join(service, "test:2", "Bram")
    service.act("test:2", "do:gather:20")                   # stays busy in the Claro
    service.store.put("hero", "test:1", {**service.store.get("hero", "test:1"), "exploration": {}})
    service.act("test:1", "do:explore:5")
    summary = run_batch(service, clock, "test:1", 8)
    line = "👋 Te cruzaste con Bram (🏰 Guerrero, nivel 1), que andaba 🪓 recolectando."
    assert summary.count(line) == 1                         # once per batch, even with chance 1.0


def test_crossing_paths_changes_nothing_else(content):
    def play(chance):
        clock = FixedClock()
        service = GameService(content, MemoryStore(), clock, world_seed=12345)
        service.content.balance["presence"]["cross_chance"] = chance
        join(service, "test:1", "Lyra")
        join(service, "test:2", "Bram")
        service.act("test:2", "do:gather:20")
        service.act("test:1", "do:explore:5")
        summary = run_batch(service, clock, "test:1", 8)
        hero = service.store.get("hero", "test:1")
        return summary, {k: hero[k] for k in ("exploration", "gold", "backpack", "xp", "energy", "hp")}

    original = content.balance["presence"]["cross_chance"]
    try:
        with_cross, state_a = play(1.0)
        without, state_b = play(0.0)
    finally:
        content.balance["presence"]["cross_chance"] = original
    assert "👋" in with_cross and "👋" not in without
    assert state_a == state_b                                # same finds, coins and exploration
    assert [line for line in with_cross.splitlines() if not line.startswith("👋")] == without.splitlines()
