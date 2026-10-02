"""Story and roleplay, simple layer (D-117, provisional).

[ES] Pruebas de la historia y el rol: el origen se elige al crear el héroe (o la primera vez que un héroe viejo abre 👤 Héroe o
📖 Historia) sin bloquear nada; las misiones del origen y del Capítulo 1 avanzan con acciones de verdad (hablar en el Claro,
explorar, recolectar, vender, fabricar, viajar, vencer al Guardián); las decisiones cambian la reputación, se recuerdan y
cambian quién te ayuda después; los rangos de facción pagan una sola vez; los encargos del día cambian cada día y pagan una
vez; los encargos de campamento cuentan lo de todos los miembros; el diario anota los hechos; /bio se guarda y se ve;
/saludar solo llega a los presentes. Toda pantalla nueva tiene 4 botones como mucho, el menú de abajo 6, no falta ningún
texto y los guardados viejos cargan.
"""

from collections import deque

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.hero import Hero, hero_stats
from engine.service import GameService
from engine.service.game import HUB_BUTTONS, HUB_KINDS
from test_camps import found_at, place

MINUTE = 60


def ids(view):
    return [a.id for a in view.actions]


def hero_of(service, account="test:1"):
    return service._load(account)


def set_story(service, account, **fields):
    hero = hero_of(service, account)
    for key, value in fields.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def win(service, account):
    """Finish the current fight with a victory (the enemy at 1 health before each attack)."""
    view = None
    for _ in range(10):
        state = service.store.get("combat", account)
        if state is None:
            break
        state["enemy"]["hp"] = 1
        service.store.put("combat", account, state)
        hero = service._load(account)
        hero.hp = hero_stats(service._kit(hero), hero.level)["max_hp"]
        service._save(hero)
        view = service.act(account, "atk")
    assert view is not None and view.kind == "combat_end"
    return view


def batch(service, clock, account, kind, steps):
    """Run a batch of `steps` in the Claro (no fights there) and return the summary view."""
    service.act(account, f"do:{kind}:{steps}")
    clock.advance(steps * 12 * MINUTE)
    return service.view(account)


def gather_until(service, clock, account, item, n):
    for _ in range(12):
        if hero_of(service, account).backpack.get(item, 0) >= n:
            return
        batch(service, clock, account, "gather", 5)
    assert hero_of(service, account).backpack.get(item, 0) >= n


# ---------------------------------------------------------------- origin


def test_new_hero_chooses_origin_after_the_class_without_being_blocked(service):
    view = make_hero(service)
    # D-190: creating asks only the name and the class; the origin is chosen later, in 👤 Héroe → 🎭 Origen (E-131)
    assert view.kind == "zone" and "Bienvenido" in view.notice
    menu = service.menu()
    assert len(menu) <= 6 and "story" not in [m.id for m in menu] and [m.id for m in menu][-1] == "options"
    assert service.act("test:1", "home").kind == "zone"                       # the menu works: nothing is blocked
    assert service.act("test:1", "explore_menu").kind == "explore_menu"
    assert "origin" in ids(service.act("test:1", "hero"))
    story = service.act("test:1", "origin")
    assert story.kind == "origin" and len(story.actions) <= 4
    page2 = service.act("test:1", "origin:1")
    assert page2.kind == "origin" and "orig:noble" in ids(page2) and len(page2.actions) <= 4
    detail = service.act("test:1", "orig:noble")
    assert detail.kind == "origin_detail" and ids(detail) == ["origpick:noble", "origin:1"]
    gold = hero_of(service).gold
    done = service.act("test:1", "origpick:noble")
    hero = hero_of(service)
    assert done.kind == "origin_card" and hero.origin == "noble" and hero.gold == gold + 100     # the gift: 1 🥈
    assert ids(done) == ["squests", "hero"]
    assert [e["k"] for e in hero.journal] == ["awoke", "origin"]
    again = service.act("test:1", "origpick:minero")                           # for ever: never changes
    assert hero_of(service).origin == "noble" and again.kind == "origin_card"
    assert service.act("test:1", "origin").kind == "origin_card"


