# Traspaso a la terminal: todo lo que sabía el chat de la web

> **Módulo** [00 · Visión](README.md) · **Depende de:** [CLAUDE.md](../../CLAUDE.md), [Decisiones](decisiones.md), [Sistema de preguntas](sistema-de-preguntas.md) · **Alimenta a:** toda sesión de IA que trabaje en la terminal · **Estado:** al día el 11-oct-2026 (versión 0.32 en el juego)

El dueño pidió pasar el trabajo del chat de Claude Code en la web a la terminal de Claude Code en su computadora, "con toda la memoria y toda la información que tiene y dónde puede tomarla y todas las indicaciones". Este documento es esa memoria. **La IA de la terminal lo lee después de [CLAUDE.md](../../CLAUDE.md).** Las reglas de CLAUDE.md siguen siendo la ley; aquí está lo que se aprendió trabajando y el estado de cada cosa.

Cuando algo de aquí quede viejo, se corrige en el mismo cambio que lo cambia.

---

## 1. Primeros pasos en la terminal

1. **Abrir la terminal dentro del proyecto**, no en otra carpeta. Si `claude` se abre fuera del repositorio, no lee CLAUDE.md ni este documento.
   ```bash
   git clone https://github.com/jams990519/RPGDungeon.git
   cd RPGDungeon
   claude
   ```
   Si el repositorio ya está clonado: `cd RPGDungeon`, luego `git checkout main` y `git pull`, y después `claude`.

   **Para traer también la conversación de la web** (opcional; la memoria importante ya está en este documento):
   - Dentro de la carpeta clonada, con el git limpio y la misma cuenta de claude.ai, correr:
     ```bash
     claude --teleport session_01HGFTXEa37dZqWfpZtB6dj9
     ```
   - Otra forma: escribir `/teleport` dentro de `claude` y elegir la sesión.
   - El traspaso va en un solo sentido, de la web a la terminal. `claude --resume` no sirve para esto, porque solo ve las sesiones de la computadora.
   - Si `claude` no está instalado:
     - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
     - macOS o Linux: `curl -fsSL https://claude.ai/install.sh | bash`
     - Luego `claude` y entrar con la cuenta de claude.ai.
2. **Preparar Python 3.11** (lo pide `.python-version`):
   ```bash
   pip install -r requirements.txt pytest
   ```
3. **Comprobar que todo anda:**
   ```bash
   python -m pytest -q                       # 539 pruebas; tarda unos 20 minutos
   python -m adapters.cli.play --fast        # jugar en la consola; "q" para salir
   ```
   Después de jugar en la consola, **borrar la carpeta `data/`** (guarda la partida de prueba en `data/consola.sqlite3` y no se sube). En Windows: `Remove-Item -Recurse data` (PowerShell) o `rmdir /s /q data` (CMD); en macOS o Linux: `rm -rf data`.
4. **La carpeta de TowerWars no se toca** (regla 1 de CLAUDE.md, D-01). Si en la computadora hay una carpeta, un repositorio o una base de TowerWars, la IA no la abre, no la lee y no la cambia.

---

## 2. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Código y diseño | GitHub `jams990519/RPGDungeon`. La rama `main` es lo que está en el juego |
| Rama de trabajo de la web | `claude/blissful-lamport-7p5hmj` (hoy igual a `main`). En la terminal conviene una rama nueva por tema |
| El bot | Telegram **@LostRealmsbot** |
| Dónde corre | Railway, proyecto **satisfied-balance**, servicio **RPGDungeon**, entorno production. IDs: proyecto `8483a1b9-1aac-4111-9b8d-81b202908953`, servicio `88e89f1b-92f9-40e4-a0b5-525993ffca90`, entorno `91fbd952-6fff-4189-9394-c3aa76a74567` |
| Cómo arranca | `railway.json`: `python -m adapters.telegram.bot`. Las partidas viven en un volumen montado en `/data` |
| Variables | Solo los nombres, en `.env.example`. **El token del bot nunca se imprime, se copia ni se sube** |
| Lo decidido | [Decisiones](decisiones.md): la última es D-274 (D-247 a D-249 las registró la terminal el 14-oct en su rama local; todavía no están en el archivo) |
| Lo que falta decidir | [Preguntas abiertas](preguntas-abiertas.md) (la última es P-235) y el [Sistema de preguntas](sistema-de-preguntas.md) (la última es E-224; E-215 la citó D-241 y no existe: no usarla) |
| Lo que dijo el dueño, por fecha | [Entrevista de voz](entrevista-de-voz.md) |
| Las notas de cada parche | `content/patches.yaml` (la última es `v0_33_1`, con `title_en` y `notes_en`) |
| Copia en texto para otras IA | Notion (§7) |
| Los dos idiomas | [Idiomas](../01-plataforma/idiomas.md): toda clave de texto va en `es*.yaml` y en `en*.yaml`; `python tools/check_locales.py` en 0 errores |
| Informes y 💬 Feedback | El chat del equipo `RPG_REPORTS_CHAT_ID` (si no está, el chat que dio el dueño; el bot prueba también la otra forma del número, con o sin -100). El bot tiene que ser miembro de ese chat (el dueño lo agregó el 18-oct). Ver [Informes](../01-plataforma/informes.md) |

