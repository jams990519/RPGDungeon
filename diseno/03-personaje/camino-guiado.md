# Camino guiado

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Creación de personaje](creacion-de-personaje.md), [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md), [Cacerías](../06-contenido/cacerias.md), [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) · **Alimenta a:** [Progresión](progresion.md), [Aprendizaje y pistas](../00-vision/aprendizaje-y-pistas.md), [Historia y rol](../06-contenido/historia-y-rol.md) · **Estado:** en el juego desde la 0.29 (D-190 confirmada; cómo se aplicó, D-193 provisional)

**Qué pediste (D-190).** La historia ya no es una opción del menú: el juego te va mandando a hacer **una acción a la vez**, cada vez que encuentras algo nuevo, y te explica lo justo. Primero el héroe (nombre y clase), después **dónde estás** (el Claro, la antorcha), **moverte**, en la zona nueva **explorar, recolectar y cazar**, el **🗺️ Mapa**, **volver al campamento**, el **campamento** y el **héroe**. Los tutoriales llegan **a medida que desbloqueas cosas, nunca todo de golpe**. Fundar campamento no se explica hasta que sales del Claro. El formato, como TowerWars: "bien ampliado, detallado y separado".

**De dónde sale.**
- **TowerWars** (el formato que pediste; se miró solo como referencia, sin tocar nada, D-01): título con emoji, secciones separadas, una cosa por línea; los avisos de "🌳 ¡Desbloqueaste…!" y la guía que muestra solo lo ya desbloqueado. Lost Realms va más guiado: un paso a la vez.
- ***World of Warcraft*** y ***Albion Online***: la primera media hora es una cadena de tareas cortas, cada una con su botón y su premio chico; las ventanas de ayuda salen la primera vez que ves algo (tu primera mazmorra, tu primera bolsa llena).
- **El tutorial viejo de pistas (D-56)**: lo que funcionaba (pasos chicos con premio) sigue; lo que cambió es que ahora dice el botón exacto, porque así lo pediste.

---

## 1. Cómo se ve

- **Al crear el héroe** sale **🔥 Llegaste al Claro**: dónde estás (el campamento base, la antorcha donde despiertan todos), que alrededor hay terrenos distintos (cada color del mapa es uno), que tendrás que moverte para investigar, juntar y hacer misiones, y **cómo moverte**: las 4 rutas, cuánto tarda cada viaje (2 minutos las zonas cercanas, más cuanto más lejos, hasta 20 por zona), que puedes cerrar el chat y que al llegar pueden salir monstruos. Los 4 botones son las rutas.
- **Un solo paso a la vez.** El paso de ahora sale como una línea **🧭 Ahora:** con el botón exacto, al final de 📍 Zona, 🧭 Explorar, 🏕️ Campamento, 👤 Héroe y el campamento enemigo (y una línea "📖 /guia" para volver a leer la explicación).
- **Al cumplir un paso**, el aviso dice **✅ Paso N de 11 hecho**, el premio (🎁 +5 🥉 · +20 de experiencia), lo que aprendiste (por ejemplo, cómo leer el mapa al abrirlo) y **👉 el paso siguiente** con su explicación.
- **/guia** muestra el paso de ahora con su explicación y su botón, y la lista de avisos que ya viste.

## 2. Los pasos (en este orden)

