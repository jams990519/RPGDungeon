# Hoja de ruta

> **Módulo** [00 · Visión](README.md) · **Depende de:** [Decisiones](decisiones.md), [Preguntas abiertas](preguntas-abiertas.md) · **Alimenta a:** todos los módulos · **Estado:** §1 y §2 describen el juego en vivo (Lost Realms 0.9.2); §3 en adelante es propuesta

**Reglas fijas.** El código está autorizado (D-59, reemplaza a D-04). Lost Realms corre en @LostRealmsbot (D-02), en el servicio RPGDungeon de Railway. Cada parche probado se une a `main` y se despliega solo (D-60, D-63). Nada más en Railway sin permiso del dueño. TowerWars no se toca (D-01). El progreso de los jugadores se guarda para siempre: el único reinicio autorizado ya se hizo (época 2, D-64).

---

## 1. Dónde estamos

El diseño se escribió primero, como un juego de años. Desde D-59 se programa en paralelo: primero una versión jugable mínima y después un parche por vez. Hoy hay un solo cliente, el bot de Telegram. El motor ya está separado de los clientes, así que la web y la app móvil (D-40, D-41) se pueden sumar sin cambiar las reglas.

### 1.1 Lo que ya está en el juego (0.9.2)

| Sistema | Qué hay hoy | Decisiones | Dónde se ve en el código |
|---|---|---|---|
| **Héroe** | Nombre único, clase para siempre y 100 niveles lentos. 1 punto de talento por nivel | D-64, D-74, D-78 | `engine/hero/`, `content/balance.yaml` (`hero`) |
| **Clases** | 15 clases. Cada una con 3 especializaciones de roles distintos (45 en total). Cada especialización tiene 8 habilidades que se abren con puntos | D-68, D-69, D-72, D-79 | `content/classes.yaml`, `engine/classes/` |
| **Talentos** | La especialización se elige con el primer punto. Se puede reiniciar por oro. Doble especialización con 10 puntos y 3 💰 bolsas | D-68, D-74, D-88 | `content/balance.yaml` (`talents`) |
| **Combate** | Por turnos, con avisos y 6 botones como máximo: ⚔️ Atacar, 3 habilidades elegibles, 🏃 Huir y 🎒 Mochila | D-46, D-79 | `engine/combat/` |
| **Mapa** | Mapa infinito por coordenadas, 9 biomas y 18 enemigos. Viajar toma 2, 2, 3, 3… minutos según la distancia al Claro o a tu campamento | D-58, D-61, D-78 | `engine/world/`, `content/biomes.yaml` |
| **Energía** | 50 como máximo y 40 por día. Moverse, explorar y recolectar gastan 1. Explorar y recolectar van en lotes de 5, 10, 20, 40 o toda | D-65, D-78, D-87 | `content/balance.yaml` (`energy`) |
| **Recursos** | 6 recursos en regiones de distintos tamaños. Cada zona se explora por porcentaje hasta el 100 %. Lo que se recolecta mucho se agota y vuelve con el tiempo | D-87 | `engine/world/resources.py` |
| **El Claro** | Campamento base de todos: **no crece** (D-98; su obra común se quitó en la 0.11). Tiene mercader, posada, costura de bolsas y armado de cofres | D-45, D-71 | `content/balance.yaml` (`settlement`) |
| **Campamentos** | Los jugadores los fundan lejos del Claro, les ponen nombre, aceptan miembros y los agrandan zona por zona hasta castillo | D-71, D-81, D-84, D-87 | `content/balance.yaml` (`camps`), `engine/world/territory.py` |
| **Equipo** | 7 ranuras y 4 rarezas. El juego dice si una pieza es para ti, pero puedes ponerte lo que quieras | D-77, D-83 | `engine/hero/gear.py`, `content/items.yaml` |
| **Salud** | La vida vuelve sola. Si caes, vuelve mucho más lento, salvo con pociones o la posada | D-83 | `content/balance.yaml` (`regen`) |
| **Monedas** | 🥉 bronce, 🥈 plata, 🥇 oro, 💰 bolsas que se cosen y 💎 diamantes que se compran. Con diamantes solo hay aceleradores y cosméticos | D-43, D-80, D-85 | `content/balance.yaml` (`currency`) |
| **Jefe** | Raigambre, el primer Guardián de región, en (5, 2). Pelea por fases, sin huida, con Recuerdo y título de Pionero | D-82 (provisional) | `content/enemies.yaml` |
| **Comunidad** | Tutorial con pistas, enlace de invitación que da energía y avisos de parche a todos | D-56, D-65, D-67 | `content/patches.yaml` |
| **Pantalla** | Máximo 4 botones arriba y 6 en el menú fijo de abajo: 📍 Zona · 🧭 Explorar · 🏕️ Campamento · 👤 Héroe · ⚙️ Opciones (D-114) | D-66, D-75, D-86, D-114 | `engine/service/game.py` (`menu`) |

