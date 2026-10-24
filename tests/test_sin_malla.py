"""⛓️ → 🦺 No more mail (D-342, confirmed; how: D-343, provisional; 0.62.2).

[ES]
Pruebas de la orden del dueño del 24-oct-2026 (D-342): "la malla la quitamos, dejamos cuero, tela y placa únicamente". La malla
nunca sale (botín, peleas automáticas, cofres de mazmorra, el Recuerdo del Guardián, el equipo inicial); cada pieza de malla tiene
su gemela de cuero (misma ranura, tier y origen; la ✒️ obra maestra, la obra maestra de su gemela); el cambio de una sola vez al
arrancar la cambia en todos lados (lo puesto con su durabilidad, la mochila aunque pase el tope, el cinturón, ✨ y ✒️, 🆕, las
órdenes de venta del 🏛️ Mercado y su índice, 📦 Entregas, un borrador, la ⚔️ Armería, los 💰 fondos, un 📜 encargo de reparación y la
bolsa de la 🌀 mazmorra) y no toca lo archivado (el héroe caído); corre una sola vez y correrlo de nuevo no cambia nada; deja el
registro "migrations"/"malla_to_leather" con su formato exacto; avisa una vez a cada jugador en su idioma; y la 🎓 ⛓️ Malla de la
Peletería se retira: quien la tenía la pierde, elige otra gratis y su dominio queda guardado.
Archivo: tests/test_sin_malla.py · Módulo: M4 Equipo e inventario (con M14 Oficios) · Prueba: engine/service/retired_gear.py,
engine/hero/gear.py (retired_types, retired_twin, roll_gear, source_choices, starter_gear), engine/world/dungeons.py (chest_gear)
"""

from conftest import legacy_content, make_hero
from engine.combat import make_combat
from engine.core import Rng
from engine.hero import Hero
from engine.hero.gear import retired_twin, retired_types, roll_gear, source_choices, starter_gear
from engine.professions import xp_for_rank
from engine.professions import rules as profession_rules
from engine.service import GameService
from engine.world import dungeons as dungeon_rules

ACC = "test:1"
OTHER = "test:2"
MAIL = "malla"


def mail_ids(content):
    return [iid for iid, it in content.items.items() if it.get("kind") == "gear" and it.get("type") == MAIL]


def restart(service):
    """The engine starting again on the same store (the one-time change runs here)."""
    return GameService(service.content, service.store, service.clock, world_seed=12345, time_scale=1.0)


def rearm(service):
    """Pretend the 0.62.2 change never ran (a store from before the patch), so the next restart runs it."""
    service.store.delete("migrations", "malla_to_leather")


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def put_hero(service, account=ACC, **values):
    data = service.store.get("hero", account)
    data.update(values)
    service.store.put("hero", account, data)


# ---------------------------------------------------------------- mail never comes into the game


def test_no_class_wears_mail_and_mail_is_a_retired_type(content):
    gear = content.balance["gear"]
    assert retired_types(content.balance) == {MAIL: "cuero"}
    assert MAIL not in gear["armor_by_group"].values()                         # not even the retired groups (evocador)
    mail = mail_ids(content)                                                     # the pieces stay in items.yaml: old saves load
    assert len([i for i in mail if not content.items[i].get("masterwork")]) == 138 and len(mail) == 138 + 67   # + ✒️ twins
    assert not any(content.items[i].get("retired") for i in mail_ids(content))


def test_mail_never_drops_as_loot_for_any_class(content):
    for level in (1, 3, 5, 8, 10, 15, 25, 47, 63, 88, 100):
        for class_id, cdef in content.classes.items():
            if cdef.get("retired"):
                continue
            hero = Hero(id="h", name="H", class_id=class_id, level=level)
            for seed in range(25):
                dropped = roll_gear(content.items, content.classes, content.balance, hero, level, Rng(seed), chance=1.0)
                assert dropped and content.items[dropped]["type"] != MAIL, (class_id, level, dropped)


