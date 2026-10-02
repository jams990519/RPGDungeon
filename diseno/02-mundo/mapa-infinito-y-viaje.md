# El mapa infinito y el viaje

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Decisiones](../00-vision/decisiones.md) (D-58, D-59, D-60), [Jefes](../06-contenido/jefes.md) (D-08) · **Alimenta a:** [Economía](../07-economia/economia.md), [Fundación y cisma](fundacion-y-cisma.md), [Misiones y exploración](../06-contenido/misiones-y-exploracion.md), [Heridas](../05-salud/heridas.md), [Social](../08-social/README.md) (jugadores en la zona, §1.13), [Profesiones](../07-economia/profesiones.md) (🧭 Explorador, §1.14), [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) (entradas de mazmorra, §1.15), [Red de oficios](../07-economia/red-de-oficios.md) (recursos de cada terreno y nodos, §1.12.2 y §1.16) · **Reemplaza a:** [Torre y pisos](torre-y-pisos.md) (se retira) · **Estado:** v0.1 en código; el resto, propuesta

**La regla del dueño (D-58, confirmada):** "Quita los pisos, deja un mapa infinito por investigar, pero que tome tiempo moverte entre lugares."

Este documento tiene dos partes:
- **Ya funciona (v0.1):** lo que hace el código hoy, con sus números. Si el código y este texto no coinciden, es un error (ver [CLAUDE.md](../../CLAUDE.md) §4).
- **Lo que viene por parches (D-60):** propuesta, en orden de prioridad. Nada de eso está confirmado.

---

## 1. Ya funciona (v0.1)

Código: [mapgen.py](../../engine/world/mapgen.py), [travel.py](../../engine/world/travel.py), [game.py](../../engine/service/game.py). Datos: [biomes.yaml](../../content/biomes.yaml), [balance.yaml](../../content/balance.yaml), textos en [es.yaml](../../content/locales/es.yaml).

### 1.1 La rejilla de zonas

- El mundo es una rejilla de **zonas** con coordenadas `(x, y)`, sin borde. Norte es `y` positivo.
- **El Claro** está siempre en `(0, 0)`: bioma propio (🔥), sin peligro, siempre descubierto.
- **Lejanía** = distancia en anillos cuadrados hasta el Claro: `max(|x|, |y|)`. Las diagonales cuentan igual que los lados. A Lejanía *d* hay 8 × *d* zonas.
- **Anillo** = franja de 3 Lejanías, del I al X. Desde Lejanía 28 todo es anillo X, sin fin.
- **Nivel de la zona** = `max(1, redondeo(1 + Lejanía × 0,9))`. La pantalla lo muestra como "Peligro de nivel".

| Lejanía | Anillo | Nivel de zona | Zonas en ese anillo de Lejanía |
|---|---|---|---|
| 0 | — (el Claro) | 1 | 1 |
| 1 | I | 2 | 8 |
| 2 | I | 3 | 16 |
| 3 | I | 4 | 24 |
| 4-6 | II | 5-6 | 32-48 |
| 10 | IV | 10 | 80 |
| 20 | VII | 19 | 160 |
| 28 y más | X | 26 y sube sin tope | 224 y más |

### 1.2 Biomas

**Desde la 0.26.2 (D-186, D-187): el terreno es un tablero salteado, "como jugando Tetris".** El dueño pidió que el mapa se vea como un tablero de ajedrez salteado: varios cuadros juntos del mismo color (cinco verdes, al lado amarillos, al lado morados...), con cantidades, orden y posiciones que cambian; y aclaró que el mejor ejemplo es Tetris. Así se arma desde la 0.26.3 (`engine/world/mapgen.py` → `terrain_at`):

- El mapa se parte en **bloques de 4 × 4 zonas**; las filas impares de bloques van corridas 2 zonas, como ladrillos, para que no se vea una cuadrícula.
- Cada bloque se llena con **piezas de Tetris de 4 zonas** (I, O, T, S, Z, J y L): una de las **117 formas** de cubrir un cuadrado de 4 × 4, elegida por la semilla (`block_tilings`).
- Cada pieza **sortea su terreno por peso** (`content/biomes.yaml` → `terrain.weight`, tabla de abajo). Los fríos (`climate: cold`: tundra y bosque oscuro) salen más hacia el norte y los calientes (`hot`: desierto, selva y sabana) más hacia el sur (`terrain.climate_slope` y `climate_strength`: hasta 3 veces más en su lado y hasta 0,15 veces en el otro), pero todos pueden salir en cualquier parte. Dos piezas vecinas del mismo terreno se ven como una mancha más grande.
- El **🔥 Claro** queda fijo en (0, 0). (En la 0.26.2 eran manchas de 3 a 12 zonas y las ruinas iban sueltas.)
- Un terreno nuevo solo agrega su `terrain` y su `color` en `content/biomes.yaml` (D-185: se pueden agregar todos los que hagan falta), además de su nombre, su peligro, su agua, su catálogo y sus enemigos (abajo).
- **Tandas (`terrain.tier`, desde la 0.28, D-188):** cada terreno dice en qué tanda se agregó (sin `tier`, la 0: los 8 de siempre). Cada pieza mira primero, con un sorteo propio de esa tanda (`terrain_tier:1`), si le toca un terreno de la tanda más nueva, con la parte del peso que les toca; si no, sortea entre los de antes **exactamente como antes**. La parte de cada terreno en todo el mapa es la misma que con un sorteo único, pero agregar terrenos solo cambia las piezas que pasan a ser de un terreno nuevo: en la 0.28, unas 3 de cada 10. Las demás conservan su terreno, sus enemigos, sus recursos propios (§1.12.2) y sus nodos (§1.16). Sin tandas, la 0.28 habría cambiado el terreno de 77 de cada 100 zonas, los recursos propios de 73 y el recurso de 1 de cada 3 nodos ya descubiertos. Un terreno nuevo va siempre en una tanda nueva.

**Los terrenos del tablero (0.28):**

| Terreno | Color en el 🗺️ Mapa | Peso | Clima | Tanda | Peligro al llegar | Zonas con agua (🐟) |
|---|---|---|---|---|---|---|
| 🌾 Pradera | 🟩 | 3 | cualquiera | 0 | 25 % | 3 de 10 |
| 🌲 Bosque | 🟢 | 3 | cualquiera | 0 | 35 % | 3 de 10 |
| ⛰️ Colinas | 🟫 | 2 | cualquiera | 0 | 30 % | — |
| 🐸 Pantano | 🟪 | 2 | cualquiera | 0 | 45 % | todas |
| 🏔️ Montaña | ⬜ | 2 | cualquiera | 0 | 40 % | — |
| 🏜️ Desierto | 🟨 | 2 | caliente (sur) | 0 | 40 % | — |
| ❄️ Tundra | 🟦 | 2 | frío (norte) | 0 | 40 % | — |
| 🏚️ Ruinas | ⬛ | 1 | cualquiera | 0 | 50 % | — |
| 🦜 Selva | 🟣 | 1,5 | caliente (sur) | 1 | 45 % | 5 de 10 |
| 🦒 Sabana | 🟧 | 1,5 | caliente (sur) | 1 | 30 % | 2 de 10 |
| 🌋 Volcán | 🟥 | 0,5 | cualquiera | 1 | 55 % | — |
| 🏞️ Cañón | 🟤 | 1 | cualquiera | 1 | 35 % | 4 de 10 |
| 🦉 Bosque oscuro | ⚫ | 1 | frío (norte) | 1 | 50 % | 3 de 10 |
| 🦆 Lago | 🔵 | 1 | cualquiera | 1 | 25 % | todas |

- **Los 6 de la 0.28 (D-188, provisional: cuáles, colores y números los propuso Claude).** Cada uno sale menos que los clásicos (peso 1 a 1,5; el 🌋 volcán, 0,5, es el más raro y el más peligroso). Cerca del Claro son unas 28 de cada 100 zonas. Los colores nuevos van en "primos" del terreno parecido cuando no queda un color propio (🟣 selva junto a 🟪 pantano, 🟤 cañón junto a 🟫 colinas, ⚫ bosque oscuro junto a ⬛ ruinas, como 🟢 bosque y 🟩 pradera); 🟧 sabana, 🟥 volcán y 🔵 lago tienen el suyo. Un color nunca se repite ni es el emoji de un recurso que puede tener nodo. Libres para más terrenos: 🔴 🟠 🟡 ⚪.
- **Sus enemigos:** no hay enemigos nuevos; cada terreno nuevo se agregó a los de terrenos parecidos (`content/enemies.yaml` → `biomes`), con 2 o más en cada franja de nivel: 🦜 selva, bestias del bosque y del pantano (arañas, caimanes, pantera, sierpe esmeralda); 🦒 sabana, de la pradera y el desierto (chacal, hiena, león, mantícora); 🌋 volcán, de montaña, colinas y ruinas que no son de hielo (fuego fatuo, chispa errante, salamandra de lava, fénix de ceniza); 🏞️ cañón, de colinas y desierto (cabra, escorpiones, wyvern, roc); 🦉 bosque oscuro, del bosque y las ruinas (lobo gris, pantera sombría, licántropo, liche); 🦆 lago, del pantano y la pradera (tortuga, sanguijuela, hidra, leviatán). El 🗡️ bandido errante sale en todos. Los terrenos de antes siguen con los mismos enemigos, en el mismo orden.
- **Lo que no tocan:** los 6 recursos de base (siguen al bioma clásico, que nunca da un terreno nuevo), la misión de la historia que pide ganar en 🌲 bosque o 🐸 pantano (los dos siguen saliendo) y las mazmorras (sus familias no dependen del terreno).
- **El terreno no decide los recursos (D-185):** los recursos de tierra siguen las regiones de antes, calculadas con el bioma "clásico" de abajo (`classic_biome`), así que ninguna zona perdió lo que tenía. El terreno sí decide los enemigos y el peligro, y el agua: un 🟪 pantano siempre tiene agua para pescar.

