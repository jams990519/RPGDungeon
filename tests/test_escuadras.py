"""The squads of 5 inside a camp's guild (D-253.1 Forma B, confirmed; how they were applied: D-331, provisional; 0.55).

[ES] Pruebas de la 1.ª parte jugable de las 🪖 escuadras (engine/service/squads.py):
- los números de balance.yaml ladder.squads dan el cupo de cada etapa (escuadras × 5 = camps.members_by_stage) y el 5 es el
  tope de objetivos de un área (chain.target_cap);
- un campamento de antes se agrupa la primera vez que se mira, en orden de llegada, sin perder a nadie;
- los que entran después van a la primera escuadra con lugar o a una nueva, y quien sale deja su lugar;
- cuántas escuadras abre cada etapa (2, 2, 3, 3, 5, 5, 8, 8, 10), nunca menos de las que pide el cupo (🛖 Cabañas, el piso de
  antes) o los miembros, y que no se puede abrir una de más;
- el voto del 🎖️ jefe: gana la mayoría de la escuadra, si no el jefe sigue; solo entre los de la misma escuadra;
- el jefe pasa a los de su escuadra a otra con lugar y no puede mover a otros; un 🤝 asistente (oficial) y el fundador
  mueven a cualquiera; una escuadra nunca pasa de 5;
- el nombre de la escuadra, solo del jefe, limpio y con largo máximo;
- 👥 Miembros y la tarjeta con sus botones (4 como mucho; la pantalla de mover con páginas);
- la línea "🪖 Escuadras con al menos un vencedor" en la 🌙 Noche de prueba y en la 🌊 oleada creciente, y en el parte, sin
  cambiar lo que piden;
- las pantallas y los avisos en los dos idiomas.
Archivo: tests/test_escuadras.py · Módulo: M15 Social, M9 Frontera y Fundación · Prueba: engine/service/squads.py
(_squad_slots, _squads_normal, _squads, _squads_view, _squad_vote, _squad_move_view, _squad_move, _squad_name_text,
_squads_winners_line, _squads_winners_report, clean_squad_name) y sus ganchos en engine/service/gremio.py
(_camp_members_view, _camp_member_view) y engine/service/game.py (_raid_lines, _resolve_raid, _name_camp, _faq_values).
"""

from conftest import make_hero
from engine.service.squads import clean_squad_name
from test_camps import old_camp_at
from test_escalera_cupo_oficiales import KEY, camp, camp_with, ghosts
from test_guilds import join, set_level
from test_idiomas import english_hero

HOUR = 3600.0
NAMES = ("Bram", "Cora", "Dax", "Eda", "Fio", "Gus", "Hela", "Ivo", "Juno", "Kai", "Lia")


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + list(view.body))


def acc(n):
    return f"test:{n}"


def squads(service):
    return camp(service).get("squads") or []


def squad_members(service):
    return [s["members"] for s in squads(service)]


def code_of(service, viewer, account):
    """The /m code the viewer's last list gave to that account (gremio_codes "members")."""
    shown = service.store.get("gremio_codes", viewer)["members"]
    return f"/m{shown.index(account) + 1}"


def pushes(out, account, kind="gremio_news"):
    return [v for a, v in out if a == account and v.kind == kind]


def camp_of(service, n_members, level=1):
    """Lyra's old camp at 6:0 with Lyra (test:1) and n_members - 1 more heroes (test:2, test:3…), all at its center."""
    camp_with(service, *NAMES[:n_members - 1], level=level)


# ---------------------------------------------------------------- 🔢 the numbers (balance.yaml ladder.squads)


def test_the_squads_of_each_stage_match_its_member_cap(service):
    cfg = service.content.balance["ladder"]["squads"]
    caps = service.content.balance["camps"]["members_by_stage"]
    assert cfg["size"] == 5 == service.content.balance["chain"]["target_cap"]      # an area ability reaches one squad
    assert cfg["by_stage"] == {"campamento": 2, "aldea": 3, "pueblo": 5, "ciudad": 8, "castillo": 10}
    for stage, cap in caps.items():
        assert cfg["by_stage"][stage] * cfg["size"] == cap, stage                 # the two caps never disagree
    assert service.content.balance["gremio"]["members_before_camp"] == cfg["size"]   # the "Casa" of 5 is one squad