def test_mail_never_comes_out_of_a_dungeon_chest_the_guardian_or_the_starter_gear(content):
    for level in (1, 5, 10, 30, 70, 100):
        for seed in range(150):
            piece = dungeon_rules.chest_gear(content.items, content.balance["gear"], level, Rng(seed), 1.0)
            assert piece and content.items[piece]["type"] != MAIL, (level, piece)
    for class_id, cdef in content.classes.items():
        if cdef.get("retired"):
            continue
        hero = Hero(id="h", name="H", class_id=class_id)
        offered = source_choices(content.items, content.classes, content.balance, hero, "guardian")
        assert len(offered) == 2 and all(content.items[i]["type"] != MAIL for i in offered), class_id
        assert all(content.items[i]["type"] != MAIL for i in starter_gear(content.items, content.classes, content.balance, hero))


def test_an_old_mail_class_starts_and_is_offered_leather():
    content = legacy_content()                                                   # the 0.31 classes, the Evocador among them
    content.balance["gear"]["armor_by_group"]["evocador"] = MAIL                 # as it was before 0.62.2
    hero = Hero(id="h", name="H", class_id="evocador_devastacion")
    assert set(starter_gear(content.items, content.classes, content.balance, hero)) == {"baston_1", "cuero_1"}
    assert source_choices(content.items, content.classes, content.balance, hero, "guardian") == ["guardian_baston", "guardian_cuero"]


def test_not_for_you_loot_is_never_mail(service, monkeypatch):
    """The "not for you" pieces (for selling) were where mail kept falling before 0.62.2: now only the other real types."""
    make_hero(service, class_id="cazador_dps")
    monkeypatch.setitem(service.content.balance["gear"], "drop_chance", 1.0)
    monkeypatch.setitem(service.content.balance["gear"], "for_you_chance", 0.0)  # only "not for you" pieces
    seen = set()
    hero = service._load(ACC)
    for seed in range(200):
        dropped = roll_gear(service.content.items, service.content.classes, service.content.balance, hero, 3, Rng(seed))
        seen.add(service.content.items[dropped]["type"])
    assert MAIL not in seen and {"placas", "tela"} <= seen


def test_a_won_fight_never_drops_mail(service, monkeypatch):
    """The real victory path: a common fight won with a drop every time (gear.drop_chance 1) never gives a mail piece."""
    make_hero(service, class_id="cazador_dps")
    monkeypatch.setitem(service.content.balance["gear"], "drop_chance", 1.0)
    monkeypatch.setitem(service.content.balance["gear"], "for_you_chance", 0.0)
    edef = service.content.enemies["lobo_ceniciento"]
    got = set()
    for seed in range(40):
        hero = service._load(ACC)
        state = make_combat("lobo_ceniciento", edef, 3, service._kit(hero), seed)
        state["outcome"] = "victory"
        service._end_combat(hero, state)
        service._save(hero)
        got |= {i for i in service._load(ACC).backpack if service.content.items.get(i, {}).get("kind") == "gear"}
    assert len(got) >= 3 and not any(service.content.items[i]["type"] == MAIL for i in got)


# ---------------------------------------------------------------- the leather twin of every mail piece


def test_every_mail_piece_has_its_leather_twin(content):
    for iid in mail_ids(content):
        item = content.items[iid]
        twin = retired_twin(content.items, iid, content.balance)
        assert twin and twin in content.items, iid
        new = content.items[twin]
        assert new["type"] == "cuero" and new["slot"] == item["slot"] and new["tier"] == item["tier"], iid
        assert new.get("source") == item.get("source") and new["req_level"] == item["req_level"], iid
        assert bool(new.get("masterwork")) == bool(item.get("masterwork")), iid
    assert retired_twin(content.items, "malla_3", content.balance) == "cuero_3"
    assert retired_twin(content.items, "cabeza_malla_12", content.balance) == "cabeza_cuero_12"
    assert retired_twin(content.items, "artesano_malla_2", content.balance) == "artesano_cuero_2"      # not espec_cuero_1
    assert retired_twin(content.items, "espec_malla_1", content.balance) == "espec_cuero_1"
    assert retired_twin(content.items, "artesano_pies_malla_7_obra", content.balance) == "artesano_pies_cuero_7_obra"
    assert retired_twin(content.items, "guardian_malla", content.balance) == "guardian_cuero"
    assert retired_twin(content.items, "cuero_3", content.balance) is None
    assert retired_twin(content.items, "espada_1", content.balance) is None
    assert retired_twin(content.items, "no_such_piece", content.balance) is None


# ---------------------------------------------------------------- the one-time change: the hero sheet