**El bioma clásico (hasta la 0.26.1 era el terreno; ahora solo cuenta para los recursos de tierra).** Cada zona sacaba su bioma de tres ruidos suaves (temperatura, humedad y altura), calculados con la semilla del mundo. El ruido forma **manchas**: zonas vecinas suelen compartir bioma.

- **Temperatura** = 0,5 − 0,03 × `y` ± 0,2 de ruido. **El norte es frío y el sur caliente:** hacia `y = +10` aparece la tundra; hacia `y = −9`, el desierto.
- **Ruinas:** 6 % de las zonas, en cualquier parte, sin seguir manchas.

Orden en que se decide (gana la primera regla que se cumple):

| # | Regla | Bioma |
|---|---|---|
| 1 | Es `(0, 0)` | 🔥 Claro |
| 2 | Sorteo de ruinas < 0,06 | 🏚️ Ruinas |
| 3 | Altura > 0,72 | 🏔️ Montaña (❄️ Tundra si temperatura < 0,35) |
| 4 | Temperatura < 0,2 | ❄️ Tundra |
| 5 | Temperatura > 0,75 y humedad < 0,5 | 🏜️ Desierto |
| 6 | Humedad > 0,7 | 🐸 Pantano |
| 7 | Humedad > 0,45 | 🌲 Bosque |
| 8 | Altura > 0,55 | ⛰️ Colinas |
| 9 | Ninguna de las anteriores | 🌾 Pradera |

### 1.3 Nombres

Cada zona tiene un nombre de dos partes sorteadas por coordenada: una de 12 primeras ("Vado", "Cerro", "Hondonada"...) y una de 12 segundas ("Gris", "del Cuervo", "de Hierro"...). Salen 144 combinaciones, así que **los nombres se repiten** lejos. Ejemplo: "Hondonada de Hierro". El Claro se llama siempre "El Claro".

### 1.4 Qué se guarda

El mapa **no se guarda**: cualquier zona se recalcula igual a partir de la semilla y sus coordenadas. Solo se guarda:

| Dato | Dónde | Contenido |
|---|---|---|
| Semilla del mundo | espacio `meta` | Se crea una vez, al primer arranque |
| Zona descubierta | espacio `zone`, clave `x:y` | Nombre del descubridor y la hora |
| Posición y actividad del héroe | espacio `hero` | `x`, `y` y el viaje o la exploración en curso con su hora de fin |
| Quién puede estar en cada zona (D-96, provisional) | espacio `presence`, clave `x:y` | Las cuentas anotadas en esa zona. Es solo un índice: quién cuenta como presente se decide al leer, con la ficha de cada héroe (§1.13) |

**El mapa recuerda los lugares (D-61), en dos memorias:**
- **La del mundo:** quién descubrió cada zona queda guardado para siempre ("🧭 La descubrió Aria").
- **La de cada héroe:** la lista de zonas que pisó (campo `known` del héroe, empieza con el Claro). Su mapa, sus rutas y su lista de Lugares usan esta memoria: una zona que descubrió otro y tú no pisaste se ve como "▪️ Otro la descubrió, pero tú no la conoces", sin bioma ni nombre.

> **Cuidado:** cambiar los umbrales de la tabla 1.2, el ruido o los IDs de bioma **cambia el mapa de un mundo ya creado**. Ver la nota `[ES]` de [mapgen.py](../../engine/world/mapgen.py).

### 1.5 El viaje

- Desde una zona se viaja **solo a las 4 vecinas** (norte, sur, este, oeste). No hay diagonales ni teletransporte.
- **1 minuto real por cuadro, cerca o lejos** (D-197, confirmada; en el juego desde la 0.29.1): 10 cuadros son 10 minutos (`travel.first_minutes: 1`, `travel.steps_per_minute: 0`). El bioma no cambia el tiempo; sigue decidiendo el peligro y lo que se recolecta.
  - **Regla del dueño:** desplazarse cuesta tiempo; trabajar (farmear solo o en caravana) cuesta energía.
  - **Antes (D-78):** las 2 primeras zonas desde el Claro o tu campamento tomaban 2 minutos, las 2 siguientes 3, luego 4, hasta un tope de 20 por zona. La fórmula sigue en el código: si `travel.steps_per_minute` vuelve a ser mayor que 0, cada tantas zonas más lejos suma 1 minuto y tu campamento reinicia la cuenta desde su borde.
  - **Energía:** moverse no gasta energía (D-190, D-197). Explorar y recolectar gastan 1 ⚡ por vuelta; cazar, 2 por presa. Máximo 50, se recuperan 40 al día (1 cada 36 minutos). El combate en sí no gasta energía. Para empezar una acción hay que tener de entrada toda la energía que pide (D-196).
  - **Pendiente:** si las monturas o mejoras acortarán el minuto por cuadro (E-161) y si mientras viajas puedes hacer otras cosas (E-162; hoy puedes mirar todo, pero no trabajar hasta llegar).
- Ningún viaje baja de 1 minuto. Un ajuste de servidor (`time_scale`) multiplica todos los tiempos; en juego normal vale 1 y en pruebas es menor.
- La pantalla redondea hacia arriba al minuto.

| Cuadros que cruzas | 1 | 2 | 5 | 10 | 20 |
|---|---|---|---|---|---|
| Minutos de viaje (D-197) | 1 | 2 | 5 | 10 | 20 |

| Bioma | Peligro al llegar |
|---|---|
| 🔥 Claro | 0 % |
| 🌾 Pradera | 25 % |
| 🌲 Bosque | 35 % |
| ⛰️ Colinas | 30 % |
| 🏚️ Ruinas | 50 % |
| 🏜️ Desierto | 40 % |
| 🐸 Pantano | 45 % |
| ❄️ Tundra | 40 % |
| 🏔️ Montaña | 40 % |
| 🦜 Selva (0.28) | 45 % |
| 🦒 Sabana (0.28) | 30 % |
| 🌋 Volcán (0.28) | 55 % |
| 🏞️ Cañón (0.28) | 35 % |
| 🦉 Bosque oscuro (0.28) | 50 % |
| 🦆 Lago (0.28) | 25 % |

### 1.6 Temporizadores, aviso y encuentro al llegar

- **Temporizadores perezosos:** el viaje guarda solo su hora de fin. Cada orden del jugador primero "cierra las cuentas" del héroe (termina lo que ya venció). No hay un proceso por héroe.
- **Aviso:** el bot de Telegram revisa cada 15 segundos quién terminó y le manda la pantalla de llegada. El jugador puede cerrar el chat.
- **Una actividad a la vez:** viajando no se explora ni se cambia de rumbo; en combate no se viaja. Sí se puede mirar el mapa, los Lugares, el héroe y la mochila.
- **📒 Lugares** (desde D-106 se abre en 🧭 Explorar → 🗺️ Mapa → 📒 Lugares, para dejarle lugar a 🏹 Cazar en 🧭 Explorar): lista los lugares que tu héroe recuerda, del más cercano al más lejano (se muestran 8), con la distancia en zonas y el tiempo estimado. Al elegir uno, el héroe viaja solo, zona por zona: primero en el eje este-oeste y después en el norte-sur. Cada tramo se encadena desde la hora en que terminó el anterior, aunque nadie mire. Un encuentro al llegar a un tramo corta el viaje ("⛔ Tu viaje se corta en…").
- **Al llegar:** se publica `TravelArrived`. Si nadie había pisado la zona, queda a nombre del héroe y se publica `ZoneDiscovered`.
- **Encuentro al llegar:** probabilidad = peligro del bioma × 1,0 (`arrival_encounter_scale`). El enemigo sale de los que viven en ese bioma y encajan con el nivel de la zona; su nivel es el de la zona, +1 con 30 % de probabilidad. El sorteo usa la semilla del mundo, el héroe y la hora de llegada: el resultado no cambia aunque se repita la orden.

### 1.7 Explorar

Explorar dura **10 minutos** en la zona actual. Al terminar sale uno de tres resultados:

| Resultado | Probabilidad | Qué da |
|---|---|---|
| ⚠️ Un enemigo te descubre | 45 % (0 % en el Claro) | Combate, con la misma regla de enemigo que al llegar |
| 🔎 Un objeto | 35 % (80 % en el Claro) | Hierba curativa 5 · Pieza de metal 3 · Venda 2 · Poción de vida 1 (pesos) |
| 💰 Oro | 20 % | Nivel de la zona × (2 a 5) + 1 |

### 1.8 Regeneración

Fuera de combate se recupera **1 % de la vida máxima por minuto**, también viajando. De 0 a lleno: 100 minutos. En combate no se regenera.

### 1.9 El mapa en texto

El botón 🗺️ Mapa dibuja 13 × 13 zonas (6 a cada lado, `map_view.radius`; en la v0.1 eran 7 × 7) y, desde D-112, marca los campamentos enemigos que ves (§1.14; desde la 0.26.1 con 👹, antes ⛺); desde D-171, las entradas de mazmorra que tienes cerca (§1.15; desde la 0.26.1 con la 🕳️ cueva, antes ❓). 🧍 eres tú. El norte está arriba. (Hasta la 0.26.1, ▪️ era lo que descubrió otro y ▫️ lo que nadie conoce; desde la 0.26.2 todo el cuadrado se pinta por terreno, D-186.)

**Colores por terreno (D-179, desde la 0.26.1).** Cada cuadrito se pinta con el color de su terreno (en la 0.26.1, solo lo que tu héroe recordaba; desde la 0.26.2, **todo el cuadrado**, como un tablero salteado de manchas, D-186 y §1.2): 🟩 pradera, 🟢 bosque, 🟫 colinas, ⬜ montaña, 🟦 tundra, 🟨 desierto, 🟪 pantano y ⬛ ruinas; el 🔥 Claro sigue con su fuego (D-182, colores elegidos por Claude). El color sale de `content/biomes.yaml` (`color`) y la leyenda del mapa se arma sola, así que un terreno nuevo solo agrega su color (quedan libres 🟧, 🟥 y los círculos). **El color es el terreno, no promete recursos:** ver verde no quiere decir que haya madera o semillas; lo que hay se sabe explorando (antes, al 100 %, la zona se pintaba con su recurso principal, D-87).

