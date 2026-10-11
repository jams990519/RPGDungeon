# Revisión completa del código y el contenido (versión 0.32)

> **Módulo** [00 · Visión](README.md) · **Depende de:** [CLAUDE.md](../../CLAUDE.md), [Mapa de impacto](../01-plataforma/mapa-de-impacto.md), [Convenciones de código](../01-plataforma/convenciones-de-codigo.md) · **Alimenta a:** la [hoja de ruta](hoja-de-ruta.md) y el [sistema de preguntas](sistema-de-preguntas.md) · **Estado:** informe del 11-oct-2026 (commit `764b9b5`, versión 0.32)

**Qué pidió el dueño.** Una revisión del proyecto entero, línea por línea, pasada por el mapa de impacto, para empezar a resolver los problemas y crear contenido nuevo.

**Qué se revisó.** Leído línea por línea: las 18.173 líneas de `engine/` (42 archivos), `adapters/` (490) y `tools/` (689). Comprobado con programas de auditoría: las 20.460 líneas de `content/*.yaml` (referencias cruzadas, claves de texto y los números sensibles del mapa de impacto §4). Medido: el simulador de combate (`tools/sim.py`, `tools/balance_report.py`) con hasta 300 peleas por clase. Las 11.018 líneas de `tests/` se revisaron por estructura y cobertura, no línea por línea.

---

## 1. Lo que está bien (para no tocarlo)

- **Las 540 pruebas pasan**: 17 min 45 s, sin fallos ni avisos.
- **El contenido no tiene una sola referencia rota.** Dos auditorías propias (ids de objetos, enemigos, biomas, recetas, oficios, especializaciones, mejoras, estudios, misiones, encargos, facciones, dudas, orígenes y cadenas `migrate_to`) dieron **0 hallazgos**. Todas las claves de texto del contenido **vivo** existen; ningún texto rompería `format()`; a ningún material, pieza de equipo o enemigo le falta precio, nivel o experiencia.
- **Todos los números sensibles del mapa de impacto §4 coinciden con `balance.yaml`**: energía de la cadena (5 + 2), costos (0/2/3/6), premio por marcas (10/25/50 %), `no_combo_mult` 0,85, tope de objetivos 5, pasiva de talentos y su tope de 50, tope de armadura 60 %, viaje de 1 minuto (D-197), 15 mejoras para castillo, umbrales de despensa 14/7/3/1, 4 % por punto de Defensa, curva de oficios 9 × (rango − 1)², especializaciones al 25 y al 75 con 7.200 de dominio.
- **La regla madre (D-232) se cumple en los esqueletos**: las 12 especializaciones comparten `base` y `per_level` dentro de su rol.
- **Higiene de código**: ni un `except` desnudo, ni un argumento mutable por defecto, ni un `== None`. Todo el azar sale de semillas y cada sistema usa su propio canal (el sigilo, los nodos, la obra maestra y los hallazgos no mueven ningún otro resultado). Los temporizadores perezosos son coherentes en todo el servicio. Las notas `[ES]` están en todos los archivos.

---

## 2. Fallos de corrección

### R-01 · El reinicio de época deja medio mundo viejo en pie · ❌ DESCARTADO POR EL DUEÑO (D-235)

> **11-oct-2026:** el dueño decidió no arreglarlo. `world.epoch` nunca se va a subir: esta versión es el formato de prueba de la versión nueva, que empezará su mundo desde cero en este mismo repositorio (D-235). El hallazgo queda escrito para que nadie lo vuelva a levantar; el código no se toca. Lo que sigue es lo que se midió.


**Dónde:** `engine/service/game.py`, `__init__` (líneas 500-516).

**Qué pasa:** al subir `world.epoch`, el servicio borra solo cuatro espacios (`hero`, `combat`, `zone`, `pending`). Se comprobó con una sonda: **sobreviven** `camp`, `territory`, `guild`, `camp_name`, `pantry`, `upgrades`, `nodes`, `dungeon` y `stock`.

**Consecuencia:** un mundo nuevo arrancaría con campamentos cuyos miembros no existen, con territorio que tapa para siempre esas zonas (y sus mazmorras y sus nodos), con nombres de campamento y de gremio ya ocupados, y con registros personales (`nodes`, `dungeon`) que heredaría el héroe nuevo de la misma cuenta.

**Por qué importa aunque D-64 diga "nunca subir la época":** el mecanismo existe justamente para poder reiniciar, y el comentario del código promete que lo hace ("wipe player data and create a new world").

