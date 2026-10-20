"""The founder's 🤝 helpers (D-289, 0.39): 1 per 5 members; they activate works, invite and answer requests, nothing more.

[ES] Pruebas de lo que pidió y respondió el dueño el 19-oct-2026 ("tienes que agregar la opción de poner un ayudante desde el
primer día que se crea el campamento y a medida que aumenta la cantidad puede aumentar también"; respuesta: 1 por cada 5
miembros; activan obras, invitan con /inv_ y aceptan solicitudes, pero no renombran ni nombran a otros ayudantes):
- el tope es máx(1, ⌈miembros ÷ 5⌉); si baja, los que ya son ayudantes se quedan pero no entra uno nuevo;
- el fundador nombra y saca ayudantes desde la tarjeta del miembro (/m2 en 🛡️ Gremio → 👥 Miembros, D-302); al miembro le
  llega el aviso; 🤝 junto a su nombre;
- un ayudante activa obras, invita con /inv_, recibe y responde las solicitudes (también desde 🙋 Solicitudes de 👥 Miembros);
  no renombra, no nombra ayudantes y no crea el gremio D-97; quien sale del campamento deja de ser ayudante;
- al fundar, los oficiales del gremio que entran al campamento quedan de ayudantes (hasta el tope); y se lee en inglés.
Archivo: tests/test_ayudantes.py · Módulo: M15 Social · Prueba: engine/service/gremio.py (_helpers_cap, _camp_manager,
_camp_member_view, _camp_helper_toggle, _camp_requests_view, _camp_members_view, _invite_code, _gremio_camp_answer) y
engine/service/game.py
(_ask_join, _answer_join, _leave_camp, _activate_work, _guild_view).
"""

from conftest import make_hero
from test_camps import old_camp_at, place
from test_guilds import join, set_level

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def pushes(service, account, kind=None):
    return [v for acc, v in service.tick() if acc == account and (kind is None or v.kind == kind)]


def camp_with(service, *names, level=5):
    """An old camp at 6:0 founded by Lyra (test:1), of `level`, with the given members (test:2, test:3…), all at its center."""
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    set_level(service, level)
    for n, name in enumerate(names, 2):
        make_hero(service, f"test:{n}", name)
        join(service, f"test:{n}")
        place(service, f"test:{n}", 6, 0)
    service.tick()


def make_helper(service, account):
    camp = service.store.get("camp", KEY)
    camp.setdefault("helpers", []).append(account)
    service.store.put("camp", KEY, camp)


def code_of(service, view, name):
    line = next(line for line in view.body if line.startswith("/m") and name in line)
    return line.split()[0]


def test_one_helper_per_five_members_never_under_one(service):
    for members, cap in ((1, 1), (2, 1), (5, 1), (6, 2), (10, 2), (11, 3), (20, 4)):
        assert service._helpers_cap({"members": [f"a{n}" for n in range(members)]}) == cap, members
    assert service.content.balance["camps"]["helpers_per_members"] == 5


def test_the_founder_names_and_removes_helpers_from_the_member_card(service):
    camp_with(service, "Bram", "Cora")
    guild = service.act("test:1", "gmembers")                                 # D-302: the members live in 👥 Miembros
    assert any("🤝 Ayudantes (0/1)" in line for line in guild.body)
    card = service.text("test:1", code_of(service, guild, "Bram"))
    assert card.kind == "gremio_member" and "ghelp:test:2" in ids(card)
    view = service.act("test:1", "ghelp:test:2")
    assert "ahora es ayudante" in view.notice and service.store.get("camp", KEY)["helpers"] == ["test:2"]
    told = pushes(service, "test:2", "gremio_news")
    assert told and "Ahora eres ayudante en Roca Alta" in told[0].body[0]
    guild = service.act("test:1", "gmembers")
    assert any(line.startswith("/m") and "🤝 Bram" in line for line in guild.body)
    assert any("🤝 Ayudantes (1/1): Bram" in line for line in guild.body)
    card = service.text("test:1", code_of(service, guild, "Cora"))             # 3 members: room for 1 only
    assert "ghelp:test:3" not in ids(card) and any("uno por cada 5" in line for line in card.body)
    assert "uno por cada 5" in service.act("test:1", "ghelp:test:3").notice
    assert service.store.get("camp", KEY)["helpers"] == ["test:2"]
    assert "Solo el fundador" in service.act("test:2", "ghelp:test:3").notice   # a helper never names another
    assert "ghelp" not in " ".join(ids(service.text("test:2", "/m1")))
    view = service.act("test:1", "ghelp:test:2")
    assert "ya no es ayudante" in view.notice and service._camp_helpers(service.store.get("camp", KEY)) == []


