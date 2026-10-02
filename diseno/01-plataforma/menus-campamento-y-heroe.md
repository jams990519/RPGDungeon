# Menús: 🏕️ Campamento, 👤 Héroe, 🧑‍🏫 Entrenador y ❓ Dudas

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Web y multiplataforma](web-y-multiplataforma.md) §3 (vistas neutras), [Decisiones](../00-vision/decisiones.md) D-190, D-191 y D-192 · **Alimenta a:** todos los módulos que tienen pantallas en el campamento o en el héroe · **Estado:** en el juego desde la 0.29 (D-190 y D-191 confirmadas; cómo se aplican, D-192 provisional)

Cómo se ordenan las pantallas principales del juego desde la 0.29: el menú de abajo, el centro de 🏕️ Campamento (en el Claro y en tu propio campamento), el centro de 👤 Héroe, el 🧑‍🏫 Entrenador y ❓ Dudas. El camino guiado de la historia (D-190), que manda al jugador a hacer una cosa nueva por vez, se describe aparte.

## De dónde sale

- **TowerWars actual** (pedido del dueño, D-190): "bien ampliado, detallado y separado". Cada sección abre su propio grupo de botones (un "centro") con todas sus opciones a la vista, de 2 en 2; los costos y tiempos van en el texto, no en el botón; lo que no se puede todavía no se esconde: explica por qué. La ficha del héroe muestra cada número como actual/máximo con su tiempo ("❤️ Vida: 80/120 (llena en 3 min)"). De TowerWars solo se toman ideas (D-01): el resumen está en el estudio del 2-oct-2026.
- **El dueño** (D-191): el campamento tiene, en orden, cocinar, investigar y fabricar (lo que no está en el héroe), un entrenador que presenta los oficios y un botón de ❓ Dudas que muestra preguntas ya respondidas, con un código para llamar cada respuesta. El héroe tiene todo lo del personaje.
- **Las pistas de los MMO de texto** (Chat Wars, TowerWars): los atajos con "/" que el jugador escribe o toca en el texto. En Telegram, un /d07 dentro del mensaje se toca como un enlace.

## 1. El menú de abajo

5 botones, de 2 en 2 (filas de 2, 2 y 1): **📍 Zona · 🧭 Explorar · 🏕️ Campamento · 👤 Héroe · ⚙️ Opciones**.

- **📖 Historia salió** (D-190): la historia ahora te guía mientras juegas. Lo que estaba ahí se repartió (E-130): el 📔 Diario con 🎯 Misiones y ⚜️ Facciones pasó a 👤 Héroe; el 📜 Tablón de encargos y 🧑 Personajes, a 🏕️ Campamento.
- **Nada viejo se rompe:** el botón 📖 Historia de un teclado viejo, /historia y el texto "📖 Historia" abren el 📔 Diario con un aviso de una línea que dice dónde quedó todo.
- **Crear el héroe** pide solo el nombre y la clase (D-190); al terminar se entra directo al juego. El origen se elige cuando quieras en 👤 Héroe → 🎭 Origen (E-131); quien ya lo tenía lo conserva. El camino guiado puede ofrecerlo una vez.

## 2. 🏕️ Campamento

Un **centro** (D-192): arriba, una línea por opción con lo que hace y sus números; abajo, sus botones, hasta 8 de 2 en 2 (E-132), en el orden que pidió el dueño.

### 2.1 En el Claro

| Botón | Qué hace | Si no se puede |
|---|---|---|
| 🍲 Cocinar | La estación de la 🍲 Cocina: carne, pescado y lo de cada terreno se vuelven raciones y guisos (rinden más en la despensa de un campamento) | — (el Claro tiene todas las estaciones básicas) |
| 🔬 Investigar | El 📚 Conocimiento de un campamento | El Claro no crece (D-98): el botón explica que se investiga en tu campamento, con la 📚 Biblioteca y desde qué nivel |
| 🛠️ Fabricar | ⚒️ Oficios: 🪚 Refinar y 🛠️ Fabricar en las estaciones de aquí | — |
| 🧑‍🏫 Entrenador | Presenta los oficios (§4) | — |
| 🛒 Mercader | Pociones, vendas, 🥖 provisiones; compra materiales | — |
| 🛏️ Posada | Dormir y despertar con la vida llena (precio y tiempo en el texto) | Con la vida llena no cobra |
| 📜 Tablón | Los 3 encargos de hoy y, con campamento, los de la semana | — |
| ❓ Dudas | Buscar respuestas (§5) | — |

