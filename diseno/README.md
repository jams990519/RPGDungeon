# Diseño del juego: *Ascendentes* (nombre provisional)

**Un MMORPG completo por turnos, en texto, para Telegram.**
- Las clases y los sistemas de World of Warcraft, corregidos para que las clases valgan lo mismo.
- Una Torre de 100 pisos al estilo Sword Art Online, que los jugadores **fundan desde cero**, conquistan juntos y pueden dividir en castillos rivales.
- Jefes con la dificultad de Elden Ring.
- Un cuerpo que se hiere y se enferma, y que curan profesionales que estudiaron.
- Una economía de jugadores al estilo Albion, con lugares escasos que se pujan.
- Más de 50 roles para que cada persona sea alguien en el mundo.

| | |
|---|---|
| **Bot** | [@thetowerwarbot](https://t.me/thetowerwarbot), un bot distinto de @TowerWarsBot. **TowerWars no se toca** |
| **Estado** | Diseño. **Todavía no hay código** y **no se despliega nada en Railway** |
| **Idioma** | Español (el juego, en español e inglés) |

---

## Cómo leerlo

1. **[00 · Visión](00-vision/README.md):** empieza aquí. Pilares, roles, red de sistemas, decisiones, **preguntas para el dueño** y hoja de ruta.
2. Después, los módulos en orden, o el que te interese.
3. **[Glosario](00-vision/glosario.md)** para los términos propios.

## Módulos

| Módulo | De qué trata | Documentos |
|---|---|---|
| [00 · Visión](00-vision/README.md) | Qué es, qué está decidido, qué falta, cómo se conecta todo, en qué orden se construye | Pilares, roles, red de sistemas, catálogo ampliado, decisiones, preguntas, hoja de ruta, glosario |
| [01 · Plataforma](01-plataforma/README.md) | Telegram, arquitectura modular (sin código), anti-trampas | 3 |
| [02 · Mundo](02-mundo/README.md) | **Fundación desde cero, nodos y cismas**, ciudades y Castillo con entrenadores, crisis, **geografía y yacimientos únicos**, la Torre de 100 pisos, mundo vivo, rumores, facciones | 7 |
| [03 · Personaje](03-personaje/README.md) | Linajes, trasfondos, 15 clases y 46 specs, **balance**, talentos, equipo, descubrimiento y colecciones, progresión a dos años | 7 |
| [04 · Combate](04-combate/README.md) | Rondas simultáneas, barras, filas, estados por acumulación, partes del cuerpo, avisos, tácticas automáticas | 3 |
| [05 · Salud](05-salud/README.md) | Heridas por zona, condiciones, enfermedades y epidemias, mente, secuelas y muerte, **curación como oficio**, rasgos adquiridos, animales y cultivos | 8 |
| [06 · Contenido](06-contenido/README.md) | Misiones, expediciones, mazmorras, bandas, jefes estilo Elden Ring, **cacerías**, **investigaciones**, **crimen y justicia**, eventos, PvP | 8 |
| [07 · Economía](07-economia/README.md) | Economía, **mercado capitalista con lugares escasos**, oficios, **profundidad de un oficio** (carpintería), fabricación, monetización | 6 |
| [08 · Social](08-social/README.md) | Gremios, **apuestas legales e ilegales**, minijuegos con los formatos longevos de Telegram | 3 |
| [09 · Construcción](09-construccion/README.md) | **Construcción como oficio**, casa propia con taller, obras de gremios y organizaciones, construir el Castillo, defensa | 4 |
| [99 · Referencias](99-referencias/README.md) | De dónde sale cada idea, investigación con fuentes, lecciones de TowerWars | 4 |

## Convenciones

- **Cada carpeta es un módulo** con su README: qué contiene, de qué depende, a qué alimenta y qué preguntas tiene abiertas.
- **Cada documento empieza con una línea de módulo** (a qué módulo pertenece, de qué depende y con qué se conecta) y casi siempre con una sección **"De dónde sale"**, que dice qué juego inspira cada idea.
- **Preguntas** con número (P-xx) en [preguntas-abiertas.md](00-vision/preguntas-abiertas.md); **decisiones** con número (D-xx) en [decisiones.md](00-vision/decisiones.md).
- Las carpetas siguen el mismo orden que los módulos de código previstos (ver [Arquitectura modular](01-plataforma/arquitectura-modular.md)).
