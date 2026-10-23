# Economía

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Mundo vivo y viaje](../02-mundo/mundo-vivo-y-viaje.md), [Equipamiento](../03-personaje/equipamiento.md) · **Alimenta a:** [Profesiones](profesiones.md), [PvP](../06-contenido/pvp.md), [Monetización](monetizacion.md) · **Estado:** propuesta; el 🏛️ Mercado de §3.0 está en el juego desde la 0.46 (D-320); las reparaciones de §5 y los encargos de reparación de §7, desde la 0.57 (D-333); los pedidos de fabricación de §7, desde la 0.59 (D-335)

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
| 🥇 **Oro** | Todo el comercio, servicios, reparaciones, impuestos | Misiones, ventas, contratos, botín | La que llevas encima, solo en zonas rojas y negras |
| ✨ **Esencia** | Mejorar equipo, maestrías, Tesoro Semanal | Matar, completar contenido | La no depositada queda en tu mancha (recuperable) |
| ⚔️ **Honor** | Recompensas de PvP | Arenas, campos, guerra de facciones | No |
| 💎 **Gemas** | Cosméticos y comodidades (moneda premium) | Telegram Stars; algunas en eventos | No |

**En el juego hoy (parches 0.7 y 0.7.3, D-80 y D-85; el 🪎 cofre, D-92 provisional):**

| Moneda | Cómo se consigue | Para qué sirve hoy |
|---|---|---|
| 🥉 **Bronce**, 🥈 **Plata**, 🥇 **Oro** | Se ganan jugando (combates, exploración, misiones, ventas) y se juntan solas: 100 🥉 = 1 🥈 y 100 🥈 = 1 🥇. En el código es un solo número contado en bronce (`Hero.gold`) | Mercader, posada, reiniciar especialización, coser bolsas |
| 💰 **Bolsas** | Se cosen en el Claro con 4 de fibra (hilo), 1 pieza de metal (el cierre) y 1 🥈. Es un sumidero de monedas y materiales | La doble especialización (desde 0.9.1, D-88) y armar cofres |
| 🪎 **Cofres** (D-92, provisional) | Se arman en el Claro (💰 Monedas → 🪎 Armar cofre) con 10 💰 bolsas, 10 de madera y 5 piezas de metal (`currency.chest_recipe`). Un cofre resume 40 de fibra, 15 de metal, 10 de madera y 10 🥈: es el sumidero más grande del juego hoy (`Hero.chests`) | Pagar lo grande: agrandar un campamento desde el nivel 6 cuesta también 1 cofre de 6 a 7, 2 de 7 a 8 y 3 de 8 a 9 (`camps.chests_from_level`, `chests_per_level`). Más adelante, castillos y obras grandes |
| 💎 **Diamantes** | Se compran con dinero real (todavía no se venden: ver P-72) | Solo aceleradores y cosméticos (D-43): ⭐ experiencia +50 % por 7 días (100 💎) y 🚩 estandarte único al lado del nombre (150 💎) |
| 🪪 **Credencial de oficio** | Llegará con los oficios | Tu carta de presentación de profesión ante otros jugadores |

El estandarte que se compra durante la beta es el de **beta tester** (🚩[Beta]). Después de la beta, el mismo producto pasa a ser un estandarte premium normal (`balance.yaml` → `currency.banner_phase`). Las recetas y los precios los propuso Claude. Desde D-92 (provisional, resuelve P-73) el 🪎 cofre está en el juego; el 💵 **billete no entra, por decisión**: con bronce, plata y oro alcanza, y más monedas confunden. La ficha del héroe muestra todas las monedas con su cantidad, también las que están en 0: 🥉 🥈 🥇 💰 🪎 💎.

**Transferibles y no transferibles** (como en WoW): el **oro** es libre y se comercia entre jugadores. La **Esencia**, el **Honor**, la **reputación de castillo** y la **moneda de temporada** (que se gana en cada temporada y compra sus recompensas) **no se pueden transferir**: son de quien las ganó. Así lo que se gana jugando no se compra con oro ni con cuentas alternas.

La reputación, los títulos de Pionero y el conocimiento **no** son monedas: son progreso.

## 3. Mercados

### 3.0 Lo que está en el juego: el 🏛️ Mercado entre jugadores (0.46, D-320 provisional; D-137 y D-26 confirmadas)

