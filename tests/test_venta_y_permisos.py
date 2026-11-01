"""💱 Selling by tiers and 🔑 camp permissions by player code (D-346, confirmed; how: D-347, provisional; 0.63).

[ES] Pruebas de lo que pidió el dueño el 31-oct-2026 ("que los jugadores puedan vender directamente sin necesidad de llegar al
campamento... dale niveles de importancia"; "agrega los permisos y que me dé la opción a través de un código de darle los
permisos a los jugadores"), con sus respuestas:
- la venta paga el 30 % desde cualquier lugar, el 50 % en una 🔥 fogata (como antes), el 60 % en tu campamento con el
  🏪 Puesto de trueque y el 70 % en un castillo; la venta a distancia paga al momento, pero antes muestra cuánto pagan los
  lugares mejores y se confirma; cada lugar compra lo mismo que antes (el 🏪 nunca la comida); el equipo también se vende de
  lejos; la fogata paga lo mismo que antes;
- solo el fundador da permisos, y son cuatro: 🏗️ Construcción, ⚒️ Oficios (con los oficios que elija), ⚔️ Armería y fondo,
  👥 Gente y chat; desde 🛡️ Gremio → 👥 Miembros → 👔 Encargados (el botón solo lo ve el fundador; 1-nov-2026): el tipo de
  permiso (/en1…/en4), la lista de miembros y el código de cada uno (/em1) lo da y el mismo código lo quita; al miembro le llega
  el aviso en su idioma; los 🤝 asistentes conservan lo suyo; quien sale pierde sus permisos; 👔 Encargados dice "👀 Lo que
  espera atención".
Archivo: tests/test_venta_y_permisos.py · Módulo: M13 Economía y M15 Social · Prueba: engine/service/sell_tiers.py,
engine/service/permissions.py y sus ganchos en engine/service/game.py y engine/service/gremio.py.
"""

from conftest import make_hero
from test_ayudantes import camp_with, make_helper, pushes
from test_camp_upgrades import build
from test_camps import place
from test_guilds import set_level

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def set_bag(service, account, **items):
    hero = service._load(account)
    hero.backpack = dict(items)
    hero.gold = 0
    service._save(hero)


# ------------------------------------------------------------------ 💱 the sale by tiers


def test_the_owners_tiers_and_what_a_stack_pays(service):
    shop = service.content.balance["shop"]
    assert shop["sell_tiers"] == {"remote": 0.30, "fire": 0.50, "camp": 0.60, "castle": 0.70}
    assert shop["sell_tiers"]["fire"] == shop["sell_ratio"]          # the campfire pays what it paid before
    # the base resources are worth 2: by the stack, every place pays something different (by the unit they would all pay 1)
    assert [service._sale_total("madera", 30, tier) for tier in ("remote", "fire", "camp", "castle")] == [18, 30, 36, 42]
    assert service._sale_total("madera", 1, "remote") == 1 and service._sale_total("madera", 0, "camp") == 0
    # every category keeps its campfire price and scales it the same way: a potion 0.25 at the fire, 0.15 from anywhere
    assert service._sale_ratio("pocion_vida", "fire") == shop["remedy_sell_ratio"]
    assert abs(service._sale_ratio("pocion_vida", "remote") - 0.15) < 1e-9
    for item_id in ("madera", "hierba_curativa", "tablon", "pocion_vida"):
        for n in (1, 3, 10, 29):
            fire = n * service._sell_price(item_id)
            assert service._sale_total(item_id, n, "remote") <= fire <= service._sale_total(item_id, n, "camp") \
                <= service._sale_total(item_id, n, "castle"), (item_id, n)


