# Idiomas: el juego en español y en inglés

> **Módulo** [01 · Plataforma](README.md) · **Depende de:** [Web y multiplataforma](web-y-multiplataforma.md) §3.3 regla 5, [Convenciones de código](convenciones-de-codigo.md) §4 · **Alimenta a:** todos los módulos que muestran texto · **Estado:** confirmado por el dueño (D-250, 17-oct-2026) y en el juego desde la 0.33; cómo se aplicó, provisional (D-251)

El dueño pidió el juego también en inglés: "añadas la traducción al inglés y la opción en un menú de escoger el idioma y que puedes cambiar de idioma si lo deseas. Dale empezar el juego y dentro del juego en sí. Asegura de traducir cada una de las acciones de los jugadores y demás. Todo." (D-250).

---

## 1. Qué ve el jugador

- **Al empezar.**
  - La primera pantalla (al tocar /start sin héroe) trae dos botones: 🇪🇸 Español y 🇬🇧 English.
  - La pregunta "🌐 Elige tu idioma…" sale en los dos idiomas, porque todavía no sabemos cuál lee el jugador.
  - Si toca uno, la misma pantalla se vuelve a escribir en ese idioma y sigue pidiendo el nombre.
  - Si escribe el nombre sin tocar ninguno, sigue en español.
- **Dentro del juego.**
  - Se cambia en ⚙️ Opciones → 🌐 Idioma, o escribiendo /idioma o /language.
  - La pantalla 🌐 marca el idioma en uso con ✅.
  - Al elegir otro, vuelve a ⚙️ Opciones ya en el idioma nuevo, y en Telegram también cambia el teclado de abajo.
- **Qué cambia.** Todo lo que el juego escribe: pantallas, botones, el menú de abajo, combate, enemigos, objetos, historia, ❓ Dudas (con palabras de búsqueda en inglés), avisos, pistas y notas de parche.
- **Qué no cambia.** Lo que escriben los jugadores: nombres de héroe, campamento y gremio, biografías y brindis.
- **Jugar juntos.**
  - Dos jugadores en idiomas distintos se ven, se saludan y comparten campamento.
  - Cada uno lee todo en el suyo, también los avisos que provoca el otro: un saludo, la oleada, una mejora construida o el informe de la partida de caza.
- **Los que ya jugaban** siguen en español sin que se les pregunte (D-251).

## 2. Cómo está hecho

| Pieza | Dónde | Qué hace |
|---|---|---|
| Un catálogo por idioma | `content/locales/es*.yaml` y `en*.yaml` | Las mismas claves en los dos. El español es la referencia |
| `Content.locales` | `engine/core/content.py` | Carga todos los idiomas: cada `<código>.yaml` sin "_" más sus `<código>_*.yaml` |
| `Texts.use(lang)` | `engine/core/i18n.py` | Fija el idioma de lo que se está atendiendo (una variable de contexto). Ninguna de las miles de llamadas a `t.t(...)` tuvo que cambiar |
| Respaldo | `engine/core/i18n.py` | Si una clave falta en inglés, sale la española y se anota en `Texts.fallbacks`. Las pruebas exigen que quede vacío |
| El idioma de cada cuenta | espacio `prefs` del almacén (`{"lang": "en"}`) | Se guarda por cuenta, antes de que exista el héroe |
| Entradas del motor | `GameService.view`, `text`, `act` (decorador `_in_player_language`), `tick`, `menu(account)`, `announcement_view(account)` | Cada una atiende en el idioma de su jugador |
| Avisos para otros | `GameService._push_each(destinatarios, armar)` | Arma el aviso una vez por destinatario, en su idioma. `armar` solo escribe textos y no cambia nada del juego |
| Atajos | `COMMANDS` y `TYPED_ALIASES` en `game.py` | Cada atajo tiene su nombre en inglés (tabla del §4) y los dos sirven para todos |
| Notas de parche | `content/patches.yaml`: `title_en` y `notes_en` | Cada jugador recibe las de su idioma. Un parche sin ellas sale en español |
| ❓ Dudas | `content/faq.yaml`: `keywords_en` | Se busca con las palabras del idioma del jugador y, además, con las españolas |
| Nombres de zona | `world.name_format` | "{first} {second}" en español ("Vado Gris") y "{second} {first}" en inglés ("Grey Ford"). Las dos listas tienen 12 palabras en el mismo orden, así una zona es el mismo lugar en los dos idiomas |
| Decimales | `common.decimal_sep` | 1,5 en español y 1.5 en inglés (`GameService._num`) |
| Telegram | `adapters/telegram/bot.py` | Teclado de abajo por jugador (`menu_keyboard(service, account)`). Entiende los botones viejos de cualquier idioma (`menu_labels`). Cambia el teclado cuando una vista trae `meta["menu_changed"]` y manda el aviso del parche en el idioma de cada uno |

