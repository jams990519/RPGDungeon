# Convenciones de código: inglés con notas [ES]

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Arquitectura modular](arquitectura-modular.md), [Decisiones](../00-vision/decisiones.md), [Lecciones de TowerWars](../99-referencias/lecciones-de-towerwars.md) · **Condiciona a:** todo el código, los datos de contenido y las pruebas · **Estado:** la regla base está confirmada (D-42); los detalles son propuesta

**Qué pediste.** Que el código tenga notas suficientes para entender todo lo que pasa alrededor de cada pieza. Que el código esté en inglés y que debajo vaya una nota en español, entre corchetes, que explique para qué sirve cada cosa y con qué se conecta. Así, cuando le pidas a la IA que cambie una sola línea, puede responderte: "ok, pero esto también va a romper esto y esto, o puede afectar esto otro".

**De dónde sale.**
- **Docstrings de Python** (PEP 257) con el **estilo de Google** para argumentos, valores de retorno y errores. Es la forma estándar de documentar dentro del código.
- **ADR** (*Architecture Decision Records*, Michael Nygard, 2011): cada decisión técnica se escribe con su contexto y sus consecuencias. Aquí ese papel lo cumple el [registro de decisiones](../00-vision/decisiones.md) (D-xx).
- **CODEOWNERS** de GitHub: cada ruta del repositorio tiene un responsable. Aquí cada archivo declara **de qué datos es dueño** y qué módulo responde por él.
- **Grafos de dependencias y contratos de importación** (en Python, herramientas como *pydeps* e *import-linter*): se dibuja quién importa a quién y se prohíben las flechas que no deben existir.
- **Lecciones de TowerWars:** el motor puro, los IDs estables, las migraciones, el registro de balance y, sobre todo, que **la wiki vieja mentía** (describía 6 clases de un modelo anterior). Ver [Lecciones de TowerWars](../99-referencias/lecciones-de-towerwars.md).

**El código ya está autorizado (D-59, que reemplaza a D-04).** Estas reglas valen desde la primera línea. Los ejemplos están en Python porque es la tecnología propuesta (P-46).

---

## 1. Regla de idioma

| Qué | Idioma | Ejemplo |
|---|---|---|
| Nombres en el código: variables, funciones, clases, archivos, carpetas, eventos, columnas de la base de datos, IDs de contenido | **Inglés** | `mitigation_fraction`, `HitReceived`, `swamp_fever` |
| Comentarios técnicos y docstrings | **Inglés** | `"""Return the fraction of damage absorbed."""` |
| **Nota [ES]** debajo del encabezado de cada archivo, de cada clase y de cada función pública | **Español** neutro y simple | `[ES] Qué hace: dice qué parte del golpe frena la armadura.` |
| Textos que ve el jugador | Español e inglés, **en archivos de idiomas** (M1) o de contenido, nunca escritos en el código del motor | `name: {es: "Fiebre del Pantano", en: "Swamp Fever"}` |
| Documentos de diseño (`diseno/`) | Español | Este documento |

**Por qué el código va en inglés.** Es el estándar: las librerías, los mensajes de error y la documentación técnica están en inglés, y cualquier programador o IA lo lee sin traducir. Además evita mezclas como `calcular_damage()`.

**Por qué va una nota en español.** La parte en inglés dice **qué hace y cómo**. La nota [ES] dice **para qué sirve, con qué se conecta y qué se rompe si cambia**, con las palabras del diseño (GolpeRecibido, Herida, Guardián). Sirve para dos lectores:
- **El dueño**, que puede leer cualquier archivo y entender su papel sin leer el código.
- **La IA**, que antes de tocar algo lee la nota y sabe a quién más afecta. La nota no traduce el docstring: es el mapa de alrededor.

**El marcador `[ES]`.** Siempre igual: `[ES]` en mayúsculas, entre corchetes, al principio de una línea. Nada más en el código usa ese texto (los documentos de `diseno/` solo lo nombran), así que buscarlo en las carpetas de código encuentra todas las notas. La única excepción son los esquemas de datos, donde la nota va en el campo `x-es` (§4); por eso la búsqueda lleva las dos marcas:

```
grep -rn -e "\[ES\]" -e "x-es:" engine/ content/ adapters/ simulator/ tests/ tools/
```

**Dónde va cada nota:**