def test_sell_from_anywhere_asks_first_with_the_better_places_and_pays_at_once(service):
    make_hero(service, "test:1", "Lyra")
    place(service, "test:1", 9, 9)
    set_bag(service, "test:1", madera=10, pocion_vida=2)
    view = service.act("test:1", "res:0")                             # 📦 Recursos has 💱 Vender
    assert "sellv" in ids(view) and len(view.actions) <= 4
    view = service.act("test:1", "sellv")
    body = text(view)
    assert view.kind == "shop_sell" and "Vendes desde aquí" in body and "👉 🎒 Desde cualquier lugar: 30 %" in body
    assert "▫️ 🏰 En tu castillo: 70 %" in body and ids(view)[-1] == "res:0"
    view = service.text("test:1", "/v01")                             # the code asks first
    assert view.kind == "sell_confirm" and service._load("test:1").backpack["madera"] == 10
    body = text(view)
    assert "(aquí): 🥉6" in body and "fogata (🛒 mercader): 🥉10" in body and "Puesto de trueque: 🥉12" in body
    assert "castillo: 🥉14" in body and ids(view) == ["sellok:madera", "sellv"]
    view = service.act("test:1", "sellok:madera")
    hero = service._load("test:1")
    assert "madera" not in hero.backpack and hero.gold == 6 and "Vendiste" in view.notice
    view = service.text("test:1", "/v61")                             # a potion: the camp and the castle do not buy it
    assert view.kind == "sell_confirm" and "no compran esto" in text(view) and "castillo:" not in text(view)


def test_the_campfire_sells_as_before_without_asking(service):
    make_hero(service, "test:1", "Lyra")                              # a new hero stands at a campfire
    set_bag(service, "test:1", madera=10, hierba_curativa=3)
    view = service.act("test:1", "shop:sell")
    assert view.kind == "shop_sell" and ids(view)[-1] == "shop" and "👉 🔥 En una fogata (🛒 mercader): 50 %" in text(view)
    service.text("test:1", "/v06")                                    # the unit price of always, no confirmation
    hero = service._load("test:1")
    expected = 3 * max(1, int(service.content.items["hierba_curativa"]["price"] * 0.5))
    assert "hierba_curativa" not in hero.backpack and hero.gold == expected
    service.act("test:1", "sell:all")
    assert "madera" not in service._load("test:1").backpack and service._load("test:1").gold == expected + 10
    hero = service._load("test:1")                                    # busy at the campfire: it is a remote sale (asks)
    hero.backpack = {"madera": 10}
    hero.activity = {"kind": "rest", "until": service.clock.now() + 3600}
    service._save(hero)
    assert service.act("test:1", "sell:all").kind == "sell_confirm"


def test_the_camp_pays_60_and_the_castle_70_never_buying_food(service):
    camp_with(service)
    build(service, "trueque")
    set_bag(service, "test:1", madera=10, carne=3)
    view = service.act("test:1", "svc:oficio")
    assert "csell" in ids(view) and "Aquí pagan el 60 %" in text(view)
    service.act("test:1", "csell")
    hero = service._load("test:1")
    assert hero.gold == 12 and hero.backpack == {"carne": 3}          # 10 wood: 12 at the camp (10 at a campfire)
    view = service.act("test:1", "sellv")                             # 💱 Vender at the camp: food goes the remote way (🎒)
    assert "Vendes en tu campamento" in text(view) and any("Carne" in line and "🎒" in line for line in view.body)
    assert service.text("test:1", "/v07").kind == "sell_confirm"
    set_level(service, 9)                                             # a castle
    set_bag(service, "test:1", madera=10)
    assert "Tu castillo paga el 70 %" in text(service.act("test:1", "svc:oficio"))
    service.text("test:1", "/v01")                                    # at your camp a material sells at once, at its tier
    assert service._load("test:1").gold == 14


def test_gear_sells_from_anywhere_after_asking(service):
    make_hero(service, "test:1", "Lyra")
    place(service, "test:1", 9, 9)
    hero = service._load("test:1")
    hero.backpack = {"espada_2": 1}
    service._save(hero)
    view = service.act("test:1", "item:espada_2")
    assert "sellgq:espada_2" in ids(view) and len(view.actions) <= 4 and "Desde aquí te dan" in text(view)
    view = service.act("test:1", "sellgq:espada_2")
    assert view.kind == "sell_confirm" and ids(view) == ["sellgok:espada_2", "item:espada_2"]
    gold = service._load("test:1").gold
    service.act("test:1", "sellgok:espada_2")
    hero = service._load("test:1")
    remote, fire = service._sale_total("espada_2", 1, "remote"), service._sale_total("espada_2", 1, "fire")
    assert "espada_2" not in hero.backpack and gold + remote <= hero.gold and remote < fire