| N | Paso | Qué hay que hacer | Se cumple con | Botón de /guia |
|---|---|---|---|---|
| 1 | Moverte | Ir a una zona vecina | Llegar a una zona que no es el Claro | Las 4 rutas |
| 2 | Explorar | 🧭 Explorar → 🔎 Explorar (un lote cualquiera) | La primera vuelta de exploración | 🧭 Explorar |
| 3 | Recolectar | 🧭 Explorar → 🪓 Recolectar | La primera vuelta de recolección | 🧭 Explorar |
| 4 | Cazar | 🧭 Explorar → 🏹 Cazar → 🏹 Buscar presa | El final de una pelea de cacería, ganada o perdida | 🏹 Cazar |
| 5 | El mapa | 🧭 Explorar → 🗺️ Mapa | Abrir el mapa: ahí se explica todo lo que muestra (colores, 🕳️ 🌀, ✨, 👹, 🏕️, 👑, coordenadas y Lejanía, 📒 Lugares) | 🗺️ Mapa |
| 6 | Volver al Claro | 📒 Lugares → El Claro (o las rutas) | Llegar al Claro (o a tu campamento); si ya estás ahí, se da por hecho | 📒 Lugares |
| 7 | El campamento | 🏕️ Campamento | Abrirlo estando en el Claro: cocinar, investigar, fabricar, entrenador, mercader, posada y ❓ Dudas (D-191) | 🏕️ Campamento |
| 8 | El entrenador | 🏕️ Campamento → 🧑‍🏫 Entrenador | Tocar el botón (la pantalla la arma el campamento, D-191): se presentan los oficios y que aprenderás más a medida que avances | 🧑‍🏫 Entrenador |
| 9 | Tu héroe | 👤 Héroe | Abrirlo: talentos, mochila, estadísticas y salud. **Fin del camino básico** (te manda a ❓ Dudas) | 👤 Héroe |
| 10 | Buscar lugar | Salir del Claro y moverte una o dos zonas más | Llegar, con 2 zonas pisadas fuera del Claro desde el fin del camino básico, a un lugar que sirve para fundar (Lejanía 2 o más, sin territorio ni otro campamento cerca, sin campamento propio) | — |
| 11 | Fundar tu campamento | 🏕️ Campamento → 🏕️ Fundar campamento aquí, y escribirle un nombre | Fundarlo (el flujo de siempre); si entraste al campamento de otro, se da por hecho | 🏕️ Campamento |

- **Premio:** 5 🥉 y 20 de experiencia por paso (con el acelerador de 💎, la experiencia sube), una sola vez. El paso 10 no paga. En total, 50 🥉 y 200 de experiencia (el tutorial viejo daba 35 y 140).
- **Fundar campamento (D-190).** Mientras estás en el Claro no se dice nada. Al salir por primera vez después del camino básico, el aviso explica que el Claro no crece y tu campamento sí, y te pide moverte una o dos zonas más. Al llegar a un buen lugar: **"🏕️ ¡Encontraste un buen lugar para tu propio campamento!"** y la lista de lo que hace falta ahí (✅ / ▫️, las reglas de siempre: Lejanía, explorar al 100 %, 4 vecinas conocidas, no tener otro campamento cerca, 20 de madera y 10 de piedra). La línea 🧭 Ahora dice lo que falta en la zona donde estés. Al fundarlo, el **tutorial corto del campamento**: 🔨 Mejoras ("aquí está el botón de mejora"), 🏘️ Servicios (el mercader, la posada y el taller llegan con sus mejoras), 🧑‍🏫 Entrenador, ⬆️ Agrandar, las oleadas y 🛡️ Defender, y que aprenderás más oficios.

## 3. Los avisos de una sola vez

Salen **la primera vez** que pasa cada cosa, **de a uno por pantalla** (si pasan dos a la vez, el segundo sale en la pantalla siguiente) y nunca se repiten. Van al final de las pantallas principales; el de la primera pelea, en la pantalla del combate.

