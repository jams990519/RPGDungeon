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
| Lo decidido | [Decisiones](decisiones.md): la última es D-326 (el 🗺️ pergamino de mapa, 0.50; D-325 es de la cosecha de la muralla, 0.49, que hizo otra sesión en paralelo; D-324, fogatas y 🔭 Reconocer, 0.48; D-323, la fila de espera del campamento, 0.46.1; D-322, el 💰 fondo del gremio para los oficios, 0.47; D-321, la lista de recetas con código; D-320, el 🏛️ Mercado, 0.46; D-247 a D-249 las registró la terminal el 14-oct en su rama local; todavía no están en el archivo) |
| Lo que falta decidir | [Preguntas abiertas](preguntas-abiertas.md) (la última es P-263, del 🗺️ pergamino de mapa; la sesión de la muralla, 0.49, usa números de antes) y el [Sistema de preguntas](sistema-de-preguntas.md) (la última es E-252, ídem; E-215 la citó D-241 y no existe: no usarla) |
| Lo que dijo el dueño, por fecha | [Entrevista de voz](entrevista-de-voz.md) |
| Las notas de cada parche | `content/patches.yaml` (la última es `v0_50`, el 🗺️ pergamino de mapa; la 0.49, la muralla, la sube otra sesión; desde la 0.33, con `title_en` y `notes_en`) |
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

