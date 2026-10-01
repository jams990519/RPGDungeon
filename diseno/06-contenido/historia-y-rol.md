# Historia y rol: lo que hace largo al juego

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Creación de personaje](../03-personaje/creacion-de-personaje.md) (trasfondos), [Misiones y exploración](misiones-y-exploracion.md), [Roles y caminos de juego](../00-vision/roles-y-caminos-de-juego.md) · **Alimenta a:** [Progresión](../03-personaje/progresion.md), [Gremios y social](../08-social/gremios-y-social.md), [Campamentos](../02-mundo/fundacion-y-cisma.md) · **Estado:** propuesta para programar (D-117, provisional)

**De dónde sale.**
- *Fallen London* y las aventuras de texto: historias con decisiones, escritas para leerse en el teléfono.
- *World of Warcraft*: campañas por zona, facciones con reputación y títulos.
- *Dragon Age: Origins*: un origen propio para cada héroe, con su primera historia.
- *The Witcher*: dilemas cuyas consecuencias se ven después.
- *Chat Wars* y los MMO de rol en Telegram: el rol entre jugadores hace la comunidad.

**Qué pidió el dueño (1-oct-2026).** "No me interesa que el progreso sea lento. Quiero más bien que el juego sea un roleplay con RPG; o sea, debe ser largo." Se tomó así: **lo largo tiene que salir de la historia y del rol**, no de subir de nivel despacio. El progreso se siente seguido (siempre hay algo que ganar), y lo que dura años es todo lo que hay para vivir: la historia del mundo, el propio personaje, las facciones, los oficios, el campamento y el castillo.

---

## 1. La capa simple para programar (en orden)

1. **🎭 El origen del héroe.** Al crearlo se elige de dónde viene, entre 5 o 6 trasfondos de [Creación de personaje](../03-personaje/creacion-de-personaje.md) §4: por ejemplo, superviviente del Colapso, hijo de artesanos, desertor o peregrino.
   - Cada origen da una frase de presentación, un rasgo chico (algo de oficio o de mundo, nunca de poder de combate) y su **cadena de misiones de origen**: 3 o 4 misiones narrativas que presentan el mundo y a sus personajes.
   - Los héroes ya creados lo eligen la primera vez que entran después del parche, sin perder nada.
2. **📖 La campaña principal por capítulos.** La historia del Colapso y del misterio de la Lejanía.
   - Cada capítulo tiene de 5 a 8 misiones narrativas con **decisiones que cambian algo**: la reputación con una facción, qué personaje te ayuda después, una recompensa u otra.
   - El capítulo 1 pasa en el Claro y sus alrededores, el 2 cuando se abre la región de Raigambre, y así con cada región y Guardián. Se escribe un capítulo por parche grande.
3. **🧑 Personajes con nombre.** El mercader, la posadera, una sanadora, un viejo explorador y un herrero del Claro tienen nombre, voz y diálogos cortos. Dan misiones, recuerdan lo que elegiste y cambian lo que te dicen.
4. **⚜️ Facciones y reputación.** Tres facciones al empezar (por ejemplo, los que quieren reconstruir, los que buscan el poder de la Lejanía y los que viven de lo que queda).
   - Las misiones, las decisiones y lo que haces suben o bajan tu reputación, por rangos: de Desconocido a Héroe.
   - Cada rango da algo: un título, una receta, una pieza de equipo o un lugar al que solo ellos te dejan entrar.
   - Más adelante, los campamentos y gremios se pueden alinear con una facción.
5. **📜 Encargos del tablón.** Encargos cortos de los personajes, que rotan cada día: cazar, recolectar, llevar algo o investigar. También hay **encargos de campamento**, que se hacen entre los miembros: es la parte de misiones con el campamento que ya estaba en la cola.
6. **📔 El diario del héroe.** Una crónica de lo que hiciste (el primer Guardián, el campamento que fundaste, las decisiones de la campaña, tus títulos), que puedes mostrar a otros jugadores.
7. **🎭 Rol entre jugadores** (de [Roles y caminos de juego](../00-vision/roles-y-caminos-de-juego.md) §3):
   - una biografía corta que escribes tú;
   - el emblema de tu rol junto al nombre ("⚕️ Lyra, Médica");
   - gestos narrados en tu zona (`/saludar`, `/brindar`, `/pregonar`);
   - la tarjeta de presentación reenviable.

## 2. El ritmo: progreso seguido, juego largo

- **Siempre hay algo cerca:** cada sesión corta da algo (un paso de misión, un rango de oficio, una mejora del campamento, un nivel en los primeros días).
- **Los niveles acompañan a la historia:** el nivel de cada capítulo marca el ritmo; no hace falta repetir lo mismo para pasar de un capítulo a otro.
- **Lo que dura años:**
  - la campaña completa, región por región;
  - los oficios hasta Gran Maestro;
  - el castillo con su gremio;
  - la reputación con todas las facciones;
  - las colecciones y los títulos;
  - el rol con los demás jugadores.
- **La velocidad de los niveles es decisión del dueño (P-77).** La propuesta: llegar al nivel 100 en unos 8 meses jugando todos los días, en vez de 2 años, sin cambiar que cada camino lleve al 100 a un ritmo parecido (D-108).

## 3. Cómo encaja con lo que ya está

| Lo que ya hay | Cómo lo usa la historia |
|---|---|
| El Claro, Raigambre, los biomas y los 105 enemigos | Escenarios y enemigos de los capítulos |
| Campamentos, gremios y oleadas | Encargos de campamento; capítulos donde tu campamento defiende algo |
| Oficios y beneficios | Misiones de oficio, recetas como premio de facción |
| Exploración y campamentos enemigos (en la cola) | Misiones de investigación e infiltración |
| Títulos y Pioneros | El diario y las recompensas de reputación |