| Pieza | Qué lleva |
|---|---|
| **Archivo** (módulo de código) | Encabezado completo (§2): propósito en inglés y nota [ES] con los 10 campos fijos |
| **Clase pública** | Docstring en inglés y nota [ES] corta (§3) |
| **Función pública** | Docstring en inglés (argumentos, retorno, errores) y nota [ES] corta (§3) |
| **Evento** | Como una clase, y la nota [ES] dice siempre quién lo publica y quién lo escucha |
| **Función interna** (nombre que empieza con `_`) | Comentario en inglés si la lógica no es obvia. Nota [ES] solo si la razón viene del diseño |
| **Línea que aplica una regla del diseño** | Comentario en inglés y, debajo, `# [ES]` con la regla y su documento |
| **Constante de balance** | Comentario en inglés, `# [ES]` y entrada en el registro de balance |
| **Migración de base de datos** | Encabezado con `-- [ES]`: qué tabla, qué módulo es su dueño, si se puede revertir |
| **Prueba** | Nombre en inglés y `[ES]` con la regla del diseño que protege |
| **Archivo de datos** (zonas del mapa, jefes, recetas…) | Encabezado `# [ES]` y una nota por tipo de dato (§4) |

**En otros lenguajes** (la web y la app móvil pueden usar otro, ver [Web y multiplataforma](web-y-multiplataforma.md)) la regla es la misma, con la sintaxis de comentario de cada uno: `/** ... [ES] ... */` en TypeScript, `# [ES]` en YAML, `-- [ES]` en SQL.

## 2. Encabezado de módulo (archivo)

Cada archivo de código empieza con un docstring: primero el propósito en inglés y, debajo, la nota [ES] con **10 campos fijos, siempre en este orden y con estas etiquetas**. Si un campo no aplica, se escribe `ninguno`; nunca se omite. Así una herramienta puede comprobar que estén todos (§8).

```python
"""<One line: what this file does.>

<Two to five lines in English: how it works, what it must never do.>

[ES]
Para qué sirve: <una o dos frases, sin tecnicismos>
Documento de diseño: <ruta en diseno/ y sección, por ejemplo diseno/05-salud/heridas.md §4>
Módulo: <M1 a M25 y su nombre, por ejemplo M7 Salud, o "capa de servicios" (§7.1)>
Depende de: <módulos, archivos y datos que este archivo usa>
Lo usan: <archivos y módulos que importan o llaman a este>
Eventos que publica: <nombre en código (nombre en el diseño), o ninguno>
Eventos que escucha: <nombre en código (nombre en el diseño), o ninguno>
Datos de los que es dueño: <tablas o archivos que SOLO este módulo escribe, o ninguno>
Reglas que nunca se rompen:
    1. <invariante, con su documento o decisión D-xx>
Si cambias esto, revisa:
    - <módulo>: <archivo> — <qué le pasa>
    - Números: <constante y dónde vive> (anotar en el registro de balance)
    - Pruebas: <archivos de prueba>
"""
```

**Qué va en cada campo:**

| Campo | Qué responde | Error típico que evita |
|---|---|---|
| Para qué sirve | ¿Qué papel cumple en el juego? | Leer 200 líneas para entender eso |
| Documento de diseño | ¿Qué regla del diseño implementa? | Que el código y el diseño se separen sin que nadie lo note |
| Módulo | ¿A cuál de los 25 módulos pertenece? | Archivos sin dueño |
| Depende de | ¿Qué necesita para funcionar? | Cambiar algo de abajo sin saber que este archivo lo usa |
| Lo usan | ¿A quién rompo si cambio una firma? | El caso típico de "arreglé esto y se rompió aquello" |
| Eventos que publica / escucha | ¿Con quién habla sin importarlo? | Las conexiones invisibles: Combate no importa Salud, pero la alimenta |
| Datos de los que es dueño | ¿Quién es el único que escribe estos datos? | Dos módulos escribiendo el mismo dato (ver regla 2 de la [arquitectura](arquitectura-modular.md)) |
| Reglas que nunca se rompen | ¿Qué tiene que seguir siendo cierto después de cualquier cambio? | Romper una decisión confirmada sin darse cuenta |
| Si cambias esto, revisa | La lista concreta de lo que puede romperse | Es el campo más importante para la IA |

**"Si cambias esto, revisa" tiene que ser concreta.** Nunca "puede afectar a otros módulos". Siempre: qué módulo, qué archivo, qué le pasa al jugador o al sistema, qué número de balance está en juego y qué pruebas hay que correr.

## 3. Clases y funciones públicas

Una clase o función es **pública** cuando otro archivo puede usarla (su nombre no empieza con `_`). Lleva un docstring en inglés con el estilo de Google y, debajo, una nota [ES] corta de tres campos.

**Función pública:**

```python
def function_name(arg_one: int, arg_two: str) -> bool:
    """<One line: what it returns or does.>

    <Optional: details, formula, edge cases.>

    Args:
        arg_one: <meaning, units, valid range>.
        arg_two: <meaning>.

    Returns:
        <what comes back and its range>.

    Raises:
        ValueError: <when>.

    [ES]
    Qué hace: <una frase>
    La llaman: <quién la usa: archivo o módulo>
    Si cambia, afecta: <qué módulos o números cambian>
    """
```

