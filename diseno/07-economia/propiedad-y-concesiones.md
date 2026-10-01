# Propiedad y concesiones: un mercado capitalista con lugares escasos

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Economía](economia.md), [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md) · **Se conecta con:** [Construcción](../09-construccion/README.md) (parcelas), [Apuestas](../08-social/apuestas.md) (licencias de casino), [Gremios](../08-social/gremios-y-social.md) · **Estado:** propuesta, con D-48 (impuesto de la casa) aplicada

**Qué pediste.** Un mercado "capitalista", donde haya **pocos lugares** (como en Albion Online), los jugadores tengan que **comprarlos**, **mantenerlos pagando tasas e intereses** y **pujar** para conseguirlos.

**De dónde sale.**
- *Albion Online*: las parcelas de las ciudades y de las islas cuestan, pagan mantenimiento y se disputan; los territorios en zona negra se conquistan y se mantienen.
- *EVE Online*: oficinas y estaciones con renta; los gremios que controlan un sistema cobran impuestos.
- *Final Fantasy XIV*: parcelas de vivienda tan escasas que se sortean.
- *Monopoly* y la economía real: el valor de la ubicación, las hipotecas y el embargo.
- **Impuesto autodeclarado** (Harberger, economía): el dueño declara cuánto vale su lugar, paga una tasa sobre ese valor, y cualquiera puede comprárselo a ese precio. Obliga a declarar un valor honesto: si lo declaras bajo, te lo compran; si lo declaras alto, pagas más impuesto.

---

## 1. Qué es escaso

| Bien escaso | Dónde | Cuántos (orientativo) | Qué da |
|---|---|---|---|
| **Puestos de mercado** | Plazas de cada asentamiento y capital | 10-40 por lugar; los de la plaza principal son los mejores | Vender en persona con menos impuesto, visibilidad en la lista del mercado, tu cartel en la plaza |
| **Locales comerciales** | Calles de las capitales | Pocos por capital | Abrir una tienda con nombre (herrería, botica, taberna de jugador) con estaciones y empleados |
| **Parcelas de vivienda** | Barrios de los asentamientos | Limitadas por asentamiento; más baratas en las regiones nuevas de la Frontera | Construir casa (ver [Casa propia](../09-construccion/casa-propia.md)) |
| **Parcelas de gremio** | Distritos de las capitales | Muy pocas | Salón y barrio de gremio |
| **Licencias** | El Castillo de cada capital | Pocas por temporada | Operar un casino legal, un corredor de apuestas, una línea de caravanas, una consulta médica en la plaza, un puesto de guía |
| **Concesiones de ruta** | Entre asentamientos | Una por ruta | Cobrar peaje o dar servicio de caravanas en una ruta |
| **Vetas y jardines exclusivos** | Territorios de zona negra | Uno por territorio | Recolección exclusiva (se conquista, ver [PvP](../06-contenido/pvp.md)) |

La escasez es **a propósito**. Si hubiera un puesto para cada uno, tener puesto no valdría nada.

## 2. Cómo se consiguen: pujas

- **Subasta inicial:** cuando se abre un lugar nuevo (por ejemplo, las plazas del asentamiento de una región recién pacificada), sus puestos y parcelas salen a **subasta** en la Lonja del Castillo durante 48 horas. Gana la puja más alta, y el oro de la subasta se quema (sumidero).
- **Reventa:** un dueño puede vender o **subarrendar** su lugar a otro jugador, con custodia del bot.
- **Licencias por temporada:** se subastan cada temporada; el ganador la tiene hasta la temporada siguiente.
- **Pujar con préstamo:** se puede pujar con oro prestado (§4).

## 3. Cómo se mantienen: tasas

Cada lugar paga una **tasa semanal**:

- **Tasa autodeclarada** (modelo Harberger), para puestos, locales y parcelas de gremio:
  1. El dueño **declara un valor** para su lugar.
  2. Paga cada semana un porcentaje de ese valor (por ejemplo, 2 %).
  3. **Cualquiera puede comprarle el lugar a ese valor declarado**, en cualquier momento. El dueño recibe el oro y tiene unos días para desalojar.
  - Así, el que lo declara barato para pagar poco se arriesga a que se lo quiten; el que lo declara caro paga mucho. El precio de cada lugar termina reflejando lo que de verdad vale.
- **Impuesto a la propiedad** (D-48), para las parcelas de vivienda. Es una **tasa fija**, no autodeclarada, para que tu casa no te la compren sin querer (§3.1).
- **Si no pagas** un puesto, un local o una parcela de gremio: una semana de gracia; después, el lugar vuelve a subasta. Lo que había dentro pasa a tu almacén: nunca se pierden los objetos. La casa tiene su propio camino (§3.1).

### 3.1 El impuesto a la propiedad de la casa (D-48)