def test_a_helper_activates_invites_and_answers_requests_but_does_not_rename_or_name(service):
    camp_with(service, "Bram")
    make_helper(service, "test:2")
    view = service.act("test:2", "upact:fogon")                              # D-291: activates works
    assert "Activaste" in view.notice and "fogon" in service._upgrades(KEY)["active"]
    make_hero(service, "test:4", "Dax")
    view = service.text("test:2", f"/inv_{service.player_code('test:4')}")   # D-280: invites into the camp
    assert "Invitaste a Dax" in view.notice
    service.act("test:4", "cinv:6:0:y")
    assert "test:4" in service.store.get("camp", KEY)["members"]
    make_hero(service, "test:5", "Eve")
    place(service, "test:5", 6, 0)
    service.tick()
    service.act("test:5", "askjoin")
    asks = pushes(service, "test:2", "camp_join")                            # the request reaches the helper too
    assert asks and all(len(a.id.encode()) <= 64 for a in asks[0].actions)
    assert "solicitud espera" in text(service.act("test:2", "guild"))        # D-302: a short line on 🛡️ Gremio
    guild = service.act("test:2", "gmembers")
    assert "creqs" in ids(guild)                                             # 🙋 Solicitudes in 👥 Miembros
    requests = service.act("test:2", "creqs")
    assert requests.kind == "camp_requests" and ids(requests) == ["join:6:0:test:5:y", "join:6:0:test:5:n", "gmembers"]
    service.act("test:2", "join:6:0:test:5:y")
    assert "test:5" in service.store.get("camp", KEY)["members"] and service._load("test:5").camp == KEY
    view = service.act("test:2", "rename")                                   # not rename...
    assert view.kind != "name_camp" and service.store.get("camp", KEY)["name"] == "Roca Alta"
    assert "Solo el fundador" in service.act("test:2", "ghelp:test:4").notice   # ...nor name helpers...
    service.act("test:2", "guildnew")                                        # ...nor create the D-97 guild
    assert service.store.get("guild", KEY) is None
    place(service, "test:4", 6, 0)
    plain = service.act("test:4", "upact:empalizada")                        # a plain member does none of it
    assert "fundador o un 🤝 ayudante" in plain.notice
    make_hero(service, "test:6", "Fio")
    assert "líder u oficial" in service.text("test:4", f"/inv_{service.player_code('test:6')}").notice


def test_if_the_cap_shrinks_helpers_stay_and_one_who_leaves_stops_being_one(service):
    camp_with(service, "Bram", "Cora", "Dax", "Eve", "Fio")                  # 6 members: room for 2
    service.act("test:1", "ghelp:test:2")
    service.act("test:1", "ghelp:test:3")
    assert service.store.get("camp", KEY)["helpers"] == ["test:2", "test:3"]
    service.act("test:6", "leave")                                           # 5 members: room for 1, both stay
    camp = service.store.get("camp", KEY)
    assert len(camp["members"]) == 5 and service._camp_helpers(camp) == ["test:2", "test:3"]
    assert "uno por cada 5" in service.act("test:1", "ghelp:test:4").notice   # but nobody new
    assert "Activaste" in service.act("test:3", "upact:fogon").notice
    service.act("test:2", "leave")
    camp = service.store.get("camp", KEY)
    assert "test:2" not in camp["members"] and camp["helpers"] == ["test:3"]
    assert not service._camp_manager(camp, "test:2")


def test_officers_of_the_guild_become_helpers_when_they_join_the_founded_camp(service, clock):
    from test_gremio_desde_el_inicio import fund_cost, join as gremio_join, keep_present, new_gremio, site
    for n, name in ((1, "Lyra"), (2, "Bram"), (3, "Cora")):
        make_hero(service, f"test:{n}", name)
    gid, _ = new_gremio(service)
    gremio_join(service, gid, "test:2")
    gremio_join(service, gid, "test:3")
    service.act("test:1", "goff:test:2")
    service.act("test:1", "goff:test:3")
    fund_cost(service, gid)
    site(service, "test:1", 6, 0)
    place(service, "test:2", 6, 0)
    service.act("test:2", "home")
    service.act("test:1", "found")
    keep_present(service, clock, ["test:1", "test:2"], 60)
    assert service.store.get("camp", KEY)["helpers"] == []
    service.act("test:2", f"gcamp:{gid}:y")
    assert service.store.get("camp", KEY)["helpers"] == ["test:2"]           # an officer: helper (room for 1 of 2 members)
    service.act("test:3", f"gcamp:{gid}:y")
    camp = service.store.get("camp", KEY)
    assert camp["members"] == ["test:1", "test:2", "test:3"] and camp["helpers"] == ["test:2"]   # no room for a 2nd


def test_helpers_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")
    set_level(service, 3)
    make_hero(service, "test:2", "Bram")
    join(service, "test:2")
    guild = service.act("test:1", "gmembers")
    card = service.text("test:1", code_of(service, guild, "Bram"))
    assert card.actions[0].label == "🤝 Make helper"
    view = service.act("test:1", "ghelp:test:2")
    assert "is now a helper" in view.notice and "[" not in text(service.act("test:1", "guild"))
    assert "🤝 Helpers (1/1): Bram" in text(service.act("test:1", "gmembers"))
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