**Arreglo:** borrar todos los espacios de datos de jugadores, con una lista explícita y una prueba que falle si se agrega un espacio nuevo y no se añade a la lista. Fuera de la lista quedan solo `player`, `invite_code` y `meta`.

### R-02 · `tick()` no pasa por `_load()` y se salta las migraciones

**Dónde:** `game.py`, `tick()` (líneas 700-720) frente a `_load()` (742-760).

**Qué pasa:** `tick()` arma el héroe con `Hero.from_dict` + `ensure_talents`, pero no aplica lo que sí aplica `_load`: la energía de la 0.6.1 (`energy_version`), la exploración vieja de la 0.8.1 y el **equipo inicial** (`gear_started`).

**Consecuencia:** a un héroe guardado antes de esos parches, si su viaje termina por `tick()`, se le resuelve el tramo y se le guarda la ficha sin lo que le faltaba; lo recibe recién en su siguiente botón. Hoy, con un jugador, es inocuo.

**Arreglo:** que `tick()` use `_load(account_id)`.

---

## 3. Balance (medido, no opinado)

### B-01 · Las 6 clases de ataque no están igualadas: del 67 % al 88 % contra el Guardián

`tools/sim.py --boss --seeds=300`, héroe de nivel 6 con equipo de su tipo:

| spec | gana % | spec | gana % |
|---|---|---|---|
| sacerdote_dps | 88 | druida_dps | 80 |
| guerrero_dps | 84 | paladin_dps | 77 |
| mago_dps | 80 | **cazador_dps** | **67** |

Con 300 peleas el error típico es de unos 2,3 puntos: **21 puntos de diferencia es señal, no ruido**. Las seis comparten esqueleto (160 de vida, 13,5 de ataque, 0,10 de armadura, +12 y +1,7 por nivel) y los mismos poderes (B 0,7 · H1 1,0 · H3 1,9). La diferencia está entera en los extras del H2 y del H3:

- `guerrero_dps`: su H3 lleva `low_hp` **×1,6** bajo el 35 % de vida.
- `sacerdote_dps`: H2 sangrado con `next_bonus` y H3 que escala con la edad del sangrado (`per_dot_age`).
- `cazador_dps`: su H3 lleva `vs_mark` **×1,25** fijo (la marca funciona: `mark: true` está puesto).
- `paladin_dps`: su H2 es un golpe **débil** (0,7) con carga, en lugar de un debilitamiento.

**Por qué se colaron:** `tests/test_clases_031.py::test_the_mother_rule_same_role_same_numbers` compara `base` y `per_level` (y los números del tanque), pero **no compara lo que rinden los botones**. La regla madre está vigilada en el esqueleto y no en el resultado.

**Arreglo, en dos pasos:** (1) igualar el valor de los extras del H2/H3 dentro de cada rol; los dos candidatos claros son el `×1,25` del Cazador y el H2 flojo del Paladín. (2) Añadir el guardián que falta: una prueba, o un paso del parche, que corra el simulador y falle si dos clases del mismo rol se separan más de N puntos.

### B-02 · Las peleas comunes no tienen riesgo en ningún nivel

`tools/balance_report.py` (escenarios a, b y c; niveles 1, 10, 25, 50, 75 y 100): **las 12 especializaciones ganan el 100 % en todos los niveles y todos los escenarios**, y terminan con entre el 54 % y el 91 % de vida. Incluso el escenario duro (b3, enemigos 3 niveles por encima) da del 94 % al 100 %. Con `--summary --real`, 100 % contra todos los enemigos de nivel 1-3.

El objetivo escrito (≥ 90 %, curación ≥ 85 %) se cumple de sobra, pero **hoy el único riesgo real del juego son el Guardián y la Noche de prueba**. Es una decisión de diseño que conviene tomar a propósito: o se acepta ("el peligro está en los jefes") o se baja el margen de las peleas comunes en los niveles altos.

### B-03 · El Guardián está en el borde fácil de su ventana

Objetivo 45-90 %. Medido: 9 de 12 especializaciones por encima del 80 %, y dos (`paladin_sanador` y `druida_tanque`) justo en el **90 %**, el techo.

### B-04 · La forma de jugar automática no usa la cadena de los sanadores