def test_every_sale_goes_through_the_trade_perk(service, monkeypatch):
    calls = []
    original = type(service)._merchant_sale

    def spy(self, hero, base, sale="goods"):
        calls.append(sale)
        return original(self, hero, base, sale)

    monkeypatch.setattr(type(service), "_merchant_sale", spy)
    camp_with(service)
    build(service, "trueque")
    set_bag(service, "test:1", madera=5, piedra=5)
    service.act("test:1", "csell")
    place(service, "test:1", 9, 9)
    set_bag(service, "test:1", madera=5)
    service.act("test:1", "sellok:madera")
    assert calls == ["barter", "goods"]


# ------------------------------------------------------------------ 🔑 permissions: 👔 Encargados (only the founder)


def grant(service, key, member, founder="test:1"):
    """👔 Encargados → the permission type (/en1…/en4) → the member's code (/em1…); returns the screen after the code."""
    from engine.service.permissions import PERM_KEYS
    service.act(founder, "staff")
    view = service.text(founder, f"/en{PERM_KEYS.index(key) + 1}")
    code = next(line.split()[0] for line in view.body if line.startswith("/em") and service._hero_name(member) in line)
    return service.text(founder, code)


def test_only_the_founder_sees_and_opens_encargados(service):
    camp_with(service, "Bram", "Cora")
    view = service.act("test:1", "gmembers")                          # 🛡️ Gremio → 👥 Miembros → 👔 Encargados
    assert "staff" in ids(view) and len(view.actions) <= 4
    assert "staff" not in ids(service.act("test:2", "gmembers"))      # nobody else gets the button
    view = service.act("test:2", "staff")                             # …and by id it refuses
    assert view.kind == "guild_members" and "solo del fundador" in view.notice
    assert service.text("test:2", "/en1").kind == "guild_members"
    view = service.act("test:1", "staff")
    body = text(view)
    assert view.kind == "camp_staff" and len(view.actions) <= 4 and ids(view) == ["armlock", "gmembers"]
    assert "/en1 🏗️ Construcción: —" in view.body and "/en2 ⚒️ Oficios: —" in view.body
    assert "/en3 ⚔️ Armería y fondo: —" in view.body and "/en4 👥 Gente y chat: —" in view.body
    assert "👀 Lo que espera atención:" in body
    view = service.text("test:1", "/en1")                             # a type: every member with a code
    assert view.kind == "camp_staff_type" and ids(view) == ["staff"]
    assert "/em1 ▫️ Bram" in view.body or "/em2 ▫️ Bram" in view.body
    assert not any("Lyra" in line for line in view.body if line.startswith("/em"))     # not the founder
    assert service.act("test:1", "perms").kind == "camp_staff"       # /permisos is the same screen
    code = service.player_code("test:2")
    card = service.text("test:1", f"/permiso {code}")                 # by player code: what they have (read-only)
    assert card.kind == "camp_perm_card" and ids(card) == ["staff", "gmembers"] and "👔 Encargados" in text(card)
    assert "No hay ningún jugador con el código 99999999" in service.text("test:1", "/permiso 99999999").notice
    make_hero(service, "test:9", "Zed")
    assert "no es miembro" in service.text("test:1", f"/permiso {service.player_code('test:9')}").notice