def test_how_many_squads_each_stage_opens(service):
    camp_of(service, 2)
    for level, slots in ((1, 2), (2, 2), (3, 3), (4, 3), (5, 5), (6, 5), (7, 8), (8, 8), (9, 10)):
        set_level(service, level)
        assert service._squad_slots(camp(service)) == slots, level
    set_level(service, 1)
    record = service._upgrades(KEY)                              # 🛖 Cabañas: 12 fit, so a 3rd squad opens
    record["built"]["cabanas"] = 0.0
    service.store.put("upgrades", KEY, record)
    assert service._members_cap(camp(service)) == 12 and service._squad_slots(camp(service)) == 3
    data = camp(service)
    data["cap_floor"] = 20                                       # an old camp that kept 20 places (D-327)
    service.store.put("camp", KEY, data)
    assert service._squad_slots(camp(service)) == 5
    data["cap_floor"] = 2
    service.store.put("camp", KEY, data)
    ghosts(service, 14)                                          # 16 members (more than the cap: nobody leaves)
    assert service._squad_slots(camp(service)) == 4              # ⌈16 ÷ 5⌉: everyone always fits


# ---------------------------------------------------------------- 🪖 grouping and placing


def test_an_old_camp_is_grouped_in_join_order_without_losing_anyone(service):
    camp_of(service, 2, level=3)                                 # aldea: 15 places, 3 squads
    ghosts(service, 10)                                          # 12 members, joined in this order
    before = list(camp(service)["members"])
    assert "squads" not in camp(service)                         # a camp of before 0.55
    view = service.act("test:1", "squads")
    assert view.kind == "squads" and view.title == "🪖 Escuadras"
    groups = squad_members(service)
    assert groups == [before[:5], before[5:10], before[10:]]     # filled in join order
    assert sorted(sum(groups, [])) == sorted(before) and camp(service)["members"] == before   # nobody lost or moved out
    chiefs = [s["chief"] for s in squads(service)]
    assert chiefs == ["test:1", before[5], before[10]]           # the founder in his squad, the first one in the others
    assert [s["n"] for s in squads(service)] == [1, 2, 3]
    body = text(view)
    assert "🪖 3 escuadras de hasta 5. En esta etapa del campamento caben 3." in body
    assert "🪖 Escuadra 1 (la tuya) · 5/5 · 🎖️ jefe: Lyra" in body and "🪖 Escuadra 3 · 2/5" in body
    assert any(line.startswith("/m1 👑 🎖️ Lyra (nv") and "🟢 en línea" in line for line in view.body)
    assert any(line.startswith("/m2 ") and "Bram" in line for line in view.body)
    assert ids(view) == ["sqname", "gmembers"]                   # Lyra is her squad's chief: ✏️ the name


def test_new_members_take_the_first_squad_with_room_or_a_new_one(service):
    camp_of(service, 5)                                          # campamento: 10 places, 2 squads; one full squad
    service.act("test:1", "squads")
    assert squad_members(service) == [[acc(1), acc(2), acc(3), acc(4), acc(5)]]
    make_hero(service, acc(6), "Fio")
    join(service, acc(6))                                        # every way in appends to camp["members"]
    service.act("test:1", "squads")
    assert squad_members(service) == [[acc(1), acc(2), acc(3), acc(4), acc(5)], [acc(6)]]   # squad 1 full: a new one
    data = camp(service)                                         # Cora leaves (🚪 Salir or 30 days without playing)
    data["members"].remove(acc(3))
    service.store.put("camp", KEY, data)
    make_hero(service, acc(7), "Gus")
    join(service, acc(7))
    service.act("test:2", "gmembers")                            # any squad screen settles it
    assert squad_members(service) == [[acc(1), acc(2), acc(4), acc(5), acc(7)], [acc(6)]]   # Cora's place, then Gus
    assert acc(3) not in sum(squad_members(service), [])


