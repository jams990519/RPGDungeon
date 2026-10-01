# Economía

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md), [Equipamiento](../03-personaje/equipamiento.md) · **Alimenta a:** [Profesiones](profesiones.md), [PvP](../06-contenido/pvp.md), [Monetización](monetizacion.md) · **Estado:** propuesta

**De dónde sale.**
- *Albion Online*: casi todo el equipo lo fabrican jugadores y cada ciudad tiene su mercado. El **Mercado Negro** compra objetos de jugadores y los pone en el botín de los monstruos. El equipo se pierde en zonas de botín completo, y el Enfoque diario sube el rendimiento de los oficios.
- *EVE Online*: mercados regionales, destrucción real de naves, seguros, contratos de transporte y un economista contratado desde 2007 que publica un informe económico mensual.
- *World of Warcraft*: casa de subastas, pedidos de fabricación, ficha de oro.
- *Star Wars Galaxies*: economía movida por artesanos, recursos con calidad variable.
- *Chat Wars* y *Dofus*: mercados entre jugadores dentro de un juego de turnos.
- **TowerWars**: libro de órdenes de compra y venta con custodia, que ya funciona en Telegram.

---

## 1. Principios

1. **La economía la mueven los jugadores.** Casi todo el equipo lo fabrican ellos; los jefes dan artefactos y materiales, no el objeto terminado (ver [Equipamiento](../03-personaje/equipamiento.md)).
2. **Todo se gasta.** Durabilidad máxima que baja, botín completo en zonas negras, consumibles, Mercado Negro. Si nada se destruye, dentro de un año nadie compra nada.
3. **Los mercados son locales.** El precio del hierro en Lejanía 4 no es el de Lejanía 9. Mover mercancía es un oficio.
4. **El oro que entra tiene que salir.** Cada fuente de oro tiene un sumidero equivalente, y se mide todos los meses.
5. **Riesgo = recompensa.** Los mejores materiales están en las zonas peligrosas (ver [PvP](../06-contenido/pvp.md)).
6. **Todo se hace con la moneda del juego.** Con dinero real solo se compran cosméticos y aceleradores (experiencia, recursos); nunca oro, equipo, Esencia ni nada que se pueda apostar (ver [Monetización](monetizacion.md)).
7. **Los sumideros son porcentajes, nunca montos fijos.** Una tasa de 100 de oro no significa nada para quien tiene millones; un impuesto del 5 % funciona igual toda la vida del juego. Impuestos, comisiones, reparaciones, tasas de parcelas y de viaje se calculan siempre como porcentaje del valor.
8. **Cada región produce cosas distintas.** Si cada zona tiene recursos propios, el comercio nace solo (§3.1).

## 2. Monedas

Pocas, para no repetir el problema de WoW, donde hay más de veinte monedas:

| Moneda | Para qué | Cómo se gana | Se pierde al caer |
|---|---|---|---|
| 🪙 **Oro** | Todo el comercio, servicios, reparaciones, impuestos | Misiones, ventas, contratos, botín | La que llevas encima, solo en zonas rojas y negras |
| ✨ **Esencia** | Mejorar equipo, maestrías, Tesoro Semanal | Matar, completar contenido | La no depositada queda en tu mancha (recuperable) |
| ⚔️ **Honor** | Recompensas de PvP | Arenas, campos, guerra de facciones | No |
| 💎 **Gemas** | Cosméticos y comodidades (moneda premium) | Telegram Stars; algunas en eventos | No |

**En el juego hoy (parches 0.7 y 0.7.3, D-80 y D-85):**

| Moneda | Cómo se consigue | Para qué sirve hoy |
|---|---|---|
| 🥉 **Bronce**, 🪙 **Plata**, 🥇 **Oro** | Se ganan jugando (combates, exploración, misiones, ventas) y se juntan solas: 100 🥉 = 1 🪙 y 100 🪙 = 1 🥇. En el código es un solo número contado en bronce (`Hero.gold`) | Mercader, posada, reiniciar especialización, coser bolsas |
| 💰 **Bolsas** | Se cosen en el Claro con 4 de fibra (hilo), 1 pieza de metal (el cierre) y 1 🪙. Es un sumidero de monedas y materiales | La doble especialización (próximo parche) y lo que venga |
| 💎 **Diamantes** | Se compran con dinero real (todavía no se venden: ver P-72) | Solo aceleradores y cosméticos (D-43): ⭐ experiencia +50 % por 7 días (100 💎) y 🚩 estandarte único al lado del nombre (150 💎) |
| 🪪 **Credencial de oficio** | Llegará con los oficios | Tu carta de presentación de profesión ante otros jugadores |

El estandarte que se compra durante la beta es el de **beta tester** (🚩[Beta]). Después de la beta, el mismo producto pasa a ser un estandarte premium normal (`balance.yaml` → `currency.banner_phase`). Las recetas y los precios los propuso Claude. El 💵 billete y el 🪎 cofre quedan como propuesta (P-73).