Debajo va la pista de siempre: el Claro no crece; para crecer, funda tu campamento.

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
🏰 Guerrero · Defensa
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

- **Cómo se aprende:** haciéndolo, sin pagar ni elegir, y sin tope (D-57).
- **Cada familia, en orden**, con lo que hace y sus oficios (con tu rango si ya lo empezaste): 🪓 recolección, 🧭 exploración, 🪚 refinado, 🛠️ fabricación, 💱 servicio y ✨ encantamiento.
- **Cuántos puedes empezar hoy** y **lo que llega más adelante:** 🏗️ Construcción con tu propio campamento, la 🎓 especialización al rango 25 y la segunda al 75, y recetas nuevas con cada rango.
- **Dónde:** si hay estaciones donde estás.
- Botones: ⚒️ Mis oficios, 🎓 Especialización, ✨ Encantamiento y ↩️ Volver. Se abre también con /entrenador y estando ocupado (es solo para leer).

El camino guiado (D-190) puede mandar al jugador aquí después de fundar su campamento.

## 5. ❓ Dudas

"Una IA que, cuando le mencionas algo, te muestra preguntas ya respondidas; con un código se llama la respuesta" (D-191). Por ahora es un **buscador por palabras** (E-129): gratis e instantáneo; una IA de verdad, si se decide, llega después.

- **Catálogo:** 55 preguntas en 7 temas (🌱 Primeros pasos, 🧭 Mapa y exploración, ⚔️ Peleas y salud, 👤 Tu héroe, 🏕️ Campamentos, ⚒️ Oficios, 💰 Monedas y comercio), en `content/faq.yaml`. Cada una tiene un **código fijo** (/d01 a /d55), palabras clave, su tema y hasta 3 relacionadas. Los textos van en `content/locales/es_dudas.yaml`.
- **Buscar:** con la pantalla de ❓ Dudas abierta, lo que escribes es una búsqueda; también /dudas y una palabra desde cualquier lado. La búsqueda ignora tildes y mayúsculas, quita palabras vacías ("cómo", "qué", "para"...) y acepta formas parecidas ("cocinar" encuentra "cocina"; "mazmorras", "mazmorra"). Salen las preguntas que coinciden, de la más a la menos parecida, cada una con su código; con un solo resultado se ve la respuesta directo.
- **Responder:** /d07 (o "d07", o tocar la pregunta) muestra la respuesta, sus relacionadas con su código y botones para ir a ellas, al tema o a ❓ Dudas.
- **Los números de las respuestas** (energía, tiempos, costos, niveles) salen de `content/balance.yaml` al mostrarse: un cambio de balance nunca deja una respuesta vieja.
- **Regla:** cada sistema nuevo del juego agrega su pregunta en el mismo cambio, con el siguiente código libre. Los códigos nunca se renombran ni se reutilizan (se pueden compartir entre jugadores).

## 6. Reglas de los centros

1. **Hasta 8 botones de 2 en 2** solo en los centros (🏕️ Campamento, 🏰 Gestionar, 👤 Héroe y ❓ Dudas); las demás pantallas siguen con 4 (D-75), el combate con 6 (D-46) y las cantidades con su fila de botoncitos (D-189). No hace falta ningún campo nuevo en la vista: los clientes ya dibujan los botones de 2 en 2 ([Web y multiplataforma](web-y-multiplataforma.md) §3.3).
2. **Una línea por opción**, en el mismo orden que los botones; los costos y tiempos van en la línea, nunca en el botón.
3. **No esconder, explicar:** si una opción no se puede donde estás, el botón queda y dice por qué y dónde.
4. **Volver con sentido:** las pantallas de 🏰 Gestionar vuelven a 🏰 Gestionar; las del centro (🍲, 🛠️, 🏘️, 📜, 🧑‍🏫, ❓), al centro.

## 7. Preguntas abiertas

- **P-133 / E-134:** cómo se reparten los botones de tu campamento, que no caben en 8 (recomendado: el centro con lo de D-191 y 🏰 Gestionar como segunda pantalla).
- **P-128 / E-129:** ❓ Dudas con IA de verdad más adelante.