def test_old_heroes_get_the_origin_choice_once_from_the_hero_sheet_or_the_story(service):
    # D-192: nothing offers the origin by itself any more (it never hijacks 👤 Héroe or the diary); it is the 🎭 Origen
    # button of 👤 Héroe, for old heroes too, and _origin_offer stays for the guided path (once).
    for account, name, first in (("test:1", "Lyra", "hero"), ("test:2", "Bram", "journal")):
        make_hero(service, account, name)
        data = service.store.get("hero", account)
        for key in ("origin", "story", "factions", "journal", "bio"):
            del data[key]                                                     # a hero saved before D-117
        service.store.put("hero", account, data)
        assert service.act(account, first).kind == first                      # the screen itself, never the offer
        assert service.act(account, "home").kind == "zone"
        choose = service.act(account, "origin")
        assert choose.kind == "origin" and len(choose.actions) <= 4
    hero = hero_of(service)
    offer = service._origin_offer(hero)
    assert offer.kind == "origin" and offer.notice and service._origin_offer(hero) is None    # once
    assert not service.texts.missing


def test_origin_traits_are_small_and_never_combat(service):
    make_hero(service)
    plain = hero_of(service)
    attack = hero_stats(service._kit(plain), 1)["attack"]
    service.act("test:1", "origpick:minero")
    hero = hero_of(service)
    assert hero_stats(service._kit(hero), 1)["attack"] == attack               # no combat power
    before = hero.professions.get("minero", 0)
    service._prof_gain(hero, "minero", 100)
    assert hero.professions["minero"] - before == 115                          # ⛏️ +15 %
    make_hero(service, "test:2", "Bram")
    service.act("test:2", "origpick:huerfano")
    other = hero_of(service, "test:2")
    price = service.content.items["provisiones"]["price"]
    assert service._shop_price(other, "provisiones") == round(price * 0.9) < price
    shop = service.act("test:2", "shop")
    assert any(service._money(service._shop_price(other, "provisiones")) in line for line in shop.body)


# ---------------------------------------------------------------- chapter 1 from real actions


def test_first_missions_advance_from_real_actions_in_the_claro(service, clock):
    make_hero(service)
    service.act("test:1", "origpick:minero")
    npc = service.act("test:1", "npc:marta")
    assert npc.kind == "npc" and ids(npc) == ["talk:marta", "npcs:0"]
    talk = service.act("test:1", "talk:marta")
    assert "Recorre los alrededores" in talk.notice                           # the next step reads as a scene
    summary = batch(service, clock, "test:1", "explore", 2)                    # exploring from the Claro
    text = summary.notice or ""
    assert text.count("«La fogata que no se apaga»: ¡paso cumplido!") == 1     # said once, in the batch summary
    assert service._load("test:1").story["q"]["c1_m1"]["s"] == 2
    gather_until(service, clock, "test:1", "madera", 4)
    hero = hero_of(service)
    wood, gold = hero.backpack["madera"], hero.gold
    view = service.act("test:1", "talk:marta")                                 # 🤲 the 4 wood are handed over
    hero = hero_of(service)
    assert "c1_m1" in hero.story["done"] and hero.backpack.get("madera", 0) == wood - 4
    assert hero.factions["llama"] == 15 and hero.gold >= gold + 10
    assert "Misión cumplida" in view.notice and "Todo vale algo" in view.notice
    assert any(e["k"] == "quest" and e["v"]["q"] == "c1_m1" for e in hero.journal)
    # c1_m2: talk to Odo, sell 3 things to the merchant, talk again
    service.act("test:1", "talk:odo")
    gather_until(service, clock, "test:1", "fibra", 3)
    sold = service.act("test:1", "sell:all")
    assert "paso cumplido" in sold.notice
    service.act("test:1", "talk:odo")
    hero = hero_of(service)
    assert "c1_m2" in hero.story["done"] and hero.factions["restos"] == 15


