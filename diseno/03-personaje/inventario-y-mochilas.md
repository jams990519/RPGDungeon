# Inventario y mochilas: qué llevas encima y dónde guardas el resto

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Equipamiento](equipamiento.md) (ranuras de Mochila, Cinturón y Montura; carga), [Profesiones](../07-economia/profesiones.md) (quién las fabrica) · **Alimenta a:** [Ronda y acciones](../04-combate/ronda-y-acciones.md) (el cinturón del botón 🎒 Mochila), [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (peso y tiempo de viaje), [Economía](../07-economia/economia.md) (cuánto se trae en cada viaje) · **Se conecta con:** [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) (qué se pierde al caer), [Casa propia](../09-construccion/casa-propia.md) (almacén), [Monetización](../07-economia/monetizacion.md) · **Estado:** propuesta, aplica D-47 (mochilas) y D-46 (cinturón)

**Qué pediste (D-47).** Mochilas fabricadas, con niveles de capacidad que se amplían; tipos de mochila según el oficio (herborista, minero, médico, comerciante…); un cinturón para el combate; alforjas, almacén y banco.

**De dónde sale.**
- *Diablo II*: el **cinturón de pociones**. Lo que está en el cinturón se usa en plena pelea; lo que está en el inventario, no. Un cinturón mejor tiene más filas.
- *Resident Evil 4*: el **maletín**. Poco espacio que obliga a decidir qué llevar, y ampliaciones que se consiguen jugando.
- *Albion Online*: el **peso** que frena, las **monturas de carga** (buey, mamut) para mover mucho, los **bancos locales** de cada ciudad y el riesgo de perder lo que llevas según la zona.
- *Kenshi*: las mochilas tienen forma y uso distintos; algunas estorban el combate o el sigilo, y la del ladrón no.
- *Escape from Tarkov*: mochilas **por tamaño** y estuches especiales (de medicinas, de documentos, de munición) que solo aceptan ciertas cosas.
- *Valheim*: el peso manda, el cinturón de fuerza sube la carga, y para mover mucho hay que construir un carro o un barco.
- *RuneScape*: **28 casillas** fijas que caben en una pantalla, el banco con pestañas y las bolsas de oficio (saco de hierbas, bolsa de gemas, bolsa de carbón).
- *Stardew Valley*: las **mejoras de mochila** (12 → 24 → 36), que se pagan con oro del juego y se sienten como un hito.

**Por qué este diseño.** En un juego de texto, el inventario tiene que caber en un mensaje y manejarse con pocos toques. Las casillas son fáciles de contar; el peso le da sentido al viaje (D-58) y al comercio. Y como la mochila se fabrica y tiene tipos por oficio, es otro producto que mueve la economía de jugadores.

---

## 1. Casillas y peso: dos números, una regla cada uno

| Número | Qué limita | Regla |
|---|---|---|
| 📦 **Casillas** | Cuántas cosas distintas llevas | **Límite duro.** Con la mochila llena no recoges más (ver §9) |
| ⚖️ **Peso** | Cuánto te frena | **Límite suave.** Pasar del peso cómodo no te impide cargar, pero te hace más lento |

- **Las cosas iguales se apilan** en una sola casilla: materiales hasta 50, consumibles hasta 10, equipo de a 1.
- **Cada objeto tiene un peso** en kilos, que se ve en su detalle (ver [Equipamiento](equipamiento.md) §3).
- **El oro y la Esencia no ocupan casillas ni pesan.** La Esencia sí se arriesga al caer (ver §8).

**Qué hace el peso de la mochila.**

| Estado | Peso de la mochila | En el viaje | En combate |
|---|---|---|---|
| **Cómodo** | Hasta el peso cómodo | Normal | Normal |
| **Cargado** | Hasta 1,5 veces el peso cómodo | +25 % de tiempo de viaje | Tu Carga sube un escalón |
| **Abarrotado** | Hasta 2 veces el peso cómodo | +50 % de tiempo de viaje | Tu Carga sube dos escalones |
| — | Más de 2 veces | No puedes recoger más | — |

- La **Carga** es la de [Equipamiento](equipamiento.md) §2 (ligera, media, pesada, sobrecargado), que sale de lo que llevas puesto. La mochila solo la empeora cuando pasa del peso cómodo. Así basta mirar un número: si la mochila dice "cómodo", no te afecta.
- Los tiempos de viaje son los de [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (fila «Carga y heridas»). Una pierna herida o una secuela que frena se suman aparte.

## 2. Mochilas fabricadas, por niveles

Todos empiezan con una **bolsa de tela**. Lo demás se fabrica: la **Peletería** hace las mochilas de cuero y la **Sastrería** las de tela (ver [Profesiones](../07-economia/profesiones.md)).

| Nivel | Mochila | Casillas | Peso cómodo | Quién la hace |
|---|---|---|---|---|
| 0 | Bolsa de tela (inicial) | 12 | 20 kg | Se recibe al crear el personaje |
| 1 | Morral | 16 | 30 kg | Sastrería o Peletería, rango Aprendiz |
| 2 | Mochila de viaje | 20 | 40 kg | Rango Oficial |
| 3 | Mochila de expedición | 24 | 50 kg | Rango Experto |
| 4 | Mochila de maestro | 28 | 60 kg | Rango Artesano, con un material raro |

Los números son orientativos y van al registro de balance.

**Se amplía, no se tira.** Una mochila sube de nivel con **mejoras** sobre la misma pieza, sin perder su tipo ni su calidad:

- **Costuras y refuerzos** (+2 casillas cada uno, hasta el tope de su nivel) y **correas** (+5 kg de peso cómodo). Los fabrica el mismo oficio.
- **Subir de nivel** pide al artesano del rango que toca, materiales y oro del juego.
- La **calidad** de la fabricación (ver [Fabricación](../07-economia/fabricacion.md)) da un pequeño extra: una mochila de calidad excelente lleva 1 casilla más.

## 3. Tipos de mochila según el oficio

Cada mochila puede llevar **un compartimento de oficio**. El compartimento tiene casillas propias que solo aceptan ciertas cosas y da una comodidad de ese oficio. **Nunca da poder de combate**: ayuda a trabajar, a viajar y a comerciar. Así el oficio hace la diferencia, como pide D-49, sin desbalancear las peleas.

| Tipo | Para | Compartimento | Qué permite | Pieza extra (otro oficio) |
|---|---|---|---|---|
| 🌿 **Mochila de herborista** | Herboristería, Agricultura | Bolsillo de hierbas (+10 casillas, solo hierbas, hongos y flores) | Las hierbas no se marchitan durante el viaje; ves la estación de cada hierba que recoges | Forro de lino (Sastrería) |
| ⛏ **Mochila de minero** | Minería, Fundición | Saco de mineral (+8 casillas, solo mineral, piedra y gemas en bruto) | El mineral pesa la mitad; el pico va colgado y no ocupa casilla | Armazón de hierro (Herrería) |
| 🩺 **Botiquín de médico** | Medicina, Primeros Auxilios | Botiquín (+8 casillas, solo vendas, remedios e instrumental) | Tratar en el campo lo que pide instrumental (suturas, entablillar) sin volver a una enfermería; el instrumental no se ensucia | Estuche de instrumental (Herrería) |
| 🪤 **Morral de cazador** | Desuello y caza | Morral de trampas (+8 casillas, solo trampas, cebos, pieles y carne) | Las trampas van armadas y se colocan en un toque; pieles y carne tardan el doble en echarse a perder | Ganchos (Herrería) |
| 🐴 **Alforjas de buhonero** | Comercio | Fardo de mercancía (+10 casillas, solo bienes empaquetados para vender) | La mercancía empaquetada pesa un 25 % menos; ves el precio del mercado local al entrar a un asentamiento | Sello de comerciante (Inscripción) |
| 🔨 **Mochila de obra** | Construcción | Cinturón de herramientas (+6 casillas, solo herramientas y piezas de obra) | Las herramientas no ocupan casillas de la mochila; llevas a la obra las piezas pequeñas sin carreta | Hebillas (Herrería) |
| ⚗️ **Estuche de alquimista** | Alquimia | Estuche de frascos (+8 casillas, solo frascos, pociones e ingredientes) | Los frascos no se rompen al caer ni al viajar; las pociones se apilan hasta 15 | Frascos de vidrio soplado (Joyería) |
| 🍲 **Fiambrera de cocinero** | Cocina, Pesca | Despensa portátil (+8 casillas, solo comida e ingredientes) | La comida y el pescado no se estropean en el viaje; cocinar al fuego de campamento sin estación | Caja aislada (Carpintería) |
| 🗝 **Mochila de ladrón** | Ladrones (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)) | Bolsillos ocultos (+4 casillas) | Lo que va en los bolsillos ocultos no aparece cuando un guardia te registra; no estorba el sigilo | Costuras dobles (Sastrería) |
| 🗺 **Portamapas de explorador** | Cartografía (Inscripción), Arqueología | Tubo de mapas (+6 casillas, solo mapas, notas y muestras) | Los mapas y las notas no se mojan ni se pierden; anotar un lugar nuevo es un toque | Tubo encerado (Carpintería) |
| 📜 **Cartapacio de escriba** | Inscripción | Cartapacio (+6 casillas, solo pergaminos, tintas y libros) | Copiar y leer pergaminos en el viaje; las tintas no se derraman | Tapas de cuero (Peletería) |

- **Una mochila, un compartimento.** Cambiar de tipo es cambiar de mochila: quien trabaja en varios oficios (D-57) tiene varias y elige cuál llevar en cada salida. Esa elección es parte del costo natural de serlo todo.
- **La mochila general** (sin compartimento) tiene 2 casillas más que una de oficio del mismo nivel. Es la mejor si no te dedicas a nada en particular.
- **Los cinturones no tienen tipo de oficio.** El cinturón decide lo que usas en combate, y el combate tiene que ser igual para todos (D-49).

## 4. El cinturón de combate

El cinturón es lo único que se abre con el botón 🎒 **Mochila** en combate (D-46). Las reglas de uso están en [Ronda y acciones](../04-combate/ronda-y-acciones.md) §4; aquí, lo que es el cinturón como objeto.

| Cinturón | Casillas | Quién lo hace |
|---|---|---|
| Cordel (inicial) | 3 | Se recibe al crear el personaje |
| Cinturón de cuero | 4 | Peletería, rango Aprendiz |
| Cinturón reforzado | 5 | Peletería, rango Experto |
| Cinturón de maestro | 6 | Peletería, rango Artesano |

- **Cada casilla lleva un solo tipo de objeto**, hasta 3 unidades. Seis casillas es el tope: con más, el menú del combate dejaría de caber en la pantalla.
- **Qué va:** pociones de vida, de resistencia y de recurso, remedios para estados (antídoto para el veneno, coagulante y venda para el sangrado, ungüento para la quemadura, tónico caliente para la congelación), vendas, bombas, comida rápida y el kit de ajuste de prótesis.
- **Límites que ya existen:** usar un objeto gasta la elección de la ronda, la **Toxicidad** limita cuántas pociones aguantas (ver [Condiciones](../05-salud/condiciones.md) §4) y hay un máximo de 3 lanzables por pelea (ver [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md)).
- **Se prepara antes de salir** y **se rellena solo** desde la mochila al terminar cada pelea, si tienes con qué.
- **Configuraciones guardadas:** el cinturón se guarda junto con cada configuración de [Talentos](talentos.md) ("solitario", "mazmorra", "PvP"). Cambiar de configuración cambia también el cinturón, en un toque.
- **En la arena clasificada** el cinturón es el mismo para todos (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md) §11).
- **No se compra con dinero real.** Ni casillas ni cinturones (D-43): el cinturón es poder de combate.