**Clase pública:**

```python
class ClassName:
    """<One line: what this object represents.>

    Attributes:
        field_one: <meaning>.

    [ES]
    Qué es: <una frase, con el nombre que tiene en el diseño>
    Quién la usa: <quién la crea y quién la lee>
    Si cambia, afecta: <qué se rompe si se quita, renombra o cambia de significado un campo>
    """
```

La nota corta puede remitir al encabezado del archivo ("ver *Si cambias esto, revisa* arriba") cuando la lista es la misma, para no repetirla.

## 4. Archivos de datos de contenido

El contenido son datos, no código (regla 4 de la [arquitectura](arquitectura-modular.md)): las zonas del mapa, los jefes, monstruos, recetas, enfermedades y misiones viven en archivos. La propuesta es **YAML**, porque admite comentarios (JSON no), y así cada archivo puede llevar su nota [ES].

**Cuatro reglas:**
1. **Cada tipo de dato tiene un esquema documentado** (`content/schemas/`), con la descripción de cada campo en inglés y su nota en español. El motor rechaza al arrancar cualquier dato que no cumpla el esquema.
2. **Cada archivo empieza con un encabezado `# [ES]`**: qué contiene, qué documento de diseño lo describe, qué módulos lo leen y qué revisar si cambia.
3. **IDs estables que solo se agregan.** Un ID nunca se renombra, nunca se borra y nunca se reutiliza. Para retirar algo se marca `retired: true`. El ID está en inglés y no se traduce; el nombre que ve el jugador va aparte, en español y en inglés.
4. **Los números de balance llevan su nota.** Si un valor se mueve, va al registro de balance.

**Ejemplo de archivo de datos** (`content/health/diseases.yaml`; los números son de ejemplo):

```yaml
# Disease catalog for the health module (M7).
# Schema: content/schemas/disease.schema.yaml
#
# [ES]
# Para qué sirve: catálogo de enfermedades. Agregar una aquí la mete en el juego sin programar.
# Documento de diseño: diseno/05-salud/enfermedades.md §3
# Lo leen: engine/health/diseases.py (M7), engine/world/ecology.py (M8, dónde se contrae),
#          engine/professions/treatments.py (M14, qué la cura)
# IDs: estables. Nunca se renombran, nunca se borran, nunca se reutilizan.
#      Para retirar una enfermedad se marca retired: true.
# Si cambias esto, revisa: content/professions/recipes.yaml (tratamientos),
#      content/world/zones.yaml (dónde aparece), tests/health/test_diseases.py

- id: swamp_fever                  # stable forever, never rename
  # [ES] Fiebre del Pantano: crónica, vuelve en brotes cada semana hasta tratarla.
  name: {es: "Fiebre del Pantano", en: "Swamp Fever"}
  tier: 4
  sources: [insect_bite, miasma]   # ids from content/world/hazards.yaml
  severity_per_hour: 3             # balance number: log every change
  outcome: chronic_weekly_flare
  treatment_ids: [bitter_bark_tonic]
  added_in: "0.1.0"
```

**Ejemplo de esquema** (`content/schemas/disease.schema.yaml`, simplificado): cada campo con su descripción en inglés (`description`) y su nota en español (`x-es`, un campo propio que los validadores ignoran):

```yaml
id:
  type: string
  pattern: "^[a-z0-9_]+$"
  description: Stable identifier. Never renamed, deleted or reused.
  x-es: ID fijo. Lo usan las recetas, las zonas y las partidas guardadas; cambiarlo las rompe.
severity_per_hour:
  type: integer
  minimum: 1
  description: Points added to the severity bar each hour.
  x-es: Qué tan rápido gana la enfermedad. Cambiarlo cambia cuántos jugadores necesitan médico (M14).
```

## 5. Ejemplos completos

Un caso real del diseño: la **mitigación de armadura** `def / (def + K)` ([Daño y estados](../04-combate/dano-y-estados.md) §1, [Balance](../03-personaje/balance.md) §4) y la **herida que nace de un golpe** ([Heridas](../05-salud/heridas.md) §4).

### 5.1 Un módulo y una función: `engine/combat/armor.py`

