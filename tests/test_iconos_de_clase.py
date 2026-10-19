"""Class and role icons are exclusive: no other content or information uses them (D-293).

[ES] Prueba de la regla del dueño (19-oct-2026): "que los íconos de las clases no se repitan con respecto a otros tipos de
contenido o información". Revisa las 6 clases y sus 12 roles (el ícono de cada rol representa al jugador, D-70):
- todos son distintos entre sí;
- ninguno aparece en otro texto (content/locales), objeto, lugar, enemigo, obra o dato (content/*.yaml) ni en el código,
  salvo en los textos de la propia clase y cuando el texto nombra a la clase ("🕊️ Sacerdote", "🕊️ Priest");
- content/patches.yaml (las notas viejas de los parches) y las clases retiradas no cuentan.
Si falla: elige para el contenido nuevo otro ícono, o para la clase uno que no use nada más.
Archivo: tests/test_iconos_de_clase.py · Módulo: M3 Personaje · Prueba: content/classes.yaml (icon),
content/locales/*clases*.yaml, es.yaml, en.yaml (class_group, class).
"""

import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _strings(node, path=()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _strings(value, path + (str(key),))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _strings(value, path + (str(i),))
    elif isinstance(node, str):
        yield path, node


def _icons(content):
    """{icon: [the class names it may stand next to, es and en]} for every active class group and role."""
    icons = {}
    for cid, cdef in content.classes.items():
        if cdef.get("retired"):
            continue
        group = cdef.get("group", cid)
        for texts in content.locales.values():
            for name in (texts["class_group"][group]["name"], texts["class"][cid]["name"]):
                icon, _, rest = name.partition(" ")
                icons.setdefault(icon, set()).add(rest)
        icons.setdefault(cdef.get("icon", ""), set())
    icons.pop("", None)
    return icons


def test_class_and_role_icons_are_all_different(content):
    seen = {}
    for cid, cdef in content.classes.items():
        if cdef.get("retired"):
            continue
        group = cdef.get("group", cid)
        group_icon = content.texts["class_group"][group]["name"].split(" ")[0]
        role_icon = cdef["icon"]
        assert content.texts["class"][cid]["name"].startswith(role_icon), cid    # the role's name shows its own icon
        seen.setdefault(group_icon, set()).add(f"class_group.{group}")
        seen.setdefault(role_icon, set()).add(f"class.{cid}")
    assert all(len(owners) == 1 for owners in seen.values()), {i: o for i, o in seen.items() if len(o) > 1}
    assert len(seen) == 18                                                         # 6 classes + 12 roles


def test_no_other_content_or_code_uses_a_class_icon(content):
    icons = _icons(content)
    found = []
    for path in sorted((ROOT / "content").rglob("*.yaml")):
        if path.name in ("patches.yaml", "classes.yaml"):
            continue
        for key, text in _strings(yaml.safe_load(path.read_text(encoding="utf-8"))):
            if key and key[0] in ("class_group", "class"):
                continue                                                           # the class's own texts
            for icon, names in icons.items():
                rest = text
                for name in names:
                    rest = rest.replace(f"{icon} {name}", "")                     # naming the class is fine
                if icon.replace("️", "") in rest:
                    found.append(f"{path.name}:{'.'.join(key)}: {icon}")
    for path in sorted((ROOT / "engine").rglob("*.py")) + sorted((ROOT / "adapters").rglob("*.py")):
        code = path.read_text(encoding="utf-8")
        for icon, names in icons.items():
            rest = code
            for name in names:
                rest = rest.replace(f"{icon} {name}", "")
            if icon.replace("️", "") in rest:
                found.append(f"{path.relative_to(ROOT)}: {icon}")
    assert not found, found