### 1.2 Los parches publicados

Las notas completas están en `content/patches.yaml`. El bot las avisa a todos al arrancar cada versión (D-67). Mismo contenido sube el último número; contenido nuevo sube el segundo (D-73).

| Versión | Qué trajo |
|---|---|
| **0.4** | Reinicio único (época 2). Las 15 clases, energía, recolección, obra común del Claro, tutorial e invitaciones |
| **0.5 a 0.5.4** | Talentos por nivel, ícono por especialización, máximo 3 especializaciones por clase, primeros campamentos, roles repartidos, cambio de especialización, ficha del héroe |
| **0.6 y 0.6.1** | Equipo y botín. Energía 50/40 para toda acción, viajes por distancia y 100 niveles |
| **0.7 a 0.7.4** | Cinco monedas. Campamentos que crecen, con nombre y miembros. Vida que vuelve sola. 7 ranuras de equipo. Pantallas más simples |
| **0.8 y 0.8.1** | Raigambre, el primer Guardián. Exploración por porcentaje, regiones de recursos, mochila con espacio, energía en lote y campamentos que eligen zonas |
| **0.9 a 0.9.2** | 8 habilidades por especialización y barra elegible. Doble especialización. Clases más parejas |

## 2. Cómo se trabaja

1. **Un parche por vez.** Cada parche abre una pieza jugable cuando está lista y probada (D-60, D-63).
2. **Primero lo más importante,** con uno o dos agentes a la vez para no gastar créditos de más (D-59).
3. **Amplio pero ligero** (D-44). Cada sistema entra con su capa simple. La capa profunda llega después, si hace falta.
4. **Diseño y código juntos.** Si un documento no coincide con el juego, se avisa al dueño y se corrigen los dos.
5. **Medir antes de subir.** Todo número de combate pasa por el simulador (`tools/sim.py`). Todo número que se mueve va al registro de balance.

## 3. Próximas fases (propuesta)

El orden lo decide el dueño. Esta es la recomendación de Claude, de lo más cercano a lo más lejano. Cada fila es uno o varios parches.