def test_a_new_world_records_an_empty_change_once(service):
    record = service.store.get("migrations", "malla_to_leather")
    assert record == {"at": service.clock.now(), "version": "0.62.2", "accounts": {},
                      "other": {"armory": 0, "gremio_fund": 0, "camp_fund": 0}}
    assert service.store.get("migrations", "peleteria_malla") is None


def test_worn_and_carried_mail_becomes_leather_with_everything_it_had(service):
    make_hero(service, class_id="guerrero_dps")
    service.set_handle(ACC, "@lyra")
    loose = {f"espada_{n}": 1 for n in range(1, 15)} | {f"daga_{n}": 1 for n in range(1, 8)}     # 21 loose pieces: over 20
    put_hero(service, level=20,
             gear={"arma": "espada_1", "armadura": "malla_3", "pies": "pies_malla_2"},
             gear_wear={"armadura": {"id": "malla_3", "cur": 41.5, "max": 96.0, "rep": 1}},
             backpack=dict(loose, malla_1=2, cuero_1=1, artesano_cabeza_malla_3_obra=1, pocion_vida=3),
             bag_wear={"malla_1": [{"id": "malla_1", "cur": 12.0, "max": 100.0, "rep": 0}],
                       "cuero_1": [{"id": "cuero_1", "cur": 50.0, "max": 100.0, "rep": 0}]},
             gear_enchants={"malla_3": {"id": "vigor", "value": 0.02}, "malla_1": {"id": "vigor", "value": 0.03},
                            "cuero_1": {"id": "vigor", "value": 0.01}, "malla_9": {"id": "vigor", "value": 0.03}},
             gear_signatures={"artesano_cabeza_malla_3_obra": "Bram"},
             gear_new=["malla_1", "cuero_1"])
    rearm(service)
    service = restart(service)
    hero = service._load(ACC)
    assert hero.gear == {"arma": "espada_1", "armadura": "cuero_3", "pies": "pies_cuero_2"}
    assert hero.gear_wear["armadura"] == {"id": "cuero_3", "cur": 41.5, "max": 96.0, "rep": 1}       # 🔧 its durability kept
    assert hero.backpack["cuero_1"] == 3 and "malla_1" not in hero.backpack
    assert hero.backpack["artesano_cabeza_cuero_3_obra"] == 1 and hero.backpack["pocion_vida"] == 3
    assert sum(n for i, n in hero.backpack.items() if service.content.items[i]["kind"] == "gear") == 25   # nothing lost over 20
    assert sorted(r["cur"] for r in hero.bag_wear["cuero_1"]) == [12.0, 50.0] and "malla_1" not in hero.bag_wear
    assert all(r["id"] == "cuero_1" for r in hero.bag_wear["cuero_1"])
    assert hero.gear_enchants["cuero_3"] == {"id": "vigor", "value": 0.02}                           # ✨ travels with it
    assert hero.gear_enchants["cuero_1"] == {"id": "vigor", "value": 0.03}                           # the better one stays
    assert "cuero_9" not in hero.gear_enchants and "malla_9" in hero.gear_enchants     # a record without its piece: no free ✨
    assert not any(i.startswith("malla") for i in hero.gear_enchants if i != "malla_9")
    assert hero.gear_signatures == {"artesano_cabeza_cuero_3_obra": "Bram"}                          # ✒️ too
    assert hero.gear_new == ["cuero_1"]
    record = service.store.get("migrations", "malla_to_leather")
    assert set(record) == {"at", "version", "accounts", "other"} and record["version"] == "0.62.2"
    assert record["at"] == service.clock.now() and record["other"] == {"armory": 0, "gremio_fund": 0, "camp_fund": 0}
    mine = record["accounts"][ACC]
    assert set(mine) == {"hero", "handle", "pieces"} and mine["hero"] == "Lyra" and mine["handle"] == "@lyra"
    assert sorted(map(tuple, mine["pieces"])) == sorted([("malla_3", "cuero_3"), ("pies_malla_2", "pies_cuero_2"),
                                                         ("malla_1", "cuero_1"), ("malla_1", "cuero_1"),
                                                         ("artesano_cabeza_malla_3_obra", "artesano_cabeza_cuero_3_obra")])
    stats = service._kit(hero)["gear_bonus"]
    assert stats["hp"] > 0                                                         # the worn leather counts in combat