- **A quién se paga:** al **reino donde está la casa**. Si está en un castillo o asentamiento de jugadores, a ese castillo; si está en una comunidad PNJ, a esa comunidad (ver [El Colapso y las comunidades](../02-mundo/el-colapso-y-las-comunidades.md)).
- **Cuánto:** cada semana, un porcentaje del **valor de catastro** de la parcela. Ese valor no lo declara el dueño: lo fija el bot según el tamaño de la parcela y su barrio.
- **Quién fija la tasa:** el gobierno del reino, **dentro de un rango** (orientativo: del 1 % al 3 % semanal del valor de catastro). En un castillo de jugadores la fija el gobernador, igual que los demás impuestos locales (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md)); en una comunidad PNJ, su consejo, donde los PNJ votan según su cultura. Se puede cambiar una vez por temporada, con una semana de aviso. Para el dueño, la tasa es fija mientras no se cambie.
- **A dónde va:** al **tesoro del reino**, que la gasta en obras, guardias y servicios. Así un reino con buenos servicios puede cobrar más, y uno que quiere atraer vecinos puede cobrar menos.
- **Se descuenta solo** cada semana de tu oro del juego. El bot avisa dos días antes si no te alcanza.
- **Si no pagas:**
  1. **Una semana de gracia:** la casa funciona igual y la deuda queda a la vista.
  2. **Cierre:** después de la gracia, la casa se cierra. No se usa el taller, ni el dormitorio, ni la enfermería, y los trabajadores paran. Puedes entrar solo para sacar tus cosas. Pagando la deuda (sin intereses) se reabre en el acto.
  3. **Nunca se pierde lo de adentro.** Si la casa sigue cerrada 8 semanas, la parcela vuelve a subasta: los objetos, los muebles y las estaciones desmontadas pasan a tu banco en ese asentamiento.
- **No se le aplica la tasa autodeclarada:** nadie puede comprarte la casa por pagar un precio.

## 4. Crédito e intereses

- **Banco PNJ del Castillo:** presta oro con garantía (tus objetos, tu casa, tu puesto) y con **interés** semanal publicado. Si no pagas, embarga la garantía y la subasta.
- **Bancos de jugadores:** un gremio o un jugador con licencia de banquero presta con el interés que quiera, y el bot guarda la garantía.
- **Hipotecas:** comprar una parcela o un local pagando una parte y el resto a plazos.
- **Registro de crédito:** el bot lleva un historial de cumplimiento. Quien no paga pierde acceso al crédito y, si el prestamista quiere, recibe una recompensa por su cabeza (ver [PvP](../06-contenido/pvp.md)).

**Nota:** el crédito es poderoso y se presta a abusos. Por eso los intereses tienen techo, las garantías las guarda el bot y todo se registra.

## 5. Impuestos del dueño

Quien controla un lugar cobra:
- Un **casino** cobra su comisión (ver [Apuestas](../08-social/apuestas.md)).
- Un **mercado de alianza** cobra su impuesto.
- Una **concesión de ruta** cobra peaje a las caravanas.
- Un **alcalde** electo fija una parte de los impuestos locales (ver [Gremios y organizaciones](../09-construccion/gremios-y-organizaciones.md)).

Encima de todo, la ciudad cobra su impuesto base. Parte se quema (sumidero) y parte financia las obras públicas del servidor. El impuesto a la propiedad de las casas va entero al tesoro del reino donde están (§3.1).

## 6. Contrapesos para que no gane siempre el más rico

1. **Tope de propiedad:** un jugador no puede tener más de 2 puestos por capital ni un gremio más de 1 parcela de gremio por capital.
2. **La tasa autodeclarada** impide acaparar barato.
3. **Lugares nuevos con cada región:** cada región pacificada abre plazas y parcelas nuevas, así que siempre hay una oportunidad para quien llega después.
4. **Parcelas de novato:** cerca del Claro hay parcelas pequeñas que solo pueden comprar jugadores de nivel bajo.
5. **El mercado de órdenes sigue abierto para todos:** tener puesto da ventaja (menos impuesto, visibilidad), pero cualquiera puede comprar y vender sin puesto.

## 7. Cómo se conecta con todo

- Los **puestos** hacen del comercio un oficio con ubicación (ver [Roles](../00-vision/roles-y-caminos-de-juego.md)).
- Las **parcelas** se construyen (ver [Construcción](../09-construccion/README.md)).
- Las **licencias** abren carreras: dueño de casino, banquero, transportista, médico con consulta en la plaza.
- Las **regiones nuevas** abren lugares nuevos: el avance de la Frontera mueve la economía de propiedades.
- Las **tasas, subastas e intereses** son sumideros de oro que se miden en el informe económico (ver [Economía](economia.md)).

Ver P-53 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
