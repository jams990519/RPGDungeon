# Menús: 🏕️ Campamento, 👤 Héroe, 🧑‍🏫 Entrenador y ❓ Dudas

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Web y multiplataforma](web-y-multiplataforma.md) §3 (vistas neutras), [Decisiones](../00-vision/decisiones.md) D-190, D-191 y D-192 · **Alimenta a:** todos los módulos que tienen pantallas en el campamento o en el héroe · **Estado:** en el juego desde la 0.29 (D-190 y D-191 confirmadas; cómo se aplican, D-192 provisional). 0.36: 👥 Jugadores en la fogata (D-265, D-274) y el centro del 🛡️ Gremio (D-269)

Cómo se ordenan las pantallas principales del juego desde la 0.29: el menú de abajo, el centro de 🏕️ Campamento (en el Claro y en tu propio campamento), el centro de 👤 Héroe, el 🧑‍🏫 Entrenador y ❓ Dudas. El camino guiado de la historia (D-190), que manda al jugador a hacer una cosa nueva por vez, se describe aparte.

## De dónde sale

- **TowerWars actual** (pedido del dueño, D-190): "bien ampliado, detallado y separado". Cada sección abre su propio grupo de botones (un "centro") con todas sus opciones a la vista, de 2 en 2; los costos y tiempos van en el texto, no en el botón; lo que no se puede todavía no se esconde: explica por qué. La ficha del héroe muestra cada número como actual/máximo con su tiempo ("❤️ Vida: 80/120 (llena en 3 min)"). De TowerWars solo se toman ideas (D-01): el resumen está en el estudio del 2-oct-2026.
- **El dueño** (D-191): el campamento tiene, en orden, cocinar, investigar y fabricar (lo que no está en el héroe), un entrenador que presenta los oficios y un botón de ❓ Dudas que muestra preguntas ya respondidas, con un código para llamar cada respuesta. El héroe tiene todo lo del personaje.
- **Las pistas de los MMO de texto** (Chat Wars, TowerWars): los atajos con "/" que el jugador escribe o toca en el texto. En Telegram, un /d07 dentro del mensaje se toca como un enlace.

## 1. El menú de abajo

6 botones, de 2 en 2 (filas de 2, 2 y 2): **📍 Zona · 🧭 Explorar · 🏕️ Campamento · 👤 Héroe · 🛡️ Gremio · ⚙️ Opciones**. 🛡️ Gremio entró en la 0.37, al lado de ⚙️ Opciones (D-281, pedido del dueño: "para que se pueda ver").

- **📖 Historia salió** (D-190): la historia ahora te guía mientras juegas. Lo que estaba ahí se repartió (E-130): el 📔 Diario con 🎯 Misiones y ⚜️ Facciones pasó a 👤 Héroe; el 📜 Tablón de encargos y 🧑 Personajes, a 🏕️ Campamento.
- **Nada viejo se rompe:** el botón 📖 Historia de un teclado viejo, /historia y el texto "📖 Historia" abren el 📔 Diario con un aviso de una línea que dice dónde quedó todo.
- **Crear el héroe** pide solo el nombre y la clase (D-190); al terminar se entra directo al juego. El origen se elige cuando quieras en 👤 Héroe → 🎭 Origen (E-131); quien ya lo tenía lo conserva. El camino guiado puede ofrecerlo una vez.

## 2. 🏕️ Campamento

Un **centro** (D-192): arriba, una línea por opción con lo que hace y sus números; abajo, sus botones, hasta 8 de 2 en 2 (E-132), en el orden que pidió el dueño.

### 2.1 En el Claro

| Botón | Qué hace | Si no se puede |
|---|---|---|
| 🍲 Cocinar | La estación de la 🍲 Cocina: carne, pescado y lo de cada terreno se vuelven raciones y guisos (rinden más en la despensa de un campamento) | Sin la 🍲 Cocina aprendida (D-257), la línea dice que primero se aprende y el botón lleva a aprenderla |
| 👥 Jugadores | **0.36 (D-265, D-274.1):** reemplaza a 🔬 Investigar, que en el Claro repetía 📚 Aprender oficios (los oficios se aprenden en 🧑‍🏫 Entrenador → 📚 Aprender oficios; el botón viejo y /aprender siguen andando). Los que jugaron en la fogata en el último minuto, con clase, nivel y gremio, cada uno con su código (/j1, en inglés /p1) que abre su tarjeta (✉️ invitar a tu gremio o 🙋 pedir entrar al suyo), y el contador **"👥 N/20 en la fogata"** (N con la regla de 15 min de 📍 Zona; 20 es `bonfire.cap`). Botones: 🛡️ Gremio, 🔄 Actualizar y ↩️ Volver. También /jugadores y /players | Lejos de la fogata, avisa que se ve ahí |
| 🛠️ Fabricar | ⚒️ Oficios: una línea corta por oficio que tienes y 🪚 Refinar y 🛠️ Fabricar en las estaciones de aquí (D-259) | Una estación sin oficios aprendidos dice cuáles aprender |
| 🧑‍🏫 Entrenador | Tus oficios, los que te faltan y cómo se aprenden (§4) | — |
| 🛒 Mercader | **🛒 Comprar** (pociones, vendas, 🥖 provisiones) y **💱 Vender** (lo que traes, con su código /v02) (D-259) | — |
| 🛏️ Posada | Dormir y despertar con la vida llena: tarda según la vida que falta, de 0 a llena en 1 hora (D-259) | Con la vida llena no cobra |
| 📜 Tablón | **Un encargo por personaje cada día** (se cobra hablando con él, en el Claro o en tu campamento) y, con campamento, los de la semana (D-259) | — |
| ❓ Dudas | Buscar respuestas (§5) | — |