def test_origin_chain_advances_and_gives_its_title(service, clock):
    make_hero(service)
    service.act("test:1", "origpick:aprendiz")
    service.act("test:1", "talk:brena")
    place(service, "test:1", 0, 0, backpack={"madera": 9})
    made = service.act("test:1", "mk:tablon:1:0")                              # a real craft at the Claro station
    assert "paso cumplido" in made.notice
    service.act("test:1", "talk:brena")
    hero = hero_of(service)
    assert "o_aprendiz_1" in hero.story["done"]
    assert service._quest_xp(service._quest_defs()["o_aprendiz_1"]) == 80    # 20 per ⚡ × 4 ⚡ at level 1 (D-108)
    # The rest of the chain, with the level it asks for
    set_story(service, "test:1", level=3)
    hero = hero_of(service)
    service._st(hero)["done"] += ["o_aprendiz_2"]
    service._save(hero)
    service.act("test:1", "talk:iria")
    service.act("test:1", "mk:tablon:2:0")
    view = service.act("test:1", "talk:brena")
    hero = hero_of(service)
    assert "o_aprendiz_3" in hero.story["done"] and "o_aprendiz" in hero.titles
    assert "Herencia del taller" in view.notice
    assert "Herencia del taller" in "\n".join(service.act("test:1", "hero").body)     # titles of the story on the sheet


def test_level_locks_a_mission_and_says_so(service):
    make_hero(service)
    hero = hero_of(service)
    service._st(hero)["done"] += ["c1_m1", "c1_m2"]
    service._save(hero)
    story = service.act("test:1", "story")
    assert any("🔒" in line and "nivel 2" in line for line in story.body)
    assert service._active_quests(hero_of(service)) == []


# ---------------------------------------------------------------- decisions


def test_decisions_change_reputation_are_remembered_and_choose_who_helps(service):
    make_hero(service)
    set_story(service, "test:1", level=3)
    hero = hero_of(service)
    service._st(hero)["done"] += ["c1_m1", "c1_m2", "c1_m3", "c1_m4"]
    service._save(hero)
    service.act("test:1", "talk:brena")
    place(service, "test:1", 0, 0, backpack={"madera": 3})
    service.act("test:1", "mk:tablon:1:0")
    quests = service.act("test:1", "squests")
    assert quests.kind == "story_quests" and ids(quests) == ["ch:c1_m5:iria", "ch:c1_m5:brena", "ch:c1_m5:odo", "journal"]
    view = service.act("test:1", "ch:c1_m5:iria")
    hero = hero_of(service)
    assert hero.story["c"]["ambar"] == "iria" and "c1_m5" in hero.story["done"]
    assert hero.factions["umbral"] == 25 and hero.factions["llama"] == -5 + 10       # the decision, then the mission's reward
    assert "como si quemara" in view.notice
    assert any(e["k"] == "choice" and e["v"]["o"] == "iria" for e in hero.journal)
    assert service.act("test:1", "ch:c1_m5:odo").kind == "story_quests"             # no second chance
    assert hero_of(service).story["c"]["ambar"] == "iria"
    assert "La astilla canta de noche" in "\n".join(service.act("test:1", "npc:iria").body)   # the greeting remembers
    # Decision 2 and the finale: the character chosen in decision 1 helps, Tano pays if you carried him
    set_story(service, "test:1", level=5)
    hero = hero_of(service)
    service._st(hero)["done"] += ["c1_m6"]
    service._st(hero)["c"]["herido"] = "cargar"
    service._save(hero)
    gold = hero_of(service).gold
    first = service.act("test:1", "talk:marta")
    assert "Tano" in first.notice and hero_of(service).gold >= gold + 50
    assert service.act("test:1", "talk:brena").notice.startswith("Brena te saluda")  # Brena is not the helper
    pending = service.act("test:1", "npc:iria")
    assert "talk:iria" in ids(pending)
    before = hero_of(service).backpack.get("unguento", 0)
    service.act("test:1", "talk:iria")
    assert hero_of(service).backpack.get("unguento", 0) == before + 2