**Railway**
- Si un despliegue falla al compilar con "build daemon returned an error < failed to solve: frontend grpc server closed unexpectedly >", el error es de Railway, no del código: el bot sigue con la versión anterior y el siguiente commit unido a `main` lo vuelve a construir (pasó con la 0.44, el 21-oct-2026).

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
14.1.1. **0.41.1 (D-313):** ⬆️ Mejorar dice exactamente qué falta (territorio con palabras, la lista entera, "faltan N" y cuándo termina cada obra), 💰 Depositar también llena el nivel y 📜 Qué pide cada nivel.
14.1.2. **0.41.1, madera (D-303; la programó un agente como 0.40.1 y salió junto con la 0.41.1):** 🪵 madera en todas las zonas (D-303): en el bosque la más rica, primera y conocida al 1 %; en el resto, pobre (hasta 0,5); el 🔎 buscador pone primero las zonas cercanas y ricas. De la madera sigue abierto el botón 🪓 Talar (E-227).
14.1.3. **0.42 (D-305, D-308; cómo se aplicó: D-314, provisional):** 🪓 Talar en 🧭 Explorar (un modo de recolectar que junta solo madera; Recolectar pasó a 🧺 y 🧭 Explorar tiene 5 botones), los 6 recursos de base vuelven 3 por hora (`stock.regen_mult` ×3) y 🩹 Descansa primero: con la vida bajo el % de 🩹 Retirarse no empieza un lote de explorar, recolectar ni talar. Preguntas nuevas: E-230 (confirmar cómo quedó) y E-231 (si la riqueza de la madera cambia lo que da talar).
14.1.4. **0.43, la parte del Entrenador y de lo que no avanzaba (D-306; cómo se aplicó: D-316, provisional):** 🎖️ los títulos de oficio se compran en el 🧑‍🏫 Entrenador (al tope de 20, 40, 60, 80 y 95 la experiencia no se guarda hasta comprar el siguiente; gratis hasta tu rango para quien ya lo pasaba; el 🧭 Explorador sin títulos; /titulos), aprender cuesta 🥈1 fabricación y 🥉50 recolección y refinado, la 🦌 piel ×2,5 y +3 de 🔪 Desollador por bestia, el botón 🎣 Pescar, 🧱 Mantenimiento (la obra que se repite para la 🏗️ Construcción) y el mercader que compra pociones y remedios a poco. La programó un agente en paralelo con el de las recetas (tramos, colores, libros, Joyería y malla), que va en la misma 0.43. Pregunta nueva: E-233 (confirmar cómo quedó).
14.1.5. **0.44, la reforma de recetas (D-306; cómo se aplicó: D-315, provisional; la programó un agente en paralelo con la 0.43, que salió antes con la otra parte):** en 🪑 🔨 🪡 🦺 💍 un tramo cada 5 rangos con pieza del nivel del tramo (180 piezas y recetas nuevas, generadas con `python tools/recipe_tiers.py`, que hay que volver a correr si cambia `balance.yaml` → `recipe_tiers`), colores 🟧 🟨 🟩 ⬜ con su experiencia en 🛠️ Fabricar, energía y experiencia que crecen con el tramo, 📚 Libros de recetas en el 🧑‍🏫 Entrenador (🥈2, 🥈10, 🥈25; gratis los de los rangos que ya tenía cada uno), 📿 Colgante de cobre (Joyería sin gema) y las 67 recetas de malla retiradas. Simulación: `python tools/sim_oficios.py` (especialista al 100 en 329 días). **Falta de esta reforma:** los tramos cada 5 y los colores del refinado, la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina salieron en la 0.52 (14.1.15); queda por decidir qué hacer con la 🎓 ⛓️ Malla ligera (E-232, P-243) y si la cadena en solitario tan lenta está bien (E-234, P-245). Los títulos que se compran, los precios por tipo, la piel, 🎣 Pescar, las obras que se repiten y el mercader que compra pociones salieron en la 0.43.
14.1.6. **0.45 (D-317, D-318; la escribió otra sesión del dueño):** edificios de oficio con lo de su oficio y mezcla de oficios desde el nivel 5. **Después:** las recetas en lista con código /rN (D-321), el recálculo de los edificios (0.45.1) y el 🏛️ Mercado entre jugadores (0.46), pedidos del dueño por medio de otra sesión el 21-oct.
14.1.6. **0.45, los edificios de oficio con lo de su oficio (D-317, confirmada, 21-oct):** los 13 edificios de oficio piden el 90 % en materiales de su oficio (tablón, tela, sillar, cuero, extracto, lingote) y el 10 % en madera y piedra, con el mismo valor en crudo; las obras activadas o empezadas antes siguen con su costo viejo (`cost_before` en `camp_upgrades.yaml`, `GameService._work_base`) y desde ahora cada obra guarda su costo al activarse. Y **D-318** (misma 0.45): desde el nivel 5 las casas y defensas piden también objetos de otros oficios (la Enfermería, 🪑 Literas, ungüentos y vendas; Muralla, Huerto, Torres: 🪑 muebles; Braseros, Foso: lingotes; Biblioteca: tela y extracto). **Por mirar:** si la piel y el metal (ahora 120 pieles y 286 metales en esas obras) frenan los campamentos y si los muebles llegan a tiempo.
14.1.7. **0.45.1, recálculo de costos y beneficios de los edificios (D-319, provisional, 21-oct):** `python tools/camp_costs.py` mide el camino al castillo (por obra y en total: crudo por recurso, energía de juntar, refinar y fabricar, oficios y rangos, 🥉, días con 5 a 10 miembros). En la 0.45 un campamento se trababa en el nivel 5 (la Muralla y el Huerto pedían muebles de 🎓, Carpintería 50 y 25) y el castillo esperaba al rango 70. Ahora lo que pide ⏫ se hace con rango 10 o menos (15 para el castillo): Literas rango 10, Armero 15, Muralla y Huerto con tablones y lingotes, la Forja sin cuero. Castillo ~17,6 días (antes de la 0.45, 15,9); las 31 obras ~41 (antes 30): pregunta E-235 (P-246). **La 0.45 todavía no está en `main`: conviene unirla junto con la 0.45.1**; si sale sola, una Muralla, Huerto o Forja activada entre las dos guarda el costo de la 0.45 con los muebles.
14.1.8. **0.46, el 🏛️ Mercado entre jugadores (pedido del dueño del 21-oct-2026: "que funcione y luego vamos arreglando"; D-137 y D-26 confirmadas; cómo se armó: D-320, provisional):** un solo libro para todos, en el 🛒 Mercader de cada fogata, en ⚒️ Oficios del campamento con el 🏪 Puesto de trueque y con /mercado; órdenes de venta para el equipo y lo fabricado (/s1 → precio en 🥉 y cantidad; se compra con /c1 desde 7 categorías, de la más barata a la más cara) y pedidos de compra para los recursos (/b07, con las monedas apartadas; se les vende con /k1); impuesto del 5 % que paga quien cobra; 📦 Entregas a los 30 min, se recoge en fogatas y en el campamento; 7 días, 10 órdenes, banda de 0,25 a 10 veces la referencia; la ✒️ firma y el ✨ viajan con la pieza; 📋 Mis órdenes con ❌ Cancelar (/o1); el informe diario lo cuenta (sección 9). Lo programó un agente en paralelo con el de los costos del campamento (`engine/service/market.py`, `tests/test_mercado.py`; [Economía](../07-economia/economia.md) §3.0). Preguntas nuevas: E-236 a E-239 (P-247 a P-250). Falta del mercado: órdenes de venta de recursos, tiempo por distancia y bandidos (D-137), bandas por historial.
14.1.9. **0.46.1 (D-323, orden del dueño con prioridad):** quien espera lugar entra solo al campamento, en orden de llegada, cuando hay lugar; los que esperaban desde antes entran en el primer tick.
14.1.10. **0.47, el 💰 fondo del gremio también para los oficios (pedido del dueño del 21-oct-2026 por otra sesión: "que los jugadores del gremio puedan primero construir las estructuras y después poder utilizar los recursos para las profesiones de cada uno"; cómo se armó: D-322, provisional):** primero las obras (el fondo sigue alimentando las obras activas y ⏫ Siguiente nivel; lo que les falta es la reserva y nunca va a oficios); lo que sobra lo usa cada miembro al refinar, fabricar o cocinar en las estaciones de su campamento (primero su mochila, después el fondo; ✅💰 en la lista /r1; "+💰n" y "💰 Del fondo del gremio, por vez" en la receta), hasta 40 por día real (`fund_crafts.daily_cap`); 💰 Fondos dice qué está guardado y qué sobra, con 📜 Quién usó qué y el interruptor 🔓/🔒 del fundador o un 🤝 asistente. No vale en las fogatas ni para quien espera lugar en el gremio (D-294). Código: `engine/service/gremio.py` (sección del fondo para oficios) y los ganchos de `engine/service/game.py`; pruebas: `tests/test_fondo_para_oficios.py`. Preguntas: E-240 a E-243.
14.1.11. **0.48, 🔥 fogatas, 🔭 Reconocer con lo del Explorador, tu territorio gris y ✨ nodos en 📒 Lugares (D-311 partes 1, 2, 3 y 6, confirmada el 20-oct; cómo se aplicó: D-324, provisional):** (1) las hogueras se llaman 🔥 fogata en todo texto (la leyenda del mapa, la cabecera de 📍 Zona "— 🔥 Fogata" también en el Claro, el menú de la fogata titulado "🔥 El Claro" o "🔥 Fogata del Norte", y los "campamento base" de la guía y ❓ Dudas); en inglés, campfire; solo textos, los ids siguen; (2) la lista de 🔭 Reconocer suma cada 👹 campamento enemigo que tu rango de 🧭 Explorador deja ver (1 zona, 3 desde el 25, todo el mapa desde el 50), con nombre, zonas, ⏱️ tiempo y, desde el 75, 💪 fuerza, y el código /rc1 en lo que puedes reconocer ahora (espacio `recon_shown`); 🧭 Explorar avisa los campamentos a la vista; el mapa sigue en blanco; (3) tu territorio gris hasta el 50 %: el código ya no hacía excepción desde la 0.30, quedó escrito y probado; (6) 📒 Lugares → ✨ Nodos con los nodos que encontraste (zona, recurso, /ir1), solo en zonas que recuerdas. Código: `engine/service/game.py`; textos en `content/locales`; pruebas: `tests/test_fogata_reconocer_lugares.py`. **Falta de D-311:** la parte 5, el 🗺️ pergamino de mapa del Explorador (salió en la 0.50, 14.1.13). Preguntas nuevas: E-244 (¿"el Claro" también cambia de nombre?), E-245 (el botón 🏕️ Campamento del menú de abajo) y E-246 (¿un botón 🔭 en el mapa para el Explorador?).
14.1.12. **0.49, la 🌾 cosecha de la muralla (D-309, confirmada el 20-oct; cómo se aplicó: D-325, provisional):** con la 🧱 Muralla construida, todo el territorio del campamento da solo el 20 % de lo que vuelve a crecer (24 por recurso y día, sin el ×3 de la 0.42: unas 27 por zona), guardado hasta 7 días y entregado cada 7 días al 💰 fondo del campamento desde `tick()` si algún miembro jugó esa semana (si no, se pierde); la fracción queda para la semana siguiente; un aviso por semana a cada miembro con `_push_each`; el 🐟 pescado no entra (es comida). La línea "🌾 Cosecha de la muralla: +N/día · guardado X (tope 7 días) · al 💰 fondo en N días" sale en ⬆️ Mejorar, 💰 Fondos e ℹ️ Información; sin muralla, desde el nivel 5, una pista; ❓ /d61. `gather.own_land_bonus` pasó a 1,0 (la clave queda) y ningún texto promete el +50 %. Ritmo (`python tools/camp_costs.py`, que ahora cuenta la cosecha; `--no-harvest` sin ella): castillo ~20,7 días (0.48: 17,6), las 31 obras ~47,7. Código: `engine/world/harvest.py`, la sección "🌾 the wall's harvest" de `engine/service/game.py` y `gremio.py` `_guild_funds_view`; números en `balance.yaml` → `harvest`; textos en `es_cosecha.yaml`/`en_cosecha.yaml`; pruebas: `tests/test_cosecha_muralla.py`. **Falta de la muralla:** la muralla por anillos con su costo y mantenimiento por zona (escalera §5.2). Preguntas nuevas: E-247 (qué zonas cierra la muralla), E-248 (contar el ×3 de la 0.42) y E-249 (los niveles antes de la muralla).
14.1.13. **0.50, el 🗺️ pergamino de mapa del Explorador (D-311 parte 5, confirmada el 20-oct; cómo se aplicó: D-326, provisional; lo programó un agente en paralelo con el de la cosecha de la muralla, D-325, 0.49):** desde el rango 15 de 🧭 Explorador, 🗺️ Mapa → 🗺️ Pergaminos → 🗺️ Hacer pergamino (/pergaminos, /scrolls): las zonas que investigaste tú al 50 % en la región de 6 × 6 donde estás (cuadrícula fija; al menos 6; nunca fogatas), por ⚡5 y 1 🦌 piel, +30 de experiencia de Explorador. Cada copia lleva sus zonas, su autor y su región (`Hero.map_scrolls`; la mochila los cuenta). 📜 Usar lo gasta y pinta esas zonas para siempre (`Hero.charted`): solo el color, ni recursos, ni nodos, ni lugares, ni viaje directo. Se vende en 🏛️ Mercado → 🗺️ Mapas (9.º botón de 🛍️ Comprar) de a uno, a precio libre de 1 🥉 a 1 🥇 (excepción de la banda D-26); el 🛒 Mercader no lo compra. Código: `engine/service/map_scroll.py` (nuevo), `engine/service/market.py`, `engine/service/game.py`, `engine/hero/hero.py`; textos en `content/locales/es_pergamino.yaml` y `en_pergamino.yaml`; pruebas: `tests/test_pergamino_mapa.py`. **Con esto D-311 queda completa.** Preguntas nuevas: E-250 (los números), E-251 (el tope de 1 🥇 del precio) y E-252 (si el gremio también ve las zonas del pergamino).
14.1.15. **0.52, la reforma de recetas en el refinado, la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina (D-306, confirmada; cómo se aplicó: D-328, provisional; la programó un agente en paralelo con el de la escalera del asentamiento):** ahora **todos** los oficios con recetas tienen un tramo cada 5 rangos hasta el 100 y colores 🟧 🟨 🟩 ⬜. El refinado gana un refinado mejor por tramo (120 materiales nuevos, `<refinado>_tramo_<N>`: su refinado de siempre + su crudo + un catalizador de terreno; valen sus materiales más su ⚡; **hoy ninguna receta los pide**, E-257); ⚗️, 🩺 y 🍲 ganan una receta por cada tramo que no tenía (19 pociones, 18 remedios, 16 platos), a mitad de camino entre las recetas de siempre (las "anclas") y un punto final en `balance.yaml` → `recipe_tiers.consumables`: curan más (pociones de vida 37-45 %, mayores 61-75 %, remedios 24-60 %) con la toxicidad de su ancla y en su mismo lugar del cinturón (`belt_slot`, `_refill_belt`: el cinturón no crece), y los platos dan de 4 a 41 raciones. Todo lo genera `python tools/recipe_tiers.py` (hay que volver a correrlo si cambia `recipe_tiers` o una receta ancla; las pruebas avisan). Códigos nuevos /101 a /280 (código de la línea + rango ÷ 5). Los ids de antes no cambian (las obras del campamento piden tablón, sillar, lingote…). Quien ya tenía rango recibe gratis una vez los libros nuevos de su oficio (`recipe_tiers.book_gifts`, `Hero.book_gifts`). La lista /r1 dice el tramo (" · tramo 45"). Ritmo (`python tools/sim_oficios.py`): especialista al 100 en 329 días en los 9 oficios (antes 368); la cadena en solitario, unas 2 veces más larga (refinado de ~1.000 a ~2.200 días; la Curtiduría ~4.000); el camino al castillo no cambia (`tools/camp_costs.py`). Código: `tools/recipe_tiers.py`, `engine/service/game.py` (`_station_view`, `_refill_belt`, `_belt_members`, `_grant_book_gifts`), `engine/hero/hero.py`; pruebas: `tests/test_tramos_refinado_alquimia_medicina_cocina.py`. Preguntas nuevas: E-257 (que las piezas de los tramos altos pidan los refinados nuevos), E-258 (cuánto curan) y E-259 (si piden nivel de héroe).
14.2. **20-oct: el dueño respondió 34 preguntas** (D-305 a D-312). Ya están en el juego: 🪓 Talar, los recursos de base ×3 y 🩹 Retirarse (0.42) y la reforma de los oficios (0.43 y 0.44; los tramos del refinado, la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina, en la 0.52, 14.1.15; [Simulación de los oficios](../07-economia/simulacion-oficios.md) §11). **Lo que sigue, en este orden:** D-311 está completa (las partes 1, 2, 3 y 6 en la 0.48, 14.1.11; el 🗺️ pergamino de mapa en la 0.50, 14.1.13); la cosecha de la muralla (D-309) salió en la 0.49 (14.1.12); el modo híbrido con las 3 habilidades (D-312) va con la reforma de estadísticas. La prioridad de lo grande es el asentamiento y el castillo (D-310).
El mundo se reinicia al abrir la beta, no antes (D-273).