Debajo va la pista de siempre: el Claro no crece; para crecer, funda tu campamento.

**🛡️ Gremio (D-269, 0.36)** se abre desde 👥 Jugadores y con /gremio. Sin gremio: qué es, 🛡️ Crear gremio (🥉20) y 🔎 Buscar gremio (los gremios sin campamento con su código /g1; cualquier texto busca). Con gremio, un **centro** (hasta 8 botones de 2 en 2): arriba el líder y "👥 N/5", la fundación en curso con su barra, el 📍 punto de reunión, el 💰 fondo, cada miembro con su código (/m1), si está en línea, dónde está y qué hace, y los últimos 📢 mensajes; abajo **📢 Mensaje · 💰 Fondo · 📍 Reunión · 🏕️ Fundar** (el líder) **· 🙋 Solicitudes** (líder u oficial, si hay) **· 🚪 Salir · ↩️ Volver**. Ya con campamento, 🛡️ Gremio es la pantalla del gremio del campamento (D-97), en 🏰 Gestionar. Mientras el gremio tiene un lugar definido, 📍 Zona suma el botón ancho **🏗️ Moverte a la construcción** (layout [2, 2, 1, 1, 1]). Cómo funciona todo: [Escalera del asentamiento](../09-construccion/escalera-del-asentamiento.md) §0.

### 2.2 En tu propio campamento

Arriba, la información de siempre (miembros, nivel, zonas, mejoras y 🛡️ Defensa, despensa, beneficios de campamento, próxima oleada). Abajo, el centro: **🍲 Cocinar · 🔬 Investigar · 🛠️ Fabricar · 🧑‍🏫 Entrenador · 🏘️ Servicios · 📜 Tablón · 🏰 Gestionar · ❓ Dudas**.

- 🍲 Cocinar pide el 🔥 Fogón; 🔬 Investigar, la 📚 Biblioteca; 🛠️ Fabricar, el 🧵 Taller o la 🔨 Herrería. Sin ellos, la línea y el botón explican qué construir y dónde (🏰 Gestionar → 🔨 Mejoras).
- 🏘️ Servicios ocupa el lugar del mercader y la posada: el 🛏️ Refugio, el 💱 Puesto de trueque y el 🧵 Taller que construyeron.
- **🏰 Gestionar** junta lo que hace crecer y mantener el campamento, que antes eran sus 4 botones: **⬆️ Agrandar · 🔨 Mejoras · 🌾 Aportar comida** (desde el nivel 3) **· 🛡️ Gremio**, cada uno con su línea (cuánto cuesta agrandar, cuánto hay construido, la despensa). Sus pantallas vuelven a 🏰 Gestionar. Es la duda E-134.
- **Durante una oleada** que todavía no peleaste, 🛡️ Defender va primero en el centro y en 🏰 Gestionar (lo pendiente arriba, como en TowerWars); para no pasar de 8, 📜 Tablón sale del centro mientras dura (sigue en /encargos).

### 2.3 En otros lugares

En una zona sin campamento, 🏕️ Campamento muestra lo que pide fundar uno; en el campamento de otro, 🙋 Pedir unirme. Las dos suman ❓ Dudas (4 botones como mucho).

## 3. 👤 Héroe

Un centro con la ficha estilo TowerWars y 8 botones: **🎒 Mochila · 🌟 Talentos · 🩺 Salud · 📊 Estadísticas · 🎛️ Barra de combate · ⚒️ Oficios · 📔 Diario · 🎭 Origen**.

La ficha, de arriba abajo:

```text
✨ Puntos de talento: 2 — ponlos en 🌟 Talentos      (solo si hay puntos sin poner)
🏰 Lyra — 📍 El Claro
🗡️ Guerrero · Defensa
🎭 Origen: Soldado desertor
🎖 Nivel 12 (34.50%)
🔥 Exp: 1234/3000
❤️ Vida: 80/120 (llena en 1 h 20 min)
⚔️ Atk: 25  🛡 Def: 18%
⚡ Energía: 30/50 (+1 en 12 min)
🔷 Ira: 100/100
🥉 40   🥈 3   🥇 0   💰 1   🪎 0   💎 0
🎒 Mochila: 34/60 — /inv
⚒️ Oficios: 4 empezados · mejor: 🪓 Leñador 12 — /oficios
```