## 5. Alforjas de montura y carretas de caravana

| Medio | Capacidad orientativa | Qué cambia | Quién lo hace |
|---|---|---|---|
| 🐎 **Alforjas de montura** | +12 casillas y +30 kg de peso cómodo | Solo mientras vas montado. No se abren en combate | Peletería (rama Monturas) |
| 🐂 **Montura de carga** (mula, buey) | +24 casillas y +80 kg | No acorta el viaje como una montura de silla; lleva mucho más | Ganadería; alforjas de Peletería |
| 🛒 **Carreta de caravana** | Cientos de casillas, toneladas | Va despacio y por caminos; se puede asaltar en zonas rojas y negras; la mejoran los caminos y las escoltas | Carpintería (carros de caravana); el oficio de Comercio suma capacidad |

- La montura y sus alforjas ocupan la ranura de **Montura** de [Equipamiento](equipamiento.md) §1.
- Las monturas y los tiempos de viaje están en [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md); las caravanas, los peajes y los asaltos, en [Economía](../07-economia/economia.md) y en [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) (concesiones de ruta).
- **Por qué conviene.** Si mover mucho fuera fácil, no habría oficio de transportista ni mercados distintos en cada lugar (D-58).

## 6. Dónde se guarda lo que no llevas

Lo guardado **nunca se pierde al caer**. Todo depósito está **en un lugar** del mapa: lo que guardas en un asentamiento está ahí, y para usarlo hay que ir (D-58).