`engine/combat/auto.py`, `chain_choice`: un sanador con la vida por encima de `heal_late_below` devuelve siempre Básico (o su H2 si golpea). Está documentado, pero tiene dos efectos: los números del simulador para `curacion` no miden su cadena, y en el juego las **peleas automáticas** de un sanador juegan claramente peor que un humano, porque nunca cobran marcas.

---

## 4. Arquitectura y mantenimiento (el riesgo grande a futuro)

### A-01 · `engine/service/game.py` tiene 10.261 líneas: el 56 % del motor en una clase

Una sola clase (`GameService`) con 35 secciones. El diseño parte el juego en 25 módulos (`arquitectura-modular.md`) y el mapa de impacto da una ficha por módulo, pero el código tiene casi todo junto: el mundo, los campamentos, los oficios, las mazmorras, el comercio, las vistas y el combate.

**Por qué importa:** es exactamente lo que D-42 quiere evitar. Hoy, para responder "si cambio esto, ¿qué se rompe?", hay que leer un archivo de 10.000 líneas. Ya hay dos piezas separadas que funcionan bien (`story.py` y `guide.py`, como *mixins*): el camino está probado.

**Arreglo sugerido, por tandas y sin cambiar comportamiento.** Sacar a su propio mixin, de lo más aislado a lo más entrelazado: mazmorras (unas 620 líneas), campamentos enemigos y Explorador (480), reconocimiento y sigilo (290), nodos (160), especializaciones de oficio (420), encantamiento (350), mejoras del campamento (840) y oficios (680). Cada tanda, su parche, y las pruebas sin tocar.

### A-02 · La subida de nivel está escrita dos veces

`_give_xp` (game.py 2660) y `_end_combat` (10190) tienen cada uno su propio bucle `while hero.level < max_level...`. Y `_guardian_rewards` suma experiencia a mano (`hero.xp += xp`) confiando en el bucle de `_end_combat`.

**Hoy no da un fallo** (los dos hacen lo mismo y el multiplicador no se aplica dos veces), pero el día que subir de nivel haga algo más (un aviso, un premio, una misión), la mitad del juego no lo hará. **Arreglo:** que `_end_combat` llame a `_give_xp`.

### A-03 · Hay contenido escrito en el motor (rompe la regla 4 de la arquitectura)

- `game.py:1186` — la tabla de hallazgos al explorar: `["hierba_curativa", "pieza_metal", "venda", "pocion_vida"]` con pesos `[5, 3, 2, 1]`.
- `game.py:2614` — `given.get("carne", 0)` para el bono del 🍖 Ahumadero.
- `game.py:5154` — `"provisiones"` en los valores de ❓ Dudas.
- `game.py`, `_health_view` — los umbrales del estado del cuerpo (100/60/25/0) escritos en el código y no en `balance.yaml`.

**Arreglo:** moverlos a `balance.yaml` (`explore.finds`, `upgrades.smoked_item`, `health.states`).

### A-04 · Siete sitios que indexan directo donde todo lo demás es defensivo

`engine/classes/talents.py`, `_group()` (`classes[hero.class_id]`: revienta si un id desaparece); `_chain_combat_view` (`next(...)` sin valor por defecto si a una clase de cadena le faltara un enlace); `_fog_stage` (`[-1]` sobre una lista que quedaría vacía si se retiran todas las etapas); `raids.pick_enemy` y `_start_combat` (asumen que la lista de enemigos nunca está vacía); `raid_rules.scale_enemy` (divide por `attack_mult`). Ninguno falla hoy porque el contenido los respeta: son trampas para el día que el contenido cambie.

### A-05 · El almacén lee espacios enteros

`SqliteStore.items()` trae todas las filas de un espacio y las convierte de JSON, y `tick()` recorre **todos** los héroes cada 15 segundos. Con un jugador no se nota; es lo primero que habrá que cambiar al abrir la beta (lo que el diseño ya prevé cuando habla de PostgreSQL).

---

## 5. Documentación que ya no dice la verdad (la lección de TowerWars)

- **D-01** · `engine/hero/hero.py:36` y `game.py:9729` dicen que la opción 🩹 Retirarse viene en **50 %**; `balance.yaml` dice **30** desde D-119. Dos comentarios que mienten sobre el mismo número.
- **D-02** · Faltan **363 claves `ability.<id>.desc`**, todas de habilidades de especializaciones **retiradas** (el contenido vivo está completo). No se ven porque esas specs ya no se juegan; si alguna pantalla las mostrara, el jugador leería `[ability.x.desc]`. O se escriben, o se quita el campo del contenido retirado, o se deja anotado a propósito.