def test_the_same_code_gives_and_takes_building_and_the_member_hears_it_in_english(service):
    camp_with(service, "Bram")
    service.store.put("prefs", "test:2", {"lang": "en"})
    record = service._upgrades(KEY)
    uid = service._available_works(service.store.get("camp", KEY), record)[0]
    service.act("test:2", f"upact:{uid}")
    assert uid not in (service._upgrades(KEY).get("active") or [])  # a plain member cannot
    view = grant(service, "build", "test:2")
    assert "Le diste a Bram el permiso 🏗️ Construcción" in view.notice and "El mismo código se lo quita" in view.notice
    assert view.kind == "camp_staff_type" and any(line.endswith("✅ Bram") for line in view.body)
    told = pushes(service, "test:2", "gremio_news")
    assert told and "you were given the 🏗️ Building permission" in told[0].body[0]
    service.act("test:2", f"upact:{uid}")
    assert uid in service._upgrades(KEY)["active"]
    guild = service.act("test:1", "gmembers")
    assert any(line.startswith("/m") and "🏗️ Bram" in line for line in guild.body) and "🔑 Permisos que dio" in text(guild)
    assert "/en1 🏗️ Construcción: Bram" in service.act("test:1", "staff").body
    view = grant(service, "build", "test:2")                          # the same code again takes it away
    assert "Le quitaste a Bram" in view.notice and not service._camp_can(service.store.get("camp", KEY), "test:2", "build")
    assert "the 🏗️ Building permission was taken from you" in pushes(service, "test:2", "gremio_news")[0].body[0]
    assert "no está en tu última lista" in service.text("test:1", "/em9").notice


def test_crafts_let_a_member_use_the_closed_fund_only_with_the_chosen_professions(service):
    camp_with(service, "Bram")
    record = service._upgrades(KEY)
    record["fund"] = {"tablon": 50}
    record["fund_crafts"] = False                                     # the founder closed it
    service.store.put("upgrades", KEY, record)
    bram = service._load("test:2")
    assert service._fund_pool(bram, "camp", "carpinteria")["usable"] == {}
    view = grant(service, "craft", "test:2")                          # ⚒️ → Bram: the professions sub-list
    assert view.kind == "camp_perm_craft" and ids(view) == ["permca:test:2", "permcn:test:2", "stf:craft"]
    view = service.text("test:1", "/pc7")                             # 🪑 Carpintería is the 7th of the list
    assert "🪑 Carpintería" in view.notice and "/pc7 ✅ 🪑 Carpintería" in view.body
    bram = service._load("test:2")
    pool = service._fund_pool(bram, "camp", "carpinteria")
    assert pool["usable"].get("tablon", 0) > 0 and service._fund_pool(bram, "camp", "cocina")["usable"] == {}
    assert service._pool_usable(pool, "carpinteria") and not service._pool_usable(pool, "herreria")
    assert any("tu permiso ⚒️ te deja usarlo con: 🪑 Carpintería" in line for line in service._fund_pool_lines(pool))
    lyra = service._load("test:1")                                    # the founder always can
    assert service._fund_pool(lyra, "camp", "cocina")["usable"].get("tablon", 0) > 0
    assert any(line.endswith("Bram: 🪑") for line in service.act("test:1", "stf:craft").body)
    service.act("test:1", "permca:test:2")
    assert len(service.store.get("camp", KEY)["perms"]["test:2"]["craft"]) == len(service._perm_professions())
    service.act("test:1", "permcn:test:2")
    assert "test:2" not in (service.store.get("camp", KEY).get("perms") or {})


def test_armory_and_fund_lock_the_armory_and_take_only_what_the_works_leave(service):
    camp_with(service, "Bram")
    hero = service._load("test:1")
    hero.backpack["espada_2"] = 1
    service._save(hero)
    service.act("test:1", "garm")
    service.text("test:1", "/a1")                                     # the founder leaves a piece
    view = service.act("test:1", "armlock")
    assert service.store.get("camp", KEY)["armory_lock"] and "🔓 Abrir la armería" in view.actions[0].label
    assert "armlock" not in ids(service.act("test:2", "garm"))       # only the founder closes or opens it
    view = service.text("test:2", "/t1")
    assert "cerró la armería" in view.notice and "espada_2" not in service._load("test:2").backpack
    record = service._upgrades(KEY)
    reserve = service._fund_reserve(service.store.get("camp", KEY), record).get("madera", 0)
    record["fund"] = {"madera": reserve + 5}
    service.store.put("upgrades", KEY, record)
    assert "hace falta el permiso ⚔️" in service.text("test:2", "/fs01").notice
    grant(service, "armory", "test:2")
    service.act("test:2", "garm")
    service.text("test:2", "/t1")
    assert service._load("test:2").backpack.get("espada_2") == 1
    hero = service._load("test:2")
    hero.backpack.pop("madera", None)
    service._save(hero)
    view = service.text("test:2", "/fs01")
    assert "Sacaste del fondo" in view.notice and service._load("test:2").backpack["madera"] == 5
    assert service._upgrades(KEY)["fund"].get("madera", 0) == reserve      # what the works need stays
    assert "No sobra" in service.text("test:2", "/fs01").notice
    assert any("📤 Bram sacó" in line for line in service._fund_log_lines(service._upgrades(KEY)))


