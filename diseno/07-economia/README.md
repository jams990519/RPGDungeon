# 07 · Economía y oficios

Una economía al estilo Albion (casi todo lo fabrican jugadores, los mercados son locales y el equipo se gasta y se pierde) con herramientas de WoW (pedidos de fabricación, profesiones con especialización) y de EVE (contratos, seguros, informe económico). Los oficios son una forma completa de jugar durante años.

| Documento | Qué contiene |
|---|---|
| [economia.md](economia.md) | Principios (sumideros siempre en porcentaje), 4 monedas, mercados locales, recursos regionales, transporte y bandidos, Mercado Negro, contratos, Enfoque, informe económico, **mecanismos de otros juegos** |
| [propiedad-y-concesiones.md](propiedad-y-concesiones.md) | **Mercado capitalista:** puestos, locales, parcelas y licencias escasos; subastas; tasa autodeclarada; crédito e intereses; contrapesos |
| [profesiones.md](profesiones.md) | **§0: la fase 1, ya en el juego (D-109):** 15 oficios encadenados (recolectar → refinar → fabricar) con rango 1-100, 36 recetas, estaciones en el Claro y en el campamento, ⚒️ Oficios y /oficios; §0.6: las 🎓 especializaciones en el juego (D-141). **§0.4, fase 2 del lado del campamento (D-115), también en el juego:** 🎣 Pescador, 🍲 Cocina, 🗿 Cantería y 🏗️ Construcción, con beneficios de campamento (rige el mejor rango entre los miembros) y las defensas que dañan las oleadas. El resto, propuesta: recolección (incluidas Agricultura y Ganadería), refinado, 11 oficios mayores (con Construcción y Medicina), menores, límites, rangos, especializaciones, maestrías, **entrenadores y exámenes**, **cobrar por trabajar** |
| [oficios-repaso-2-oct.md](oficios-repaso-2-oct.md) | **El repaso de oficios del dueño (D-194, D-195), solo diseño:** cada oficio con su recolección, refinado y fabricación; recolectores con variedad (común, del terreno, raro) que mejoran sus nodos; el refinado pasa a ser estructuras del asentamiento con trabajadores; tres armaduras y tres oficios que las fabrican (D-208 quitó la malla y el Mallero); Ladrón, Agricultura y Ganadería; la granja de cada etapa del asentamiento. Del 2-oct: el Joyero refina las gemas desde la mena del Minero (D-198, sin Gemólogo), ranuras solo en armaduras y armas (D-199) y la comida de la granja la comen los aldeanos (D-205). Lo pendiente, en las preguntas E-137 a E-160 y E-169 |
| [red-de-oficios.md](red-de-oficios.md) | **La red completa (D-115):** 26 oficios (8 de recolección, 6 de refinado, 12 de fabricación) y Comercio, 3 especializaciones por oficio (§3.1: en el juego, una al rango 25 y otra al 75, D-141), quién necesita a quién, los ciclos que mantienen el sistema y en qué orden entran al juego (las fases 1, 1.5 y el lado del campamento de la 2 y las especializaciones, en el juego) |
| [profundidad-de-un-oficio.md](profundidad-de-un-oficio.md) | Las 10 capas de un oficio profundo y la **Carpintería** como ejemplo completo: perderse meses siendo carpintero del castillo |
| [fabricacion.md](fabricacion.md) | Minijuego por turnos (estilo FFXIV), fabricación rápida, calidad de las vetas (estilo SWG), recetas y descubrimiento, planos, estaciones, trabajadores, obras maestras, un ejemplo completo |
| [monetizacion.md](monetizacion.md) | Qué se vende y qué nunca, Telegram Stars, la ficha, juegos de azar y ley, calendario |

**Depende de:** [Mundo](../02-mundo/README.md) (mercados locales, vetas, transporte), [Equipamiento](../03-personaje/equipamiento.md).
**Alimenta a:** [Personaje](../03-personaje/README.md) (equipo), [Salud](../05-salud/README.md) (servicios médicos), [PvP](../06-contenido/pvp.md) (riesgo y recompensa).

**Preguntas abiertas:** P-32 a P-40 y P-53 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).

**En el código:** `content/professions.yaml`, `engine/professions/` y la sección "professions" de `engine/service/game.py` (fase 1 de los oficios, D-109). Lo que sigue es el mercado entre jugadores (segunda tanda), para que cada uno venda lo que hace.