def test_heroes_without_mail_are_not_touched_or_recorded(service):
    make_hero(service)
    make_hero(service, OTHER, "Bram")
    put_hero(service, OTHER, backpack={"malla_2": 1})
    before = service.store.get("hero", ACC)
    rearm(service)
    service = restart(service)
    assert service.store.get("hero", ACC) == before
    assert list(service.store.get("migrations", "malla_to_leather")["accounts"]) == [OTHER]
    assert service.store.get("migration_notice", ACC) is None


# ---------------------------------------------------------------- the one-time change: every other place


def test_mail_in_the_market_deliveries_armory_funds_repairs_and_dungeon_becomes_leather(service):
    make_hero(service)
    make_hero(service, OTHER, "Bram")
    put_hero(service, gear={"armadura": "malla_4"}, gear_wear={"armadura": {"id": "malla_4", "cur": 30.0, "max": 100.0, "rep": 0}})
    store = service.store
    store.put("market_order", "m1", {"id": "m1", "side": "sell", "good": "malla_2", "n": 2, "n0": 2, "price": 40, "by": OTHER,
                                     "name": "Bram", "at": 0, "until": 10 ** 9, "x": 0, "y": 0, "enchant": None, "sig": None,
                                     "wear": [{"id": "malla_2", "cur": 5.0, "max": 100.0, "rep": 0}, None]})
    store.put("market_order", "m2", {"id": "m2", "side": "sell", "good": "espada_2", "n": 1, "n0": 1, "price": 30, "by": OTHER,
                                     "name": "Bram", "at": 0, "until": 10 ** 9, "x": 0, "y": 0})
    store.put("market_index", "sell:armor", {"ids": [[40, "m1", "malla_2"]]})
    store.put("market_index", "sell:weapons", {"ids": [[30, "m2", "espada_2"]]})
    store.put("market_box", ACC, {"items": [{"good": "manos_malla_3", "n": 1, "at": 0, "from": "Bram", "why": "bought",
                                            "told": True, "wear": [{"id": "manos_malla_3", "cur": 70.0, "max": 100.0, "rep": 0}]},
                                           {"good": "pocion_vida", "n": 2, "at": 0, "why": "bought", "told": True}]})
    store.put("market_open", OTHER, {"side": "sell", "good": "malla_2", "price": 40, "n": 1})
    store.put("armory", "g1", {"items": [{"id": 1, "item": "piernas_malla_5", "enchant": {"id": "vigor", "value": 0.02},
                                          "sig": None, "by": "Bram", "by_id": OTHER, "at": 0,
                                          "wear": {"id": "piernas_malla_5", "cur": 9.0, "max": 92.0, "rep": 2}}],
                               "log": [{"k": "in", "who": "Bram", "item": "piernas_malla_5", "at": 0}], "seq": 1})
    store.put("gremio", "g1", {"id": "g1", "name": "Los Raíz", "fund": {"malla_1": 2, "madera": 5}, "gave": {OTHER: {"malla_1": 2}}})
    store.put("upgrades", "6:0", {"fund": {"cabeza_malla_1": 1}, "gave": {ACC: {"cabeza_malla_1": 1}}})
    store.put("repair_order", f"{ACC}|armadura", {"id": "r1", "by": ACC, "name": "Lyra", "slot": "armadura", "item": "malla_4",
                                                 "price": 30, "at": 0, "until": 10 ** 9})
    store.put("dungeon", ACC, {"day": 0, "delves": {}, "best": 3,
                               "deep": {"x": 3, "y": 3, "day": 0, "floor": 3, "fight": 0, "cleared": 2,
                                        "pot": {"coins": 10, "items": {"piel": 1}, "gear": ["espada_3", "malla_5"]}}})
    store.put("fallen_hero", f"{OTHER}#1", {"account": OTHER, "at": 0, "hero": {"name": "Viejo", "gear": {"armadura": "malla_1"}},
                                            "box": [{"good": "malla_1", "n": 1}]})
    archive = store.get("fallen_hero", f"{OTHER}#1")
    rearm(service)
    service = restart(service)
    order = store.get("market_order", "m1")
    assert order["good"] == "cuero_2" and order["n"] == 2 and order["wear"] == [{"id": "cuero_2", "cur": 5.0, "max": 100.0, "rep": 0}, None]
    assert store.get("market_order", "m2")["good"] == "espada_2"
    assert store.get("market_index", "sell:armor") == {"ids": [[40, "m1", "cuero_2"]]}
    assert store.get("market_index", "sell:weapons") == {"ids": [[30, "m2", "espada_2"]]}
    box = store.get("market_box", ACC)["items"]
    assert box[0]["good"] == "manos_cuero_3" and box[0]["wear"][0]["id"] == "manos_cuero_3" and box[1]["good"] == "pocion_vida"
    assert store.get("market_open", OTHER)["good"] == "cuero_2"
    armory = store.get("armory", "g1")
    assert armory["items"][0]["item"] == "piernas_cuero_5" and armory["items"][0]["wear"]["id"] == "piernas_cuero_5"
    assert armory["items"][0]["enchant"] == {"id": "vigor", "value": 0.02}
    assert armory["log"][0]["item"] == "piernas_malla_5"                                          # history stays as it was
    gremio = store.get("gremio", "g1")
    assert gremio["fund"] == {"cuero_1": 2, "madera": 5} and gremio["gave"] == {OTHER: {"malla_1": 2}}
    assert store.get("upgrades", "6:0")["fund"] == {"cabeza_cuero_1": 1}
    assert store.get("repair_order", f"{ACC}|armadura")["item"] == "cuero_4"                    # the order still counts
    assert store.get("dungeon", ACC)["deep"]["pot"]["gear"] == ["espada_3", "cuero_5"]
    assert store.get("fallen_hero", f"{OTHER}#1") == archive                                     # a memorial: untouched
    record = store.get("migrations", "malla_to_leather")
    assert record["other"] == {"armory": 1, "gremio_fund": 2, "camp_fund": 1}
    assert sorted(map(tuple, record["accounts"][ACC]["pieces"])) == sorted(
        [("malla_4", "cuero_4"), ("manos_malla_3", "manos_cuero_3"), ("malla_5", "cuero_5")])
    assert record["accounts"][OTHER]["pieces"] == [["malla_2", "cuero_2"], ["malla_2", "cuero_2"]]
    assert record["accounts"][OTHER]["hero"] == "Bram" and record["accounts"][OTHER]["handle"] == ""
    hero = service._load(ACC)
    assert hero.gear["armadura"] == "cuero_4" and service._repair_view(hero).kind      # the repair screen still opens