### 1.10 Pantalla de ejemplo

Salida real del motor (semilla 1), tras ir norte, norte y este desde el Claro:

```text
📍 Llegaste a Hondonada de Hierro (🌾 Pradera).
🧭 ¡Nadie había pisado esta zona! Queda en el mapa con tu nombre.

📍 Dónde estás
Hondonada de Hierro — 🌾 Pradera
Lejanía 2 · Anillo I · Peligro de nivel 3
🧭 La descubrió Aria
❤️ 135/135 · 💰 10 · Nivel 1

Rutas:
⬆️ Norte: ❔ Tierra sin cartografiar · 19 min
⬇️ Sur: ❔ Tierra sin cartografiar · 19 min
➡️ Este: ❔ Tierra sin cartografiar · 19 min
⬅️ Oeste: 🏚️ Ruinas Cañada Rojo · 30 min

[⬆️ Norte · 19 min] [⬇️ Sur · 19 min] [➡️ Este · 19 min] [⬅️ Oeste · 30 min]
[🔎 Explorar · 10 min] [📒 Lugares] [🗺️ Mapa] [👤 Héroe] [🎒 Mochila]
```

```text
🗺️ Tu mapa
🧍 tú · ▪️ la descubrió otro · ▫️ nadie la conoce · el norte está arriba
▫️▫️▫️▫️▫️▫️▫️
▫️▫️▫️▫️▫️▫️▫️
▫️▫️▫️▫️▫️▫️▫️
▫️▫️🏚️🧍▫️▫️▫️
▫️▫️🌾▫️▫️▫️▫️
▫️▫️🔥▫️▫️▫️▫️
▫️▫️▫️▫️▫️▫️▫️

Coordenadas 1, 2 · Lejanía 2
```

---

### 1.11 Campamentos que crecen (D-81)

- **Al fundarlo, un campamento ocupa 1 zona.** Cada vez que sus miembros lo agrandan (⬆️ Agrandar campamento), suma 1 zona más: 2, 3, 4… El costo es 15 de madera, 10 de piedra y 5 de fibra, multiplicado por el nivel actual (`camps.grow_cost_per_level`). Desde el nivel 6 también cuesta 🪎 cofres: 1 de 6 a 7, 2 de 7 a 8 y 3 de 8 a 9 (D-92, provisional; ver [Fundación y cisma](fundacion-y-cisma.md) §2.4).
- **Hacia dónde crece:** desde 0.8.1 (D-87) tú eliges qué zona vecina toma tu campamento, viendo los recursos que conoces de cada una; no puede tomar zonas de otro campamento ni del Claro. La espiral fija (norte, este, sur, oeste, diagonales, anillo siguiente; `engine/world/territory.py`) queda solo para el Claro.
- **El Claro no crece** (D-98): ocupa las zonas de la etapa que tenía cuando se quitó su obra común (1 por etapa) y ya no suma más.
- **Qué da el territorio:**
  - Al llegar a una zona del territorio no te atacan.
  - Nadie puede fundar otro campamento encima.
  - Para tu viaje, cada cuadro toma 1 minuto (D-197). Con la regla vieja (D-78), la distancia se contaba desde la zona más cercana de tu campamento o del Claro.
- La línea "🏕️ Territorio de…" aparece en la pantalla de la zona.
- **Nombre y miembros (D-84):** al fundarlo, el fundador escribe el nombre (único; puede cambiarlo). Otros jugadores piden unirse desde el campamento y el fundador acepta o rechaza con un botón. Caben 2 miembros al nivel 1 y 2 más por cada nivel. Cada jugador pertenece a un solo campamento, cuenta la distancia del viaje desde él y puede salir cuando quiera.
- Lo pidió el dueño. Los costos y la seguridad al llegar los propuso Claude.

### 1.12 Exploración por porcentaje y recursos (D-87)

- **Cada acción fuera del combate (salvo moverse) se hace en lote.** Al tocar 🔎 Explorar o 🪓 Recolectar, eliges cuánta energía gastar seguido: ⚡ 5, 10, 20, 40 o todo (`energy.batch`). **Desde la 0.27.1 (D-189)** todas las cantidades salen a la vez, como botoncitos con solo el número en una fila ("5", "10", "20", "40", "Todo") y un botón ancho ❌ Cancelar abajo; el tiempo de cada una va en una línea del texto ("⏱️ 5 → 50 min · 10 → 1 h 40 min...").
  - Antes de empezar puedes ❌ Cancelar sin gastar nada.
  - Ya en marcha, ❌ Detener corta el lote y devuelve la energía de la vuelta en curso.
  - Cada vuelta gasta 1 ⚡ al empezar.
  - El lote se corta si te atacan (con ✋ Manual; con ⚔️ Peleas automáticas el héroe pelea solo y sigue, §1.12.1), si se acaba la energía, si se llena la mochila o, al explorar, si ya no queda nada por explorar desde donde estás (tu zona y las de alrededor al 100 %, D-107).
  - El bot te escribe una sola vez, al terminar, con el resumen.
- **Explorar sube un porcentaje:** cada vuelta suma entre 15 % y 30 % de la zona (`exploration.per_step`).
  - Al 1 %, 20 %, 40 %, 60 % y 80 % descubres el primero, el segundo, el tercero, el cuarto y el quinto recurso; al 100 %, todos (`exploration.reveal_at`; hasta la 0.26.1 eran 1 %, 50 % y 100 % para 3 recursos: nadie conoce menos que antes).
  - Al 100 % la zona ya no se explora más: conoces todo lo que tiene. (Hasta la 0.26 la zona aparecía en tu mapa con el color de su recurso principal; desde la 0.26.1 el mapa pinta el terreno, §1.9.)
  - **Desde 0.13.1 (D-107), explorar sigue alrededor sin moverte.** Con tu zona al 100 %, cada vuelta estudia la primera casilla vecina que no esté al 100 % (primero norte, este, sur y oeste; después las diagonales; `explore.around_radius` = 1, las 8 vecinas). El héroe no se mueve: los ataques, los hallazgos y las monedas son de la zona donde estás; lo que avanza es el porcentaje y los recursos de la vecina, que queda en tu memoria y en tu mapa. Así un lote grande completa tu zona y sigue con las de alrededor, en el mismo cuadro. Cuando tu zona y sus 8 vecinas están al 100 %, hay que moverse para seguir explorando.
  - Tu héroe recuerda los recursos de cada zona que exploró.
  - Fundar un campamento pide la zona explorada al 100 %.
- **Regiones de recursos:** hay 6 recursos de base: madera, piedra, fibra, hierba curativa, metal y arcilla.
  - Cada uno forma manchas de distinto tamaño: unas de 2 o 3 zonas, otras de 5×5 o más (`engine/world/resources.py`).
  - Una zona tiene de 1 a 3 de base. El bioma ayuda, pero no manda.
  - **Desde la 0.27 (D-180), cada terreno suma los suyos:** cada zona trae además 2 o 3 recursos propios de su terreno, hasta quedar con **4 a 6 recursos** (§1.12.2). Los de base siguen exactamente en las mismas zonas.
  - Recolectar solo da lo que esa zona tiene. Una zona con un **nodo de recursos** da el doble de su recurso (§1.16).
- **Los recursos se agotan:** cada unidad recolectada baja un 2 % el recurso de esa zona, para todos los jugadores, y vuelve un 2 % por hora (`stock`). Si se recolecta mucho en un lugar, da menos; por debajo del 15 % no da nada hasta que se recupere. La pantalla muestra cuánto queda (▰▰▰▱▱).
- **Espacio en la mochila:** 60 unidades (`hero.backpack_capacity`). El cinturón y lo puesto no cuentan. Con la mochila llena, recolectar se detiene.
  - **Lo que encuentras nunca se pierde (D-90, provisional):** el botín, el equipo, la carne y los hallazgos de explorar entran aunque la mochila pase de 60 (se ve, por ejemplo, 63/60).
  - Con la mochila en 60 o más **no se recolecta ni se compra** en el mercader hasta vender o usar cosas: "🎒 Mochila llena (63/60): vende o usa cosas para volver a recolectar o comprar." No se gasta energía ni monedas.
- **El territorio vale:** al agrandar tu campamento eliges qué zona vecina toma, viendo los recursos que conoces de cada una. En tu territorio recolectas un 50 % más. El campamento cambia de nombre al crecer: campamento, aldea (nivel 3), pueblo (5), ciudad (7) y castillo (9).
- Lo pidió el dueño. Los números los propuso Claude.
- **Falta (P-74):** sembrar, comprar semillas a otros jugadores y hacer abonos para que una zona produzca más.

### 1.12.1 Tiempo estimado y ⚙️ Opciones de pelea en los lotes (D-114)

El dueño pidió (1-oct-2026):
- **Tiempo estimado (en el juego desde la 0.14.1):** cada cantidad de energía que se elige para un lote muestra cuánto tardará en total (hasta la 0.27 iba en el botón, "⚡ 20 · ⏱️ 3 h 20 min"; desde la 0.27.1, D-189, en una línea del texto: "⏱️ 5 → 50 min · 20 → 3 h 20 min..."), y la pantalla dice cuánto tarda cada vuelta y cuánto tardaría con toda la energía. Las peleas que salgan lo alargan un poco.
- **⚙️ Opciones (en el juego):** "Si te sale una pelea durante un lote, el jugador puede elegir antes: automática, o manual si el jugador está activo. Agrega un botón de opciones donde eliges qué pasa y qué no."
  - **Dónde:** **⚙️ Opciones** es el 5.º botón del menú de abajo (D-46 deja hasta 6; en Telegram quedan 3 filas: 2, 2 y 1) y también **/opciones**. Se puede abrir mientras exploras, recolectas o cazas (vale desde la próxima pelea); en combate no. La pantalla tiene un botón por opción, que la cambia, y ↩️ Volver: 4 botones.
  - **Palomitas (D-178, desde la 0.26.1):** los dos interruptores (⚔️ Peleas automáticas y 🧪 Pociones) muestran ✅ verde cuando están activos y ☑️ gris cuando están apagados ("✅ Peleas automáticas", "☑️ Pociones"). 🩹 Retirarse no es un interruptor: elige entre 30, 50 y 70 %.
  - **⚔️ Peleas en un lote:** **✋ Manual** (por defecto, como hasta ahora): el lote se corta y peleas tú; para el que está conectado. **⚔️ Automática:** el héroe pelea solo y, si gana, el lote sigue; para el que sale y vuelve después.
  - **🩹 Retirarse con menos de:** 30, 50 o 70 % de vida (por defecto 30 % desde la 0.22.1, D-119; antes 50 %; `auto_fight.retreat_choices`). Si al terminar una pelea automática la vida quedó por debajo, el lote se corta. Si una pelea sale cuando la vida ya está por debajo, el héroe no pelea solo: el lote se corta y la pelea te espera, como en manual.
  - **🧪 Pociones en peleas automáticas:** sí (por defecto) o no: si el héroe bebe las pociones y usa las vendas del cinturón.
  - Cada héroe empieza con ✋ Manual, 30 % y pociones sí (`auto_fight.defaults`), también los que ya existían; solo se guarda lo que cada uno cambia.