def test_the_squads_never_open_more_than_the_stage_allows(service):
    camp_of(service, 7)                                          # campamento: 2 squads of 5 (7 members: 5 + 2)
    service.act("test:1", "squads")
    assert [len(m) for m in squad_members(service)] == [5, 2]
    card = service.act("test:1", f"gmem:{acc(6)}")
    view = service.act("test:1", f"sqmv:0:{acc(6)}")             # Fio (squad 2): squad 1 is full and no 3rd squad opens
    assert "Ninguna otra escuadra tiene lugar" in text(view) and f"sqmv:0:{acc(6)}" not in ids(card)
    view = service.act("test:1", f"sqto:3:{acc(6)}")             # forcing a 3rd squad is refused
    assert "Ninguna otra escuadra tiene lugar" in text(view) and len(squads(service)) == 2
    view = service.act("test:1", f"sqto:1:{acc(6)}")             # nor a 6th in squad 1
    assert "Esa escuadra ya tiene 5." in text(view) and [len(m) for m in squad_members(service)] == [5, 2]
    set_level(service, 3)                                        # aldea: a 3rd squad opens
    view = service.act("test:1", f"sqmv:0:{acc(6)}")
    assert view.kind == "squad_move" and ids(view) == [f"sqto:3:{acc(6)}", f"gmem:{acc(6)}"]
    assert view.actions[0].label == "🆕 Escuadra 3 (nueva)"


# ---------------------------------------------------------------- 🗳️ the chief vote


def test_the_squad_votes_its_chief_by_majority(service):
    camp_of(service, 4)                                          # one squad: Lyra (chief by default), Bram, Cora, Dax
    service.act("test:1", "squads")
    service.tick()
    assert squads(service)[0]["chief"] == acc(1)
    card = service.act(acc(2), f"gmem:{acc(3)}")
    assert f"sqvote:{acc(3)}" in ids(card) and "🗳️ Votos para que sea jefe: 0 de 4 (lo es con 3)." in card.body
    view = service.act(acc(2), f"sqvote:{acc(3)}")               # 1 of 4: Lyra stays
    assert "Votaste a Cora como jefe de tu escuadra: 1 de 4 (lo es con 3)." in view.notice
    assert squads(service)[0]["chief"] == acc(1) and ids(view)[0] == f"sqvote:{acc(3)}"
    assert view.actions[0].label == "✖️ Quitar mi voto"
    service.act(acc(3), f"sqvote:{acc(3)}")                      # 2 of 4 (her own vote counts): not a majority yet
    assert squads(service)[0]["chief"] == acc(1)
    view = service.act(acc(4), f"sqvote:{acc(3)}")               # 3 of 4: Cora is the chief
    assert squads(service)[0]["chief"] == acc(3) and "🎖️ Cora es el nuevo jefe de la Escuadra 1." in view.notice
    out = service.tick()
    for other in (acc(1), acc(2), acc(3)):                       # the rest of the squad hears it, in their language
        assert any("🎖️ Cora es el nuevo jefe de la Escuadra 1 de Roca Alta." in v.body[0] for v in pushes(out, other))
    assert not pushes(out, acc(4))                               # the voter reads it on the screen
    view = service.act(acc(2), f"sqvote:{acc(3)}")               # Bram takes his vote back: 2 of 4, Cora stays
    assert "Quitaste tu voto" in view.notice and squads(service)[0]["chief"] == acc(3)
    service.act(acc(1), f"sqvote:{acc(2)}")
    service.act(acc(2), f"sqvote:{acc(2)}")                      # Bram 2, Cora 2: no majority, the chief stays
    assert squads(service)[0]["chief"] == acc(3)
    assert squads(service)[0]["votes"] == {acc(1): acc(2), acc(2): acc(2), acc(3): acc(3), acc(4): acc(3)}