def test_the_change_runs_once_and_again_changes_nothing(service):
    make_hero(service)
    put_hero(service, backpack={"malla_1": 1})
    rearm(service)
    service = restart(service)
    first = service.store.get("migrations", "malla_to_leather")
    put_hero(service, backpack={"cuero_1": 1, "malla_2": 1})        # mail that shows up later is not touched by a restart...
    service = restart(service)
    assert service.store.get("migrations", "malla_to_leather") == first
    assert service._load(ACC).backpack == {"cuero_1": 1, "malla_2": 1}
    put_hero(service, backpack={"cuero_1": 1})
    hero_before = service.store.get("hero", ACC)
    rearm(service)
    service = restart(service)                                      # ...and running it again on a clean store changes nothing
    assert service.store.get("hero", ACC) == hero_before
    assert service.store.get("migrations", "malla_to_leather")["accounts"] == {}


# ---------------------------------------------------------------- the notice


def test_the_player_reads_once_which_pieces_became_leather(service):
    make_hero(service)
    put_hero(service, gear={"armadura": "malla_3"}, backpack={"malla_1": 2})
    rearm(service)
    service = restart(service)
    view = service.view(ACC)
    assert "La malla ya no existe" in view.notice and "Cota de malla" in view.notice and "×2" in view.notice
    assert "No perdiste nada" in view.notice
    again = service.view(ACC)
    assert not again.notice or "La malla ya no existe" not in again.notice
    assert service.store.get("migration_notice", ACC) is None


def test_the_notice_comes_in_english_for_an_english_player(service):
    make_hero(service)
    service.act(ACC, "lang:en")
    put_hero(service, backpack={"malla_1": 1})
    rearm(service)
    service = restart(service)
    view = service.act(ACC, "hero")
    assert "Mail no longer exists" in view.notice and "Patched Mail" in view.notice and "You lost nothing" in view.notice