- **Cómo pelea solo** (`engine/combat/auto.py`): una forma de jugar básica pero atenta. Con menos de 45 % de vida usa su habilidad de curar; con menos de 35 % bebe una poción (primero la que más cura sin pasarse); con menos de 30 %, una venda. Si el aviso es un golpe grande (potencia mayor que 1,5), lo corta si puede y llega antes, si no lo esquiva, lo bloquea o se escuda, y contra uno de 2 o más sin respuesta usa 🌀 Esquivar. Si no, mantiene sus mejoras y los debilitamientos del enemigo, remata con 3 combos y pega. Los umbrales están en `auto_fight.policy`.
  - Es **la misma** forma de jugar que usa el simulador de balance (`tools/sim.py`): lo que dice el simulador es lo que hace un héroe que pelea solo. Al mudarla al motor, el simulador dio exactamente los mismos números.
  - **Pelear solo da lo mismo que pelear a mano:** las mismas reglas, el mismo sorteo y el mismo final (experiencia, monedas, botín, equipo, victorias del gremio, presas de la partida de caza, 🔪 Desollador; y al perder, malherido y un 10 % de las monedas). La diferencia es que el jugador atento juega mejor.
  - Una pelea que no termina en 60 rondas (`auto_fight.max_rounds`) se deja, sin premio ni castigo.
  - **Solo pelean solos** los encuentros comunes que salen en un lote (🔎 explorar, 🪓 recolectar) y las presas de 🏹 Cazar en lote. **Nunca** el Guardián, las defensas del campamento (🛡️ Defender, Noche de prueba) ni las emboscadas del viaje.
- **El resumen del final** dice, por ejemplo, "⚔️ 3 peleas automáticas: 3 ganadas", lo que dieron (experiencia y monedas), el botín, lo que subieron los oficios, las subidas de nivel y por qué terminó el lote. Con el chat cerrado pasa igual (el reloj del lote corre solo) y el bot escribe **una sola vez**, al final, aunque haya habido muchas peleas.
- **🏹 Cazar en lote:** con ⚔️ Automática, el botón 🏹 Buscar presa pasa a ser **🏹 Cazar en lote**: eliges la energía (⚡ 4, 10, 20, 40 o todo; `hunt.batch`), con el tiempo estimado en cada botón ("⚡ 10 · ⏱️ 1 h 20 min"). Cada presa cuesta 2 ⚡ (D-108) y tarda 16 minutos (`hunt.batch_minutes`, 8 min por ⚡, como recolectar). El lote se corta al perder, con la vida bajo el límite, sin energía o con ❌ Detener (devuelve los 2 ⚡ de la presa en curso). No empieza malherido ni con la vida ya bajo el límite. Cada presa cuenta para la partida de caza del campamento (D-106), y quien caza en lote cuenta como presente en su zona ("🏹 cazando", D-96). Con ✋ Manual se caza como antes: una presa a la vez, enseguida.
- **Cuántas peleas dura un lote** (medido con el motor, héroe de nivel 2 al lado del Claro, cinturón de inicio, la vida que vuelve sola en 4 horas, D-103): con el límite en 50 %, unas 4 o 5 peleas automáticas antes de que el lote se corte; con 30 %, casi todo el lote (~10 peleas al explorar 20 veces, ~16 de 20 presas), con menos de 1 % de derrotas; con 70 %, unas 2. Ver el registro de [Balance](../03-personaje/balance.md) §7.
- Lo pidió el dueño. Los números (30/50/70 %, 16 minutos por presa, 60 rondas, los umbrales de la forma de jugar) los propuso Claude; los umbrales son los que ya usaba el simulador.

### 1.12.2 El catálogo de cada terreno (D-180, D-183, en el juego desde la 0.27)

El dueño pidió (1-oct-2026): **cada tipo de terreno tiene un catálogo de 10 a 15 recursos posibles, y cada casilla trae solo una parte** (por ejemplo, 4 o 6 de los 15), en cantidades variables. **El color no garantiza un recurso**: ver verde no quiere decir que siempre haya madera o semillas; hay que ir a investigar (D-179). Cómo se aplicó (D-183, provisional, con la recomendación de E-123):

- **Los 6 de base no se mueven.** Siguen en las mismas zonas, con la misma riqueza (`zone_resources` da lo mismo que antes). Así nadie pierde lo que ya sabía de sus zonas.
- **Cada terreno suma los suyos** (`content/biomes.yaml` → `own`). Su catálogo son los de base que favorece (`gather`) más los propios: **10 u 11 por terreno** hoy (los de la 0.28, 10 u 11).
- **Cada zona suma 2 o 3 de los propios de su terreno** (`resources.terrain`), con su propio sorteo de la semilla y una riqueza de 0,3 a 1,0. Nunca pasa de 6 recursos de tierra ni queda con menos de 4 (con 1 de base suma 3). El 🐟 pescado de las zonas con agua va aparte, como antes. El Claro no suma nada.
- **Pueden repetirse entre terrenos** (hay setas en el bosque y en el pantano).
- **Bastante al azar (D-185):** cada propio que trae una zona tiene **3 de 10** (`resources.terrain.foreign_chance`) de salir del catálogo de **otro** terreno: puede haber resina en el desierto o sal en el bosque. Y los 6 de base siguen sus regiones de siempre, que no dependen del terreno que se ve (desde la 0.26.2, §1.2): el color nunca garantiza un recurso.

| Terreno | De base que favorece | Propios |
|---|---|---|
| 🟩 Pradera | fibra, hierba, piedra | 🫐 bayas, 🍯 miel silvestre, 🌽 mazorca silvestre, 🌼 lino, 🍃 tomillo, 🍄 setas, 🥕 raíz amarga |
| 🟢 Bosque | madera, hierba, fibra | 💧 resina, 🍂 corteza, 🍄 setas, 🫐 bayas, 🍯 miel, 🌱 musgo, 🥕 raíz amarga |
| 🟫 Colinas | piedra, madera, metal | 🌑 carbón, 🧂 sal de roca, 🔹 cuarzo, 🍃 tomillo, 🌽 mazorca, 🍂 corteza, 🫐 bayas |
| 🟪 Pantano | hierba, fibra | 🎋 juncos, 🪷 nenúfar, 🍄 setas, 🌱 musgo, 🥕 raíz amarga, 🌼 lino, 💧 resina, 🍂 corteza |
| ⬜ Montaña | piedra, metal | 🌑 carbón, 🔹 cuarzo, 🧂 sal, 🧊 hielo eterno, 💮 flor de escarcha, 🌱 musgo, 🍃 tomillo, 💧 resina |
| 🟨 Desierto | piedra, metal, fibra | ⏳ arena fina, 🧂 sal, 🌵 pulpa de cactus, 🌴 dátiles, 🔹 cuarzo, 🍃 tomillo, 🔧 chatarra |
| 🟦 Tundra | piedra, madera, metal | 🧊 hielo, 💮 flor de escarcha, 🌱 musgo, 🫐 bayas, 💧 resina, 🍂 corteza, 🌑 carbón |
| ⬛ Ruinas | metal, piedra | 🔧 chatarra, 🔹 cuarzo, 🌑 carbón, 🍄 setas, 🌱 musgo, ⏳ arena, 🍂 corteza, 🥕 raíz amarga |
| 🟣 Selva (0.28) | madera, hierba, fibra | 🌴 dátiles, 🫐 bayas, 🍯 miel, 🍄 setas, 💧 resina, 🍂 corteza, 🌱 musgo, 🥕 raíz amarga |
| 🟧 Sabana (0.28) | fibra, madera, piedra | 🌽 mazorca, 🌼 lino, 🍯 miel, 🍃 tomillo, 🫐 bayas, 🌴 dátiles, 💧 resina, 🌵 cactus |
| 🟥 Volcán (0.28) | piedra, metal | 🖤 obsidiana (nueva, solo aquí), 🌑 carbón, 🧂 sal, 🔹 cuarzo, ⏳ arena, 🌱 musgo, 🍃 tomillo, 💧 resina |
| 🟤 Cañón (0.28) | piedra, metal, arcilla | ⏳ arena, 🧂 sal, 🔹 cuarzo, 🍃 tomillo, 🌵 cactus, 🌑 carbón, 🔧 chatarra, 🫐 bayas |
| ⚫ Bosque oscuro (0.28) | madera, hierba, fibra | 🍄 setas, 🌱 musgo, 🥕 raíz amarga, 🍂 corteza, 💧 resina, 🫐 bayas, 🍯 miel, 🌑 carbón |
| 🔵 Lago (0.28) | fibra, hierba, arcilla | 🎋 juncos, 🪷 nenúfar, 🌼 lino, 🌱 musgo, ⏳ arena, 🍄 setas, 🫐 bayas, 🥕 raíz amarga |