**Esperan respuesta del dueño** (están en el [Sistema de preguntas](sistema-de-preguntas.md), tanda 1):

| Pregunta | De qué trata | Recomendación |
|---|---|---|
| E-187 en adelante | Estadísticas (puntos, afinidad, tope, armas), E-194 (descubrir zonas), E-173 a E-176 y el resto de la tanda 1 | Ver el [Sistema de preguntas](sistema-de-preguntas.md) |
| E-230, E-231 | 🪓 Talar de la 0.42: confirmar 🧺 Recolectar y los 5 botones; si la riqueza de la madera cambia lo que da talar | Dejarlo así hasta medirlo |
| E-233 | La 0.43 (D-316): en el tope de un título la experiencia no se guarda, el título se compra solo en el tope, el Explorador sin títulos, ✨ 🥈1 y 🏗️ 🥉50, dónde sale 🎣 Pescar, 🧱 Mantenimiento sin otro efecto y el mercader al 25 % | Dejarlo así y medirlo con el informe diario |
| E-232, E-234 | Recetas de la 0.44: qué hacer con la 🎓 ⛓️ Malla ligera; si la cadena en solitario tan lenta está bien | Retirar la Malla ligera con cambio gratis; dejar la cadena así y sacar primero el mercado |
| E-236 a E-239 | El 🏛️ Mercado de la 0.46 (D-320): confirmar sus números (5 %, 30 min, 7 días, 10 órdenes, banda 0,25-10); recursos también con órdenes de venta; transporte por distancia y bandidos; si el 🛒 Mercader sigue comprando pociones | Dejarlo así y medirlo con el informe diario; la distancia con las caravanas; el mercader, como piso por ahora |
| E-240 a E-243 | El 💰 fondo del gremio para los oficios de la 0.47 (D-322): el tope por día (40), si empieza abierto, si vale también en las fogatas y si quien espera lugar en el gremio lo usa | 40 y medirlo; abierto; solo en tu campamento; quien espera, no hasta que entre |
| E-244 a E-246 | La 0.48 (D-324): si "el Claro" también cambia de nombre, el nombre del botón 🏕️ Campamento del menú de abajo y un botón 🔭 Reconocer en el mapa para el Explorador | Dejar "el Claro" y el botón 🏕️ Campamento; sumar 🔭 al mapa desde el rango 10 |
| E-247 a E-249 | La 0.49 (D-325): qué zonas cierra la muralla (hoy, todo el territorio con la 🧱 Muralla), si la cosecha cuenta el ×3 de la 0.42 (hoy no: castillo ~20,7 días; con el ×3, 17,4) y qué pasa en los niveles antes de la muralla | Todo el territorio hasta la muralla por anillos; dejar 24 y medir en la beta; dejarlo así, la muralla es la meta del pueblo |
| E-257 a E-259 | La 0.52 (D-328): que las piezas, pociones y remedios de los tramos altos pidan los refinados nuevos (hoy no los pide nada); cuánto curan las pociones y remedios nuevos (hasta 75 % y 60 %; por pelea, hasta 120 %); si piden nivel de héroe | Que los pidan desde el tramo 25, en un parche aparte y medido; dejar lo que curan y medir en la beta; sin nivel |
| Tandas 1 a 6 | El resto: 75 preguntas en la tanda 1 | — |

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