**Transferibles y no transferibles** (como en WoW): el **oro** es libre y se comercia entre jugadores. La **Esencia**, el **Honor**, la **reputación de castillo** y la **moneda de temporada** (que se gana en cada temporada y compra sus recompensas) **no se pueden transferir**: son de quien las ganó. Así lo que se gana jugando no se compra con oro ni con cuentas alternas.

La reputación, los títulos de Pionero y el conocimiento **no** son monedas: son progreso.

## 3. Mercados

- **Libro de órdenes** en cada asentamiento: órdenes de compra y de venta con custodia, cruzadas por precio y antigüedad. Es el formato de Albion y EVE, y el que TowerWars ya usa para sus recursos.
- **Mercados regionales grandes** en las capitales regionales, con más volumen y más productos.
- **Mercados locales chicos** en los asentamientos, con menos variedad.
- **Los precios difieren por ciudad.** El Goblin ve el precio medio en otras ciudades; los demás lo ven en el canal del Mercado, con un día de retraso.
- **Vencimiento de las órdenes:** 7 días (como en TowerWars), renovables pagando la tasa otra vez.
- **Precio mínimo y máximo obligatorio** por objeto, calculado según su historial de ventas (como las bandas de precio de Black Desert). Nadie puede vender una espada épica a 1 de oro a su cuenta alterna, ni inflar un precio para lavar oro. Es una regla fija (D-26).
- **Equipo comerciable** con firma del artesano, calidad y durabilidad a la vista.

### 3.1 Recursos regionales

- Cada terreno produce lo suyo y carece de lo demás (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md)), y hay **yacimientos únicos** en puntos concretos del mapa.
- Cada anillo tiene **materiales que solo existen ahí** (la madera liviana de los Jardines Flotantes, el cristal de la Cueva de Cristal, las especias del Desierto), y cada región tiene su especialidad dentro del anillo.
- Las ciudades necesitan cosas que no producen: la región helada necesita comida de la región de la pradera, y la pradera necesita el metal de las cuevas.
- Resultado: **siempre hay algo que llevar de un lado a otro**, y los precios difieren por ciudad sin que nadie lo fuerce.

## 4. Transporte

Ver [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md). En resumen:
- **No hay teletransporte:** viajar toma tiempo real y la carga pesada lo alarga (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md)), así que mover cargas grandes rápido es caro.
- **Las caravanas** son baratas por kilo, pero cruzan zonas rojas y se pueden emboscar. Hay escoltas contratables (jugadores) y seguros (§7).
- **El correo** es seguro y lento, o seguro y caro.

- **Bandidos:** las caravanas que cruzan zonas rojas pueden ser asaltadas por jugadores. El bandido gana el botín y karma; el escolta gana su paga si la defiende (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)).

**Por qué conviene.** Nacen el comerciante, el transportista, el escolta y el bandido como formas de jugar, y cada mercado tiene su propia historia de precios.

## 5. Fuentes y sumideros de oro

| Fuentes (entra oro) | Sumideros (sale oro) |
|---|---|
| Misiones y encargos | **Impuesto de mercado** (tasa por publicar + impuesto sobre la venta) |
| Venta a PNJ (recompra de materiales y equipo) | Reparaciones |
| Botín de monstruos | Postas, peajes de caminos y correo |
| Recompensas de PvP y eventos | Sanatorio, templo, multas de karma |
| Mercado Negro (compra equipo a los artesanos) | Mantenimiento de vivienda y territorios |
| | Estaciones de oficio (tasa de uso) |
| | Cambio de nombre, de facción, de apariencia |
| | Juegos de azar de la taberna (comisión de la casa) |
| | Porcentaje quemado en las transferencias entre jugadores |

- **Impuestos de referencia:** alrededor de 1,5 % por publicar una orden y 4 % sobre la venta, con descuento para Premium (como en Albion). Se ajustan con el informe mensual.
- **Precio techo de servicios:** el sanatorio y los PNJ de reparación ponen un precio máximo a lo que pueden cobrar los jugadores por lo mismo, y los jugadores compiten por debajo.

## 6. Mercado Negro

**De dónde sale.** Albion Online. El Mercado Negro de Caerleon compra objetos a los jugadores y los reparte en el botín de monstruos y cofres, así que todo lo que suelta un monstruo lo fabricó alguien.

**Cómo funciona aquí.**
- Un PNJ en cada capital compra equipo fabricado a precio de demanda.
- Ese equipo aparece después en el botín de los monstruos y cofres del mundo.
- Si nadie vende al Mercado Negro, los monstruos sueltan menos equipo.
- También saca del juego equipo viejo de los anillos cercanos al Claro.

**Por qué conviene.** Hasta el jugador que solo pelea y nunca fabrica depende de los artesanos, y los artesanos siempre tienen a quién vender.

## 7. Contratos, pedidos y seguros

