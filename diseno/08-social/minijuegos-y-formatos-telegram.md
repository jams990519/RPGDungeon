# Minijuegos y formatos longevos de Telegram, dentro del juego

> **Módulo** [08 · Social](README.md) · **Depende de:** [Telegram](../01-plataforma/telegram.md), [Economía](../07-economia/economia.md) · **Estado:** propuesta

Pediste buscar todos los formatos de juego que llevan años en Telegram, de cualquier tipo, para incorporarlos. La investigación completa, con más de 30 bots, años y fuentes, está en [Investigación: juegos de Telegram](../99-referencias/investigacion-juegos-telegram.md). Este documento dice **dónde entra cada formato en el mundo** y qué da.

---

## 1. Reglas para todos los minijuegos

1. **Opcionales.** Ningún minijuego es obligatorio para progresar.
2. **Dan cosas pequeñas o estéticas:** cosméticos, títulos, algo de oro o de reputación, cartas coleccionables. Nunca poder de combate.
3. **Son sumideros cuando se puede:** entrada con oro, comisión de la casa, objetos de un solo uso.
4. **A prueba de bots:** nada se gana solo por velocidad o por repetir; las recompensas tienen tope diario.
5. **Cada uno es un complemento** del módulo M16 (ver [Arquitectura](../01-plataforma/arquitectura-modular.md)): se agregan y se quitan sin tocar el resto.
6. **Viven en un lugar del mundo.** La taberna, la plaza, el gremio, el santuario. Así se sienten parte del juego y no una aplicación pegada.

## 2. En la taberna

| Minijuego | Formato original | Por qué duró | Cómo entra aquí | Qué da |
|---|---|---|---|---|
| **Naipes de la Torre** (cartas estilo UNO) | **@unobot** (2016, código abierto, sigue respondiendo en 2026) | No hay que instalar nada, dura 5-10 minutos y tu mano la ves solo tú, por modo inline | Partidas de 2 a 6 en la taberna o en el chat del gremio; tu mano llega por modo inline | Fichas de taberna, títulos |
| **Mazo de Bestias** (cartas coleccionables estilo Gwent) | **@unobot** + el Gwent de *The Witcher 3* y el Hearthstone de WoW | Un juego de cartas dentro del mundo da ganas de coleccionar | Cada monstruo vencido puede soltar su carta, y los jefes, cartas raras. Duelos 1v1 por turnos | Colección, torneos, cosméticos |
| **Dados del Mentiroso y dardos** | **Dados animados nativos** 🎲🎯 (desde 2020; los decide el servidor de Telegram) | La tirada no se puede trucar y el grupo entero la ve | Apuestas de taberna con tope; dardos con 🎯 | Oro (con comisión de la casa) |
| **Póker y blackjack** | **@PokerBot** (cartas por privado, mesa en el grupo) y **@BlackJackBot** | Reglas conocidas por todos | Noche de póker del gremio, con entrada en oro; el bote se reparte y no se crea oro nuevo | Oro, títulos. Ver la nota legal en [Monetización](../07-economia/monetizacion.md) |
| **Juego de mesa del piso** | Bots regionales de juegos tradicionales, como **Hokm** o el Ludo iraní (@telehokmbot, @MenchoolBot) | No hace falta aprender reglas | Cada tramo tiene su propio juego de mesa en su taberna (dominó, damas, un juego inventado del lugar): una excusa para viajar | Reputación local, cosméticos |
| **Justa de Bardos** | Juegos de fiesta como **Chat Against Humanity** y **@RatherGameBot** | Risas en grupo | Los jugadores completan versos con cartas y el "rey de la mesa" (rota) elige el mejor | Títulos, baja el estrés (ver [Mente](../05-salud/mente.md)) |
| **Charadas del Juglar** | **Crocodile** (@Crocodile_Game_Bot, ruso): uno explica una palabra y los demás adivinan | Sencillo y social | Palabras del propio juego: monstruos, objetos, lugares | Reputación de taberna |

## 3. En el gremio

| Minijuego | Formato original | Cómo entra aquí | Qué da |
|---|---|---|---|
| **La Máscara** (deducción social) | **@werewolfbot** (Werewolf for Telegram, 2016, código abierto, enorme en Irán y en Brasil) y los bots de **Mafia** | Un "Cultista del Abismo" infiltrado en el gremio, con roles de sabor de clase: el Paladín protege, el Pícaro espía, el Sacerdote revela. Se juega por noches y días en el chat del gremio | Si el gremio descubre al traidor, gana un bono de banda; si no, el traidor se lleva un botín simbólico del almacén (nunca real). Se venden objetos de un solo uso, como un documento falso o un antídoto (sumidero) |
| **Jefe Errante** | **Ragna** (@ragna_bot, desde 2017): un jefe que se invoca en cualquier chat para una pelea de 5 minutos con roles | Un Cuerno de Invocación (fabricado) llama a un jefe al chat del gremio; pelea corta con avisos (ver [Jefes](../06-contenido/jefes.md)) | Cajas de botín para los que pelearon |
| **Estandarte vivo** | Bots de mascotas y **tamagotchi** (DinoGochi; Catizen en versión masiva) | Una mascota del gremio que todos alimentan con materiales; si se descuida, pierde sus bonos | Bonos de comodidad del gremio |
| **Trivia de gremio contra gremio** | **Quizarium** (pistas progresivas y más puntos por rapidez) | Torneos semanales de preguntas de lore | Trofeos de gremio |

## 4. En la plaza y en los chats de piso