| Depósito | Dónde | Capacidad orientativa | Para qué |
|---|---|---|---|
| 🛏 **Cuarto** | Tu comunidad o tu asentamiento de residencia | 10 casillas | Lo básico; sus guardias lo cuidan (ver [El Colapso y las comunidades](../02-mundo/el-colapso-y-las-comunidades.md)) |
| 🏦 **Banco personal** | Cada asentamiento con banco | 50 casillas por banco, en pestañas | Lo tuyo, en ese lugar. Un banco en cada ciudad donde comercias |
| 🏦 **Banco de cuenta** | En los mismos bancos | 20 casillas por banco | Compartido entre los personajes de tu cuenta, en ese lugar. Sirve para pasarle cosas a otro héroe tuyo |
| 🏠 **Almacén de casa** | Tu casa (ver [Casa propia](../09-construccion/casa-propia.md)) | Según la habitación y sus estanterías y cofres | Lo grande: materiales del taller, cosechas, trofeos. Al lado de tus estaciones |
| 🏰 **Almacén de gremio** | El salón del gremio | Según la obra | Compartido, con permisos por rango (ver [Gremios y social](../08-social/gremios-y-social.md)) |

- **Los bancos cobran una pequeña tasa** por sacar objetos (sumidero de oro). Guardar es gratis.
- **El banco amplía pestañas** con oro del juego y con logros.