- **Los terrenos de la 0.28 (D-188):** reusan los 21 recursos de la 0.27 y suman uno solo, la **🖤 obsidiana** del 🌋 volcán (⛏️ Minero, 5 🥉 en el mercader): la 🗿 Cantería hace un sillar con 1 piedra y 1 obsidiana en vez de 3 piedras. El raro de sus nodos (`node_rare`): 💠 gema en bruto en el volcán y el cañón; 🌸 flor de luna en los demás. Los de base que favorecen (`gather`) solo cuentan para su catálogo: en esas zonas los de base siguen al bioma clásico, como en todas.

- **Para qué sirven (capa ligera, D-44):** cada uno tiene al menos una receta y se vende al mercader (💱 Vender todo los vende, como la madera). Son otra forma de hacer lo de siempre: la 🧶 Tejeduría hace tela con 🌼 lino o 🎋 juncos; la 🔥 Fundición, lingotes con 🌑 carbón (3 piezas dan 2) o 🔧 chatarra; la 🪣 Curtiduría, 2 cueros con 3 pieles y 🍂 corteza; la 💧 Destilación, extracto con 🥕 raíz amarga; la 🗿 Cantería, sillares con ⏳ arena y menos piedra; la ⚗️ Alquimia, pociones con ⏳ arena o 💧 resina en vez de arcilla, y pociones mayores con 🪷 nenúfar o 💮 flor de escarcha en vez de la 🌸 flor de luna; la 🩺 Medicina, ungüentos con 🌱 musgo o 🌵 cactus y botiquines con 🍯 miel; la 🍲 Cocina, raciones con 🍄 setas o 🫐 bayas, pescado asado con 🧂 sal o 🌽 mazorca, guisos con 🍃 tomillo o 🌴 dátiles, conservas con 🧊 hielo y sal, y festines con 🍯 miel y bayas. El detalle está en [Red de oficios](../07-economia/red-de-oficios.md) §5.1.
- **Quién los junta:** lo leñoso (💧 resina, 🍂 corteza), el 🪓 Leñador; lo mineral (🌑 🧂 🔹 ⏳ 🧊 🔧 y, desde la 0.28, 🖤), el ⛏️ Minero; las plantas, los hongos y la miel, el 🌿 Herbolario. Su beneficio, su unidad de más y su raro valen también para estos.
- **Balance:** cada vuelta de recolección saca las mismas unidades que antes (se reparten entre más recursos: no se multiplican), y los precios quedan cerca de los de base (2 a 5 🥉), así recolectar rinde lo mismo en monedas.
- **Lo que queda abierto:** si el dueño prefería que los recursos de cada terreno fueran variedades del material de siempre (roble, pino, granito...) que cuentan como madera o piedra (E-123, la otra opción).

### 1.13 Otros jugadores en tu zona (D-96, provisional)

**Lo que pidió el dueño (por voz):** "Si un jugador coincide contigo en la zona, no en el mapa, sino que al darle a Zona vas a poder ver la lista de jugadores en esa zona, en cuanto a la actividad. Puede que te lo topes incluso en las misiones y demás." Interpretación tomada (provisional): se ven solo los que están **ahora** en tu zona y **activos**, cada uno con lo que está haciendo; el mapa no muestra a nadie.

- **Dónde se ve:** en **📍 Zona**, debajo de los recursos, un bloque 👥 con una línea por jugador: nombre (con su estandarte, si compró uno), clase, nivel y qué hace. Si no hay nadie, no aparece nada (pantallas cortas, D-86). Si estás explorando, recolectando o durmiendo, 📍 Zona te muestra la pantalla de tu actividad, y ahí sale el mismo bloque. No agrega botones.
- **Quién cuenta como presente:** su héroe está en esa zona **y**:
  - tocó un botón en los últimos **15 minutos** (`presence.minutes`), **o**
  - está explorando, recolectando o durmiendo ahí, aunque tenga el chat cerrado (un lote de exploración puede durar horas).
  - Nunca te ves a ti mismo.
  - Quien se fue, ya no existe o lleva más de 15 minutos sin jugar (y no está ocupado ahí) sale de la lista, y vuelve con su próximo botón.
- **Qué está haciendo:** 🔎 explorando · 🪓 recolectando · ⚔️ peleando · 🛌 descansando · 🚶 de paso (salió de viaje desde aquí) · 🧍 por aquí (sin actividad).
- **Tope:** se muestran **5** nombres (`presence.max_listed`), primero el que jugó hace menos; el resto sale como "… y N más".
- **Cruzarse al explorar:** en cada vuelta de 🔎 exploración o 🪓 recolección que no termina en pelea, con probabilidad **15 %** (`presence.cross_chance`), si hay alguien presente en la zona, el resumen del lote dice "👋 Te cruzaste con Bram (🏰 Guerrero, nivel 2), que andaba 🪓 recolectando." A cada jugador te lo cruzas una sola vez por lote.
  - Es **solo texto**: sin premio, sin pelea, sin PvP. Vale en cualquier zona, también en el Claro y en los campamentos.
  - Usa su propio sorteo fijo (semilla del mundo, héroe y hora de la vuelta), así que no cambia ningún otro resultado de la vuelta (hallazgos, monedas, porcentaje explorado).
- **Cómo se sabe quién está, sin revisar a todos los héroes:** el espacio `presence` guarda, por zona, a quién se anotó ahí. Se escribe al tocar un botón (solo si faltabas) y al llegar a una zona (sales de la que dejas y entras en la nueva, aunque tengas el chat cerrado). Al leer se poda: se vuelve a mirar la ficha de cada anotado y se quita a quien ya no está.
- **Lo que falta (propuesta):** que el otro también reciba el aviso del cruce; un botón para saludar o invitar a un grupo cuando existan los grupos ([Gremios y vida social](../08-social/gremios-y-social.md) §3); cruzarse en las misiones cuando existan ([Misiones y exploración](../06-contenido/misiones-y-exploracion.md)).
- Lo pidió el dueño. Los números (15 minutos, 5 nombres, 15 %) y las etiquetas los propuso Claude.

**De dónde sale.** Las listas de "quién está en esta sala" de los MUD de texto (el comando `who` y la línea "Aquí también están…"), los jugadores que se ven pasar en las zonas de WoW y los fantasmas de otros jugadores de *Dark Souls* y *Journey*, que dan compañía sin mecánica.

### 1.14 El Explorador y los campamentos enemigos (D-112, en el juego)

El dueño pidió (1-oct-2026) que **explorar sea como una especialización o una profesión**, y que haya **zonas que no se dejan explorar** porque hay enemigos acampados. Esta es la capa simple, **ya en el juego**. Los números son propuesta de Claude (se ajustan en la beta) y viven en `content/balance.yaml` → `explorer` y `enemy_camps`; el oficio, en `content/professions.yaml`; las cuentas de los campamentos, en `engine/world/enemy_camps.py`; las pantallas, en `engine/service/game.py` (sección "enemy camps and the 🧭 Explorador"); los textos, en `content/locales/es_exploracion.yaml`. Pruebas: `tests/test_enemy_camps.py`.

**🧭 El oficio de Explorador** (con los oficios de D-109, rango 1 a 100; en ⚒️ Oficios sale en su propia rama, 🧭 Exploración):
- **Sube explorando:** cada vuelta de exploración da **5** de experiencia de Explorador, y **6** más al dejar una zona al 100 % (también las de alrededor, D-107). Son unos 6 por ⚡, como refinar: rango 10 en ~3 días de toda la energía, 25 en ~3 semanas, 50 en ~3 meses y 100 en ~1 año dedicado (la curva es la de todos los oficios, 9 × (R − 1)²). El resumen del lote lo dice ("⚒️ Oficios: 🧭 Explorador +40") y avisa cada umbral nuevo.
- **Los más avanzados ven más en el mapa.** Lo que se abre con el rango (⚒️ Oficios muestra la lista, con ✅ en lo que ya tienes, y el próximo umbral):

| Rango | Qué ves de más |
|---|---|
| 1 | Lo de siempre: tus zonas, su porcentaje y su color, y los 👹 campamentos de tu zona y de las 8 vecinas |
| 10 | ⏱️ 📒 Lugares lista hasta **8** lugares con su tiempo (sin rango, 3; los botones siguen siendo 3), y el 🗺️ Mapa dice cuánto tardas a cada campamento que ve, a la guarida del Guardián y a tu campamento. **🔭 Reconocer** de lejos a **1** zona (D-172, abajo) |
| 25 | Los 👹 campamentos enemigos hasta **3** zonas a la redonda (7 × 7), aunque no las hayas pisado |
| 30 | **🕵️ Infiltrarse** en un campamento enemigo. 🔭 Reconocer hasta **2** zonas |
| 50 | Los campamentos enemigos de todo tu mapa (13 × 13). 🔭 Reconocer hasta **3** zonas |
| 75 | 👹 La fuerza de cada campamento desde el mapa y en su zona: cuántos enemigos quedan, de qué nivel, su jefe y su cofre |
| 100 | 🏅 Título «Gran Explorador» (para siempre, en la ficha y el 📔 Diario) |

- **Su beneficio** (como todo oficio, D-111): **+1 punto de exploración por vuelta cada 20 rangos**, hasta **+5** al rango 100 (`perk: {explore: 5}`; se usa la parte entera, sin otro sorteo), y el **🥷 Sigilo** de D-172 (abajo): hasta **25 %** de evitar una pelea al azar (`perk: {stealth: 0.25}`).