---

## 3. Cómo se publica un parche

Así se hizo cada versión de la 0.6 a la 0.32. Se publica solo lo probado (D-60, D-63).

1. **Trabajar en una rama**, nunca en `main`.
2. **Antes de subir:**
   - Correr las pruebas completas.
   - Arrancar la consola: `printf 'Nombre\n1\n1\nq\n' | python -m adapters.cli.play` crea un héroe y sale (en Windows, abrir `python -m adapters.cli.play`, crear el héroe a mano y salir con `q`). Después, borrar `data/`.
   - Verificar los enlaces de los documentos (el comando está en CLAUDE.md §5).
3. **Si el parche es jugable,** agregar su entrada al final de `content/patches.yaml`:
   - Mismo contenido: 0.33.1 → 0.33.2.
   - Contenido nuevo: 0.34 (D-67, D-73).
   - Desde la 0.33 cada entrada lleva también `title_en` y `notes_en` (D-250).
   - Las notas van en lenguaje de jugador.
4. **Commit en español,** con un tema por commit y en lenguaje de resultado. **Agregar los archivos por nombre**, nunca con `git add -A` ni `git add .`. Antes, `git status`, para no subir archivos ajenos (por ejemplo `.claude/` o `data/`).
5. **Push de la rama** y **pull request en borrador** contra `main`.
6. **Pasar el pull request a listo y unirlo con "merge"** (no squash ni rebase). Railway publica `main` solo, en un par de minutos.
7. **Comprobar en los registros de Railway** que salen dos líneas:
   - `running as @LostRealmsbot`;
   - `patch announced to N players`, si había nota nueva.
8. **Contarle al dueño, en español,** qué quedó, qué falta y qué necesita de él.

**Nunca:**
- subir `world.epoch` en `content/balance.yaml`: borraría el progreso de todos (D-64);
- borrar datos del volumen;
- tocar otro servicio de Railway;
- hacer `push --force`.

---

## 4. Lo que se aprendió trabajando (además de CLAUDE.md)

**El dueño**
- Habla por voz: se interpreta la intención sin pedirle que repita.
- Si la interpretación cambia algo importante, se registra como decisión provisional y se le dice cuál se tomó.
- Lo que él dice va como **confirmada**. Lo que decide la IA va como **provisional**, con la pregunta en el sistema de preguntas.
- Quiere respuestas cortas: qué quedó, qué falta, qué necesita de él, y una recomendación en cada pregunta.
- Si pide "para todo y haz esto primero", eso pasa adelante de todo lo demás.

**Las pruebas**
- La suite completa tarda unos 20 minutos. Se puede partir en dos mitades y correrlas a la vez.
- `tests/conftest.py` tiene `legacy_content()`, que reactiva en memoria las especializaciones retiradas en la 0.31 (`retired_in: "0.31"`). Así las pruebas del sistema viejo siguen corriendo; no se borran.
- Si una prueba se cuelga, revisar que `spend_point` y `make_hero` no caigan en un ciclo con una especialización retirada.

**El balance**
- Toda cifra de combate se mide con el simulador antes de subir:
  ```bash
  python tools/sim.py --summary --real            # contra los enemigos de nivel 1 a 3
  python tools/sim.py --boss --seeds=80           # contra el Guardián al nivel 6
  python tools/sim.py --boss --seeds=80 --only=paladin,sacerdote
  ```
