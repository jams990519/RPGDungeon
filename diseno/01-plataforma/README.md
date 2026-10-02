# 01 · Plataforma

Dónde vive el juego (Telegram primero, también la web y la app móvil), cómo se parte en piezas (arquitectura modular) y cómo se protege (anti-trampas). Este módulo **condiciona a todos los demás**: cualquier sistema que no funcione en cualquier cliente de texto por turnos no entra.

| Documento | Qué contiene |
|---|---|
| [telegram.md](telegram.md) | Lo que Telegram permite y prohíbe, los diez principios de diseño, dónde ocurre cada cosa, carga del servidor |
| [arquitectura-modular.md](arquitectura-modular.md) | Los 25 módulos del juego, quién depende de quién, eventos entre módulos, herramientas de administración (sin código) |
| [web-y-multiplataforma.md](web-y-multiplataforma.md) | Un mundo y un motor con varios clientes (Telegram, web, Mini App, app móvil): capas, vistas neutras, cuentas vinculadas, juego cruzado, tabla de equivalencias de cada función de Telegram, avisos, seguridad, orden sugerido |
| [convenciones-de-codigo.md](convenciones-de-codigo.md) | Código en inglés con notas `[ES]` en español: encabezados, notas por función y por archivo de datos, cómo avisar el impacto de un cambio (D-42) |
| [mapa-de-impacto.md](mapa-de-impacto.md) | Qué se mueve cuando se cambia algo: dependencias por módulo, números y pantallas, para avisar antes de editar (D-42) |
| [menus-campamento-y-heroe.md](menus-campamento-y-heroe.md) | Los menús de la 0.29 (D-190 a D-192): el menú de abajo sin 📖 Historia, los centros de 🏕️ Campamento y 👤 Héroe (hasta 8 botones de 2 en 2, estilo TowerWars), 🏰 Gestionar, el 🧑‍🏫 Entrenador y ❓ Dudas con sus códigos /d01 |
| [seguridad-y-anti-trampas.md](seguridad-y-anti-trampas.md) | Multicuentas, bots, comercio con dinero real, sanciones, privacidad, moderación |

**Preguntas abiertas de este módulo:** P-44 (Mini App), P-45 (Vigor), P-46 (tecnología), P-47 (presupuesto), P-48 (API pública), P-58 a P-60 (web), P-61 y P-62 (app móvil), P-133 (botones de tu campamento). Ver [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
