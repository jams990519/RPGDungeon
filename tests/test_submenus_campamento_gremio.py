"""Submenus of the camp and the guild (D-302, 0.39.4): the camp hub shows what you can do, ℹ️ Información the rest; the guild
screen keeps its top part and opens 👥 Miembros, 💰 Fondos and 📢 Chat as buttons.

[ES] Pruebas de lo que pidió el dueño el 20-oct-2026 ("vas a separarlo en dos partes. Lo que puedes hacer en el campamento, eso
es lo que se va a mostrar. Y dentro del menú, vas a poner un apartado que explique la parte de arriba"; del gremio: "lo de
arriba… perfecto, eso se mantiene", "👥 Miembros… lo vas a volver un botón", "Fondo del campamento → un botón… listado en orden
con su código", "Últimos mensajes → conviértelo en un botón de 📢 Chat… el listado del chat del último día"; y su regla D-287:
"prefiero que haya submenús con más información"):
- el centro de tu campamento muestra solo su nombre y lo que puedes hacer; lo de arriba (fundador, etapa, nivel, miembros,
  costo de agrandar, mejoras y 🛡️ Defensa, despensa, beneficios, próxima oleada) está en 🏰 Gestionar → ℹ️ Información, con
  ↩️ Volver; una oleada en curso (y 🛡️ Defender) sigue a la vista en el centro; los visitantes ven lo de siempre;
- 🛡️ Gremio después de fundar: arriba el gremio (nivel, lo que pide para subir, "cuenta lo que hacen todos…"), y los botones
  👥 Miembros (N/cupo), 💰 Fondos del campamento y 📢 Chat; la ⚔️ Armería muestra su "0/30" solo en su pantalla;
- 👥 Miembros lista a los miembros con su código y a los que esperan lugar, con 🙋 Solicitudes cuando hay;
- 💰 Fondos del campamento lista cada recurso con su código de 📦 Recursos, en orden por código, dice para qué sirve el fondo
  y tiene 💰 Depositar;
- 📢 Chat muestra los mensajes del último día (el más nuevo al final), como mucho gremio.chat_shown y gremio.chat_max_chars
  letras, y tiene 📢 Mensaje;
- antes de fundar, la pantalla del gremio tiene la misma forma; los botones viejos siguen; y todo se lee en inglés.
Archivo: tests/test_submenus_campamento_gremio.py · Módulo: M14 Construcción y M15 Social · Prueba: engine/service/game.py
(_camp_here_view, _camp_info_view, _camp_info_lines, _camp_summary_lines, _camp_member_actions, _guild_view, _raid_lines) y
engine/service/gremio.py (_gremio_view, _guild_members_view, _gremio_members_view, _camp_members_view, _guild_funds_view,
_fund_item_lines, _guild_chat_view, _chat_lines, _gremio_post); content/balance.yaml (gremio.messages_kept, chat_hours,
chat_shown, chat_max_chars); content/locales/es_submenus.yaml y en_submenus.yaml.
"""

from conftest import make_hero
from engine.service.game import HUB_BUTTONS, button_cap
from test_camps import found_at, old_camp_at, place
from test_espera_del_gremio import waiting_cora
from test_gremio_desde_el_inicio import join as gremio_join, new_gremio
from test_guilds import join

KEY = "6:0"
DAY = 24 * 3600
HOUR = 3600
RAID_GAP = 7 * DAY / 3          # D-154: 3 raids per real week (balance.yaml raids.per_week)
INFO_BITS = ("fundado por", "🏰 Etapa:", "Eres parte", "Agrandar el territorio", "Mejoras construidas", "Próxima oleada")   # D-304


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def set_hero(service, account, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)


def put_messages(service, key, messages):
    camp = service.store.get("camp", key)
    camp["messages"] = messages
    service.store.put("camp", key, camp)


# ---------------------------------------------------------------------------------------------------- 🏕️ the camp hub