def test_one_votes_only_inside_ones_own_squad(service):
    camp_of(service, 7)                                          # squad 1: test:1-5; squad 2: Fio (test:6), Gus (test:7)
    service.act("test:1", "squads")
    card = service.act(acc(6), f"gmem:{acc(2)}")
    assert not any(i.startswith("sqvote:") for i in ids(card))
    assert "🪖 Escuadra 1 · 🎖️ jefe: Lyra" in card.body and not any("Votos" in line for line in card.body)
    view = service.act(acc(6), f"sqvote:{acc(2)}")
    assert "Solo votas a alguien de tu propia escuadra." in view.notice and not squads(service)[0]["votes"]
    service.act(acc(7), f"sqvote:{acc(7)}")                      # Gus votes himself: 1 of 2 is not more than half
    assert squads(service)[1]["chief"] == acc(6)
    service.act(acc(6), f"sqvote:{acc(7)}")                      # 2 of 2
    assert squads(service)[1]["chief"] == acc(7)


# ---------------------------------------------------------------- 🔀 who moves whom


def test_a_chief_moves_the_members_of_their_own_squad_and_no_one_else(service):
    camp_of(service, 7, level=3)                                 # aldea: 3 squads; squad 2 is Fio (chief) and Gus
    service.act("test:1", "squads")
    assert squads(service)[1]["chief"] == acc(6)
    card = service.act(acc(6), f"gmem:{acc(7)}")                 # Fio, chief of squad 2, opens Gus's card
    assert f"sqmv:0:{acc(7)}" in ids(card) and len(card.actions) <= 4
    view = service.act(acc(6), f"sqmv:0:{acc(7)}")
    assert view.kind == "squad_move" and "¿A qué escuadra pasa Gus? Hoy está en la Escuadra 2." in view.body
    assert ids(view) == [f"sqto:3:{acc(7)}", f"gmem:{acc(7)}"]   # squad 1 is full; a 3rd squad opens in the aldea
    view = service.act(acc(6), f"sqto:3:{acc(7)}")
    assert "🔀 Gus pasó a la Escuadra 3." in view.notice and view.kind == "gremio_member"
    assert squad_members(service) == [[acc(1), acc(2), acc(3), acc(4), acc(5)], [acc(6)], [acc(7)]]
    assert squads(service)[2]["chief"] == acc(7)                 # alone in his new squad: its chief
    out = service.tick()
    assert any("🔀 Fio te pasó a la Escuadra 3 de Roca Alta." in v.body[0] for v in pushes(out, acc(7)))
    card = service.act(acc(6), f"gmem:{acc(2)}")                 # Bram is in squad 1: Fio does not move him
    assert not any(i.startswith("sqmv:") for i in ids(card))
    view = service.act(acc(6), f"sqto:2:{acc(2)}")
    assert "El 🎖️ jefe pasa a los de su escuadra" in view.notice and acc(2) in squads(service)[0]["members"]
    view = service.act(acc(2), f"sqmv:0:{acc(6)}")               # a plain member moves nobody
    assert "El 🎖️ jefe pasa a los de su escuadra" in view.notice
    service.act(acc(7), f"sqto:2:{acc(7)}")                      # Gus, chief of squad 3, moves himself back to Fio's
    assert squad_members(service)[1] == [acc(6), acc(7)] and squad_members(service)[2] == []
    assert squads(service)[2]["chief"] is None and squads(service)[1]["chief"] == acc(6)


