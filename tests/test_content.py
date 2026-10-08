"""Content integrity: every id referenced exists and has its texts. [ES] Pruebas de que el contenido está completo."""

from engine.core import Texts


def test_classes_have_six_button_bar(content):
    for cid, cdef in content.classes.items():
        if cdef.get("system") == "chain":
            # 0.31 (D-225): Básico (the attack) + H1, H2, H3; with 🛡️ Defenderse and 🎒 Mochila, 6 buttons (D-46)
            assert cdef["attack"]["link"] == "B" and [a["link"] for a in cdef["abilities"]] == ["H1", "H2", "H3"], cid
            continue
        # The retired specs (D-79, D-110) keep their 3 or 8 abilities, with a response among the first 3.
        assert cdef.get("retired") and len(cdef["abilities"]) in (3, 8), cid
        assert any(a["kind"] == "response" for a in cdef["abilities"][:3]), cid


def test_texts_exist_for_content(content):
    t = Texts(content.texts)
    for cid, cdef in content.classes.items():
        assert t.has(cdef["name_key"]) and t.has(f"class.{cid}.attack_name")
        for ability in cdef["abilities"] + ([cdef["attack"]] if cdef.get("system") == "chain" else []):
            assert t.has(f"ability.{ability['id']}.name"), ability["id"]
            if cdef.get("system") == "chain":
                assert t.has(f"ability.{ability['id']}.desc"), ability["id"]     # 0.31: each button says what it does
    for eid, edef in content.enemies.items():
        assert t.has(edef["name_key"])
        for move in edef["moves"]:
            assert t.has(f"enemy.{eid}.moves.{move['id']}.warn"), (eid, move["id"])
        for item_id in edef.get("loot", {}):
            assert item_id in content.items
    for biome in content.biomes.values():
        assert t.has(biome["name_key"])
    for item in content.items.values():
        assert t.has(item["name_key"])


def test_every_biome_has_enemies(content):
    for biome in content.biomes:
        if biome == "claro":
            continue
        assert any(biome in e["biomes"] for e in content.enemies.values()), biome


def test_plural_forms():
    from engine.core import Texts
    texts = Texts({"a": "Exploraste {n} {n|vez|veces}", "b": "te {left|falta|faltan} {left}"})
    assert texts.t("a", n=1) == "Exploraste 1 vez"
    assert texts.t("a", n=3) == "Exploraste 3 veces"
    assert texts.t("b", left=1) == "te falta 1" and texts.t("b", left=0) == "te faltan 0"