```python
"""Armor mitigation: how much physical damage a defender's armor absorbs.

Pure rules, no I/O, no database, no knowledge of Telegram, web or mobile.
The same function serves PvE, PvP, castle wars and the balance simulator,
so there is exactly one source of truth for armor.

[ES]
Para qué sirve: convierte la armadura de quien recibe el golpe en el porcentaje
    de daño que se absorbe, con la fórmula def / (def + K).
Documento de diseño: diseno/04-combate/dano-y-estados.md §1 · diseno/03-personaje/balance.md §4
Módulo: M5 Combate
Depende de: ningún otro archivo. K llega como argumento: damage.py la lee de
    content/balance/armor.yaml (un valor por anillo).
Lo usan: engine/combat/damage.py (cada golpe físico), engine/combat/buildup.py
    (la armadura frena la acumulación de estados), simulator/ (M21).
Eventos que publica: ninguno (cálculo puro).
Eventos que escucha: ninguno.
Datos de los que es dueño: ninguno. K vive en content/balance/armor.yaml.
Reglas que nunca se rompen:
    1. El resultado está entre 0 y 1 y nunca llega a 1: la armadura no da inmunidad.
    2. La armadura cuenta siempre: ningún golpe la ignora entera con un "daño mínimo"
       (TowerWars revirtió la "mordida" por esto).
    3. Es la única fórmula de armadura del juego: PvP y la guerra no calculan la suya.
Si cambias esto, revisa:
    - M5 Combate: engine/combat/damage.py y buildup.py — cambia todo el daño físico
      y la velocidad a la que se llenan sangrado, veneno, etc.
    - M7 Salud: engine/health/wound_rules.py — más o menos golpes cruzan el 50 % y el
      25 % de vida, así que cambia cuántas heridas aparecen.
    - M12 PvP: duración de duelos y arena; poder de guerra de castillos.
    - M21 Simulador: correr todos los escenarios (objetivo: mitigación de tanques a ±4 %).
    - M4 Equipo y M13 Economía: cuánto vale cada punto de armadura y el precio de las piezas.
    - M14 Oficios: demanda de herreros, peleteros y sastres; trabajo de Medicina si hay
      más o menos heridas.
    - Números: K = 60 en el anillo I, crece por anillo (content/balance/armor.yaml).
      Todo cambio va al registro de balance.
    - Pruebas: tests/combat/test_armor.py, tests/health/test_wound_rules.py,
      tests/simulator/test_tank_mitigation.py
"""
from __future__ import annotations


def mitigation_fraction(armor: float, k: float) -> float:
    """Return the fraction of physical damage absorbed by armor.

    Uses ``armor / (armor + k)``. With ``k = 60``, 60 armor absorbs 50 %
    and 180 armor absorbs 75 %: each extra point is worth a little less.

    Args:
        armor: Defender's armor against this damage type, already summed
            from equipment by ``engine/equipment``. Must be >= 0.
        k: Tier constant from ``content/balance/armor.yaml``. Must be > 0.

    Returns:
        A float in [0, 1). Never 1, so armor never grants immunity.

    Raises:
        ValueError: If ``armor`` is negative or ``k`` is not positive.

    [ES]
    Qué hace: dice qué parte del golpe frena la armadura (0,5 = la mitad).
    La llaman: apply_hit() en engine/combat/damage.py y el simulador (M21).
    Si cambia, afecta: todo el daño físico del juego. Ver "Si cambias esto, revisa"
        en el encabezado de este archivo.
    """
    if armor < 0:
        raise ValueError(f"armor must be >= 0, got {armor}")
    if k <= 0:
        raise ValueError(f"k must be > 0, got {k}")
    return armor / (armor + k)
```

### 5.2 Una clase: el evento `HitReceived` (GolpeRecibido)

Los eventos son el lugar donde un cambio rompe cosas **sin dar error**: Combate no importa a Salud, así que si cambia el significado de un campo, nada falla al arrancar, pero el juego se comporta distinto. Por eso su nota [ES] es la más cuidada.

```python
from __future__ import annotations

from dataclasses import dataclass

from engine.core.types import BodyZone, DamageType


@dataclass(frozen=True, slots=True)
class HitReceived:
    """Event: a combatant took a hit that landed.

    Published by the combat engine once per landed hit, after armor and
    after health was reduced. Listeners react in their own module and
    never change combat state.

    Attributes:
        combat_id: Id of the fight; replayable with its stored seed.
        attacker_id: Hero or enemy that landed the hit. Health uses it to
            look up what the attacker spreads (contagion bar).
        target_id: Hero or enemy that took the hit.
        zone: Body zone that was hit.
        damage_type: Damage family and type (slash, pierce, blunt, fire...).
        damage: Final damage after armor, already applied.
        critical: True if the hit was a critical strike.
        hp_before: Target health before the hit.
        hp_after: Target health after the hit.

    [ES]
    Qué es: el evento GolpeRecibido del diseño (arquitectura-modular.md §4).
    Quién la usa: la crea engine/combat/round.py. La escuchan M7 Salud (¿hay herida?
        y la barra de Contagio del monstruo que golpeó, bestiario.md §5.1),
        M4 Equipo (desgaste de durabilidad) y la mente en M7 (estrés por críticos,
        Sombra y Vacío).
    Si cambia, afecta: quitar o renombrar un campo rompe a todos los que escuchan.
        Agregar un campo con valor por defecto es seguro. Cambiar el significado de
        `damage` (antes o después de la armadura) o de hp_before/hp_after cambia
        cuántas heridas aparecen sin dar ningún error: es el cambio más peligroso.
    """

    combat_id: str
    attacker_id: str
    target_id: str
    zone: BodyZone
    damage_type: DamageType
    damage: int
    critical: bool
    hp_before: int
    hp_after: int
```