def test_the_founder_and_an_officer_move_anyone(service):
    camp_of(service, 7, level=3)
    service.act("test:1", "ghelp:test:2")                        # Bram is a 🤝 assistant (the officers, D-327)
    service.act("test:1", "squads")
    card = service.act(acc(2), f"gmem:{acc(4)}")                 # Bram is not a chief, but an officer
    assert f"sqmv:0:{acc(4)}" in ids(card)
    view = service.act(acc(2), f"sqto:2:{acc(4)}")               # Dax: squad 1 → squad 2
    assert "Dax pasó a la Escuadra 2" in view.notice
    assert squad_members(service)[0] == [acc(1), acc(2), acc(3), acc(5)]
    assert squad_members(service)[1] == [acc(6), acc(7), acc(4)]
    view = service.act(acc(1), f"sqto:3:{acc(6)}")               # the founder moves Fio, squad 2's chief, to a new squad
    assert "Fio pasó a la Escuadra 3" in view.notice
    assert squads(service)[1]["chief"] == acc(7)                 # squad 2 gets a new chief: its first member now
    out = service.tick()
    assert any("🎖️ Gus es el nuevo jefe de la Escuadra 2 de Roca Alta." in v.body[0] for v in pushes(out, acc(4)))
    assert sorted(sum(squad_members(service), [])) == sorted(camp(service)["members"])     # still everyone, once


# ---------------------------------------------------------------- ✏️ the name


def test_only_the_chief_names_the_squad_and_the_name_is_cleaned(service):
    camp_of(service, 3)
    service.act("test:1", "squads")
    view = service.act(acc(2), "sqname")                         # Bram is not the chief
    assert "Solo el 🎖️ jefe de la escuadra le pone nombre." in view.notice and not view.expects_text
    ask = service.act("test:1", "sqname")
    assert ask.kind == "squad_name" and ask.expects_text and "hasta 20 letras" in text(ask) and ids(ask) == ["squads"]
    view = service.text("test:1", "  Lobos​ <b>Grises</b>  ")
    assert view.kind == "squads" and "Tu escuadra ahora es la Escuadra 1 «Lobos bGrises/b»." in view.notice
    assert squads(service)[0]["name"] == "Lobos bGrises/b"
    assert "🪖 Escuadra 1 «Lobos bGrises/b» (la tuya)" in text(view)
    service.act("test:1", "sqname")
    view = service.text("test:1", "<<>>")                        # nothing left: asked again
    assert view.kind == "squad_name" and view.expects_text and "Ese nombre no sirve" in view.notice
    view = service.text("test:1", "Los Que Nunca Duermen Bajo La Luna")
    assert squads(service)[0]["name"] == "Los Que Nunca Duerme"   # 20 letters at most
    service.act("test:1", "sqname")
    service.act("test:1", "squads")                              # ❌ Cancelar: nothing changes, the next text is chat
    assert not service.store.get("camp_naming", "test:1") and squads(service)[0]["name"] == "Los Que Nunca Duerme"


def test_clean_squad_name_drops_control_and_invisible_characters():
    assert clean_squad_name("Lobos\nGrises", 20) == "Lobos Grises"
    assert clean_squad_name("\tLos​  Fieros‮ ", 20) == "Los Fieros"
    assert clean_squad_name("«Escuadra» <script>", 30) == "Escuadra script"
    assert clean_squad_name("🐺 Lobos 🐺", 20) == "🐺 Lobos 🐺"           # emojis stay
    assert clean_squad_name("x" * 50, 20) == "x" * 20
    assert clean_squad_name(" ​\n ", 20) == ""


# ---------------------------------------------------------------- 👥 Miembros and the buttons


def test_members_show_your_squad_and_the_squads_button(service):
    camp_of(service, 7)
    members = service.act(acc(6), "gmembers")
    assert "🪖 Tu escuadra: Escuadra 2 · 🎖️ jefe: Fio (en total, 2 escuadras)." in members.body
    assert ids(members) == ["squads", "guild"] and len(members.actions) <= 4
    view = service.act(acc(6), "squads")
    assert view.body[2].startswith("🪖 Escuadra 2 (la tuya)")    # your own squad goes first
    assert ids(view) == ["sqname", "gmembers"]                   # Fio is squad 2's chief
    assert ids(service.act(acc(7), "squads")) == ["gmembers"]    # Gus is not
    code = code_of(service, acc(6), acc(2))                      # the codes follow the squads list: /m3 is Bram here
    card = service.text(acc(6), code)
    assert card.kind == "gremio_member" and card.body[0].startswith(f"{code} ") and "Bram" in card.body[0]