| Minijuego | Formato original | Cómo entra aquí | Qué da |
|---|---|---|---|
| **Criaturas y reliquias que aparecen** | Bots que hacen aparecer personajes en el chat, que se lleva el primero en nombrarlos, y **El Profesor Oak** (@ProfesorOak_bot, en español, época de Pokémon GO) | Tras un rato de actividad aparece una criatura o una reliquia en el chat del piso. Para quedártela hay que superar **un reto real** (una pregunta del Bestiario, un mini combate), no solo escribir rápido: así no sirven los bots | Mascotas, cartas, curiosidades |
| **Pintar el mapa** | **Not Pixel** (lienzo colectivo de 1000×1000; torneo "Pixel Battle" con 1.024 comunidades en noviembre de 2024) | Mapa de conquista que los gremios pintan con sus colores, y un torneo por eliminatorias cada temporada | Prestigio de gremio (ver [Eventos](../06-contenido/eventos.md)) |

## 5. En el santuario y el diario

| Minijuego | Formato original | Cómo entra aquí | Qué da |
|---|---|---|---|
| **Rezar en el santuario** | Bots de "crecimiento diario": un comando al día da un cambio al azar (a veces negativo) en un marcador del chat | `/rezar` una vez al día da favor divino, que puede ser positivo o negativo. Cada gremio tiene un "Elegido del día" con un bono pequeño | Bono pequeño del día, rachas |
| **Enigma del día** | El combo diario y el cifrado diario de **Hamster Kombat** (2024), que generaron todo un ecosistema de videos con la respuesta del día | Un acertijo diario de lore cuya respuesta circula entre la comunidad. Es publicidad gratis | Esencia, cosméticos por racha |
| **Quiz semanal de lore** | **@QuizBot** oficial y las encuestas en modo quiz (enero de 2020) | Un quiz semanal en el canal; la explicación de cada respuesta enseña la historia del mundo | Títulos de erudito |

## 6. En el salón recreativo (Mini App / HTML5)

| Minijuego | Formato original | Cómo entra aquí | Qué da |
|---|---|---|---|
| **Forja rítmica, pesca, ganzúa** | **@gamebot** (Lumberjack, Math Battle, Corsairs; octubre de 2016) y **GAMEE** (unos 50 millones de registrados) | Minijuegos de destreza con récord por chat (`setGameScore`, que avisa cuando alguien te supera) | Récords, cosméticos. **Nunca** la calidad real de un objeto: la destreza con los dedos no debe decidir el poder en un juego por turnos |

## 7. Formatos que ya son sistemas del juego

| Formato original | Dónde está en el diseño |
|---|---|
| **Chat Wars** (@ChatWarsBot, diciembre de 2016): batallas de castillos a hora fija, órdenes fijadas, estamina, misiones con temporizador, almacén de gremio, caravanas | [Guerra de facciones](../06-contenido/pvp.md), [Encargos](../06-contenido/misiones-y-exploracion.md), caravanas en [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) |
| **Wasteland Wars** (@WastelandWarsBot, 2017): avanzar kilómetro a kilómetro y volver con el botín | [Expediciones](../06-contenido/misiones-y-exploracion.md) |
| **Bastion Siege** (@bastionsiegebot, hacia 2017): fortalezas y alianzas | [Territorios y asedios](../06-contenido/pvp.md) |
| **ORNEST** (2025): jefe mundial semanal | [Jefe semanal](../06-contenido/jefes.md) |
| **Batallas de mascotas de WoW** (ya por turnos) | **Duelos de mascotas:** las mascotas capturadas o criadas pelean 3 contra 3 por turnos, con tipos y debilidades. Es casi un juego aparte, y probado |
| **@ChessBot**: ajedrez asíncrono | **Ajedrez de guerra:** los líderes de dos gremios que se asedian pueden resolver quién tiene la iniciativa en la primera ronda con una partida de un tablero táctico simple |
| **Iris** (@iris_cm): quema un 5 % de cada transferencia de su moneda | Porcentaje quemado en las transferencias (ver [Economía](../07-economia/economia.md)) |
| **@EpicFishingBot**: pescar, vender, intercambiar | Oficio de **Pesca** con minijuego (ver [Profesiones](../07-economia/profesiones.md)) |
| **Chats de rol textual** con máster humano | [Rol con máster](gremios-y-social.md) |

## 8. Lo que enseñan los juegos que murieron

1. **El token mata al juego.** Los juegos de tocar para ganar se desplomaron el día que repartieron su token (Hamster Kombat perdió un 86 % de jugadores mensuales en 2024). Lo que sostiene a un juego tiene que ser el juego mismo.
2. **Bots y multicuentas.** Chat Wars tuvo userbots que jugaban solos, y TapSwap se retrasó por granjas de bots. Solución: nada que se gane repitiendo, una API oficial para herramientas legítimas y retos que un script no puede pasar (ver [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md)).
3. **Un solo desarrollador y sin ingresos.** 7 de 18 bots de juegos recomendados ya no responden en 2026, y Bastion Siege 1 murió. El proyecto necesita un plan de sostenimiento desde el principio (ver [Monetización](../07-economia/monetizacion.md)).
4. **Riesgo país.** Irán bloqueó Telegram en 2018 con unos 40 millones de usuarios. Por eso conviene que el motor no dependa de Telegram (ver [Arquitectura](../01-plataforma/arquitectura-modular.md)).

## 9. Orden sugerido

1. **Primero:** dados de taberna (🎲), trivia de lore y rezar en el santuario. Son baratos y rápidos de hacer.
2. **Después:** Naipes de la Torre, La Máscara y el Jefe Errante.
3. **Más adelante:** Mazo de Bestias, duelos de mascotas, pintar el mapa, salón recreativo.

Ver P-36 y P-41 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