| Aviso | Cuándo sale | Qué dice |
|---|---|---|
| ⚔️ Tu primera pelea | En tu primer combate | Una acción por ronda, leer el ⚠️ aviso, 🎒 Mochila gasta el turno |
| 🩹 Caíste en combate | Al quedar malherido | La vida vuelve lento; poción, posada o esperar; 🩺 Salud |
| 🌟 Punto de talento | Al subir de nivel con un punto sin gastar | 👤 Héroe → 🌟 Talentos; el primero elige la especialización |
| ⚡ Energía | Con 10 ⚡ o menos | Se recupera sola (+1 cada 36 minutos); qué la gasta; invitar da más |
| 🎒 Mochila llena | Al llenarla | No se recolecta ni se compra; vender, fabricar o aportar |
| 🕳️ Mazmorras | Parado en una entrada | Chica y profunda; se entra desde 🧭 Explorar; cambian cada día |
| 👹 Campamento enemigo | Parado en uno | Bloquea la zona; ⚔️ Asaltar hasta el jefe y su cofre |
| ✨ Nodo de recursos | Al descubrir el primero | Rinde el doble y a veces da un raro; es fijo para todos |
| ⚒️ Oficios | Al subir el primer oficio de rango | Suben haciéndolos, sin tope; /oficios |
| 🛡️ Oleada | La primera oleada en tu campamento | 🛡️ Defender; qué se pierde y qué no |
| ⚙️ Peleas automáticas | Con 3 peleas ganadas, después del paso Cazar | ✋ Manual o ⚔️ Automática en ⚙️ Opciones |
| 🎭 Tu origen (opcional) | Al terminar el camino básico, si no tienes origen | Se elige con **/origen**, cuando quieras (E-131) |

## 4. Los jugadores de antes (E-133, respuesta provisional)

- Quien **terminó el tutorial viejo** o tiene **nivel 5 o más** tiene el camino básico hecho, **sin premio**. Igual recibe los avisos nuevos de lo que todavía no conoce, y el de fundar campamento si no tiene uno.
- Los demás empiezan en el primer paso que no hicieron a la vista: si ya están fuera del Claro o pisaron otra zona, moverte está hecho; si exploraron fuera del Claro, explorar; si pasaron el paso de recolectar del tutorial viejo, recolectar; si ganaron alguna pelea, cazar. Lo hecho a la vista no paga.
- Los avisos de lo que ya conocen quedan vistos (primera pelea, nivel 2, un oficio subido, un nodo, ⚙️ Opciones usadas, origen elegido, oleadas pasadas).
- **Nada se borra (D-64):** el índice del tutorial viejo queda guardado y se sigue leyendo; lo que se guarda del camino solo crece.

## 5. El origen y la historia (E-130, E-131)

- **El origen** ya no se elige al crear el héroe: el camino lo ofrece al final del camino básico, como paso opcional, con **/origen**. Quien ya lo eligió lo conserva.
- **La campaña** del capítulo 1, las facciones y el 📜 tablón siguen andando igual (sus misiones avanzan con lo que haces); dónde se ven ahora lo deciden los menús nuevos (D-191).

## 6. Dónde está en el código

- Pasos y avisos: `content/guide.yaml` (IDs estables: solo se agregan; para retirar, `retired: true`). Textos: `content/locales/es_guia.yaml`. Números: `content/balance.yaml` → `guide` (premio, nivel de veterano, movimientos antes de fundar, umbral de energía, peleas para el aviso de ⚙️ Opciones).
- Reglas: `engine/service/guide.py` (`GuideMixin`). Lo guardado: `Hero.guide` (`done`, `tips`, `away`).
- Un solo gancho, `_guide_event`, en explorar, recolectar, llegar, el final de cada pelea y fundar; los pasos de botón se miran antes de armar cada pantalla.
- Lo que se rompe si algo cambia: [mapa de impacto](../01-plataforma/mapa-de-impacto.md), cascada C-29. Pruebas: `tests/test_camino_guiado.py`.

## 7. Preguntas

- **E-135 (P-134):** dijiste que moverse no gasta energía, pero hoy cada viaje gasta 1 ⚡ (D-78). El texto del camino dice el número real; si lo pasamos a 0, cambia solo.
- Abiertas de antes: E-129 a E-133 (Dudas, lo que estaba en 📖 Historia, el origen, los 8 botones, los jugadores de antes). Aquí se aplican las recomendadas.