def test_a_card_never_shows_more_than_four_buttons_and_the_move_screen_pages(service):
    camp_of(service, 5, level=9)                                 # a castle: 10 squads; 5 members, one per squad
    data = camp(service)
    data["squads"] = [{"n": i + 1, "name": "", "members": [acc(i + 1)], "chief": acc(i + 1), "votes": {}}
                      for i in range(5)]
    service.store.put("camp", KEY, data)
    card = service.act("test:1", "gmem:test:1")                  # the founder's own card: 🗳️ and 🔀
    assert ids(card) == ["sqvote:test:1", "sqmv:0:test:1", "gmembers"]
    data = camp(service)                                         # Bram joins Lyra's squad
    data["squads"][1]["members"] = []
    data["squads"][0]["members"].append(acc(2))
    service.store.put("camp", KEY, data)
    card = service.act("test:1", f"gmem:{acc(2)}")
    assert ids(card) == [f"ghelp:{acc(2)}", f"sqvote:{acc(2)}", f"sqmv:0:{acc(2)}", "gmembers"]    # 4: the most
    view = service.act("test:1", f"sqmv:0:{acc(2)}")             # squads 2 (empty) to 5 have room, and a 6th can open
    assert len(view.actions) == 4 and ids(view) == [f"sqto:2:{acc(2)}", f"sqto:3:{acc(2)}", f"sqmv:1:{acc(2)}",
                                                    f"gmem:{acc(2)}"]
    assert view.actions[2].label == "➡️ Más escuadras"
    assert ids(service.act("test:1", f"sqmv:1:{acc(2)}"))[:2] == [f"sqto:4:{acc(2)}", f"sqto:5:{acc(2)}"]
    last = service.act("test:1", f"sqmv:2:{acc(2)}")
    assert ids(last)[0] == f"sqto:6:{acc(2)}" and last.actions[0].label == "🆕 Escuadra 6 (nueva)"
    assert ids(last)[1] == f"sqmv:0:{acc(2)}"                    # ➡️ goes round to the first page
    assert all(len(i.encode()) <= 64 for i in ids(view) + ids(card))
    view = service.act("test:1", f"sqto:2:{acc(2)}")             # the empty squad 2 takes him (and he leads it)
    assert squads(service)[1]["members"] == [acc(2)] and squads(service)[1]["chief"] == acc(2)


# ---------------------------------------------------------------- 🌙 the Noche de prueba and 🌊 the growing waves (info only)


def open_raid_with(service, kind, fights, wave=None):
    data = camp(service)
    now = service.clock.now()
    raid = {"kind": kind, "at": now, "until": now + HOUR, "required": 10, "wins": sum(r == "won" for r in fights.values()),
            "fights": dict(fights), "enemy": "lobo", "level": 1, "defense": 0}
    if wave:
        raid.update(wave=wave, wave_mult=1 + 0.2 * wave)
    data["raid"] = raid
    service.store.put("camp", KEY, data)
    return raid


def test_the_trial_and_the_waves_say_how_many_squads_had_a_winner(service):
    camp_of(service, 7, level=8)                                 # squads: test:1-5 and test:6-7
    open_raid_with(service, "trial", {acc(1): "won", acc(2): "won", acc(6): "lost"})
    lines = service._raid_lines(camp(service))
    assert "🪖 Escuadras con al menos un vencedor: 1 de 2." in lines
    open_raid_with(service, "trial", {acc(1): "won", acc(7): "won"})
    assert "🪖 Escuadras con al menos un vencedor: 2 de 2." in service._raid_lines(camp(service))
    open_raid_with(service, "raid", {acc(1): "won"}, wave=2)     # a 🌊 growing wave of the castle
    lines = service._raid_lines(camp(service))
    assert any("oleada creciente 2 de 5" in line for line in lines) and "🪖 Escuadras con al menos un vencedor: 1 de 2." in lines
    open_raid_with(service, "raid", {acc(1): "won"})             # a normal raid: no squads line
    assert not any("🪖" in line for line in service._raid_lines(camp(service)))
    trial = service._trial_view(service._load("test:1"), camp(service))
    assert not any("🪖" in line for line in trial.body)          # the normal raid is on, not the trial