# ---------------------------------------------------------------- the 🎓 ⛓️ Malla specialization


def test_the_mail_specialization_is_retired_and_its_place_is_free_again(service, monkeypatch):
    monkeypatch.setattr(GameService, "_knows", lambda self, hero, pid: True)
    make_hero(service)
    make_hero(service, OTHER, "Bram")
    put_hero(service, gold=0, professions={"peleteria": rank_xp(service, 30)}, prof_specs={"peleteria": ["peleteria_malla"]},
             spec_xp={"peleteria_malla": 1234})
    put_hero(service, OTHER, gold=0, professions={"peleteria": rank_xp(service, 80)},
             prof_specs={"peleteria": ["peleteria_malla", "peleteria_cuero"]}, spec_xp={"peleteria_malla": 10, "peleteria_cuero": 5})
    rearm(service)
    service = restart(service)
    hero = service._load(ACC)
    assert hero.prof_specs == {} and hero.spec_xp == {"peleteria_malla": 1234}                     # its mastery stays saved
    assert service._pspec_choice(hero, "peleteria", "peleteria_cuero") == "pick"                   # a free place: no switch cost
    assert service._pspec_choice(hero, "peleteria", "peleteria_malla") == "locked"                 # never offered again
    screen = service.act(ACC, "pspec:peleteria")
    assert "pspv:peleteria_malla" not in [a.id for a in screen.actions] and "Malla" not in "\n".join(screen.body)
    assert "pspp:peleteria_malla" not in [a.id for a in service.act(ACC, "pspv:peleteria_malla").actions]
    view = service.act(ACC, "pspp:peleteria_cuero")
    hero = service._load(ACC)
    assert hero.prof_specs == {"peleteria": ["peleteria_cuero"]} and hero.gold == 0                # picked for free
    other = service._load(OTHER)
    assert other.prof_specs == {"peleteria": ["peleteria_cuero"]} and other.spec_xp["peleteria_malla"] == 10
    assert service._pspec_choice(other, "peleteria", "peleteria_talabarteria") == "pick"           # rank 80: the 2nd is free too
    record = service.store.get("migrations", "peleteria_malla")
    assert record["version"] == "0.62.2" and record["accounts"][ACC]["specs"] == [["peleteria", "peleteria_malla", 1234]]
    assert record["accounts"][OTHER]["hero"] == "Bram"
    notice = service.view(OTHER).notice
    assert "🎓" in notice and "Malla" in notice and "elige otra gratis" in notice
    assert "malla_to_leather" not in (service.store.get("migration_notice", OTHER) or {})
    assert view.kind == "prof_specs"


def test_the_mail_specialization_gives_nothing_and_its_old_exclusives_stay_closed(content):
    specs = content.professions["specs"]
    assert profession_rules.spec_owner(specs, "peleteria_malla") == (None, None)
    assert [s["id"] for s in profession_rules.spec_list(specs, "peleteria")] == ["peleteria_cuero", "peleteria_talabarteria"]
    held = {"peleteria": ["peleteria_malla"]}
    assert profession_rules.spec_bonus(specs, held, {"peleteria_malla": 10 ** 6}, 100, "masterwork", type=MAIL) == 0.0
    recipes = content.professions["recipes"]
    assert recipes["espec_malla_1"].get("retired") and recipes["espec_malla_2"].get("retired")
    perk = content.professions["professions"]["peleteria"]["perk"]
    assert MAIL not in perk["armor_type"]
    alloys = next(s for s in specs["fundicion"] if s["id"] == "fundicion_aleaciones")
    assert all(MAIL not in e.get("types", []) for e in alloys["effects"])


# ---------------------------------------------------------------- texts


def test_texts_in_both_languages_and_no_class_says_mail(service):
    for lang in ("es", "en"):
        with service.texts.use(lang):
            for key in ("nomail.notice", "nomail.line", "nomail.line_n", "nomail.kept", "nomail.spec"):
                assert service.texts.has(key), (lang, key)
            for group in ("cazador", "chaman", "evocador"):
                desc = service.texts.t(f"class_group.{group}.desc").lower()
                assert "malla" not in desc and "mail" not in desc, (lang, group)
            alloys = service.texts.t("spec.fundicion_aleaciones.desc").lower()
            assert "malla" not in alloys and "mail" not in alloys
    assert not service.texts.missing