### 5.3 Una función que escucha: la herida que nace del golpe (`engine/health/wound_rules.py`)

```python
def on_hit_received(event: HitReceived, hero: HeroHealth, rng: SeededRng) -> Wound | None:
    """Decide whether a landed hit leaves a wound, and create it.

    A wound is rolled only on a critical hit or when health crosses 50 %
    or 25 % of max in this fight. Zone armor lowers chance and severity.
    Downs (HeroDowned) and boss moves that wound have their own listeners.

    Args:
        event: The ``HitReceived`` published by combat.
        hero: Health state of the target (wounds, level, zone armor).
        rng: Seeded random source of this fight, so the result is replayable.

    Returns:
        The new ``Wound``, or ``None`` if the hit left no wound.

    [ES]
    Qué hace: decide si un golpe deja herida y, si la deja, la crea y publica
        WoundCreated (HeridaCreada).
    La llama: el bus de eventos de M1 cada vez que Combate publica HitReceived.
    Si cambia, afecta: cuántas heridas hay → trabajo de Medicina y Primeros Auxilios (M14),
        venta de vendas y férulas (M13), uso del sanatorio (sumidero de oro) y
        el tope de 2 heridas graves (heridas.md §7).
    """
    if not (event.critical or crossed_threshold(event.hp_before, event.hp_after, hero.max_hp)):
        return None
    wound = roll_wound(event.zone, event.damage_type, hero.zone_armor(event.zone), rng)
    # Novice protection: up to and including level 10, wounds are always minor.
    # [ES] Protección de novato: hasta el nivel 10 (incluido) solo hay heridas leves
    #      (heridas.md §7). El umbral se repite en otros documentos: cambiarlo aquí
    #      obliga a cambiarlos todos (mapa-de-impacto.md §4.7 y §6.2).
    if hero.level <= 10:
        wound = wound.capped_at(Severity.MINOR)
    publish(WoundCreated(hero_id=hero.hero_id, wound=wound))
    return wound
```

Con solo leer las notas [ES] de estos tres ejemplos se ve la cadena completa: **armadura → daño → golpe → herida → médicos, vendas y sanatorio → oro**. Eso es lo que la IA tiene que poder contarle al dueño antes de tocar una línea.

## 6. Protocolo de cambio para la IA

### 6.1 Por dónde se propaga un cambio

Un cambio en un archivo puede llegar a otro por cinco caminos. La IA revisa los cinco:

| Camino | Ejemplo | Cómo se encuentra |
|---|---|---|
| **Importación directa** | `damage.py` llama a `mitigation_fraction()` | Campo "Lo usan" y búsqueda del nombre en el código |
| **Eventos** | Combate publica `HitReceived` y Salud crea heridas | Campos "Eventos que publica / escucha" y búsqueda del nombre del evento |
| **Datos compartidos** | Las recetas apuntan al ID `swamp_fever` | Campo "Datos de los que es dueño", encabezado del archivo de datos y búsqueda del ID |
| **Números de balance** | Subir K cambia el precio de las armaduras sin tocar Economía | Campo "Si cambias esto, revisa" y el mapa de impacto |
| **Contrato con los clientes** | Cambiar lo que devuelve el motor rompe el bot, la web o la app | Las respuestas del motor son un contrato: se agrega, no se cambia (ver [Web y multiplataforma](web-y-multiplataforma.md)) |

Los dos últimos son los peligrosos: **no dan error**, solo cambian cómo se juega.

### 6.2 Los pasos

**Antes de editar:**
1. **Leer el encabezado y las notas [ES]** del archivo y de cada función o clase que se va a tocar.
2. **Consultar el [mapa de impacto](mapa-de-impacto.md)** para el módulo del archivo: su ficha, sus cascadas y sus números sensibles.
3. **Comprobar en el código** quién lo usa de verdad: buscar el nombre de la función, el evento o el ID. La nota puede estar vieja. Si no coincide con el código, se le avisa al dueño y se corrige la nota.
4. **Leer el documento de diseño enlazado.** Si el cambio contradice una regla del diseño o una decisión confirmada (D-xx), se detiene y se pregunta.
5. **Darle al dueño el mensaje de impacto** en español (§6.3): "esto también afecta a…".
6. **Esperar su respuesta** cuando el cambio toca una regla que nunca se rompe, un número de balance, un evento, un esquema de datos, la base de datos o más de un módulo. Un cambio interno de riesgo bajo (un nombre local, un comentario, un error evidente) se informa y se hace.