- **📔 Diario** es la pantalla de la historia (E-130): tu tarjeta, el origen y el capítulo, qué hacer ahora, los encargos de hoy, las facciones y tus últimos hechos; botones 🎯 Misiones, ⚜️ Facciones, 📣 Mostrar en la zona y ↩️ Volver.
- **🎭 Origen** abre la elección si no tienes origen; si ya lo tienes, su tarjeta (frase, rasgo, regalo y cuánto llevas de su historia). Se usa 🎭 porque es el emoji del origen en toda la historia.

## 4. 🧑‍🏫 Entrenador

Lo pidió el dueño: "cuando el jugador vuelve, le presenta los oficios" y le cuenta que aprenderá más a medida que avance.

**Desde la 0.33 (D-257, D-259), corto:**
- **Cómo se aprende:** una vez, pagando su primera receta; después sube haciendo recetas. La recolección y la exploración suben solas.
- **✅ Tus oficios** con su rango, y abajo **📚 los que te faltan por aprender**.
- **Más adelante:** 🏗️ Construcción con tu propio campamento y la 🎓 especialización al rango 25 y la segunda al 75.
- Botones: 📋 Mis oficios (una línea por oficio con su código), 📚 Aprender oficios, 🎓 Especialización y ↩️ Volver. El ✨ Encantamiento ya no tiene botón aquí: se aprende como los demás. Se abre también con /entrenador y estando ocupado.

Antes (0.29 a 0.32) presentaba cada familia con sus oficios ("se aprende haciéndolo, sin pagar ni elegir", D-57) y tenía los botones ⚒️ Mis oficios, 🎓 Especialización, ✨ Encantamiento y ↩️ Volver.

El camino guiado (D-190) puede mandar al jugador aquí después de fundar su campamento.

## 5. ❓ Dudas

"Una IA que, cuando le mencionas algo, te muestra preguntas ya respondidas; con un código se llama la respuesta" (D-191). Por ahora es un **buscador por palabras** (E-129): gratis e instantáneo; una IA de verdad, si se decide, llega después.

- **Catálogo:** 55 preguntas en 7 temas (🌱 Primeros pasos, 🧭 Mapa y exploración, ⚔️ Peleas y salud, 👤 Tu héroe, 🏕️ Campamentos, ⚒️ Oficios, 💰 Monedas y comercio), en `content/faq.yaml`. Cada una tiene un **código fijo** (/d01 a /d55), palabras clave, su tema y hasta 3 relacionadas. Los textos van en `content/locales/es_dudas.yaml`.
- **Buscar:** con la pantalla de ❓ Dudas abierta, lo que escribes es una búsqueda; también /dudas y una palabra desde cualquier lado. La búsqueda ignora tildes y mayúsculas, quita palabras vacías ("cómo", "qué", "para"...) y acepta formas parecidas ("cocinar" encuentra "cocina"; "mazmorras", "mazmorra"). Salen las preguntas que coinciden, de la más a la menos parecida, cada una con su código; con un solo resultado se ve la respuesta directo.
- **Responder:** /d07 (o "d07", o tocar la pregunta) muestra la respuesta, sus relacionadas con su código y botones para ir a ellas, al tema o a ❓ Dudas.
- **Los números de las respuestas** (energía, tiempos, costos, niveles) salen de `content/balance.yaml` al mostrarse: un cambio de balance nunca deja una respuesta vieja.
- **Regla:** cada sistema nuevo del juego agrega su pregunta en el mismo cambio, con el siguiente código libre. Los códigos nunca se renombran ni se reutilizan (se pueden compartir entre jugadores).

## 6. Reglas de los centros

1. **Hasta 8 botones de 2 en 2** solo en los centros (🏕️ Campamento, 🏰 Gestionar, 👤 Héroe, ❓ Dudas y, desde la 0.36, 🛡️ Gremio antes del campamento); las demás pantallas siguen con 4 (D-75), el combate con 6 (D-46) y las cantidades con su fila de botoncitos (D-189). No hace falta ningún campo nuevo en la vista: los clientes ya dibujan los botones de 2 en 2 ([Web y multiplataforma](web-y-multiplataforma.md) §3.3).
2. **Una línea por opción**, en el mismo orden que los botones; los costos y tiempos van en la línea, nunca en el botón.
3. **No esconder, explicar:** si una opción no se puede donde estás, el botón queda y dice por qué y dónde.
4. **Volver con sentido:** las pantallas de 🏰 Gestionar vuelven a 🏰 Gestionar; las del centro (🍲, 🛠️, 🏘️, 📜, 🧑‍🏫, ❓), al centro.

## 7. Preguntas abiertas

- **P-133 / E-134:** cómo se reparten los botones de tu campamento, que no caben en 8 (recomendado: el centro con lo de D-191 y 🏰 Gestionar como segunda pantalla).
- **P-128 / E-129:** ❓ Dudas con IA de verdad más adelante.
