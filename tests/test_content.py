"""Content integrity: every id referenced exists and has its texts. [ES] Pruebas de que el contenido está completo."""

from engine.core import Texts


def test_classes_have_six_button_bar(content):
    for cid, cdef in content.classes.items():
        # 8 abilities per active spec (D-79); the bar still shows Atacar + 3 (D-46). Retired specs keep their 3.
        assert len(cdef["abilities"]) == (3 if cdef.get("retired") else 8), cid
        assert any(a["kind"] == "response" for a in cdef["abilities"][:3]), cid


def test_texts_exist_for_content(content):
    t = Texts(content.texts)
    for cid, cdef in content.classes.items():
        assert t.has(cdef["name_key"]) and t.has(f"class.{cid}.attack_name")
        for ability in cdef["abilities"]:
            assert t.has(f"ability.{ability['id']}.name"), ability["id"]
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