**Al editar:**

7. **Un cambio por vez.** No mezclar un cambio de regla con una limpieza de código.
8. **Correr las pruebas** del módulo tocado y de todos los que aparecen en "Si cambias esto, revisa". Si se movió un número de balance, correr también el simulador (M21).
9. **Arrancar el motor y al menos un cliente** en local. "Que un módulo importe no significa que arranque" (lección de TowerWars).

**Después de editar:**

10. **Actualizar las notas [ES]** del archivo: sobre todo "Lo usan", "Eventos" y "Si cambias esto, revisa".
11. **Actualizar el mapa de impacto** si apareció o desapareció una conexión.
12. **Actualizar el documento de diseño** en el mismo cambio, si cambió una regla (§7).
13. **Anotar en el registro de balance** todo número que se movió, con su antes → después y la medición.
14. **Informar al dueño:** qué cambió, qué pruebas pasaron y qué quedó pendiente.

**Niveles de riesgo:**

| Riesgo | Cuándo | Qué hace la IA |
|---|---|---|
| **Bajo** | Afecta solo al archivo y no cambia ningún resultado del juego | Informa y lo hace |
| **Medio** | Cambia un resultado del juego en uno o dos módulos | Mensaje de impacto y espera el sí |
| **Alto** | Toca una regla que nunca se rompe, un evento, datos guardados, la base de datos, o tres módulos o más | Mensaje de impacto, propone cómo probarlo y espera el sí |

### 6.3 Plantilla del mensaje de impacto

```
Cambio: <qué se quiere cambiar, en una frase>
Dónde: <archivo> · <módulo Mx> · diseño: <documento §>
Esto también afecta a:
  1. <módulo>: <qué cambia para el jugador o para el sistema>
  2. <módulo>: <...>
Reglas que toca: <ninguna | cuál, y por qué sigue cumpliéndose o no>
Números de balance: <ninguno | constante: antes → después>
Pruebas que voy a correr: <lista>
Voy a actualizar: <notas [ES] | mapa de impacto | documento de diseño | registro de balance>
Riesgo: <bajo | medio | alto> · ¿Sigo?
```

**Ejemplo.** El dueño dice: "la armadura protege demasiado, bájala".

```
Cambio: subir K de la armadura de 60 a 70 en el anillo I, para que absorba menos.
Dónde: content/balance/armor.yaml · M5 Combate · diseño: 03-personaje/balance.md §4
Con 60 de armadura, lo absorbido pasa de 50 % a 46 % (el daño recibido sube cerca de 8 %).
Esto también afecta a:
  1. Combate (M5): sube todo el daño físico, y sangrado y veneno se llenan más rápido.
  2. Salud (M7): más golpes cruzan el 50 % y el 25 % de vida, así que habrá más heridas.
  3. Oficios (M14): más trabajo para Medicina y Primeros Auxilios.
  4. Economía (M13): se venden más vendas y férulas, y se usa más el sanatorio (sumidero).
  5. Equipo (M4): cada punto de armadura vale menos; puede bajar el precio de las piezas pesadas.
  6. PvP (M12): los duelos y la guerra de castillos duran menos.
  7. Simulador (M21): hay que volver a medir la mitigación de las 11 specs de Defensa (objetivo ±4 %).
Reglas que toca: ninguna. La armadura sigue contando siempre y nunca da inmunidad.
Números de balance: K anillo I: 60 → 70.
Pruebas que voy a correr: tests/combat/, tests/health/test_wound_rules.py, simulador completo.
Voy a actualizar: registro de balance y balance.md §4 (hoy dice K = 60).
Riesgo: medio · ¿Sigo?
```

## 7. Trazabilidad entre diseño y código

**La regla:** el diseño y el código **se actualizan juntos, en el mismo cambio**. TowerWars tenía una wiki que describía 6 clases de un modelo que ya no existía: la documentación vieja miente, y una IA que la lea se equivoca con toda seguridad.

**En los dos sentidos:**
- **Del código al diseño:** cada archivo de código dice en su encabezado qué documento de diseño implementa (campo "Documento de diseño", con la sección).
- **Del diseño al código:** cuando exista código, cada documento de diseño suma en su línea de módulo el campo **Código:** con los archivos que lo implementan, por ejemplo `**Código:** engine/combat/armor.py, engine/combat/damage.py`.
- **Las decisiones también se citan:** si una regla del código sale de una decisión confirmada, la nota la nombra. Ejemplo para Economía: "Reglas que nunca se rompen: los sumideros son siempre un porcentaje (D-27)".
- **El estado del documento acompaña:** propuesta → confirmado → implementado.