---

## 6. Cliente de Telegram

- **T-01 · En grupos, los avisos y el respaldo de los botones van al privado.** `bot.py` usa el id de usuario como id de chat (`send_view(query.bot, query.from_user.id, ...)` y `notifier`). Si un botón no se puede editar, la respuesta sale por privado, o falla si el jugador nunca abrió el bot. `PLACE_CODE_RE` ya acepta `/ir1@bot`, así que jugar en grupo está previsto: habría que guardar el chat de cada mensaje.
- **T-02 · El recorte a 4.096 caracteres puede romper el HTML.** `render.py` corta con `text[:4095] + "…"`; si el corte cae dentro de una entidad escapada (`&amp;`), Telegram rechaza el mensaje. Conviene cortar por líneas, o escapar después de recortar.

---

## 7. Detalles menores (anotados, sin urgencia)

1. `chain_round.py`, `apply`, rama `debuff`: si una habilidad llevara solo `weaken`, el texto mostraría ese valor como si fuera `expose`. Hoy la única habilidad `debuff` viva (`mago_ruptura_arcana`) lleva los dos, así que es una trampa latente, no un fallo.
2. `_pantry`: una despensa nueva se llena con la ración **por defecto**, ignorando el descuento del 🌾 Granero que sí se usa al consumir.
3. `_raid_reward` paga a todos los que salieron a defender, incluidos los que perdieron o huyeron. Puede ser a propósito; conviene decidirlo.
4. `enemy_camps.chest` depende de que la variable del `for` sobreviva al bucle (`res`). Funciona; es frágil de leer.
5. `story.py`, `_choice_of` busca la decisión por `goal["id"]`, y `_choose` la guarda con un id compuesto si falta. Hoy todas las decisiones de `story.yaml` tienen `id` (comprobado), así que no se dispara.
6. `Texts.t` solo atrapa `KeyError` e `IndexError`; un `ValueError` de `format()` subiría. Hoy ningún texto lo provoca (comprobados los de todos los archivos de idioma).
7. `max_times` devuelve 0 para una receta sin materiales (no existe ninguna hoy).
8. Las herramientas (`sim.py`, `balance_report.py`) imprimen UTF-8 en la consola de Windows y sale "Guardi?n". Solo molesta a quien mide.

---

## 8. Qué haría primero

*(Actualizado el 11-oct-2026 con D-235: R-01 queda descartado.)*

1. **B-01** (las 6 clases de ataque, del 67 % al 88 %): decidir los números con el dueño y añadir el guardián de simulador. Es lo que más se nota jugando y es lo único del informe que afecta al jugador de hoy.
2. **R-02** (`tick` sin `_load`): un arreglo de una línea. Con D-235 su valor baja (solo afecta a héroes guardados antes de parches viejos), pero quita una incoherencia.
3. **A-02** y **A-03**: media hora cada uno, y quitan dos trampas futuras.
4. **B-02**: pregunta para el dueño antes de tocar nada (¿las peleas comunes deben seguir sin riesgo?). Entra en el sistema de preguntas.
5. **A-01** (partir `game.py`): por tandas, una por parche, empezando por las mazmorras. Con D-235 pesa más, no menos: lo que se pruebe aquí es lo que se lleva a la versión nueva, y hoy el 56 % del motor está en un archivo.

**Lo que D-235 abre como pregunta.** Si esta versión es un banco de pruebas, media docena de sistemas del motor existen solo para no perder progreso que, de todas formas, no va a viajar a la versión nueva: `energy_version`, la exploración de la 0.8.1, `gear_started`, las cadenas `migrate_to` de 48 especializaciones retiradas, `legacy_content()` en las pruebas y los "vacío por defecto: los héroes guardados antes cargan igual" de casi todos los campos de `Hero`. Conviene que el dueño diga si se sigue pagando esa compatibilidad o si, de aquí en adelante, un cambio de datos puede pedir empezar un héroe nuevo.

## De dónde sale

- **La revisión del 11-oct-2026** que pidió el dueño sobre el commit `764b9b5` (versión 0.32), con las reglas de [CLAUDE.md](../../CLAUDE.md) y el [mapa de impacto](../01-plataforma/mapa-de-impacto.md) §2 y §4 como vara de medir.
- **Las medidas** de `tools/sim.py --summary --real`, `--boss --seeds=80` y `--boss --seeds=300`, y de `tools/balance_report.py` (escenarios a, b, c y b3).