def test_people_and_chat_answer_requests_and_send_announcements(service):
    camp_with(service, "Bram", "Cora")
    grant(service, "people", "test:2")
    pushes(service, "test:2")
    make_hero(service, "test:9", "Zed")
    place(service, "test:9", 6, 0)
    service.act("test:9", "askjoin")
    assert any(v.kind == "camp_join" for v in pushes(service, "test:2"))     # 👥 gets the request too
    view = service.act("test:2", "gmembers")
    assert "creqs" in ids(view) and "staff" not in ids(view)
    service.act("test:2", f"join:{KEY}:test:9:y")
    assert "test:9" in service.store.get("camp", KEY)["members"]
    view = service.act("test:2", "gchat")
    assert "gnote" in ids(view) and "gnote" not in ids(service.act("test:3", "gchat"))
    service.act("test:2", "gnote")
    view = service.text("test:2", "Mañana todos a la muralla")
    assert "Anuncio enviado" in view.notice
    assert service.act("test:3", "guild").body[0] == "📣 Bram: Mañana todos a la muralla"
    assert any(v.kind == "gremio_message" and "Mañana" in v.body[0] for v in pushes(service, "test:3"))


def test_assistants_keep_their_powers_and_leaving_takes_the_permissions(service):
    camp_with(service, "Bram", "Cora")
    make_helper(service, "test:3")
    camp = service.store.get("camp", KEY)
    assert service._camp_can(camp, "test:3", "build") and service._camp_can(camp, "test:3", "people")
    assert not service._camp_can(camp, "test:3", "armory") and not service._camp_can(camp, "test:3", "craft", "cocina")
    assert service._camp_can(camp, "test:1", "craft", "cocina")      # the founder can everything
    view = grant(service, "build", "test:3")                          # an assistant has it by the role: nothing changes
    assert "por su cargo de asistente" in view.notice and "test:3" not in (service.store.get("camp", KEY).get("perms") or {})
    assert any("🤝 Cora (por su cargo" in line for line in view.body)
    grant(service, "armory", "test:2")
    service.act("test:2", "leave")
    camp = service.store.get("camp", KEY)
    assert "test:2" not in camp["members"] and "test:2" not in (camp.get("perms") or {})
    assert not service._camp_can(camp, "test:2", "armory")


def test_what_waits_for_attention(service):
    camp_with(service, "Bram")
    view = service.act("test:1", "staff")
    assert "👀 Lo que espera atención:" in view.body and any(line.startswith("▶️") for line in view.body)
    make_hero(service, "test:9", "Zed")
    place(service, "test:9", 6, 0)
    service.act("test:9", "askjoin")
    view = service.act("test:1", "staff")
    assert any(line.startswith("🙋 1 solicitud para entrar: con 👥") for line in view.body)


def test_patch_faq_and_both_languages(service):
    patch = service.content.patches["v0_63"]
    assert patch["version"] == "0.63" and patch["title_en"] and len(patch["notes"]) == len(patch["notes_en"])
    assert "v0_63" in service.content.patches                                       # 0.63.1 came after it
    faq = service.content.faq["questions"]
    for code in ("d68", "d69"):
        assert code in faq
        for lang in ("es", "en"):
            assert service.content.locales[lang]["faq"][code]["a"]       # (every key in both: tests/test_idiomas.py)