**👹 Campamentos enemigos:**
- **Dónde y cuándo:** cada día real (el mismo corte de día que la despensa y el 📜 Tablón) unas **3 %** de las zonas de **Lejanía 2 o más** tienen uno: en un mapa de 13 × 13, unos 4 o 5. El lugar sale solo de la semilla del mundo, el día y las coordenadas: **todos los jugadores ven los mismos** y no hay un reloj que los mueva. Nunca salen en el Claro, en la guarida del Guardián ni en el territorio de un campamento de jugadores, y **nunca dos días seguidos en la misma zona**: al otro día aparecen en otro lado.
- **Mientras está en pie, su zona no se explora ni se recolecta.** 🔎 Explorar y 🪓 Recolectar se rechazan con un aviso y **sin gastar energía**; explorar alrededor (D-107) se salta esa zona. Si un lote cruza la medianoche y aparece un campamento donde estás, se corta y devuelve la energía de la vuelta. Al llegar a la zona lo dice ("👹 ¡Un campamento enemigo!"), 📍 Zona lo muestra y las rutas vecinas llevan 👹. 🏹 Cazar sigue abierto (sus presas son las comunes de la zona).
- **🧭 Explorar en esa zona:** el menú cambia a **⚔️ Asaltar · ⚡2**, **🕵️ Infiltrarse · ⚡3** (o "🕵️ Infiltrarse (rango 30)"), **🏹 Cazar** y **🗺️ Mapa**: 4 botones. Dice cuántos vencieron hoy entre todos y, si te infiltraste o eres Explorador de rango 75, quiénes quedan, el jefe y el cofre.
- **La guarnición:** de **4 a 8** enemigos (contando al jefe), del bioma de la zona y del **nivel de la zona + 1**. El último es el **jefe**: el más fuerte de los que salen ahí, en versión élite (**+80 % de vida y +20 % de ataque**, solo en esa pelea).
- **⚔️ Asaltar:** cada pelea cuesta **2 ⚡** (como una presa, D-108) y es contra el siguiente de la guarnición. **Cada victoria vence a uno, para todos** (se guarda por día y zona en el almacén): varios jugadores lo bajan juntos el mismo día. El jefe solo cae en su propia pelea, aunque dos peleen a la vez. Ganar o perder te anota como alguien que peleó ahí (huir no). Tras ganar sale **⚔️ Seguir asaltando**. Malherido o sin energía, no se puede (aviso, nada se cobra). **Nunca es automática** (D-114): ni en un lote ni con ⚔️ Peleas automáticas.
- **Cuando cae el jefe:** el campamento queda destruido hasta el día siguiente (la zona vuelve a explorarse y 📍 Zona dice quién lo terminó). **Quien lo termina** se lleva el cofre: **nivel × 25 🥉**, **3 a 5** materiales de la zona, **60 × (1 + 0,15 × (nivel − 1))** de experiencia y **50 %** de una pieza de equipo del nivel del campamento (el sorteo de botín de siempre). **Cada otro que peleó ahí ese día** gana **nivel × 8 🥉** y **30 × (1 + 0,15 × (nivel − 1))** de experiencia, aunque no esté jugando, con un aviso. Se paga **una sola vez**: el que termina una pelea después ve "ya había caído" (lo que ganó en su pelea es suyo). Queda en el 📔 Diario.
- **🕵️ Infiltrarse (Exploradores de rango 30 o más):** cuesta **3 ⚡** y no es una pelea. Te descubren con **45 %** al rango 30, 0,5 puntos menos por rango (**10 %** al 100, nunca menos de 5 %): entonces empieza una pelea, a mano, con el siguiente de la guarnición (cuenta como un asalto). Si sale bien ves cuántos quedan y quiénes, el jefe y lo que guarda el cofre (es justo lo que se gana), ganas **+10 %** de exploración de esa zona (la única forma de explorarla mientras siga en pie) y **15** de experiencia de Explorador, y ese día ves su fuerza en 🧭 Explorar y en el mapa. Una vez por campamento y día.
- **🗺️ Mapa:** 👹 marca los campamentos que ves; debajo, los más cercanos (hasta 4) con su distancia, su tiempo desde el rango 10 y su fuerza desde el 75, y hasta dónde ves. El botón **👹 Ir al más cercano** te lleva zona por zona, como 📒 Lugares (3 botones en el mapa).
- **Cuánto da** (registro de [Balance](../03-personaje/balance.md) §7): una pelea del asalto da ~10 % más experiencia por ⚡ que cazar en la misma zona (~22 contra ~20 con un lobo en una zona de nivel 3, D-108), porque es del nivel + 1; un campamento entero en solitario (6 peleas y el cofre) da ~29 por ⚡, y ~22 contando el viaje para llegar. El jefe se gana 85-97 % de las veces con el equipo y los puntos de su nivel (37 % al nivel 3 sin nada); los guardias, ~100 %, dejando ~65 % de vida.
- **Para qué sirve:** le da trabajo a cada uno. El Explorador encuentra y estudia los campamentos, los que pelean los destruyen, y todos ganan botín. Y cambia el mapa cada día.
- **Lo que queda abierto:** si un Explorador veterano debería empezar con experiencia por lo que ya exploró antes de este parche (hoy todos empiezan en rango 1); si fundar o agrandar un campamento de jugadores sobre un campamento enemigo en pie debería esperar a destruirlo (hoy el territorio nuevo lo hace desaparecer); si el jefe debería pedir grupo en los anillos lejanos.

#### 🔭 Reconocer y 🥷 Sigilo (D-172, en el juego)

El dueño pidió (1-oct-2026) que **el Explorador aprenda sigilo y reconocimiento**: saber qué hay en un lugar **antes de llegar**, con experiencia y recompensas propias. Esta es la capa simple (D-44), **ya en el juego**. Los números son propuesta de Claude (se ajustan en la beta) y viven en `content/balance.yaml` → `recon` y `explorer` (`ranks.recon`, `recon_far`, `recon_wide` y `stealth_max`); el sigilo, en `content/professions.yaml` (el `perk` del explorador y la 🎓 🕵️ Infiltrado); las pantallas, en `engine/service/game.py` (sección "reconnaissance and stealth"); los textos, en `content/locales/es_reconocimiento.yaml`. Pruebas: `tests/test_reconocimiento.py`.

**🔭 Reconocer de lejos** (desde el rango **10** del 🧭 Explorador):
- **Qué se puede reconocer:** las entradas de mazmorra que marca tu 🗺️ Mapa (🕳️ o 🌀, §1.15) y los 👹 campamentos enemigos en pie que ves, a **1 zona** a la redonda en el rango 10, **2** en el 30 y **3** en el 50 (el cuadrado alrededor, como la vista de los campamentos). Nunca tu propia zona: ahí se entra, se asalta o se 🕵️ infiltra. Si un campamento tapa una entrada, la zona cuenta como campamento.
- **Dónde está:** el atajo **/reconocer** (en Telegram se toca en el texto). El 🗺️ Mapa dice cuántos lugares puedes reconocer hoy y suma el botón **🔭 Reconocer** cuando cabe (4 botones como mucho); 🧭 Explorar dice "🔭 N lugares para reconocer de lejos: /reconocer" cuando hay alguno (sus 4 lugares ya están tomados). La pantalla lista hasta **6** lugares a tu alcance, con ✅ y lo que hay hoy en los que ya reconociste, y ofrece los 3 más cercanos sin reconocer como botones (más ↩️ Volver).
- **Cuánto cuesta y qué da:** **2 ⚡** cada uno. Da **12** de experiencia de Explorador (6 por ⚡, como explorar), **6** de experiencia de héroe (como 2 vueltas de explorar) y **nivel del lugar × 2 🥉** (nivel 4: 8 🥉; nivel 40: 80 🥉, parecido a lo que dan 2 ⚡ de explorar en monedas). Sin objeto que se venda: si la información debería ser un 📜 informe que se vende queda para cuando se decida P-120.
- **Una vez por lugar y día.** No es una pelea, no te mueve y se puede hacer en medio de un lote (no en combate). Antes del rango 10, fuera de alcance, ya reconocido hoy o sin energía, se rechaza sin cobrar.
- **Qué muestra** (lo mismo que vería cualquiera ese día: sale de la semilla del mundo y del registro compartido del campamento):
  - De una **mazmorra:** si es 🕳️ chica o 🌀 profunda, su nivel, **la familia de hoy** y **su jefe**; de la chica, también su cofre de hoy; de la profunda, **el récord de hoy** (🏆 el más hondo del día, para superarlo) y el tuyo.
  - De un **campamento enemigo:** su nivel, el tamaño de la guarnición, **cuántos quedan y quiénes** y **su jefe**. **No el cofre**: eso sigue siendo de 🕵️ Infiltrarse, que además da exploración de la zona. Reconocer no gasta la infiltración del día. Si tapa una entrada de mazmorra, lo dice.
- **Lo que queda para el día:** en el 🗺️ Mapa, una mazmorra reconocida se sabe 🕳️ chica o 🌀 profunda (para siempre: la entrada nunca se mueve) y, ese día, su línea dice "🔭 hoy 🐺 Manada"; un campamento reconocido muestra su fuerza (👹 quedan · nivel · jefe) como al rango 75. En 📍 Zona, la ruta hacia una mazmorra vecina reconocida lleva su marca y la familia ("🌀🦅"). Al otro día, todo se puede reconocer de nuevo.
- **Cuánto hay para reconocer:** con la semilla de prueba, desde una zona cualquiera de Lejanía 3 a 8 hay en promedio **0,5** lugares a 1 zona, **1,7** a 2 y **3,2** a 3 (contando todas las entradas y campamentos, antes de ver si están en tu mapa). Es un rato del día, no un camino entero: unos 2 a 8 ⚡.