def test_the_camp_hub_shows_its_name_and_what_you_can_do_and_info_has_the_rest(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    hub = service.act("test:1", "claro")
    assert hub.kind == "player_camp" and hub.body[0] == "🏕️ Campo 1 6" and "🏕️ Lo que puedes hacer en tu campamento:" in hub.body
    assert not any(bit in text(hub) for bit in INFO_BITS), text(hub)
    assert len(hub.actions) <= HUB_BUTTONS and "campmgmt" in ids(hub)            # the hub keeps its 8 (E-132)
    manage = service.act("test:1", "campmgmt")
    assert "campinfo" in ids(manage) and len(manage.actions) <= button_cap(manage.kind)
    assert any(line.startswith("ℹ️ Información:") for line in manage.body)       # 🏰 Gestionar names it
    info = service.act("test:1", "campinfo")
    assert info.kind == "camp_info" and info.title == "ℹ️ Información del campamento"
    assert all(bit in text(info) for bit in INFO_BITS), text(info)
    assert any("Miembros: 1 de 5" in line for line in info.body) and any("Gremio: Campo 1 6" in line for line in info.body)
    assert ids(info) == ["campmgmt"] and len(info.actions) <= button_cap(info.kind)   # ↩️ back to 🏰 Gestionar


def test_info_only_at_your_camp_and_visitors_see_the_summary_as_before(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    place(service, "test:1", 7, 0)                                               # away from its camp
    assert service.act("test:1", "campinfo").kind != "camp_info"
    place(service, "test:2", 6, 0)                                               # a visitor
    visit = service.act("test:2", "claro")
    assert visit.kind == "player_camp" and "fundado por Lyra" in text(visit) and "🛡️ Defensa" in text(visit)
    assert "askjoin" in ids(visit) and "campinfo" not in ids(visit)


def test_a_raid_going_on_stays_on_the_hub(service, clock):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    clock.advance(RAID_GAP)
    hub = service.act("test:1", "claro")
    assert service.store.get("camp", KEY).get("raid") and ids(hub)[0] == "defend"
    assert any(line.startswith("🔔 ¡Oleada!") for line in hub.body) and "🛡️ ¡Oleada en curso! Toca 🛡️ Defender y pelea una vez." in hub.body
    assert not any(bit in text(hub) for bit in INFO_BITS[:5])                    # the rest is still in ℹ️ Información


def test_the_hub_still_settles_the_pantry_and_info_shows_it(service, clock):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    camp = service.store.get("camp", KEY)
    camp["level"] = 3                                                            # aldea: the pantry opens
    service.store.put("camp", KEY, camp)
    service.act("test:1", "claro")
    service.store.put("pantry", KEY, {"rations": 10.0, "at": clock.now()})
    clock.advance(DAY)
    hub = service.act("test:1", "claro")
    assert service.store.get("pantry", KEY)["rations"] == 9                      # consumed on the visit, as before
    assert not any("Despensa" in line for line in hub.body)
    assert any("Despensa" in line for line in service.act("test:1", "campinfo").body)


# ---------------------------------------------------------------------------------------------------- 🛡️ the guild after founding

def test_the_guild_keeps_its_top_and_opens_members_funds_and_chat(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    guild = service.act("test:1", "guild")
    body = text(guild)
    assert guild.kind == "guild" and "🛡️ Campo 1 6 · nivel 1" in body and "Para subir a nivel 2" in body
    assert "Cuenta lo que hacen todos los miembros desde que entran." in body
    assert ids(guild)[:5] == ["gmembers", "gfunds", "gchat", "garm", "gzones"] and len(guild.actions) <= HUB_BUTTONS
    assert guild.actions[0].label == "👥 Miembros (1/5)" and guild.actions[1].label == "💰 Fondos del campamento"
    assert guild.actions[2].label == "📢 Chat"
    assert not any(line.startswith("/m") for line in guild.body)                # the members: in 👥 Miembros
    assert "Últimos mensajes" not in body and "Fondo" not in body and "Armería" not in body
    armory = service.act("test:1", "garm")
    assert "🗃️ 0/30 piezas" in armory.body and ids(armory) == ["guild"]          # ⚔️ its count, on its own screen


def test_members_list_the_members_and_who_waits_for_room(service):
    waiting_cora(service)                                                         # Lyra's full camp; Cora waits in its guild
    members = service.act("test:1", "gmembers")
    assert members.kind == "guild_members" and members.title == "👥 Miembros del gremio"
    lines = [line for line in members.body if line.startswith("/m")]
    assert lines[0].startswith("/m1 👑 Lyra") and "Bram" in lines[1] and lines[2].startswith("/m3 ⏳ Cora")
    assert "⏳ Esperando lugar en el campamento (1/10):" in members.body and any("🤝 Asistentes" in line for line in members.body)   # D-304: asistentes
    assert ids(members) == ["guild"] and len(members.actions) <= button_cap(members.kind)
    assert ids(service.text("test:1", "/m3"))[-1] == "gmembers"                   # a card goes back to 👥 Miembros
    assert "gmembers" in ids(service.act("test:3", "guild"))                     # who waits sees it too
    assert any("Cora" in line for line in service.act("test:3", "gmembers").body)


def test_join_requests_wait_in_members(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    place(service, "test:2", 6, 0)
    service.act("test:2", "askjoin")
    guild = service.act("test:1", "guild")
    assert "🙋 1 solicitud espera: míralas en 👥 Miembros." in guild.body and "creqs" not in ids(guild)
    members = service.act("test:1", "gmembers")
    assert ids(members) == ["creqs", "guild"]
    requests = service.act("test:1", "creqs")
    assert requests.kind == "camp_requests" and ids(requests)[-1] == "gmembers"


def test_funds_list_each_resource_with_its_code_in_code_order(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    record = service._upgrades(KEY)
    record["fund"] = {"fibra": 3, "piedra": 5, "madera": 12}
    service.store.put("upgrades", KEY, record)
    funds = service.act("test:1", "gfunds")
    assert funds.kind == "guild_funds" and funds.title == "💰 Fondos del campamento"
    assert "obras activas" in funds.body[0] and any(line.startswith("🔨 0 obras activas") for line in funds.body)
    lines = [line for line in funds.body if line.startswith("/")]
    codes = [service._resource_code(i) for i in ("madera", "piedra", "fibra")]
    assert codes == sorted(codes) and all(codes)                                  # the 📦 Recursos codes, in order
    assert lines == [f"{codes[0]} 🪵 Madera ×12", f"{codes[1]} 🪨 Piedra ×5", f"{codes[2]} 🧵 Fibra ×3"]
    assert ids(funds) == ["gfund", "guild"] and funds.actions[0].label == "💰 Depositar"
    deposit = service.act("test:1", "gfund")
    assert deposit.kind == "camp_fund" and ids(deposit) == ["gfunds"]             # ↩️ back to 💰 Fondos
    assert service.text("test:1", codes[0]).kind == "resource"                   # the code says what it is for (D-243)
    record["fund"] = {}
    service.store.put("upgrades", KEY, record)
    assert "El fondo está vacío" in text(service.act("test:1", "gfunds"))


def test_chat_shows_the_last_day_capped_newest_last_with_the_write_button(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    join(service, "test:2")
    now = clock.now()
    old = [{"by": "Bram", "id": "test:2", "text": "viejo", "at": now - 25 * HOUR}]
    recent = [{"by": "Bram", "id": "test:2", "text": f"m{n}", "at": now - (30 - n) * 60} for n in range(30)]
    put_messages(service, KEY, old + recent)
    chat = service.act("test:1", "gchat")
    shown = [line for line in chat.body if line.startswith("💬 Bram:")]
    cap = service.content.balance["gremio"]["chat_shown"]
    assert chat.kind == "guild_chat" and len(shown) == cap == 20
    assert shown[-1] == "💬 Bram: m29" and shown[0] == "💬 Bram: m10" and "💬 Bram: viejo" not in chat.body
    assert ids(chat) == ["gmsg", "guild"] and any("le llega a todo tu gremio" in line for line in chat.body)
    service.content.balance["gremio"]["chat_max_chars"] = 60                    # long chats: only what fits
    shown = [line for line in service.act("test:1", "gchat").body if line.startswith("💬 Bram:")]
    assert 1 <= len(shown) < 20 and shown[-1] == "💬 Bram: m29" and sum(len(line) + 1 for line in shown) <= 60
    put_messages(service, KEY, old)
    assert "No hay mensajes del último día." in service.act("test:1", "gchat").body
    assert service.act("test:1", "gmsg").actions[0].id == "gchat"                # ❌ Cancelar goes back to 📢 Chat
    view = service.text("test:1", "Traigan piedra")
    assert view.kind == "guild_chat" and "💬 Lyra: Traigan piedra" in view.body
    assert service.content.balance["gremio"]["messages_kept"] == 50


# ---------------------------------------------------------------------------------------------------- before founding

def test_the_guild_before_founding_has_the_same_shape(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cora")
    gid, _ = new_gremio(service)
    gremio_join(service, gid, "test:2")
    service.act("test:3", f"greq:{gid}")
    guild = service.act("test:1", "guild")
    assert guild.kind == "gremio" and ids(guild)[:7] == ["gmembers", "gfunds", "gchat", "garm", "gmeet", "gzones", "gfound"]
    assert len(guild.actions) <= HUB_BUTTONS and "🙋 1 solicitud espera: míralas en 👥 Miembros." in guild.body
    assert not any(line.startswith("/m") for line in guild.body) and "Fondo" not in text(guild)
    members = service.act("test:1", "gmembers")
    assert [line[:3] for line in members.body if line.startswith("/m")] == ["/m1", "/m2"]
    assert ids(members) == ["greqs", "gleave", "guild"] and any("/inv_" in line for line in members.body)
    assert ids(service.act("test:1", "greqs"))[-1] == "gmembers"
    assert ids(service.act("test:2", "guild"))[-2] == "gleave"                   # 🚪 Salir fits for a plain member
    set_hero(service, "test:2", backpack={"piedra": 4, "madera": 7})
    service.text("test:2", "/f02")
    service.text("test:2", "/f01")
    funds = service.act("test:1", "gfunds")
    lines = [line for line in funds.body if line.startswith("/")]
    assert funds.title == "💰 Fondo del gremio" and lines == [f"{service._resource_code('madera')} 🪵 Madera ×7",
                                                              f"{service._resource_code('piedra')} 🪨 Piedra ×4"]
    assert any("Fundar el campamento pide" in line for line in funds.body) and ids(funds) == ["gfund", "guild"]
    assert ids(service.act("test:1", "gfund")) == ["gfunds"]
    service.text("test:2", "Nos vemos")
    chat = service.act("test:1", "gchat")
    assert "💬 Bram: Nos vemos" in chat.body and ids(chat) == ["gmsg", "guild"]


def test_old_buttons_still_work_and_everything_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    make_hero(service, "test:2", "Bram")
    place(service, "test:2", 6, 0)
    service.act("test:2", "askjoin")
    service.text("test:1", "Hello")
    for action in ("gmsg", "gfund", "creqs", "garm", "gfund:svc"):              # buttons of old Telegram messages
        assert "[" not in text(service.act("test:1", action)), action
    hub = service.act("test:1", "claro")
    assert hub.body[0] == "🏕️ Campo 1 6" and "[" not in text(hub)
    assert service.act("test:1", "campmgmt").actions[-2].label == "ℹ️ Info"
    info = service.act("test:1", "campinfo")
    assert info.title == "ℹ️ Camp info" and "[" not in text(info)
    guild = service.act("test:1", "guild")
    assert [a.label for a in guild.actions[:3]] == ["👥 Members (1/5)", "💰 Camp funds", "📢 Chat"]
    assert "request is waiting" in text(guild)
    for action in ("gmembers", "gfunds", "gchat"):
        view = service.act("test:1", action)
        assert view.title and "[" not in text(view), action
    assert service.act("test:1", "gchat").title == "📢 Guild chat"
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
