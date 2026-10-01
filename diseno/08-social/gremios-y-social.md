# Gremios y vida social

> **Módulo** [08 · Social](README.md) · **Depende de:** [Telegram](../01-plataforma/telegram.md), [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §2 (los campamentos) · **Alimenta a:** [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md), [PvP](../06-contenido/pvp.md), [Mente](../05-salud/mente.md), [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §2.4 (el castillo) · **Estado:** §0 está en el juego (el gremio del campamento, capa simple, D-97 provisional); lo demás es propuesta

**De dónde sale.** Los gremios de WoW (rangos, banco, calendario, niveles de gremio que existieron en *Cataclysm*), las alianzas de Albion, los gremios de Chat Wars (almacén común, órdenes fijadas en el chat del castillo), los grupos de SAO (los "clearers", la orden de caballeros, el informante, la herrera) y lo que TowerWars ya probó en Telegram: almacén de gremio, vales por reenvío y alianzas.

---

## 0. En el juego (capa simple): el gremio del campamento

**Qué pidió el dueño** (por voz, 1-oct-2026). Que, una vez creado tu campamento, puedas crear un **gremio**. El gremio deja entrar a cierta cantidad de jugadores, pero pide requisitos: exploraciones, misiones, combates y demás. A medida que progresa, crece su capacidad, y hasta te deja tener un **castillo** con esa cantidad de jugadores. Lo ideal sería que se junten jugadores de las mismas horas de juego, pero eso lo dijo **solo como comentario**.

**Cómo se tomó** (D-97, provisional, en [decisiones.md](../00-vision/decisiones.md)). Un gremio por campamento de jugadores, ligado a él: sus miembros son los del campamento, sube de nivel con lo que hacen todos juntos, cada nivel deja entrar a más gente y el castillo pide un gremio listo. Lo de las mismas horas de juego no tiene reglas: la pantalla solo muestra cuándo jugó cada miembro.

### 0.1 Crearlo

- Lo crea **el fundador del campamento, estando en su campamento**: 🏕️ Campamento → 🛡️ Gremio → **🛡️ Crear gremio**. Cuesta **50 🥉** (`guild.found_coins`), un sumidero chico.
- Después escribe el nombre: de 3 a 24 caracteres, **único entre los gremios** (puede repetir el de un campamento). Si en vez de escribirlo toca otro botón, la pregunta se cancela y no se cobra nada.
- **Un gremio por campamento.** Vive con su campamento y no se borra. Por ahora no cambia de nombre.
- El Claro no tiene gremio: no tiene dueño (D-95).

### 0.2 Miembros

- **Los miembros del gremio son los del campamento.** Entrar al campamento (🙋 Pedir unirme y el sí del fundador, D-84) es entrar al gremio; salir del campamento es salir del gremio.
- **Con gremio, el cupo del campamento es el del gremio** (tabla de §0.3). Sin gremio sigue la cuenta de siempre: 2 al nivel 1 y 2 más por nivel del campamento.
- **Nunca se saca a nadie.** Si el cupo baja (un campamento grande que crea su gremio pasa a tener cupo 4), los que ya están se quedan; solo no entra nadie más hasta que el gremio suba. La pantalla lo avisa antes de crearlo.
- La pantalla del gremio muestra a cada miembro con su nivel y **cuándo jugó por última vez** ("activo hace 2 h"). Sirve para ver quién juega a las mismas horas, que era el comentario del dueño. Ninguna regla lo usa.

### 0.3 Niveles y requisitos

Para subir, el gremio tiene que juntar, **entre todos sus miembros y después de que cada uno entró**: exploraciones (1 por cada energía gastada explorando), peleas ganadas (también contra el Guardián) y recursos recolectados. Cada nivel pide unas 1,6 veces lo del anterior.

| Nivel | Cupo | Para subir al siguiente |
|---|---|---|
| 1 | 4 | 40 exploraciones, 20 peleas ganadas y 100 recursos |
| 2 | 6 | 65 exploraciones, 32 peleas ganadas y 160 recursos |
| 3 | 8 | 100 exploraciones, 50 peleas ganadas y 260 recursos |
| 4 | 12 | 165 exploraciones, 80 peleas ganadas y 410 recursos |
| 5 | 16 | 260 exploraciones, 130 peleas ganadas y 650 recursos |
| 6 | 20 | 420 exploraciones, 210 peleas ganadas y 1.050 recursos |
| 7 | 25 | 670 exploraciones, 335 peleas ganadas y 1.680 recursos |
| 8 | 30 | El último por ahora |

- Cuando cumplen, **cualquier miembro, estando en el campamento**, toca **⬆️ Subir el gremio**. Lo que sobra pasa al nivel siguiente y los demás miembros reciben un aviso.
- Un gremio **nunca baja de nivel**, y el nivel da comodidad (cupo, poder llegar a castillo), nunca poder de combate.
- **Las misiones contarán cuando existan**: todavía no hay misiones en el juego. La comida aportada a la despensa podría contar también más adelante.
- Los números están en `content/balance.yaml` → `guild.levels`. Son orientativos y se ajustan en la beta.

### 0.4 El castillo

- Para que un campamento pase de ciudad a **castillo** (del nivel 8 al 9) hace falta, además de lo de siempre (los materiales y una despensa que no esté vacía), un **gremio de nivel 5 o más con 10 miembros o más** (`guild.castle_min_level`, `guild.castle_min_members`). **Sin gremio, un campamento se queda en ciudad.**
- La pantalla **⬆️ Agrandar campamento** muestra esos requisitos con ✅ y ▫️ y, si falta algo, no deja elegir zona.
- Solo se pide en ese paso: un castillo sigue creciendo después del nivel 9 sin pedir nada nuevo.

### 0.5 Pantallas

- **🏕️ Campamento** (para sus miembros): ⬆️ Agrandar campamento · 🌾 Aportar comida (desde el nivel 3) · **🛡️ Gremio** · ↩️ Volver. Para no pasar de 4 botones, ✏️ Cambiar nombre y 🚪 Salir del campamento se mudaron adentro de 🛡️ Gremio. Quien visita un campamento ve el nombre y el nivel de su gremio.
- **🛡️ Gremio:** nombre, nivel, miembros (n de cupo), la lista con nivel y "activo hace", y las barras de lo que pide el nivel, como la obra del Claro. Botones: 🛡️ Crear gremio o ⬆️ Subir el gremio, ✏️ Renombrar campamento (fundador) o 🚪 Salir del campamento (miembros), y ↩️ Volver. Sin gremio explica qué es, cuánto cuesta y qué pide el castillo.
- **/gremio** abre la pantalla desde cualquier lugar, solo para mirar: crear, subir, renombrar y salir se hacen en el campamento.

### 0.6 Lo que todavía no tiene

Rangos y permisos, banco, salón, chat vinculado, calendario, alianzas y expulsar inactivos son la capa profunda de §1 y §2. Dos números de §1 no rigen en la capa simple: crear un gremio no pide nivel 5 (pide tener campamento, que ya cuesta progreso), y el cupo va de 4 a 30 miembros, no de 10 a 100.

**Dónde está.** Código: `engine/social/guilds.py` (las cuentas) y `engine/service/game.py` (pantallas, ganchos en la exploración, la recolección y la victoria). Números: `content/balance.yaml` → `guild`. Textos: `guild.*` en `content/locales/es.yaml`. Pruebas: `tests/test_guilds.py`.

**De dónde sale.** Los niveles de gremio de WoW *Cataclysm*, que subían con lo que hacían sus miembros; los gremios de Chat Wars, atados a un castillo; y los gremios de Albion, que necesitan un territorio propio.

## 1. Gremios

| Aspecto | Cómo funciona |
|---|---|
| **Creación** | Desde el nivel 5, con costo en oro (sumidero) |
| **Tamaño** | Crece con el nivel del gremio: de 10 a 100 miembros |
| **Rangos** | Líder, oficiales y rangos personalizables, con permisos (banco, invitar, guerra, territorio) |
| **Banco** | Oro y objetos, con registro de movimientos y límites diarios por rango. Los objetos salen con **vales por reenvío**, solo dentro del gremio, y caducan rápido (probado en TowerWars) |
| **Nivel de gremio** | Sube con la actividad de los miembros (contenido, fabricación, guerra). Da ventajas **de comodidad**: más banco, más miembros, descuentos de viaje, un salón. Nunca poder de combate |
| **Salón** | Espacio del gremio en una capital, con estaciones de oficio, trofeos de jefes y una taberna propia (ver [Casa propia](../09-construccion/casa-propia.md)) |
| **Chat** | Un grupo de Telegram vinculado, con temas: #órdenes, #banda, #mercado, #taberna, #rol. El bot publica ahí los avisos del gremio |
| **Calendario** | Bandas, asedios y eventos con confirmación de asistencia por botón |
| **Inactivos** | Los oficiales pueden expulsar a quien no juega hace 14 días o más (regla de TowerWars) |

## 2. Alianzas

- Varios gremios forman una **alianza** para bandas, asedios y territorios.
- Un almacén de alianza opcional, con aportes de cada gremio.
- En la guerra de facciones cada jugador pelea por su facción, pero la alianza coordina (ver [PvP](../06-contenido/pvp.md)).

## 3. Grupos y buscador

- **Grupo:** hasta 5 jugadores, con un chat retransmitido por el bot.
- **Buscador por rol** para mazmorras, Profundidades, bandas de Buscador, campos de batalla y cacerías (ver [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md)).
- **Calificación después de cada grupo:** un "👍" opcional por compañero, que suma a un indicador de buen compañero visible en el perfil. No hay votos negativos, para que no se use para acosar; los reportes van por separado.

## 4. Botín a la vista: Necesidad y Codicia con el dado nativo

**De dónde sale.** El "Necesidad / Codicia" de WoW y los dados animados de Telegram, cuyo valor decide el servidor de Telegram y todos ven.

- Cuando cae un objeto comerciable en un grupo armado al azar, cada uno elige *Necesidad* (lo usa), *Codicia* (lo quiere vender) o *Paso*.
- Entre quienes empatan en la categoría más alta, el bot tira un 🎲 por cada uno **en el chat de la sala**. Gana el número más alto; si hay empate, se vuelve a tirar.
- Nadie puede acusar al bot de trucar la tirada.

## 5. Mentoría

- Los jugadores de nivel alto pueden anotarse como **mentores**.
- A un novato se le asigna un mentor hasta el nivel 20.
- El mentor gana una moneda de mentoría (cosméticos, títulos) cuando su aprendiz alcanza metas: su primer Guardián vencido, su primera mazmorra, su primer oficio a 20.
- **Por qué conviene:** en un juego tan grande, el mejor tutorial es otra persona.

## 6. Hermandad de armas

Dos jugadores pueden sellar una **hermandad** (una "amistad" formal, sin matrimonio obligatorio):
- Pueden invocarse entre ellos con descuento.
- Ven el estado de salud del otro.
- Ganan un pequeño bono de experiencia cuando juegan juntos.
- Tienen un título compartido.

## 7. Canales del juego

| Canal | Qué publica |
|---|---|
| **Gaceta** | Pioneros, avance de la Frontera, epidemias, caídas del Juramento de Hierro, recetas descubiertas, obras maestras, partes de guerra |
| **Mercado** | Precios de referencia, órdenes grandes, informe económico mensual |
| **Salón de los Caídos** | Los personajes del Juramento de Hierro que cayeron, con su historia |
| **Novedades** | Notas de versión (en lenguaje de resultado, sin fórmulas; así trabaja TowerWars) |

## 8. Rol con máster humano

**De dónde sale.** Los chats de rol textual con máster humano, muy activos en la comunidad rusoparlante de Telegram.

- Grupos oficiales de rol en la taberna, con herramientas para el máster: el bot tira dados nativos, genera PNJ y muestra la ficha real de cada héroe (linaje, cicatrices, trasfondo).
- Los mejores másters pueden recibir herramientas para crear **misiones de comunidad** (texto) que, tras revisión, entran al juego con su firma.

## 9. Moderación

Ver [Seguridad y anti-trampas](../01-plataforma/seguridad-y-anti-trampas.md), §7. Los grupos oficiales tienen moderadores voluntarios con herramientas del bot, y todo mensaje que el juego genera usa plantillas.