**🥷 Sigilo** (pasivo, crece con el rango):
- **Qué hace:** cuando sale una **pelea al azar**, puedes pasar sin que te vean. La probabilidad sube **pareja con el rango**: **0,25 % por rango**, **25 %** al rango 100 (12,5 % al 50). La 🎓 especialización **🕵️ Infiltrado** suma hasta **10 puntos** más con todo el dominio (35 %), y nunca pasa de **50 %** (`explorer.stealth_max`). Usa su propio sorteo: no cambia nada más de la vuelta ni del viaje.
- **Dónde vale:** en la pelea al azar de **🔎 explorar con ✋ Manual** (la vuelta sigue sin hallazgo ni monedas, y el resumen del lote dice "🥷 Sigilo: N peleas evitadas") y en la **emboscada al llegar de un viaje** (el viaje sigue y una línea lo dice; la emboscada es siempre a mano, así que vale con cualquier opción).
- **Dónde no vale nunca:** con **⚔️ Automática** (elegiste pelear: el lote pelea todas), en **🏹 Cazar** y la caza en lote (es una pelea que eliges), al **🪓 recolectar**, al **⚔️ Asaltar** un campamento, en las **mazmorras**, en las **oleadas** del campamento ni contra el **Guardián**.
- **Dónde se ve:** en ⚒️ Oficios, en la línea del beneficio del Explorador ("🥷 12,5 % de evitar peleas al azar..."), y en ⚙️ Opciones, que recuerda que con ⚔️ Automática no se usa.
- **Lo que queda abierto:** si recolectar con ✋ Manual también debería usar el sigilo; si el sigilo debería poder apagarse (hoy, quien quiere pelear usa ⚔️ Automática o 🏹 Cazar); si el informe de reconocimiento debería ser un objeto que se vende (P-120).

### 1.15 Las entradas de mazmorra en el mapa: hay algo, no se sabe qué (D-171, en el juego)

El dueño pidió (1-oct-2026) que **el mapa muestre que hay algo, no qué es**: en cada tramo, 1 o 2 mazmorras que no se sabe qué son hasta ir a investigar. Esta es la parte de las **mazmorras para uno** ([Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) §0, D-164 y D-170); los nodos de oficio de D-171 vienen después. Números en `content/balance.yaml` → `dungeons`; cuentas en `engine/world/dungeons.py`; pantallas en `engine/service/game.py` (sección "solo dungeons"). Pruebas: `tests/test_mazmorras.py`.

- **Dónde:** el mapa se parte en **tramos de 6 × 6 zonas**, y cada tramo tiene **2 entradas, o 3 con 50 %** (D-181, desde la 0.26.1; antes 1 o 2: las que había no se movieron, solo se sumaron), desde **Lejanía 2**, nunca pegadas dentro del tramo; **1 de cada 4 es 🌀 profunda**, las demás 🕳️ chicas. Sale solo de la semilla del mundo y las coordenadas: **nunca se mueven** y son las mismas para todos (lo que cambia cada día es lo de adentro). Nunca en el Claro ni en la guarida; el **territorio de un campamento de jugadores** la tapa mientras exista, y un **👹 campamento enemigo** en pie sobre su zona tapa la entrada ese día.
- **🕳️ Una cueva:** el 🗺️ Mapa marca con la **🕳️ cueva** (D-181; hasta la 0.26 era ❓) una entrada si anduviste cerca: si recuerdas (pisaste o estudiaste) alguna zona a **2 zonas o menos** de ella (`dungeons.hint_radius`). Sabes que ahí hay una mazmorra, no cuál.
- **🕳️ / 🌀 Ya sabes qué es:** al **pisar su zona**, o al **estudiarla desde la de al lado** (explorar alrededor, D-107: la zona queda en tu memoria), sabes si es 🕳️ chica (la cueva sigue igual en el cuadrito y la línea de abajo lo dice) o 🌀 profunda (el cuadrito pasa a 🌀). Al llegar a su zona sale el aviso "🕳️ ¡La entrada de una mazmorra chica!" y 📍 Zona dice qué familia de enemigos la ocupa hoy.
- **Debajo del mapa:** las **3 más cercanas** que ves ("🕳️ (3, -5) · a 4 zonas: una cueva, ve a ver qué mazmorra es"; "🌀 (-1, -5) · a 2 zonas: mazmorra profunda"), con el tiempo de viaje desde el rango 10 del 🧭 Explorador. El botón **🕳️ Ir a la cueva** (o **🕳️ / 🌀 Ir a la mazmorra**) te lleva a la más cercana zona por zona, como 📒 Lugares; con el de 👹 son 4 botones como mucho.
- **En el cuadrito**, la marca de la mazmorra va debajo de 🧍 tú, 👑 la guarida, 👹 un campamento enemigo y 🏕️ un campamento de jugadores, y encima del color o el bioma.
- **En la zona:** 🧭 Explorar cambia 🏹 Cazar por **🕳️ Entrar** o **🌀 Descender** (siguen 4 botones); 🏹 Cazar queda dentro de la pantalla de la mazmorra.
- **🔭 Reconocer (D-172):** desde el rango 10 del 🧭 Explorador, una entrada cercana se puede reconocer de lejos: sabes para siempre si es 🕳️ chica o 🌀 profunda y, ese día, se ve su familia (§1.14, "🔭 Reconocer y 🥷 Sigilo").
- **Lo que queda abierto:** si "2 o 3 por zona" era por tramo (como quedó) o en todo el mapa (P-125 / E-126). Los nodos de recursos de D-181 llevan su propio símbolo genérico, ✨ (0.27, §1.16).

### 1.16 Nodos de recursos: un símbolo genérico que se descubre al llegar (D-171, D-181, D-184, en el juego desde la 0.27)

El dueño pidió (1-oct-2026): **los nodos de recursos se colocan al azar con un símbolo genérico, y solo al llegar se descubre qué tipo de nodo principal es** (D-181); en cada tramo se ven 2 o 3 iconos de nodos (D-171). Cómo se aplicó (D-184, provisional, con la recomendación de E-124). Números en `content/balance.yaml` → `nodes`; cuentas en `engine/world/nodes.py`; pantallas en `engine/service/game.py` (sección "resource nodes"). Pruebas: `tests/test_nodos_y_terrenos.py`.

- **Un nodo es parte de una zona.** El mapa se parte en **tramos de 6 × 6 zonas** (como las mazmorras) y cada tramo tiene **2 o 3 nodos** (`nodes.count`), desde **Lejanía 1**. Salen solo de la semilla del mundo: **nunca se mueven** y son los mismos para todos. Nunca en el Claro (ni en todo el territorio que podría tener), en la guarida del Guardián ni en la entrada de una mazmorra, y **nunca pegados** (tampoco entre tramos vecinos). **Sí pueden caer dentro del territorio de un campamento de jugadores**: al agrandar tu campamento puedes elegir zonas con buenos nodos (D-87); ⬆️ Agrandar campamento marca " ✨🪵" en las zonas cuyo nodo ya descubriste.
- **Su recurso principal** es uno de los recursos de tierra de su zona: 6 de cada 10, uno propio del terreno (`nodes.own_share`); los demás, el más fuerte de la zona. Nunca el 🐟 pescado.
- **Qué da (E-124):** su recurso **rinde el doble** en esa zona (cada unidad que recolectas vale 2, `nodes.yield_mult`), **se agota la mitad de rápido** (`nodes.stock_mult`) y **cada vuelta de recolección ahí tiene 5 % de dar un material raro de su terreno** (`nodes.rare_chance`; 💠 gema en bruto o 🌸 flor de luna según el terreno, `node_rare` en `content/biomes.yaml`). Las unidades de más y el raro usan su propio sorteo: la vuelta saca lo mismo que sin nodo. Lo usa **cualquiera que llegue**. Los nodos que mejora el carpintero (E-96, D-168) y los especiales de los expertos (E-78, D-160) vienen después.
- **✨ En el mapa:** un nodo que no descubriste se ve con el símbolo genérico **✨** (`node.icon_unknown`) si recuerdas alguna zona a **2 o menos** de él (`nodes.hint_radius`), como las cuevas. En el cuadrito va debajo de 🧍 tú, 👑 la guarida, 👹 un campamento enemigo, 🏕️ un campamento de jugadores y las mazmorras, y encima del color del terreno. Debajo del mapa, los **2 más cercanos** ("✨ (-2, 0) · a 2 zonas: un nodo de recursos, llega para saber de qué es"). No hay botón nuevo: siguen 4 como mucho.
- **Solo al llegar:** al **llegar a su zona** (al final de un tramo de viaje, o si ya estás parado ahí, por ejemplo cuando llegó el parche) lo descubres **para siempre** (se guarda por héroe en el espacio `nodes` del almacén). Sale el aviso "✨ ¡Encontraste un nodo de recursos! Es de 🪵 Madera: aquí su recurso rinde ×2 al recolectar y se agota más despacio, y a veces da 🌸 Flor de luna", 📍 Zona lo dice en una línea y el mapa muestra el emoji de su recurso (🪵) en lugar de ✨. **Explorar alrededor desde la zona de al lado (D-107) no lo descubre**, ni el 🔭 Reconocer del Explorador (E-125 sigue abierta).
- **Al recolectar:** el resumen de 🪓 Recolectar dice lo que dio el nodo ("✨ El nodo de 🪵 Madera te dio +4 de más."; "✨ En el nodo encontraste 🌸 Flor de luna ×1.").
- **Lo que queda abierto:** si el 🔭 Reconocer del Explorador debería descubrir los nodos de lejos desde el rango 25 (E-125); los nodos que sube de nivel el 🪑 carpintero (E-96) y los especiales de los expertos (E-78).

## 2. Lo que viene por parches (propuesta)

Cada parche abre una pieza cuando está lista (D-60). Todas siguen "amplio pero ligero" (D-44): la **capa simple** es la que ve cualquiera; la **capa profunda** es opcional. Ninguna agrega teletransporte (D-58).