def test_decision_two_rewards_are_a_or_b(service):
    for account, name, option in (("test:1", "Lyra", "cargar"), ("test:2", "Bram", "rastro")):
        make_hero(service, account, name)
        set_story(service, account, level=4)
        hero = hero_of(service, account)
        service._st(hero)["done"] += ["c1_m1", "c1_m2", "c1_m3", "c1_m4", "c1_m5"]
        service._st(hero)["q"]["c1_m6"] = {"s": 2, "n": 0}
        service._save(hero)
        service.act(account, f"ch:c1_m6:{option}")
    lyra, bram = hero_of(service, "test:1"), hero_of(service, "test:2")
    assert lyra.factions["restos"] == 20 and lyra.factions["llama"] == 10 and not lyra.backpack.get("flor_luna")
    assert bram.factions["umbral"] == 20 and bram.factions["restos"] == -10 and bram.backpack["flor_luna"] == 2
    assert "Tano no para de contar" not in "\n".join(service.act("test:1", "npc:marta").body)   # m6 not finished yet
    service.act("test:1", "talk:anselmo")
    assert "Tano no para de contar" in "\n".join(service.act("test:1", "npc:marta").body)
    service.act("test:2", "talk:anselmo")
    assert "Tano no volvió" in "\n".join(service.act("test:2", "npc:odo").body)
    assert "mal" in "\n".join(service.act("test:2", "factions").body).lower()          # restos −10: Mal visto


def test_lair_and_guardian_steps_and_the_end_of_chapter_one(service, clock):
    make_hero(service)
    set_story(service, "test:1", level=6)
    hero = hero_of(service)
    service._st(hero)["done"] += ["c1_m1", "c1_m2", "c1_m3", "c1_m4", "c1_m5", "c1_m6"]
    service._st(hero)["q"]["c1_m7"] = {"s": 2, "n": 0}
    service._save(hero)
    cfg = service._guardian_cfg()
    place(service, "test:1", cfg["x"], cfg["y"] - 1)
    service.act("test:1", "go:n")
    clock.advance(60 * MINUTE)
    service.view("test:1")
    hero = hero_of(service)
    assert (hero.x, hero.y) == (cfg["x"], cfg["y"]) and hero.story["q"]["c1_m7"]["s"] == 3     # arrived: the lair step is done
    if service.store.get("combat", "test:1"):
        win(service, "test:1")
    service.act("test:1", "boss")
    end = win(service, "test:1")
    hero = hero_of(service)
    assert hero.story["q"]["c1_m7"]["s"] == 4 and "paso cumplido" in "\n".join(end.body)
    assert any(e["k"] == "guardian" for e in hero.journal) and any(e["k"] == "title" for e in hero.journal)   # Pioneer too
    place(service, "test:1", 0, 0)
    final = service.act("test:1", "talk:marta")
    hero = hero_of(service)
    assert "c1_m7" in hero.story["done"] and "c1_brasa" in hero.titles
    assert "Capítulo 1" in final.notice and any(e["k"] == "chapter" for e in hero.journal)
    story = service.act("test:1", "story")
    assert any("completo" in line for line in story.body)


# ---------------------------------------------------------------- factions


def test_faction_ranks_pay_once_and_noble_gets_a_bit_more(service):
    make_hero(service)
    hero = hero_of(service)
    _, lines = service._rep_gain(hero, "llama", 100)
    assert "llama_conocido" in hero.titles and any("Conocido" in line for line in lines)
    service._rep_gain(hero, "llama", -150)
    assert service._rank_of(hero, "llama") == 0                              # Mal visto
    potions = hero.backpack.get("pocion_vida", 0)
    service._rep_gain(hero, "llama", 350)                                     # back to Conocido, then Apreciado
    assert hero.titles.count("llama_conocido") == 1
    assert sum(1 for e in hero.journal if e["k"] == "rank" and e["v"]["r"] == "conocido") == 1
    assert hero.backpack["pocion_vida"] == potions + 2
    service._rep_gain(hero, "llama", -10)
    service._rep_gain(hero, "llama", 10)
    assert hero.backpack["pocion_vida"] == potions + 2                         # Apreciado pays once
    make_hero(service, "test:2", "Bram")
    service.act("test:2", "origpick:noble")
    noble = hero_of(service, "test:2")
    gained, _ = service._rep_gain(noble, "umbral", 100)
    assert gained == 110
    view = service.act("test:1", "factions")
    assert view.kind == "factions" and len(view.actions) <= 4