| Orden | Fase | Capa simple que entraría | Por qué en este orden | Detalle |
|---|---|---|---|---|
| 1 | **Pulir lo que hay** (0.9.x) | Arreglos, balance con el simulador, textos más claros, preguntas de la beta | Mismo contenido: no cambia el segundo número | [Cuestionario de beta](cuestionario-beta.md) |
| 2 | **Vida en el campamento** | Un almacén común del campamento, un servicio propio (posada o mercader) al llegar a aldea y un aviso a los miembros cuando alguien aporta | Los campamentos ya crecen, pero adentro no hay nada que hacer | [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md), [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md) |
| 3 | **Primeros oficios** | Sembrar y abonar (P-74), un oficio de fabricación simple y la 🪪 credencial de oficio | Los recursos y la mochila ya existen. Falta qué hacer con ellos además de aportar | [Profesiones](../07-economia/profesiones.md) |
| 4 | **Mercado entre jugadores** | Vender y comprar en el Claro con precio fijo y comisión | Con oficios aparece algo que vender. La comisión es un sumidero de monedas | [Economía](../07-economia/economia.md) |
| 5 | **Lugares y eventos del camino** | Lugares dentro de cada zona y avisos con plazo a mitad de viaje | Llenan el mapa antes de agrandarlo | [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §2 |
| 6 | **La Frontera y más Guardianes** | Regiones con su Guardián, esfuerzo de guerra común y combate en grupo | Raigambre ya probó la pelea por fases. La Frontera da una meta común al servidor | [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §2.1, [Jefes](../06-contenido/jefes.md) |
| 7 | **Heridas, capa simple** | Una herida por zona del cuerpo que frena algo, y su cura con vendas o la posada | Hoy caer solo es más lento. Las heridas hacen falta para Medicina | [05 · Salud](../05-salud/README.md) |
| 8 | **Cliente web** | Las mismas pantallas del bot en el navegador, con la misma cuenta | El motor ya no sabe desde qué cliente juega cada uno | [Web y multiplataforma](../01-plataforma/web-y-multiplataforma.md) |
| 9 | **Asentamiento profundo** | Despensa, incursiones y gobierno, primero en el Claro | Pide oficios, heridas y combate en grupo antes | [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md), [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) |

**Más adelante** (sin orden todavía): mazmorras con grupos, PvP opcional, apuestas con oro del juego, crimen y justicia, cismas y guerra de castillos, temporadas, app móvil de texto.

### 3.1 El largo plazo: anillos y expansiones (propuesta)

Las 15 clases ya están en el juego, así que las expansiones ya no traen clases. Traen **anillos** del mapa y sistemas grandes. Cada anillo es una franja de Lejanía con biomas y Guardianes propios (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md)).

| Etapa | Anillo | Sistemas grandes |
|---|---|---|
| **Lanzamiento (1.0)** | I a III, con la primera Gran Barrera | Asentamiento profundo, primeros castillos con gobierno, mazmorras, mercado completo |
| **E1** | IV (Pantano) | Zonas negras, territorios y fortalezas, asedios, epidemias de servidor |
| **E2** | V (Desierto, Gran Barrera) | Talentos de héroe, justas, linaje familiar |
| **E3** | VI (Picos Helados) | Clima extremo completo, vampirismo y licantropía |
| **E4** | VII (Ruinas y costas) | Barcos, rutas marítimas, piratería, arqueología mayor |
| **E5** | VIII (Ciudadela, Gran Barrera) | Corrupción, Pesadillas mayores |
| **E6** | IX (Abismo) | Cordura, el Gran Misterio de la Lejanía |
| **Final** | X (Jardines) y la Lejanía profunda | El cierre de la primera era |

Con un ritmo de 4 a 6 meses por expansión, la primera era dura entre 2 y 4 años. Eso coincide con los 100 niveles lentos (D-78): con toda la energía cada día, el nivel 100 llega en unos 2,5 años.

## 4. El producto que ya es distinto

Lo que hoy ya no existe en otro juego de Telegram:
1. Un Claro que todos levantan juntos, de fogata a castillo.
2. Campamentos propios que crecen eligiendo zonas con recursos.
3. Un mapa sin borde donde cada paso toma tiempo y cada zona se explora.
4. 45 especializaciones al estilo de WoW, con 8 habilidades cada una.
5. Un Guardián con fases y avisos al estilo de Elden Ring.

Lo que falta para la promesa completa (propuesta): heridas por zona que curan médicos que estudiaron, oficios con profundidad real y un asentamiento que hay que sostener.

## 5. Riesgos

| Riesgo | Cómo se enfrenta |
|---|---|
| **Alcance** (muy grande para un equipo chico) | Parches chicos, capa simple primero, uno o dos agentes a la vez |
| **Límites de Telegram** | Máximo 4 botones arriba y 6 abajo (D-75), mensaje vivo, lotes de energía (ver [Telegram](../01-plataforma/telegram.md)) |
| **Balance de 45 especializaciones** | Simulador (`tools/sim.py`), registro de balance y ajustes por parche, como 0.9.2 |
| **Perder el progreso de los jugadores** | La época no se sube sin permiso explícito del dueño (D-64). Los IDs nunca se borran: se retiran |
| **Bots y multicuentas** | Energía limitada por día, retos contextuales (ver [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md)) |
| **Costos del servidor** | Un solo servicio en Railway. Presupuesto por definir (P-47) |
| **Mundo vacío** | Densidad antes que tamaño (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §2.2) |
| **Economía que se rompe** | Sumideros (bolsas, posada, reinicio de talentos), informe de monedas, palancas en `balance.yaml` |
| **Nombres y propiedad intelectual** | Mundo y nombres propios (ver [Referencias](../99-referencias/referencias.md)) |

## 6. Reglas de trabajo

- Antes de subir: correr las pruebas **y** arrancar el motor con al menos un cliente.
- Cada parche jugable agrega su entrada al final de `content/patches.yaml`, en lenguaje de jugador.
- Todo número de balance que se mueve va al registro, con su antes → después y la medición.
- Credenciales: nombres de variables sí, valores jamás.
- Nada en Railway fuera del servicio RPGDungeon sin permiso del dueño.

## 7. De dónde sale

- **World of Warcraft:** contenido por expansiones y parches con notas para el jugador.
- **TowerWars:** las reglas de trabajo (probar y arrancar antes de subir, registro de balance), resumidas en [Lecciones de TowerWars](../99-referencias/lecciones-de-towerwars.md).
- **Juegos de servicio** (Path of Exile, Albion): primero un núcleo jugable y después capas, medidas con jugadores reales.