## 7. Ampliaciones: se fabrican y se ganan

| Cómo | Qué amplía |
|---|---|
| 🔨 **Se fabrican** | Mochilas, mejoras de mochila, cinturones, alforjas, carretas, estanterías y cofres del almacén. Es la vía principal y la que mueve la economía |
| 🏆 **Se ganan jugando** | Correas y costuras raras que dan cacerías, jefes y colecciones (por ejemplo, *correa de piel de Wyrm*: +5 kg); pestañas de banco por logros; la mochila de oficio de rango Maestro como premio del examen del oficio |
| 💳 **Dinero real** (D-43) | **Nada.** El dinero real solo compra cosméticos y aceleradores (ver [Monetización](../07-economia/monetizacion.md)), y el espacio no es ninguna de las dos cosas |

**Por qué nada.** Más mochila es más botín por viaje, más cinturón es más poder en la pelea y más banco es más ventaja en el comercio. Por eso **la mochila, el cinturón, las alforjas, las carretas y el banco nunca se venden por dinero real** (ver también [Equipamiento](equipamiento.md) §8).

## 8. Qué se pierde al caer

La tabla general está en [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1. Esto define qué parte del inventario cae en cada zona:

| Zona | Mochila | Cinturón | Alforjas | Lo puesto |
|---|---|---|---|---|
| 🔵 **Azul** | No se puede caer | — | — | — |
| 🟡 **Amarilla** | Se queda contigo | Se queda contigo | Se quedan contigo | −10 % de durabilidad |
| 🔴 **Roja** | **Se puede saquear**, compartimento incluido | **Se puede saquear** | La montura huye y vuelve al último establo con sus alforjas | Se queda contigo, con −10 % de durabilidad |
| ⚫ **Negra** | Se puede saquear | Se puede saquear | Se pueden saquear | Se puede saquear |

- **Nunca se pierde:** lo guardado (§6), las **prótesis**, los objetos de misión y los objetos **atados** a tu personaje (ver [Equipamiento](equipamiento.md) §5).
- **No hay casillas a salvo.** No existe un "contenedor seguro" como el de *Tarkov*: el riesgo de la zona tiene que ser real. Lo que no quieres arriesgar se deja en el banco.
- **Juramento de Hierro:** las mismas reglas, con lo que ya dice [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.2.

## 9. Ligero de manejar: filtros y orden automático

La capa simple no pide ordenar nada (D-44):

- **Orden automático.** La mochila se ordena sola por grupos: 📦 Materiales, 🧪 Consumibles, ⚔️ Equipo, 📜 Misión, 💰 Para vender. Las pilas se juntan solas.
- **Filtros de un toque.** Cada grupo es un botón con su número; se abre solo lo que pides.
- **Al compartimento, solo.** Lo que va en el compartimento de oficio entra ahí primero, sin preguntar.
- **🏦 Depositar materiales.** En un banco o en tu casa, un toque manda todos los materiales al depósito. Los consumibles y el cinturón se quedan.
- **💰 Vender lo sobrante.** En un mercader PNJ, un toque vende lo marcado "para vender" (el equipo que no te sirve, ver [Botín](botin.md)). Lo marcado con 🔒 nunca se vende ni se tira.
- **Mochila llena.** El bot no pierde nada en silencio: ofrece cambiar lo nuevo por lo de menos valor, dejarlo o abrir la mochila.

**Capa profunda (opcional):** reglas de recogida ("no recoger lo gris", "solo hierbas de calidad buena o mejor"), pestañas de banco con nombre y orden a mano.

## 10. Cómo se ve

**La mochila** (comando `/mochila` o botón 🎒 fuera de combate):

```
🎒 Mochila de herborista · Nivel 3 (Expedición)
📦 18/24 casillas · ⚖️ 41/50 kg · cómodo

🌿 Bolsillo de hierbas 7/10 · no se marchitan
   Hoja de plata ×14 · Hongo nocturno ×6 · Flor de escarcha ×3

[📦 Materiales 8] [🧪 Consumibles 5]
[⚔️ Equipo 2] [📜 Misión 1] [💰 Para vender 2]
[🪢 Cinturón] [🏦 Depositar materiales]
```

**El cinturón** (botón 🪢 Cinturón):

```
🪢 Cinturón reforzado · 5 casillas · hasta 3 por casilla
Configuración: Solitario ✓ · Mazmorra · PvP

1. 🧪 Poción de vida ×3
2. 🔥 Resistencia al fuego ×2
3. 💊 Coagulante ×2
4. 🩹 Venda ×3
5. 🍖 Pan de viaje ×3

↻ Se rellena solo al terminar cada pelea
   (quedan 🧪 ×7 y 🩹 ×4 en la mochila)

[✏️ Cambiar una casilla] [💾 Guardar en esta configuración]
```

**Mochila llena:**

```
⚠️ Mochila llena. Encontraste 🪨 Mineral de hierro ×3.

[🔄 Cambiarlo por 🦴 Hueso ×2 (lo de menos valor)]
[🗑 Dejarlo aquí] [🎒 Abrir la mochila]
```

## 11. Red de sistemas

| Consume | Produce |
|---|---|
| Cuero, tela, hilo, piezas de otros oficios (hierro, vidrio, madera), oro del juego para mejoras y tasas de banco | Demanda para Peletería, Sastrería y los oficios de las piezas extra; un límite a lo que se trae por viaje, que crea transportistas, caravanas y mercados locales; riesgo real en zonas rojas y negras; la preparación del cinturón como conocimiento del jugador (D-49) |

Se conecta con la [Red de sistemas](../00-vision/red-de-sistemas.md) por la economía (fabricación y sumideros), el viaje (peso) y el combate (cinturón).

## 12. Todo en texto, por turnos y sin dinero real que dé poder

- Todo es texto y botones: casillas que se cuentan, pesos en kilos y un mensaje por pantalla.
- El motor guarda el inventario igual para los tres clientes (Telegram, web y app). La web puede mostrar más casillas por pantalla, pero las reglas son las mismas (D-40, D-41).
- El dinero real no amplía nada de esto: solo compra cosméticos y aceleradores (D-43).