El dueño pidió el 21-oct-2026 que los jugadores se vendan entre ellos el equipo que encuentran o fabrican, con órdenes de venta para el equipo y lo fabricado y órdenes de compra para los recursos, "que funcione y luego vamos arreglando". La forma de hoy es la más simple que cumple **D-137** (una sola subasta para todos, transportistas que tardan) y **D-26** (precio mínimo y máximo obligatorio). Todo en `engine/service/market.py`; los números en `content/balance.yaml` → `market`.

| Qué | Cómo está hoy |
|---|---|
| **Dónde** | Un solo libro para todos. Se abre en cualquier 🔥 fogata (🛒 Mercader → 🏛️ Mercado), en el centro de tu campamento si construyó el 🏪 Puesto de trueque (⚒️ Oficios de 🏘️ Servicios) y con /mercado o /market. Fuera de esos lugares solo se mira; cancelar una orden se puede desde cualquier lado |
| **Órdenes de venta** (equipo y lo fabricado) | Piezas de equipo, pociones, remedios, muebles, comida, 💰 bolsas y 🪎 cofres, de la mochila. Eliges con /s1, escribes el precio por unidad en 🥉 (y la cantidad con "x5") o usas ×1, ×2 y ×3 del precio de referencia. Las unidades salen de la mochila a la orden (custodia). Se compran desde 7 categorías, de la más barata a la más cara (/c1); el equipo dice si te sirve |
| **Pedidos de compra** (recursos) | Cualquier material con código (de base, del terreno, refinados, pescado, esencias). Eliges con /b07 (el código de 📦 Recursos); las monedas quedan apartadas. Quien lleva el recurso le vende con /k1, en parte o todo, y cobra al momento |
| **Impuesto** | 5 % de cada venta (`market.tax`), lo paga quien cobra y se quema; sin tasa por publicar. Es la mitad de lo que propone §5 (1,5 % + 4 %), y se ajusta con el informe |
| **Transporte** | Lo comprado llega a 📦 Entregas a los 30 min (`delivery_minutes`), igual para todos. Se recoge en cualquier fogata o en tu campamento, hasta donde quepa en la mochila (desde la 0.62, D-338: hasta el tope de su tipo, o del equipo suelto); el resto espera. Lo que vuelve de una orden está listo al instante |
| **Vida y topes** | Una orden dura 7 días (`order_days`, como §3); al vencer o cancelar vuelve todo lo que queda. Hasta 10 órdenes por jugador (`max_orders`) y 500 unidades por orden. Nadie se compra a sí mismo |
| **Banda de precio** | De 0,25 a 10 veces el precio de referencia (`price_min`, `price_max`): `price` de items.yaml; una bolsa o un cofre, lo que cuesta su receta. Todavía no sale del historial de ventas |
| **Equipo** | La ✒️ obra maestra viaja con su firma y la pieza con su ✨ encantamiento, como en la ⚔️ Armería. **Desde la 0.57 (D-333)**, también con su 🔧 durabilidad: cada unidad lleva la suya hasta 📦 Entregas, la lista y la oferta la muestran ("🔧 80/96") y al publicar salen primero las copias más gastadas |
| **🗺️ Pergaminos de mapa** (0.50, D-311.5 confirmada, D-326 provisional) | El 🧭 Explorador vende sus pergaminos de a uno (cada copia lleva sus zonas, su autor y su región, que viajan en la orden y en 📦 Entregas) en una 8.ª categoría de 🛍️ Comprar, 🗺️ Mapas. **Precio libre:** es la excepción de la banda, de 1 🥉 a 1 🥇 (`map_scroll.price_min`, `price_max`); la referencia (1 🥈) solo abre el borrador. La oferta le dice a quien mira cuántas zonas son nuevas para él. El 🛒 Mercader no los compra ([Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.9.4) |
| **📜 Pedidos de fabricación** (0.59, D-140 confirmada, D-335 provisional) | El 7.º botón del mercado (/pedidos): encargas una receta a un artesano, pones los materiales o le pagas para que los consiga (a su referencia), más su **mano de obra**, siempre aparte (sugerida 8 🥉 por ⚡ × (1 + rango ÷ 20), dentro de la banda: 0,25 a 10 veces). Las monedas y los materiales quedan en custodia; el artesano lo hace en su estación, cobra menos el 5 % sobre todo lo que cobra y lo hecho llega a 📦 Entregas a los 30 min (la ✒️ obra maestra, con su firma). 7 días; hasta 10 pedidos abiertos, aparte de las órdenes ([Profesiones](profesiones.md) §0.13) |
| **🎒 Mochilas de oficio** (0.62, D-338 confirmada, D-339 provisional) | Las mochilas que hacen los 5 oficios de recolección (básica y grande; [Profesiones](profesiones.md) §0.15) se venden en una 10.ª categoría de 🛍️ Comprar (🎒 Mochilas de oficio), solo las que no están puestas. **Desde la 0.62 la mochila cuenta tipos** (50 tipos y 30 de cada uno, el equipo suelto aparte): 📦 Recoger trae cada cosa hasta el tope de su tipo y lo demás espera; el aviso dice qué tope frena |
| **Medición** | Cada día se anota en `market_log` cuántas compras, unidades, monedas e impuesto hubo y cuántas órdenes se publicaron, cancelaron o vencieron, y desde la 0.59 cuántos pedidos de fabricación se publicaron, hicieron, cancelaron y vencieron, con sus monedas y su impuesto; el informe diario lo muestra en su sección 9 ([Informes](../01-plataforma/informes.md)) |

**Lo que todavía no está** (preguntas P-247 a P-250): órdenes de venta de recursos y pedidos de compra de equipo, transporte que tarda según la distancia y bandidos que asaltan transportes (D-137), bandas de precio por historial, el canal del mercado con precios, los pedidos de fabricación personales y de gremio (los públicos están desde la 0.59, D-335; E-280), mercados locales (descartados por D-137) y el 💱 Comercio, que sigue bloqueado hasta las caravanas (D-298).

### El diseño completo del mercado (propuesta)

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
- **Desde la 0.62 (D-338, D-339): la mochila por tipos.** Con 50 tipos y 30 de cada uno (antes 60 unidades en total) se trae mucho más por salida: más material llega al 🏛️ Mercado y a las obras, y se vende menos seguido al 🛒 mercader (entra menos bronce de golpe, pero más en total si se farmea más). Las 🎒 mochilas de oficio son un producto nuevo de los oficios de recolección y suben la demanda de 🟤 cuero, 🧵 fibra y 🧣 tela. Medirlo con el informe diario (E-287 a E-289).
- **En el juego desde la 0.59 (D-140, D-335):** los 📜 **pedidos de fabricación** queman el impuesto del mercado (5 %) sobre todo lo que cobra el artesano (la mano de obra y los materiales que consiguió); lo demás pasa de un jugador a otro, no entra ni sale oro.
- **En el juego desde la 0.57 (D-139, D-333):** las **reparaciones** son un sumidero: el herrero de cualquier 🔥 fogata cobra 3 × lo que valen los materiales (`durability.npc_mult`) y esas monedas se queman; los 📜 encargos entre jugadores (§7) pagan 2 × y queman el impuesto del mercado. Es el precio techo de arriba: el herrero de la fogata siempre cuesta más que un artesano. Detalle en [Equipamiento](../03-personaje/equipamiento.md) §4.1 y [Profesiones](profesiones.md) §0.12.

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

**En el juego desde la 0.57 (D-140, D-333): el 📜 encargo de reparación**, el primer pedido entre jugadores: el dueño de una pieza aparta las monedas (2 × el valor de los materiales), un artesano con el oficio lo hace desde una estación y cobra al momento menos el impuesto del mercado; si nadie lo toma en 7 días, las monedas vuelven ([Profesiones](profesiones.md) §0.12).

**En el juego desde la 0.59 (D-140, D-335): el 📜 pedido de fabricación**, con la forma de arriba en su capa simple: público (lo ve cualquier artesano que puede hacerlo; el de gremio y el personal, E-280). Quien encarga pone los materiales (en custodia) o paga para que el artesano los consiga, más la **mano de obra**, siempre aparte (D-140), dentro de la banda del mercado; el artesano lo hace en su estación con su rango, cobra menos el impuesto del mercado y lo hecho llega a 📦 Entregas, una ✒️ obra maestra con su firma. Dura 7 días; cancelar o vencer devuelve todo ([Profesiones](profesiones.md) §0.13).

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