# ---------------------------------------------------------------- daily and camp tasks


def test_daily_tasks_rotate_by_day_one_per_faction_and_pay_once(service, clock):
    make_hero(service)
    pool = service.content.story["daily"]
    seen = set()
    for _ in range(6):
        today = service._daily_ids()
        assert len(today) == 3
        factions = [service.content.story["npcs"][pool[t]["giver"]]["faction"] for t in today]
        assert factions == ["llama", "umbral", "restos"]
        assert service._daily_ids() == today                                  # the same all day
        seen.add(tuple(today))
        clock.advance(24 * 60 * MINUTE)
    assert len(seen) > 1                                                       # they change with the days
    for _ in range(40):                                                        # a day whose llama task is wood or fiber
        if service._daily_ids()[0] in ("d_lena", "d_fibra"):
            break
        clock.advance(24 * 60 * MINUTE)
    tid = service._daily_ids()[0]
    item = pool[tid]["goal"]["item"]
    hero = hero_of(service)
    gold, rep = hero.gold, hero.factions.get("llama", 0)
    for _ in range(10):
        if tid in hero_of(service).story.get("daily", {}).get("done", []):
            break
        batch(service, clock, "test:1", "gather", 5)
        hero = hero_of(service)
        hero.backpack = {}                                                    # keep space; only what is gathered counts
        service._save(hero)
    hero = hero_of(service)
    assert tid in hero.story["daily"]["done"] and hero.factions["llama"] == rep + 10 and hero.gold > gold
    board = service.act("test:1", "board")
    assert board.kind == "board" and len(board.actions) <= 4 and any("✅" in line for line in board.body)
    paid = hero.factions["llama"]
    batch(service, clock, "test:1", "gather", 5)
    assert hero_of(service).factions["llama"] == paid                          # once a day
    assert service._st(hero)["tasks"] >= 1
    assert item in ("madera", "fibra")


def test_camp_tasks_count_every_member_and_pay_each_helper(service, clock):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    make_hero(service, "test:2", "Bram")
    camp = service.store.get("camp", "6:0")
    camp["members"].append("test:2")
    service.store.put("camp", "6:0", camp)
    set_story(service, "test:2", camp="6:0", x=6, y=0, exploration={})
    service._camp_task_ids = lambda key, camp: ["ct_mapa"]                   # this week's task: explore 30 together
    record = service._camp_tasks("6:0")
    record["p"]["ct_mapa"], record["by"]["ct_mapa"] = 29, {"test:1": 29}
    service.store.put("camp_tasks", "6:0", record)
    lyra_gold, bram_gold = hero_of(service, "test:1").gold, hero_of(service, "test:2").gold
    view = service.act("test:2", "board")
    assert any("29/30" in line for line in view.body)
    batch(service, clock, "test:2", "explore", 1)                             # Bram explores once in the camp's land
    record = service.store.get("camp_tasks", "6:0")
    assert record["paid"] == ["ct_mapa"] and record["by"]["ct_mapa"] == {"test:1": 29, "test:2": 1}
    assert hero_of(service, "test:1").gold == lyra_gold + 30                  # paid while offline
    assert hero_of(service, "test:2").gold > bram_gold
    assert service.store.get("outbox", "test:1")                              # and told
    outsider = make_hero(service, "test:3", "Cora")
    assert outsider.kind == "zone"                                           # D-190: straight to the game
    assert service._camp_event(hero_of(service, "test:3"), "explore", {"x": 0, "y": 0, "lejania": 0}) == []


# ---------------------------------------------------------------- journal, bio, gestures, emblem