**Si el diseño y el código no coinciden,** es un error. La IA no elige sola cuál vale: se lo dice al dueño, que decide, y se corrigen los dos.

**Una regla del juego en el código sin documento de diseño** es una regla escondida: se documenta antes de seguir.

### 7.1 Módulos y carpetas de código

Con la regla de idioma, las carpetas del código van en inglés (la [arquitectura](arquitectura-modular.md) §6 las propone en español; hay que alinearlas antes del primer archivo de código, D-59). `diseno/` queda igual.

```
engine/       pure rules, one package per module (M1-M25, except M21)
content/      data: map, bosses, classes, recipes, diseases, quests, balance, schemas
adapters/     telegram/, web/, mobile/, api/, admin/
simulator/    M21 balance simulator
tests/        one folder per module, no Telegram needed
tools/        checks for notes, ids and dependencies (§8)
diseno/       design documents (Spanish)
```

| Módulo | Paquete | Módulo | Paquete |
|---|---|---|---|
| M1 Núcleo | `engine/core` | M14 Oficios | `engine/professions` |
| M2 Héroe | `engine/hero` | M15 Social | `engine/social` |
| M3 Clases y talentos | `engine/classes` | M16 Minijuegos y apuestas | `engine/minigames` |
| M4 Equipo e inventario | `engine/equipment` | M17 Colecciones y logros | `engine/collections` |
| M5 Combate | `engine/combat` | M18 Temporadas y rankings | `engine/seasons` |
| M6 Enemigos y jefes | `engine/enemies` | M19 Mensajería | `engine/messaging` |
| M7 Salud | `engine/health` | M20 Administración y telemetría | `engine/telemetry` |
| M8 Mundo | `engine/world` | M21 Simulador de balance | `simulator/` |
| M9 Frontera y Fundación | `engine/front` | M22 Pagos | `engine/payments` |
| M10 Misiones | `engine/quests` | M23 Anti-trampas | `engine/anticheat` |
| M11 Instancias | `engine/instances` | M24 Construcción | `engine/construction` |
| M12 PvP, crimen y justicia | `engine/pvp` | M25 Propiedad | `engine/property` |
| M13 Economía | `engine/economy` | | |

**Fuera de los 25 módulos están los servicios de juego:** la puerta única entre los clientes y el motor ([Web y multiplataforma](web-y-multiplataforma.md) §2). Reciben órdenes, llaman a los módulos y devuelven vistas, sin reglas propias. En el código viven en `engine/service/`, y su encabezado dice "capa de servicios" en el campo Módulo y nombra los módulos que une.

**Cada módulo expone su parte pública en su `__init__.py`.** Los demás importan solo desde ahí, nunca un archivo interno de otro módulo. Así, lo que se puede romper desde fuera es poco y está a la vista.

### 7.2 Diccionario diseño ↔ código

El diseño usa nombres en español y el código en inglés. Este diccionario es el puente: la IA lo usa para buscar en el código un término del diseño, y la nota [ES] usa el nombre del diseño. **Una vez elegido, el nombre en inglés es estable como un ID**: renombrar un evento rompe a quien lo escucha y a los registros guardados.

| Diseño | Código | Diseño | Código |
|---|---|---|---|
| `GolpeRecibido` | `HitReceived` | Héroe | `hero` |
| `HeroeDerribado` / `HeroeCaido` | `HeroDowned` / `HeroFallen` | Herida · gravedad | `wound` · `severity` |
| `HeridaCreada` / `HeridaTratada` | `WoundCreated` / `WoundTreated` | Zona del cuerpo | `body_zone` |
| `EnfermedadContagiada` | `DiseaseContracted` | Enfermedad | `disease` |
| `ParteRota` | `PartBroken` | Aguante · Firmeza · Postura | `stamina` · `tenacity` · `poise` |
| `JefeDerrotado` | `BossDefeated` | Esencia · Mancha | `essence` · `bloodstain` |
| `RegionAbierta` (antes `PisoAbierto`, D-58) | `RegionOpened` | Región · Jefe · Receta (Piso se retira, D-58) | `region` · `boss` · `recipe` (`floor`: retirado) |
| `ObjetoFabricado` | `ItemCrafted` | Oficio | `profession` |
| `OrdenEjecutada` | `OrderFilled` | Anillo | `tier` |
| `ObjetoDestruido` | `ItemDestroyed` | Sello (se retira, D-58) · Pionero | `seal` · `pioneer` |

El diccionario crece en esta misma sección cada vez que el código necesita un término nuevo del diseño.