| Herramienta | Qué es | De dónde sale |
|---|---|---|
| **Pedido de fabricación** | Mandas materiales y una comisión a un artesano (público, de gremio o personal), y él fabrica con su nivel y su firma | WoW (desde *Dragonflight*) |
| **Contrato de transporte** | Pagas para que alguien lleve tu carga de un asentamiento a otro, con garantía | EVE |
| **Contrato de recompensa** | Oro por un objetivo: un jugador rojo, un monstruo, un material | EVE, SAO |
| **Contrato de intercambio** | Objetos por objetos u oro, con custodia del bot | EVE |
| **Seguro** | Pagas una prima y, si pierdes el equipo asegurado en PvP, recuperas una parte del valor | EVE (seguro de naves) |
| **Préstamo** | Un gremio o un jugador presta oro con garantía en objetos, y el bot hace de custodio | Emergente |

**Vales por reenvío.** Un vale del almacén del gremio se cobra reenviando el mensaje, solo dentro del gremio, y caduca rápido. TowerWars lo usa así y funciona.

## 8. Enfoque diario

**De dónde sale.** Albion: puntos diarios de Enfoque, con tope acumulable, que suben el rendimiento de fabricar y recolectar.

- Cada día se recarga una cantidad de **Enfoque**, con un tope acumulable de varios días.
- Fabricar o recolectar gastando Enfoque rinde más (más calidad, más retorno de materiales).
- **Por qué conviene:** premia entrar un rato cada día sin castigar a quien entra cada tres. Además limita a los que fabricarían sin parar con bots.

## 9. Medición: el informe económico

- **Informe mensual público** (como el de EVE): oro que entró y salió por fuente y sumidero, precios de referencia por ciudad, objetos destruidos, volumen de comercio.
- **Tablero interno:** inflación del oro, concentración de riqueza, precios anómalos (posible comercio con dinero real), sumideros que no funcionan.
- **Ajustes:** los impuestos, las recompensas de PNJ y los precios del Mercado Negro son las palancas. Cada ajuste va al registro de balance.

## 10. Mecanismos de otros juegos que se incorporan

| Mecanismo | Juego | Cómo entra aquí |
|---|---|---|
| Mercados locales por ciudad | Albion Online | Un libro de órdenes por asentamiento (§3) |
| Mercado Negro que siembra el botín | Albion Online | §6 |
| Órdenes de compra y venta con custodia | EVE Online, TowerWars | §3 |
| Contratos de transporte, intercambio y recompensa | EVE Online | §7 |
| Seguros de equipo | EVE Online | §7 |
| Informe económico mensual y un economista | EVE Online | §9 |
| Pedidos de fabricación | WoW | §7 |
| Ficha de oro por dinero real | WoW, Albion, EVE (PLEX) | **Descartada:** el oro nunca se vende por dinero real (ver [Monetización](monetizacion.md)) |
| **Límite de compra por horas** en el mercado (no comprar más de N unidades cada 4 horas) | RuneScape (Grand Exchange) | Contra la manipulación y el acaparamiento de materiales clave |
| **Bandas de precio** (precio mínimo y máximo por objeto, según su historial) | Black Desert | Contra el comercio con dinero real (nadie vende una espada épica a 1 de oro) |
| **Cargamentos de comercio cuyo valor depende de la distancia y cae si se entregan muchos** | ArcheAge | Los pedidos de las ciudades pagan más por traer mercancía de lejos, y pagan menos a medida que se cubren |
| **Moneda que se consume al fabricar** | Path of Exile (los orbes) | Las runas y esencias del encantamiento son a la vez moneda de trueque y material: su uso es un sumidero natural |
| Vendedores de jugador en su casa o puesto | Ultima Online, Star Wars Galaxies | Puestos y locales (ver [Propiedad y concesiones](propiedad-y-concesiones.md)) |
| Subasta semanal de casas con renta | Tibia | Subastas de parcelas y tasas (ver [Propiedad y concesiones](propiedad-y-concesiones.md)) |
| Impuestos del dueño del castillo | Lineage 2 | El consejo y el alcalde fijan impuestos (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md)) |
| Comisión de publicación + comisión de venta | Guild Wars 2 (5 % + 10 %) | Referencia para calibrar los impuestos (§5) |
| **Especulación con bienes perecederos** | Animal Crossing (el mercado de nabos) | Mercancía de temporada cuyo precio cambia dos veces al día en cada ciudad y que se pudre si la guardas mucho |
| Cadenas de producción según las necesidades de la población | Anno, Victoria 3 | Las necesidades de la ciudad (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md)) |
| Rutas de comercio con oferta y demanda | Elite Dangerous | Recursos regionales (§3.1) y caravanas (§4) |
| **Lección:** la subasta con dinero real se cerró en 2014 | Diablo III | Nunca se vende oro, equipo ni materiales con dinero real |

## 11. Roles económicos que deben existir solos

Comerciante, transportista, escolta, especulador, cartógrafo, informante, banquero de gremio, médico, artesano famoso, recolector de zonas negras. Si alguno de estos roles no aparece por sí solo en la beta, algo del diseño está mal.

Ver P-32 a P-36 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