def test_journal_lists_deeds_and_others_can_read_the_card(service):
    make_hero(service)
    service.act("test:1", "origpick:curandero")
    service.text("test:1", "/bio Curandera sin aldea, buscando la flor que brilla.")
    hero = hero_of(service)
    service._grant_title(hero, "c1_brasa")
    service._save(hero)
    journal = service.act("test:1", "journal")
    text = "\n".join(journal.body)
    assert journal.kind == "journal" and ids(journal) == ["squests", "factions", "jshow", "hero"]   # D-192: the story's screen
    assert "Despertó junto a la fogata" in text and "Curandero de aldea" in text and "Brasa del Claro" in text
    make_hero(service, "test:2", "Bram")
    card = service.text("test:2", "/diario lyra")
    assert card.kind == "card" and "Lyra" in card.title and any("flor que brilla" in line for line in card.body)
    missing = service.text("test:2", "/diario Nadie")
    assert missing.notice and "Nadie" in missing.notice
    assert service.act("test:2", service.commands()["/diario"]).kind == "journal"
    service.act("test:1", "home")                                              # Lyra plays now (D-96 presence)
    service.store.delete("outbox", "test:1")
    shown = service.text("test:2", "/diario mostrar")                          # same as 📣 Mostrar: the card to who is here
    assert shown.kind == "journal" and "1 persona" in shown.notice
    assert service.store.get("outbox", "test:1")["items"][0]["kind"] == "card"


def test_bio_is_stored_trimmed_and_shown_on_the_hero_sheet(service):
    make_hero(service)
    view = service.text("test:1", "/bio  Cazadora   de lobos\ndel norte.  ")
    assert view.kind == "bio" and hero_of(service).bio == "Cazadora de lobos del norte."
    assert any("Cazadora de lobos del norte." in line for line in service.act("test:1", "hero").body)
    service.text("test:1", "/bio " + "x" * 500)
    assert len(hero_of(service).bio) == service.content.balance["story"]["bio_max"]
    service.text("test:1", "/bio borrar")
    assert hero_of(service).bio == ""
    assert service.act("test:1", service.commands()["/bio"]).kind == "bio"
    assert service.text("test:1", "/stats").kind == "stats"                   # plain shortcuts still work through text()
    assert service.text("test:1", "/nada").kind in ("origin", "zone")


def test_saludar_reaches_only_players_present_in_the_zone(service, clock):
    for account, name in (("test:1", "Lyra"), ("test:2", "Bram"), ("test:3", "Cora")):
        make_hero(service, account, name)
    place(service, "test:3", 1, 0)
    for account in ("test:2", "test:3"):
        service.act(account, "home")                                          # they play now (D-96 presence)
    for account in ("test:2", "test:3"):
        service.store.delete("outbox", account)
    view = service.text("test:1", "/saludar")
    assert "saluda" in view.notice and "1 persona" in view.notice
    box = service.store.get("outbox", "test:2")
    assert box and box["items"][0]["kind"] == "gesture" and "Lyra" in box["items"][0]["body"][0]
    assert service.store.get("outbox", "test:3") is None                      # another zone: nothing
    again = service.text("test:1", "/brindar por la Llama")
    assert "Espera" in again.notice and len(service.store.get("outbox", "test:2")["items"]) == 1   # one per minute
    clock.advance(2 * MINUTE)
    service.act("test:2", "home")
    toast = service.text("test:1", "/brindar ¡Por la Llama!")
    assert "¡Por la Llama!" in toast.notice
    clock.advance(2 * MINUTE)
    service.act("test:2", "home")
    targeted = service.text("test:1", "/saludar bram")
    assert "saluda a" in targeted.notice and "Bram" in targeted.notice
    clock.advance(2 * MINUTE)
    assert "no está" in service.text("test:1", "/saludar Cora").notice
    alone = service.text("test:3", "/saludar")
    assert "No hay nadie" in alone.notice
    assert service.act("test:1", "gesture:saludar").kind in ("zone", "activity")