## 3. Las reglas (D-251)

1. **Toda clave nueva va en los dos idiomas en el mismo cambio:** primero en `es*.yaml` y después en el `en*.yaml` que le corresponde. `python tools/check_locales.py` tiene que dar 0 errores; `tests/test_idiomas.py` lo exige.
2. **Mismas claves, mismos huecos, mismas etiquetas:**
   - Los huecos `{nombre}` y los plurales `{n|uno|varios}` se mantienen; en inglés: `{n|time|times}`.
   - Las etiquetas HTML no cambian.
   - Las listas que el motor lee por posición (`world.name_first`, `world.name_second`, `dungeon.rooms`, `dungeon.boss_rooms`) tienen el mismo largo.
3. **Nombres propios:**
   - Los de personajes y seres únicos se quedan como están (Raigambre, Marta, Odo, Iria, Anselmo, Brena).
   - Los descriptivos se traducen («Espada de Raíz Viva» → «Living Root Sword»).
4. **Un aviso para otro jugador** se arma con `_push_each`, nunca armándolo antes del bucle, porque saldría en el idioma de quien lo provoca.
5. **El glosario de la traducción** fija el inglés de cada término del juego (el Claro → the Clearing, campamento → camp, Gastador → Spender…). Está en el encabezado de cada `en*.yaml` y en la tabla del §4.
6. **El diseño (`diseno/`) sigue en español,** igual que las notas `[ES]` del código.

## 4. Términos y atajos

| Español | Inglés | | Español | Inglés |
|---|---|---|---|---|
| 📍 Zona | 📍 Zone | | /dudas | /help (o /faq) |
| 🧭 Explorar | 🧭 Explore | | /monedas | /coins |
| 🏕️ Campamento | 🏕️ Camp | | /oficios | /professions |
| 👤 Héroe | 👤 Hero | | /opciones | /options |
| ⚙️ Opciones | ⚙️ Options | | /historia, /diario | /story, /journal |
| ❓ Dudas | ❓ Help | | /encargos | /board |
| el Claro | the Clearing | | /saludar, /brindar | /greet, /toast |
| 🔥 fogata (antes «hoguera», D-311) | 🔥 campfire | | /habilidades | /skills |
| mazmorra chica / profunda | small / deep dungeon | | /zona, /equipo | /zone, /gear |
| oleada · Noche de prueba | wave · Trial Night | | /doble, /gremio, /salud | /dual, /guild, /health |
| Básico · Constructor · Preparador · Gastador | Basic · Builder · Primer · Spender | | /encantar, /especialidad | /enchant, /specialty |
| Tanque · Sanador · DPS · Soporte | Tank · Healer · DPS · Support | | /reconocer, /entrenador | /recon, /trainer |
| bronce · plata · oro | bronze · silver · gold | | /guia, /origen | /guide, /origin |
| Guerrero · Paladín · Druida | Warrior · Paladin · Druid | | /idioma | /language |
| Cazador · Sacerdote · Mago | Hunter · Priest · Mage | | /ir1, /ir2… | /go1, /go2… |
| 📋 Mis oficios | 📋 My professions | | /misoficios, /aprender | /myprofessions, /learn |
| 📚 Aprender oficios | 📚 Learn professions | | /feedback | /feedback |

/stats, /inv, /hero, /bio, /start y los códigos son iguales en los dos idiomas: ❓ Dudas (/d07), 📦 Recursos (/07), vender al mercader (/v07) y los oficios (/minero, /cocina: el código es el id del oficio).

## 5. Para agregar un idioma más

1. Copiar `en.yaml` y cada `en_*.yaml` como `<código>.yaml` y `<código>_*.yaml`, y traducirlos. El juego lo encuentra solo.
2. Agregar `keywords_<código>` en `content/faq.yaml` y `title_<código>`/`notes_<código>` en las notas de parche nuevas.
3. Correr `python tools/check_locales.py`, que compara el español con cada idioma, y las pruebas.

## De dónde sale

- **El pedido es del dueño** (17-oct-2026).
- **Elegir el idioma en la primera pantalla y cambiarlo en Opciones** es lo habitual en los juegos de Telegram y en los MMO (World of Warcraft deja cambiar el idioma del cliente, y cada jugador ve el juego en el suyo en un mismo reino).
- **Que cada uno lea en su idioma lo que le manda el otro** viene de los mensajes del sistema de los MMO, que se escriben del lado de quien los lee.