- **Objetivos:** contra los enemigos de nivel 1 a 3, el 90 % o más (curación: 85 %). Contra el Guardián, entre 45 y 90 %.
- **Regla madre (D-232):** las clases de un mismo rol comparten `base` y `per_level`.
- **No cambiar `hero.xp_formula`** sin permiso del dueño.

**Los IDs**
- Solo se agregan. Para quitar algo: `retired: true`.
- Para mover a los jugadores: `migrate_to`, más `retired_in` con la versión. `ensure_talents` sigue la cadena de `migrate_to` hasta 5 saltos.

**Notion**
- Si un sistema de seguridad bloquea una página, no se reintenta, no se reescribe y no se parte: se salta y se anota.
- Las páginas de TowerWars en Notion tampoco se tocan.

**Agentes**
- Uno o dos a la vez como mucho, por los créditos (regla 6 de CLAUDE.md).

---

## 5. Cómo está el juego (17-oct-2026)

- **0.33 (D-250, D-251), el juego también en inglés:** cada jugador elige su idioma en la primera pantalla o en ⚙️ Opciones → 🌐 Idioma; todo sale en su idioma, también los avisos que le mandan otros. Trae además lo que la terminal dejó listo el 11-oct en la rama `revision/codigo-0.32` (la revisión del código, R-02, R-03, cada rol guarda sus puntos, el tiempo total del lote). Ver [Revisión del código](revision-codigo-0.32.md) y la hoja de ruta nueva ([Hoja de ruta](hoja-de-ruta.md) §0). La 0.33 trae también tres pedidos del 17-oct (D-255): 📦 Recursos corto con código (/07, D-243), el botón 🔗 Moverte con la emboscada que ya no corta el viaje (D-244) y viajar a la fogata estando ocupado. Y la **fogata ordenada** (D-257 a D-261): los oficios se aprenden pagando su primera receta (la recolección y la exploración suben solas), 📋 Mis oficios corto con códigos, 🛒 mercader con Comprar y Vender, posada según la vida que falta, un encargo por personaje cada día (se cobra en el Claro o en tu campamento), ⚙️ Opciones sin peleas automáticas y con 💬 Feedback, el 📔 Diario que vuelve a donde se abrió, y el **informe diario de jugadores** en el chat del equipo ([Informes](../01-plataforma/informes.md)). El dueño dio el sí para publicarla el 17-oct (pull request #76).
- **0.33.1 (D-262, D-263), el juego solo por privado:** en un grupo de Telegram el bot no juega; a un comando responde "🔒 se juega por privado" con un botón a su chat. El informe y el feedback prueban las dos formas del número del chat y el feedback que no sale vuelve a la cola.
- **Diseño del 17-oct, sin código:** la escalera de 5 a 200 jugadores (D-252 a D-254): el grupo nace al construir, nunca en la fogata; 10 etapas con un solo cupo, escuadras de 5, líder y oficiales; quien no juega libera su lugar a los 30 días; la muralla crece con la etapa y la tierra de adentro cosecha sola. Ver [Escalera del asentamiento](../09-construccion/escalera-del-asentamiento.md).

- **Versión 0.32 en el juego** (commit `65faad7`, pull request #74, publicado el 9-oct-2026).
- **El parche anterior: 0.31** ([Combate en cadena](../04-combate/combate-en-cadena.md), D-225 a D-232):
  - 6 clases con 2 roles cada una.
  - 4 botones: Básico, Constructor, Preparador y Gastador.
  - Energía que arranca en 5 y sube 2 por turno.
  - Marcas, y un premio de hasta +50 %.
  - Segundo rol al nivel 5.
  - Las 46 especializaciones viejas quedaron retiradas y cada héroe pasó a la más parecida.
- **0.32 (D-233, D-234):**
  - El 🦁 Paladín reemplazó al Chamán.
  - Hay dos clases por armadura y salen de dos en dos al crear el héroe: Guerrero y Paladín (placa), Druida y Cazador (cuero), Sacerdote y Mago (tela).
- **Lo de antes, en una línea:**
  - Mapa infinito en blanco, que se revela explorando.
  - Viajes con tiempo real.
  - Exploración, nodos de recursos, oficios en cadena, campamentos con despensa e incursiones, gremios.
  - Mazmorras para uno, el Guardián, historia en capa simple, el camino guiado.
  - Menús de 🏕️ Campamento y 👤 Héroe, y 📒 Lugares con código (/ir1).
  - El detalle de cada parche está en `content/patches.yaml` y en [Hoja de ruta](hoja-de-ruta.md).
- **Jugadores:** 1 (el dueño).

---

## 6. Lo que falta

**El 18-oct el dueño decidió mucho de una vez (D-264 a D-273)** y pidió publicar todo solo y preguntarle antes de empezar (D-264, CLAUDE.md §6). La cola, en este orden:
1. **0.34 (publicada el 18-oct):** encuentros al moverte de 6 a 14 % por zona y monstruos de afuera de tu nivel (D-266), botón 🗺️ Mapa en 📍 Zona y al viajar (D-268), campamentos de jugadores visibles (D-267, D-274), el Entrenador recomienda el oficio de tu armadura (D-271).
2. **0.35 (publicada el 18-oct):** cambio de clase con precios (D-270), solo el Explorador sube solo (D-272) y el 💬 Feedback llega al chat del equipo con su @, tipo, prioridad y pasos con botones (D-275).
3. **0.36 (publicada el 18-oct):** 👥 Jugadores en la fogata y el gremio desde el primer momento, con fondo, fundación que tarda según los presentes y obras según los miembros en el territorio (D-265, D-269, reemplaza a D-252). Lo programó un agente en una copia aparte (`engine/service/gremio.py`); las reglas chicas que decidió Claude están en D-276 (provisional) y se le preguntan al dueño (E-225).
4. **0.36.1 (publicada el 18-oct):** coordenadas en todo lugar y /ir x y (D-278), 🛡️ Gremio en cualquier lugar (D-279) e invitar con /inv_ y el código de jugador (D-280).
5. **0.37 (publicada el 18-oct):** las 9 hogueras con tope de 20 y el desborde (D-265). Cómo, ya decidido (D-277): el peligro desde la hoguera más cercana, las 9 visibles desde el inicio, nombres por su lado y una sola despensa.
6. **0.38 (publicada el 18-oct):** lo que explora uno del gremio (o del campamento) lo sabe todo el gremio, menos la experiencia, y la pantalla 🗺️ Zonas del gremio (D-282). Antes, ya publicado: 🛡️ Gremio en el menú de abajo (D-281) y la prueba de la energía de cada acción.
7. **0.38.1 (publicada el 19-oct):** el chat del gremio: con gremio o campamento, lo que escribes le llega a todos (D-285); y en el 🗺️ Mapa cada compañero con el emoji de su clase y una línea con su nombre, clase y coordenadas (D-286).
8. **0.38.2 y 0.38.3 (publicadas el 19-oct):** el Guerrero con espada (D-292) y los íconos de clase únicos (D-293).
9. **0.39 (publicada el 19-oct):** no se muestra lo que no es de tu nivel (D-287); 🏘️ Servicios por tipo y un edificio por oficio (D-288); 🤝 ayudantes (D-289); ⚔️ Armería (D-290); obras que activa el fundador o un ayudante, 💰 Depositar y el gremio completo después de fundar (D-291); gremio en espera (D-294); cada obra nueva cuesta más (D-295). La programaron dos agentes en paralelo y se unió aquí.
10. **0.39.1 (publicada el 19-oct):** 🔎 buscador de recursos en 🛡️ Gremio y 🏰 Gestionar, solo zonas al 50 % o más (D-296). Espera respuesta: cómo arreglar la madera escasa (E-227, P-238).
11. **0.39.2:** 💱 Comercio bloqueado hasta las caravanas (D-298). Después, 📚 Guías en ❓ Dudas (D-297, la programa un agente).
12. **0.39.3:** 📚 Guías en ❓ Dudas (D-297) y ❓ Dudas también en ⚙️ Opciones; /d54 vuelve a ser «¿qué hay de nuevo?» y la de coordenadas pasa a /d56.
13. **0.39.4:** 🔁 Equipar en lista solo con lo que no llevas (/e1) y 🔽 Desequipar (/q1) (D-299).
14. **0.40:** más madera (D-300), 📒 Lugares por botones (D-301) y submenús del campamento y del gremio (D-302).
14.1. **0.41 (D-304):** ⬆️ Mejorar campamento con ⏫ Siguiente nivel (la lista de obras y materiales que se va completando) y 🗺️ Agrandar territorio (minimapa, dirección y tope de zonas por etapa, E-218); el ayudante pasa a llamarse 🤝 asistente y elige la dirección con el fundador; 🔨 Mejoras muestra todo a todos. Las obras de cada nivel y los materiales los eligió Claude (provisional).
14.2. **20-oct: el dueño respondió 34 preguntas** (D-305 a D-312). Lo que falta programar, en este orden (D-306.6): **0.42** 🪓 Talar, los 6 recursos de base vuelven 3 por hora (D-305) y 🩹 Retirarse que no deja empezar un lote con poca vida (D-308); **después la reforma de los oficios** (D-306: tramos de recetas cada 5 y colores, títulos que se compran al Entrenador, precios por tipo y libros, los cuatro arreglos, sin tope de oficios; [Simulación de los oficios](../07-economia/simulacion-oficios.md)); después lo de D-311 (🔥 Fogata en todo el juego, el 🧭 Explorador en 🔭 Reconocer, tu territorio gris hasta el 50 %, el 🗺️ pergamino de mapa, los nodos en 📒 Lugares) y la muralla (D-309); el modo híbrido con las 3 habilidades (D-312) va con la reforma de estadísticas. La prioridad de lo grande es el asentamiento y el castillo (D-310).
El mundo se reinicia al abrir la beta, no antes (D-273).

**Esperan respuesta del dueño** (están en el [Sistema de preguntas](sistema-de-preguntas.md), tanda 1):

| Pregunta | De qué trata | Recomendación |
|---|---|---|
| E-187 en adelante | Estadísticas (puntos, afinidad, tope, armas), E-194 (descubrir zonas), E-173 a E-176 y el resto de la tanda 1 | Ver el [Sistema de preguntas](sistema-de-preguntas.md) |
| Tandas 1 a 6 | El resto: 73 preguntas en la tanda 1 | — |

**Otras cosas pendientes con el dueño**
- **Notas del "mundo abierto"** que trajo de otro chat el 8-oct: modo campamento, nodos por guerra de grupos, territorios con impuesto y cuadrantes, y 7 preguntas. Se le pidió el texto completo; todavía no se registraron como decisiones.
- **`tests/test_lugares.py`:** pidió deshacer cambios en ese archivo, pero en ese turno no se había tocado. Se le recomendó dejarlo y se espera su respuesta.
- **Copia en texto en Notion:** está en pausa (§7).

**Trabajo siguiente:** el orden de la [Hoja de ruta](hoja-de-ruta.md) §0 (11-oct, fases 0 a 9): primero la telemetría (fase 1), después la fórmula de armadura y las estadísticas (fases 2 y 3). El arreglo de la cadena de movimiento (D-244) ya está hecho en la 0.33. Las decisiones D-235 a D-249 (11 y 14-oct) contestaron varias de las preguntas de abajo (por ejemplo, las de las clases, E-208 a E-213, en D-238): antes de preguntar, revisar decisiones.md. Lo que sigue es la lista vieja, del 11-oct:

1. **"Subir de nivel no da estadísticas" (D-232).** Espera la reforma de estadísticas del equipo (D-210, D-211, E-170 a E-176): con el equipo de hoy, un héroe de nivel 20 quedaría con la fuerza de uno de nivel 1.
2. **Cómo se forman las civilizaciones** (en curso). Ver [El Colapso y las comunidades](../02-mundo/el-colapso-y-las-comunidades.md), [Caravanas y aldeanos](../02-mundo/caravanas-y-aldeanos.md), D-201 y D-202.
3. **Economía de jugadores, 2.ª tanda:** mercado de órdenes, pedidos de fabricación, durabilidad y reparación (D-109, D-113).
4. **Asentamiento por escalones:** la casa primero, misiones de grupo por nivel, castillo exigente (D-122, D-136, D-153, D-155, D-158).
5. **Razas y 3 facciones nuevas;** día, tarde y noche con la zona horaria de cada jugador (D-124, D-126, D-129, D-130).

---

## 7. La copia en texto en Notion

**Para qué es:** el dueño la pidió para analizar el proyecto con otra IA ("en puro texto, del código con todas las informaciones y preguntas y respuestas").

**Cómo está armada:** cada archivo del repositorio es una página de texto, debajo de la página de su carpeta:

| Carpeta | Página de Notion |
|---|---|
| raíz del repositorio | `3f2476db16ab81b88da9c6bbb322b6c2` |
| diseno | `3f2476db16ab8161939cdaa32b7628cd` |
| diseno/00-vision | `3f2476db16ab81e7bf9ce1a05cc43def` |
| diseno/01-plataforma | `3f2476db16ab811f9e4eda526ee85edc` |
| diseno/02-mundo | `3f2476db16ab81c8a712da27cdfb2722` |
| diseno/03-personaje | `3f2476db16ab81939858c5523c95f739` |
| diseno/04-combate | `3f2476db16ab81998766c1e937804084` |
| diseno/05-salud | `3f2476db16ab819ab86ecb29477386fb` |
| diseno/06-contenido | `3f2476db16ab8121b503f1c28336bc83` |
| diseno/07-economia | `3f2476db16ab81b6b3ebcf3d9bc3cbe4` |
| diseno/08-social | `3f2476db16ab81c08b26f02fed2b5bc7` |
| diseno/09-construccion | `3f2476db16ab818fa1afef9f480decb5` |
| diseno/99-referencias | `3f2476db16ab8161b323c513c443a3f2` |
| engine | `3f2476db16ab81bf99a4c0f9efb7c834` |
| content | `3f2476db16ab819d975fe73e3f1bcb48` |
| adapters | `3f2476db16ab81e585b9e657d637c418` |
| tests | `3f2476db16ab81768ec2c1b358076936` |
| tools | `3f2476db16ab81c3b2f8ccef5208d1f1` |

**Cómo está:** al día con la 0.30.2, y con la 0.31 solo en parte.
- Ya se refrescó para la 0.31: CLAUDE.md, los documentos de `00-vision` (menos el glosario), `01-plataforma` y una parte de `content/`.
- **Falta:**
  - los documentos y el código cambiados en la 0.31 y la 0.32;
  - reparar 4 páginas:
    - el **glosario**: un bloqueo de seguridad lo cortó en "Dominio";
    - **`content/balance.yaml`**: quedó solo con su encabezado;
    - `supervivencia-del-asentamiento.md` y `camino-guiado.md`: también se saltaron por bloqueos de seguridad;
  - una página índice **"Empieza aquí"** para la IA que lea la copia.
- **Cómo se hacía:**
  - Un programa convertía cada archivo a Markdown de Notion, en trozos de unos 19 KB.
  - Agentes los pegaban página por página, en tres modos: crear, reemplazar o agregar al final.
  - Ese programa vivía en la sesión de la web y no se guardó. En la terminal se puede rehacer, o la otra IA puede leer el repositorio directo.
- **Antes de seguir, preguntarle al dueño** si todavía la quiere. Con la terminal, la otra IA puede leer los archivos sin Notion. Si sigue, se rehace al día con la 0.32.
- **Más fácil que Notion:** también se le mandaron 4 archivos de texto de la 0.31, que se pueden regenerar:
  - parte 1: diseño, decisiones y preguntas;
  - parte 2: contenido y textos;
  - parte 3: código del motor y los clientes;
  - parte 4: pruebas.

---

## 8. Herramientas: lo que tenía la web y cómo tenerlo en la terminal

| La web usaba | En la terminal |
|---|---|
| El conector de GitHub (pull requests, merge) | `git` y la herramienta `gh` de GitHub (`gh pr create --draft`, `gh pr ready`, `gh pr merge --merge`), con la sesión de GitHub del dueño |
| El conector de Railway (despliegues y registros) | La herramienta `railway` (`railway logs`) o el conector de Railway agregado a Claude Code; los registros también se ven en railway.com |
| El conector de Notion | El conector de Notion agregado a Claude Code (solo si se sigue con la copia en texto) |

- **Conectores:** si la terminal entra con la cuenta de claude.ai, los conectores conectados en claude.ai (por ejemplo Notion) aparecen solos; se revisan con `/mcp`.
- **Agregar uno a mano:** `claude mcp add --transport http notion https://mcp.notion.com/mcp`. Para Railway, la dirección `https://mcp.railway.com` no está comprobada; hay que revisarla en la documentación de Railway.
- **Más ayuda:** https://code.claude.com/docs/en/mcp.md y https://code.claude.com/docs/en/claude-code-on-the-web.md
| Telegram | No hace falta: el bot corre en Railway. Para probar, la consola (`python -m adapters.cli.play`) |

## De dónde sale

- **Del chat de Claude Code en la web** que llevó el proyecto del diseño a la versión 0.32 (30-sep al 11-oct-2026).
- **Lo pidió el dueño el 11-oct-2026** para seguir trabajando desde la terminal de su computadora.