**Dos trampas de nombres.** *Zona* nombra tres cosas en el diseño: la zona del cuerpo (`body_zone`), el color de zona del PvP y, con D-58, la casilla del mapa. En el código cada una lleva su propio nombre, que se elige al agregarla aquí. Y *M1* a *M25* son siempre módulos: los grados de Maestría que [Investigación y maestría](../07-economia/investigacion-y-maestria.md) escribe M10, M20… no lo son.

## 8. Herramientas de control (se escriben junto con el código)

Ya se puede programar (D-59). Estas herramientas se escriben junto con el primer código y, desde que existan, corren en local antes de cada subida. Si alguna falla, no se sube.

| Herramienta | Qué hace |
|---|---|
| **Revisor de notas** (`tools/check_notes.py`) | Comprueba que todo archivo de código (`engine/`, `adapters/`, `simulator/`, `tests/` y `tools/`) tenga encabezado en inglés y nota [ES] con los 10 campos; que todo archivo de `content/` tenga su encabezado `# [ES]` (§4); que cada clase y función pública tenga docstring y nota [ES]; y que las rutas de "Documento de diseño" existan |
| **Grafo de dependencias real** (`tools/dependency_graph.py`) | Construye el grafo con las importaciones, las suscripciones a eventos y las lecturas de archivos de datos. Lo compara con el mapa de impacto y con los campos "Depende de" y "Lo usan", y avisa de cuatro cosas: una dependencia que no está declarada, una declarada que ya no existe, el motor importando un cliente, y un módulo que escribe datos de los que no es dueño. Puede dibujar el grafo en el formato de los diagramas del diseño |
| **Contratos de importación** | Prohíben las flechas que no deben existir: `engine/` nunca importa `adapters/`, y ningún módulo importa archivos internos de otro |
| **Revisor de IDs** (`tools/check_ids.py`) | Compara el contenido con la versión anterior: falla si un ID desapareció, cambió de nombre o se reutilizó |
| **Pruebas por módulo** | `tests/<módulo>/`, sin Telegram. Cada regla que nunca se rompe tiene su prueba, con una nota [ES] que cita el documento de diseño. Se corren las del módulo tocado y las de los afectados |
| **Registro de balance** | Cada número que se mueve, con fecha, antes → después, la medición y quién lo pidió. Falla si cambió un valor de `content/balance/` sin su entrada |
| **Índice en español** | Junta todas las notas [ES] de encabezado en una sola página para el dueño: qué hace cada archivo y con qué se conecta, sin abrir el código |
| **Revisor de credenciales** | Falla si encuentra un token, una contraseña o una clave en el repositorio |

## 9. Reglas heredadas de TowerWars

| Regla | Qué significa aquí |
|---|---|
| **IDs estables, solo se agregan** | En TowerWars los códigos por orden de aparición se rompían al insertar algo en el medio. Aquí todo ID se agrega al final, nunca se reutiliza y se retira con `retired: true` (§4) |
| **Migraciones de base de datos desde el día uno** | En TowerWars, agregar una columna tocaba seis lugares del código. Aquí cada cambio de tabla es un archivo de migración numerado, con su nota `-- [ES]`. Una migración ya aplicada no se edita nunca: se escribe otra |
| **Probar y arrancar antes de subir** | Pruebas **y** arrancar el motor con al menos un cliente. Al depurar, borrar los `.pyc` viejos, que confunden |
| **Credenciales: nombres sí, valores jamás** | Las claves van en variables de entorno fuera del repositorio. En el repositorio solo queda un archivo de ejemplo con los nombres (ver [Seguridad](seguridad-y-anti-trampas.md)) |
| **Motor sin dependencias de los clientes** | "Nada en el motor importa nada de los adaptadores". El motor no sabe si el jugador está en Telegram, en la web o en la app (D-40, D-41). Los textos para el jugador viven en archivos de idiomas, no en el motor |
| **Una sola fuente de verdad** | "La ropa no contaba": la guerra calculaba el poder por su lado. Cada número y cada validación viven en un solo lugar del motor, y su nota [ES] lo dice ("es la única fórmula de armadura del juego") |
| **Registro de balance obligatorio** | "Si un número de balance se movió y no está ahí, se movió a ciegas" |
| **Registro de cambios en orden** | El de TowerWars quedó desordenado. Aquí se escribe en orden, con cada cambio enlazado a su documento de diseño |
| **Nada en Railway sin permiso** | Ni despliegues ni variables sin que el dueño lo pida (D-03) |

---

**Preguntas abiertas de este documento** (pendientes de numerar en [Preguntas abiertas](../00-vision/preguntas-abiertas.md)):
- ¿Los datos de contenido van en YAML (admite comentarios y notas [ES]) o en otro formato?
- ¿Las notas [ES] se exigen también en las funciones internas que aplican reglas del diseño, o solo en las públicas?
- ¿La IA espera confirmación en todo cambio de riesgo medio, o solo en los de riesgo alto?