| Orden | Parche | Capa simple | Capa profunda (opcional) |
|---|---|---|---|
| 1 | **Lugares dentro de la zona** | Explorar revela de 3 a 8 lugares (ruina, mina, lago, campamento, cueva). Moverse entre lugares de una zona tarda 1-3 min | Lugares ocultos que solo salen con pista, rumor o habilidad |
| 2 | **Carga y heridas** | Llevar más del peso cómodo suma tiempo al viaje (+25 %, +50 %). Una pierna herida, también | Peso por objeto, mulas y mochilas grandes; secuelas que frenan siempre (D-51, ver [Heridas](../05-salud/heridas.md)) |
| 3 | **Eventos del camino** | A veces, a mitad de viaje, llega un aviso con plazo ("Un viajero pide ayuda. Tienes 10 min"). Si no respondes, sigue el viaje sin premio ni castigo | Cadenas de eventos y eventos que dependen del clima, la estación y la ecología |
| 4 | **Regiones con Guardián y la Frontera** | Manchas de zonas del mismo bioma forman una región con su Guardián (jefe de mundo, D-08). La Frontera avanza región por región, en cuatro fases (2.1) | Grandes Barreras en ciertos anillos, que piden un Guardián mayor y una obra común |
| 5 | **Pioneros** | El primer grupo que vence a un Guardián recibe título y cosmético únicos ("Pionero de la región X"). Sin poder | Crédito por facción y por castillo; placa en el asentamiento |
| 6 | **Nombres del descubridor** | Quien descubre una zona puede ponerle nombre una vez (filtro y moderación). Si no lo hace, queda el generado | Los lugares también se nombran; el castillo dueño puede renombrar su región |
| 7 | **Caminos** | Los jugadores construyen un camino entre dos zonas vecinas: el viaje por ahí tarda la mitad | Los caminos se gastan y piden mantenimiento; puentes y pasos de montaña; peajes del dueño |
| 8 | **Monturas y postas** | Una montura baja el tiempo un 30 %. Las postas (construidas por jugadores) dejan cambiar de montura y descansar | Cría, doma y fabricación (ver [Profesiones](../07-economia/profesiones.md)); monturas de carga; barcos por ríos y costas |
| 9 | **Cartografía y mapas como objeto** | Un Cartógrafo dibuja un mapa de un área; quien lo lee conoce los lugares y las rutas sin haber ido | Mapas con errores, mapas del tesoro, mapas de vetas que se venden (ver [Mundo vivo](mundo-vivo-y-viaje.md) §6) |
| 10 | **Viento de Cola y Techo de la Frontera** | Las regiones muy por detrás de la Frontera dan más experiencia. La experiencia baja cuando tu nivel supera por mucho al de la Frontera | Ajustes finos por anillo y por cantidad de jugadores activos |
| 11 | **Asentamientos** | Al pacificar una región se puede fundar un asentamiento en uno de sus lugares (ver [Fundación y cisma](fundacion-y-cisma.md) y [El Colapso y las comunidades](el-colapso-y-las-comunidades.md)) | Capitales regionales, mercados locales y rutas de caravana entre ellos |

**Por qué este orden.** Los lugares (1) llenan cada zona antes de agrandar el mapa. Carga y eventos (2-3) le dan peso al viaje que ya existe. La Frontera (4-5) da la meta común del servidor. Caminos y monturas (7-8) llegan cuando ya hay algo que conectar: si llegaran antes, solo acortarían un mapa vacío.

### 2.1 La Frontera y sus cuatro fases

La **Frontera** es hasta dónde llega el mundo explorado y pacificado del servidor. Cada región nueva pasa por las cuatro fases que tenía un piso de la Torre:

| Fase | Qué pasa | Cuándo termina |
|---|---|---|
| 1. Descubrimiento | Los jugadores pisan las zonas de la región | Cuando se descubre un porcentaje de sus zonas y aparece la guarida del Guardián |
| 2. Esfuerzo de guerra | Todos donan materiales y oro a un campamento, con metas visibles | Al completar las metas |
| 3. Asalto | El Guardián se abre como jefe de mundo (D-08) | Cuando cae. El primer grupo es Pionero |
| 4. Asentamiento | La región queda pacificada: menos peligro al llegar, se puede fundar. El Guardián queda como **Eco** para los que llegan tarde | Permanente |

### 2.2 Cómo evitar el mundo vacío

Un mapa infinito vacío es el riesgo más grande de este diseño (la lección de No Man's Sky). Reglas:

- **Densidad antes que tamaño:** lugares, eventos y rastros dentro de cada zona antes de abrir más tipos de bioma.
- **Huellas de otros jugadores:** la zona muestra quién la descubrió, quién pasó hace poco, caminos, tumbas y carteles. El mundo cuenta lo que hizo la gente. Ya funciona: quién la descubrió (§1.4) y **quién está ahora** (§1.13, D-96 provisional).
- **Razones para volver atrás:** vetas que se mueven, ecología y estaciones (ver [Mundo vivo](mundo-vivo-y-viaje.md)) hacen que una zona vieja cambie.
- **La gente se junta en la Frontera:** las metas comunes (2.1) están en un solo lugar a la vez, no repartidas por un mapa sin fin.
- **Lo lejano es raro, no solo difícil:** más allá del anillo X aparecen hallazgos únicos, no solo enemigos con más números.

### 2.3 Conexión con la red de sistemas

Según la [red de sistemas](../00-vision/red-de-sistemas.md) (D-20, D-38):

| Consume | Produce |
|---|---|
| Tiempo real, aguante y salud del héroe, materiales para caminos y postas, monturas | Distancia (que crea mercados locales y oficio de comerciante), descubrimientos, encuentros, materiales por bioma y Lejanía, rutas, mapas para vender |

---

## 3. De dónde sale

| Juego | Qué tomamos | Lección |
|---|---|---|
| *Minecraft* | Mundo infinito generado con semilla; solo se guarda lo que cambian los jugadores | Lo generado puede ser enorme si cuesta casi nada guardarlo |
| *Valheim* | Biomas más duros cuanto más lejos del centro | La distancia al inicio basta como escalera de dificultad |
| *Albion Online* | Riesgo por zona, transporte con peso, mercados locales | Si mover cosas es gratis, no hay comercio |
| *Torn* | Viajes con temporizador real y aviso al llegar | Un viaje de minutos funciona en texto si avisa y deja cerrar la app |
| *Chat Wars* | Acciones con tiempo real dentro de Telegram | El ritmo lento cabe en un bot si cada acción tiene resultado claro |
| *Wurm Online* | Caminos que construyen los jugadores y aceleran el viaje | La infraestructura de los jugadores es contenido |
| *Death Stranding* | Caminos y postas compartidos entre jugadores | Ayudar al que viene detrás es una forma de juego social |
| *No Man's Sky* | Nombrar lo que descubres | Un mundo infinito y vacío aburre: primero densidad, después tamaño |

---

## 4. Conversión desde la Torre vieja

Qué pasa con cada concepto de [Torre y pisos](torre-y-pisos.md):

| Torre (se retira) | Mapa infinito | Estado |
|---|---|---|
| Piso | **Zona** (una casilla) y **región** (manchas de zonas con Guardián) | Zona: v0.1. Región: propuesta |
| Número de piso | **Lejanía** | v0.1 |
| Tramo de 10 pisos | **Anillo** (de 3 en 3 Lejanías, I a X) | v0.1 |
| El Frente | **La Frontera**, con las mismas cuatro fases | Propuesta |
| Guardián del piso y su Eco | **Guardián de la región** y su Eco | Propuesta |
| Pionero del Piso | **Pionero de la región** | Propuesta |
| Sello del Piso | **Se retira.** No hay escalera: el avance es tu nivel, tus rutas y tu reputación | Propuesta |
| Muros (pisos 25, 50 y 75) | **Grandes Barreras** en ciertos anillos | Propuesta |
| Techo del Piso | **Techo de la Frontera** | Propuesta |
| Viento de Cola | **Viento de Cola** por distancia a la Frontera | Propuesta |
| Piedra de paso (teletransporte) | **Se retira.** Caminos, monturas y postas | Propuesta (D-58 pide tiempo) |
| Capitales cada 10 pisos | **Capitales regionales** en lugares clave | Propuesta |
| Piso 1, el Claro | **El Claro** en `(0, 0)`, Lejanía 0 | v0.1 |
| Gran Misterio de la Torre | **Gran Misterio de la Lejanía:** qué causó el Colapso y qué hay muy lejos | Propuesta |

---

## 5. Preguntas para el dueño

**¿Habrá viaje rápido?**
- A. Ninguno: solo caminos, monturas y postas.
- B. Teletransporte entre asentamientos, cobrando por peso.
- C. Solo entre capitales, una vez al día.
- *Recomiendo A,* porque es lo que pide D-58 y porque la distancia sostiene los mercados locales y el oficio de comerciante.

**¿Cuánto debe tardar cruzar a una zona vecina a pie?** ✅ Decidido por el dueño: 1 minuto por cuadro (D-197, 2-oct-2026; antes D-78: 2, 2, 3, 3, 4, 4… minutos según la distancia al Claro o a tu campamento).
- A. 5-10 minutos.
- B. 15-50 minutos según el bioma (lo de v0.1).
- C. 1-2 horas.
- *Recomiendo B,* con caminos que lo bajan a la mitad y monturas un 30 % más: se nota la distancia sin frenar una sesión corta en el celular.

**¿Se puede pagar con dinero real para viajar más rápido?**
- A. No.
- B. Sí, como acelerador.
- *Recomiendo A.* D-43 permite aceleradores de experiencia y botín, pero si el viaje se compra, el que paga gana en comercio y en la Frontera, y se rompe la distancia que pide D-58.

**¿El mapa descubierto es de todos o de cada uno?**
- ✅ **Decidido por D-61:** mixto. El mundo recuerda quién descubrió cada zona; cada héroe recuerda lo que pisó. Falta decidir si se podrán comprar mapas para aprender zonas sin pisarlas (recomiendo que sí, como oficio del Cartógrafo).

**Si te emboscan mientras viajas desconectado, ¿qué pasa?**
- A. El combate espera a que vuelvas (como en v0.1).
- B. Se pelea solo, con reglas simples.
- C. Huyes solo y pierdes algo de lo que llevas.
- *Recomiendo A,* con un aviso claro; es lo más justo para quien juega poco y no cambia nada para quien está conectado.

**¿Dónde aparece el primer Guardián?**
- A. Muy cerca (Lejanía 3-4), en la primera semana.
- B. En el anillo II (Lejanía 4-6).
- C. Más lejos, para dar tiempo a explorar.
- *Recomiendo B,* porque deja una o dos semanas de exploración y da una meta común temprana.
- *Provisional (D-82):* Claude eligió B para el primer Guardián, Raigambre: su guarida está fija en (5, 2), Lejanía 5, y por ahora se pelea en solitario. Detalle en [Jefes](../06-contenido/jefes.md) §6.