def test_profession_emblem_shows_next_to_the_name(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    set_story(service, "test:1", professions={"medicina": 5000})
    service.act("test:1", "home")
    lines = service.act("test:2", "home").body
    assert any("🩺 Lyra" in line for line in lines)
    sheet = "\n".join(service.act("test:1", "hero").body)
    assert "Emblema: 🩺 Medicina" in sheet
    assert service._emblem_name(hero_of(service, "test:2")) == "Bram"         # rank 1 everywhere: no emblem


# ---------------------------------------------------------------- screens, texts, old saves


def test_every_story_screen_has_four_buttons_at_most_and_no_missing_text(content):
    def build(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        make_hero(service, "test:1", "Lyra")
        view = service.act("test:1", "story")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue, pressed = set(), deque([[]]), 0
    while queue and pressed < 120:
        path = queue.popleft()
        service, view = build(path)
        pressed += 1
        assert len(view.actions) <= (6 if view.kind == "combat" else 8 if view.kind in HUB_KINDS else 4), (path, view.kind)
        assert len(service.menu()) <= 6
        assert not service.texts.missing, (path, service.texts.missing)
        key = (view.kind, tuple(ids(view)))
        if key in seen:
            continue
        seen.add(key)
        for action in ids(view):        # D-192: stay on the story's screens (the hero and camp hubs have their own crawls)
            if len(path) < 4 and not action.startswith(("go:", "explore", "gather", "inn", "do:", "bag", "talents", "health",
                                                        "stats", "bar", "oficios", "claro")):
                queue.append(path + [action])
    kinds = {k for k, _ in seen}
    assert {"journal", "story_quests", "npcs", "npc", "factions", "origin", "origin_detail", "board"} <= kinds


def test_every_story_id_has_its_texts(service):
    t = service.texts
    data = service.content.story
    keys = []
    for oid in data["origins"]:
        keys += [f"story.origin.{oid}.{k}" for k in ("name", "intro", "trait", "gift")]
    for nid, npc in data["npcs"].items():
        keys += [f"story.npc.{nid}.name", f"story.npc.{nid}.role"] + [f"story.npc.{nid}.lines.{line['key']}" for line in npc["lines"]]
    for fid in data["factions"]:
        keys += [f"story.faction.{fid}.name", f"story.faction.{fid}.desc"]
    for rank in service.content.balance["story"]["ranks"]:
        keys.append(f"story.rank.{rank['id']}")
    for fid, rewards in data["rank_rewards"].items():
        keys += [f"story.titles.{r['title']}" for r in rewards.values() if r.get("title")]
    for cid in data["chapters"]:
        keys.append(f"story.chapter.{cid}")
    for qid, quest in data["quests"].items():
        keys += [f"story.quest.{qid}.title", f"story.quest.{qid}.done"]
        if quest.get("reward", {}).get("title"):
            keys.append(f"story.titles.{quest['reward']['title']}")
        for step in quest["steps"]:
            keys.append(f"story.quest.{qid}.{step['id']}")
            goal = step["goal"]
            if goal["kind"] == "choice":
                keys += [f"story.quest.{qid}.opt_{o}" for o in goal["options"]]
            for item in list((goal.get("items") or {})) + list((step.get("reward") or {}).get("items", {})):
                assert item in service.content.items, (qid, item)
    for tid in data["daily"]:
        keys.append(f"story.daily.{tid}")
    for tid in data["camp_tasks"]:
        keys.append(f"story.camp_task.{tid}")
    missing = [k for k in keys if not t.has(k)]
    assert not missing, missing
    for qid, quest in data["quests"].items():                                  # every mission belongs to a chain
        assert quest["chain"] == "origin" or qid in data["chapters"][quest["chain"]]["quests"]
    assert all(len(o["chain"]) in (3, 4) for o in data["origins"].values()) and 5 <= len(data["origins"]) <= 6
    assert 5 <= len(data["chapters"]["c1"]["quests"]) <= 8
    choices = [s for q in data["chapters"]["c1"]["quests"] for s in data["quests"][q]["steps"] if s["goal"]["kind"] == "choice"]
    assert len(choices) >= 2


def test_old_saves_load_and_play_the_story(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    for key in ("origin", "story", "factions", "journal", "bio"):
        del data[key]
    service.store.put("hero", "test:1", data)
    hero = Hero.from_dict(service.store.get("hero", "test:1"))
    assert hero.origin is None and hero.story == {} and hero.factions == {} and hero.journal == [] and hero.bio == ""
    for action in ("story", "story", "squests", "npcs", "npc:odo", "board", "factions", "journal", "hero", "origin"):
        view = service.act("test:1", action)
        assert len(view.actions) <= (8 if view.kind in HUB_KINDS else 4)      # D-192: the hero hub, up to 8
    assert service.act("test:1", "journal").kind == "journal"
    assert not service.texts.missing