def test_the_report_counts_the_squads_but_the_trial_rules_do_not_change(service):
    camp_of(service, 7, level=8)
    raid = open_raid_with(service, "trial", {acc(1): "won", acc(6): "won"})   # both squads won, but 2 of the 10 needed
    data = camp(service)
    data.pop("raid")
    service._resolve_raid(data, raid, service._load("test:1"))
    service.store.put("camp", KEY, data)
    ends = {a: text(v) for a, v in service.tick() if v.kind == "camp_raid_end"}
    assert "🪖 2 de 2 escuadras tuvieron al menos un vencedor." in ends[acc(1)]
    assert not camp(service).get("trial_won") and camp(service).get("trial_retry_at")     # still lost: 2 < 10 wins
    assert service._squads_winners_report(camp(service), {"kind": "raid", "fights": {acc(1): "won"}}) == []


# ---------------------------------------------------------------- the two languages


def test_the_squads_read_well_in_both_languages(service):
    english_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")
    make_hero(service, acc(2), "Bram")                           # Bram plays in Spanish
    join(service, acc(2))
    english_hero(service, acc(3), "Cora")
    join(service, acc(3))
    view = service.act("test:1", "squads")
    assert view.title == "🪖 Squads" and "🪖 Squad 1 (yours) · 3/5 · 🎖️ chief: Lyra" in view.body
    assert "🪖 1 squad of up to 5. This stage of the camp has room for 2." in view.body
    assert any(line.startswith("/m1 👑 🎖️ Lyra (lv") for line in view.body)
    members = service.act("test:1", "gmembers")
    assert "🪖 Your squad: Squad 1 · 🎖️ chief: Lyra (1 squad in all)." in members.body
    assert members.actions[ids(members).index("squads")].label == "🪖 Squads"
    card = service.act("test:1", f"gmem:{acc(2)}")
    assert "🗳️ Votes for them as chief: 0 of 3 (2 make the chief)." in card.body
    labels = {a.id: a.label for a in card.actions}
    assert labels[f"sqvote:{acc(2)}"] == "🗳️ Vote as chief" and labels[f"sqmv:0:{acc(2)}"] == "🔀 Change squad"
    view = service.act("test:1", f"sqto:2:{acc(2)}")
    assert "🔀 Bram moved to Squad 2." in view.notice
    out = service.tick()
    assert any("🔀 Lyra te pasó a la Escuadra 2 de Grey Rock." in v.body[0] for v in pushes(out, acc(2)))   # his language
    service.act(acc(3), f"sqvote:{acc(3)}")                      # Cora: 1 of 2 votes, not the chief yet
    view = service.act("test:1", f"sqvote:{acc(3)}")
    assert "🎖️ Cora is the new chief of Squad 1." in view.notice
    assert any("🎖️ Cora is the new chief of Squad 1 in Grey Rock." in v.body[0] for v in pushes(service.tick(), acc(3)))
    ask = service.act(acc(3), "sqname")
    assert "up to 20 letters" in text(ask)
    view = service.text(acc(3), "Grey Wolves")
    assert "✏️ Your squad is now Squad 1 “Grey Wolves”." in view.notice
    for lang in ("es", "en"):
        with service.texts.use(lang):
            values = service._faq_values()
            answer = service.texts.t("faq.d37.a", **values)
            assert "{" not in answer and ("escuadras de 5" in answer if lang == "es" else "squads of 5" in answer)
    assert not service.texts.fallbacks.get("en") and not service.texts.missing
