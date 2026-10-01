# El mapa infinito y el viaje

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Decisiones](../00-vision/decisiones.md) (D-58, D-59, D-60), [Jefes](../06-contenido/jefes.md) (D-08) · **Alimenta a:** [Economía](../07-economia/economia.md), [Fundación y cisma](fundacion-y-cisma.md), [Misiones y exploración](../06-contenido/misiones-y-exploracion.md), [Heridas](../05-salud/heridas.md) · **Reemplaza a:** [Torre y pisos](torre-y-pisos.md) (se retira) · **Estado:** v0.1 en código; el resto, propuesta

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

Cada zona saca su bioma de tres ruidos suaves (temperatura, humedad y altura), calculados con la semilla del mundo. El ruido forma **manchas**: zonas vecinas suelen compartir bioma.

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

**El mapa recuerda los lugares (D-61), en dos memorias:**
- **La del mundo:** quién descubrió cada zona queda guardado para siempre ("🧭 La descubrió Aria").
- **La de cada héroe:** la lista de zonas que pisó (campo `known` del héroe, empieza con el Claro). Su mapa, sus rutas y su lista de Lugares usan esta memoria: una zona que descubrió otro y tú no pisaste se ve como "▪️ Otro la descubrió, pero tú no la conoces", sin bioma ni nombre.

> **Cuidado:** cambiar los umbrales de la tabla 1.2, el ruido o los IDs de bioma **cambia el mapa de un mundo ya creado**. Ver la nota `[ES]` de [mapgen.py](../../engine/world/mapgen.py).

### 1.5 El viaje

- Desde una zona se viaja **solo a las 4 vecinas** (norte, sur, este, oeste). No hay diagonales ni teletransporte.
- Los minutos dependen **solo de la distancia** al punto de partida más cercano: el Claro o tu campamento (D-78). Las 2 primeras zonas toman **2 minutos** cada una, las 2 siguientes 3, luego 4, y así (`travel.first_minutes`, `steps_per_minute`). El bioma ya no cambia el tiempo; sigue decidiendo el peligro y lo que se recolecta.
  - **Tu campamento reinicia la cuenta:** al fundarlo, la distancia se mide desde él, igual que desde el Claro. Cuando el campamento crezca y ocupe más zonas, se medirá desde su borde.
  - **Tope por tramo: 20 minutos** (`travel.max_minutes`), para que lo muy lejano no se vuelva eterno. Este tope lo propuso Claude; el dueño puede moverlo.
  - **Energía (D-78):** moverse a una zona vecina, explorar y recolectar gastan 1 ⚡ cada uno. Máximo 50, se recuperan 40 al día (1 cada 36 minutos). Un viaje de varias zonas gasta 1 por tramo y se detiene si se acaba. El combate no gasta energía.
- Ningún viaje baja de 2 minutos. Un ajuste de servidor (`time_scale`) multiplica todos los tiempos; en juego normal vale 1 y en pruebas es menor.
- La pantalla redondea hacia arriba al minuto.

| Zonas desde el Claro o tu campamento | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | … | 37 o más |
|---|---|---|---|---|---|---|---|---|---|---|
| Minutos para entrar | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 5 | … | 20 (tope) |

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

### 1.6 Temporizadores, aviso y encuentro al llegar

- **Temporizadores perezosos:** el viaje guarda solo su hora de fin. Cada orden del jugador primero "cierra las cuentas" del héroe (termina lo que ya venció). No hay un proceso por héroe.
- **Aviso:** el bot de Telegram revisa cada 15 segundos quién terminó y le manda la pantalla de llegada. El jugador puede cerrar el chat.
- **Una actividad a la vez:** viajando no se explora ni se cambia de rumbo; en combate no se viaja. Sí se puede mirar el mapa, los Lugares, el héroe y la mochila.
- **📒 Lugares:** lista los lugares que tu héroe recuerda, del más cercano al más lejano (se muestran 8), con la distancia en zonas y el tiempo estimado. Al elegir uno, el héroe viaja solo, zona por zona: primero en el eje este-oeste y después en el norte-sur. Cada tramo se encadena desde la hora en que terminó el anterior, aunque nadie mire. Un encuentro al llegar a un tramo corta el viaje ("⛔ Tu viaje se corta en…").
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

El botón 🗺️ Mapa dibuja 7 × 7 zonas (3 a cada lado). 🧍 eres tú, el emoji del bioma marca lo que **tu héroe recuerda**, ▪️ lo que descubrió otro y ▫️ lo que nadie conoce. El norte está arriba.

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

- **Al fundarlo, un campamento ocupa 1 zona.** Cada vez que sus miembros lo agrandan (⬆️ Agrandar campamento), suma 1 zona más: 2, 3, 4… El costo es 15 de madera, 10 de piedra y 5 de fibra, multiplicado por el nivel actual (`camps.grow_cost_per_level`).
- **Hacia dónde crece:** en una espiral fija alrededor del centro: norte, este, sur, oeste, las diagonales y después el anillo siguiente. Salta las zonas que ya son de otro campamento o del Claro (`engine/world/territory.py`).
- **El Claro también crece:** ocupa 1 zona por cada etapa de su obra común (fogata 1, campamento 2, aldea 3…).
- **Qué da el territorio:**
  - Al llegar a una zona del territorio no te atacan.
  - Nadie puede fundar otro campamento encima.
  - Para tu viaje, la distancia se cuenta desde la zona más cercana de tu campamento o del Claro (2, 2, 3, 3… minutos).
- La línea "🏕️ Territorio de…" aparece en la pantalla de la zona.
- Lo pidió el dueño. Los costos y la seguridad al llegar los propuso Claude.

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
- **Huellas de otros jugadores:** la zona muestra quién la descubrió, quién pasó hace poco, caminos, tumbas y carteles. El mundo cuenta lo que hizo la gente.
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

**¿Cuánto debe tardar cruzar a una zona vecina a pie?** ✅ Decidido por el dueño (D-78): 2, 2, 3, 3, 4, 4… minutos según la distancia al Claro o a tu campamento.
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
