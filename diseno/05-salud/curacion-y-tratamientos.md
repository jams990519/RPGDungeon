# Curación: cómo se tratan las enfermedades y los problemas del cuerpo y la mente

> **Módulo** [05 · Salud](README.md) · **Depende de:** [Heridas](heridas.md), [Condiciones](condiciones.md), [Enfermedades](enfermedades.md), [Mente](mente.md), [Secuelas](secuelas-y-muerte.md) · **Se conecta con:** [Profesiones](../07-economia/profesiones.md) (Medicina, Alquimia, Herboristería), [Construcción](../09-construccion/casa-propia.md) (enfermería), [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md) (sanatorio y templo) · **Estado:** propuesta

Los demás documentos de salud dicen **qué te puede pasar**. Este dice **cómo se cura**: quién, dónde, con qué, cuánto cuesta y qué puede salir mal. Es también el corazón del oficio de médico.

**De dónde sale.**
- *Darkest Dungeon*: el sanatorio, con su lista de espera, sus precios y sus tratamientos por rareza.
- *Project Zomboid*: primeros auxilios paso a paso.
- *Two Point Hospital* y *Theme Hospital*: diagnóstico antes del tratamiento; diagnosticar mal cuesta.
- *Achaea* (MUD): cada remedio tiene su enfriamiento, y en combate importa el **orden** en que se curan las aflicciones.
- *RimWorld*: la calidad del médico y de la medicina decide el resultado, y las cirugías pueden fallar.
- *Mount & Blade II*: la Medicina del cirujano decide cuántos heridos se salvan.
- *Torn*: hospital con tiempo real, reducible con objetos médicos.
- *Pathologic 2*: remedios que solo alivian los síntomas y antibióticos escasos.
- *Final Fantasy XIV*: el minijuego de fabricación, del que sale el minijuego de cirugía.

---

## 0. Curar es un oficio que se estudia

Pediste que quien cura enfermedades tenga que **estudiar**, como una profesión (enfermero o algo así), con su minijuego y cobrando por ello. Así queda:
- **Los sanadores de clase** (Sacerdote, Paladín Sagrado, Druida Restauración…) curan **vida** en combate y estabilizan. **No curan enfermedades** ni heridas graves.
- **Las enfermedades, las heridas graves y las cirugías** solo las trata quien estudió **Medicina** (ver [Profesiones](../07-economia/profesiones.md)), con sus rangos:

| Rango | Nivel de Medicina | Qué puede hacer |
|---|---|---|
| **Enfermero** | 1-30 | Vendar y suturar bien, cuidar a pacientes internados (acelera su recuperación), dar remedios, diagnóstico básico |
| **Médico** | 31-70 | Diagnóstico completo, tratamientos de enfermedades, heridas graves, desintoxicación |
| **Cirujano** | 71-100 | Cirugía (minijuego), heridas críticas, prótesis, amputaciones limpias, vacunas (con Epidemiología) |

- Se estudia con los **entrenadores** del ala de Oficios del Castillo, con **exámenes** en cada rango (ver [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md)).
- Se **cobra** por cada consulta, tratamiento y cirugía (§6), y un gremio puede pagar un sueldo a su médico.

## 1. El camino de una cura

```
SÍNTOMA ──> DIAGNÓSTICO ──> TRATAMIENTO ──> RECUPERACIÓN ──> (secuela o alta)
```

1. **Síntoma.** El jugador ve lo que siente ("fiebre alta, tos seca"), no siempre el nombre de lo que tiene. Durante la incubación, ni eso.
2. **Diagnóstico.** Un médico (jugador o PNJ) examina y dice qué es, con qué seguridad y qué conviene. Un buen diagnóstico ahorra tratamientos inútiles.
3. **Tratamiento.** Remedios, cirugía, magia, reposo o ritual, según el problema.
4. **Recuperación.** El tiempo hace el resto, más rápido si descansas bien.
5. **Alta o secuela.** Si todo sale bien, te vas sano (y a veces inmune). Si no, puede quedar un mal crónico (ver [Secuelas](secuelas-y-muerte.md)).

## 2. Diagnóstico

| Quién diagnostica | Qué tan bien | Costo |
|---|---|---|
| **Tú mismo** | Solo lo evidente (una fractura, una quemadura). Para una enfermedad, te dice "algo en los pulmones" | Gratis |
| **Licántropo** (linaje) | Huele la enfermedad y su familia | Gratis |
| **Médico jugador** | Según su nivel de Medicina: desde "fiebre de pantano, probablemente" hasta el nombre exacto, la fase y el mejor tratamiento | Lo que cobre |
| **Sanatorio del Castillo** | Exacto siempre | Caro |

**Diagnóstico equivocado:** tratar una enfermedad con la cura de otra gasta el remedio y no ayuda (y a veces empeora). Por eso un médico con buena fama vale oro.

## 3. Tipos de tratamiento

| Tratamiento | Qué hace | Para qué sirve | Quién lo da |
|---|---|---|---|
| **Primeros auxilios** | Vendar, torniquete, limpiar, entablillar de emergencia | Frenar el sangrado, evitar infecciones, estabilizar | Cualquiera con el objeto |
| **Remedios** (pociones, ungüentos, tinturas, píldoras) | Suben la inmunidad, frenan la gravedad, alivian síntomas, quitan el dolor | Enfermedades, dolor, toxicidad, venenos | Alquimistas y herboristas los fabrican; cualquiera los usa |
| **Tratamiento médico** | Suturas, recolocar huesos, limpiar heridas infectadas, tratamientos largos | Heridas moderadas y graves, infecciones | Médico |
| **Cirugía** (minijuego, §4) | Operar | Heridas críticas, hemorragia interna, amputación limpia, implantar prótesis, extraer parásitos | Médico con rango de cirujano |
| **Magia sanadora** | Devuelve vida, frena el sangrado, estabiliza, baja un nivel a heridas leves y moderadas | Combate y emergencias (ver [Heridas](heridas.md)) | Sanadores |
| **Restauración** | Cura una herida de cualquier gravedad | Lo irremediable | Sanadores, una vez al día, con reactivo raro |
| **Reposo** | Sube la inmunidad y acelera toda curación | Todo | Posada, casa, enfermería |
| **Dieta** | Comidas que suben la inmunidad o curan males digestivos | Enfermedades, parásitos | Cocineros |
| **Ritual** | Purificar, levantar maldiciones, curar vampirismo y licantropía, limpiar corrupción | Maldiciones, corrupción | Templo, sacerdotes, misiones |
| **Terapia de la mente** | Música, compañía, templo, descanso | Estrés, aflicciones, colapso | Bardos, taberna, templo, gremio |
| **Desintoxicación** | Baja la toxicidad y la dependencia | Abuso de pociones, adicciones | Médico, alquimista, tiempo |
| **Cuarentena** | Aísla para no contagiar; mientras dura, la inmunidad sube más rápido por reposo | Epidemias | El asentamiento o el gremio la declaran |
| **Vacuna** | Inmunidad preventiva durante un tiempo | Enfermedades ya investigadas | Médicos, después de investigar la cura (ver [Investigaciones](../06-contenido/investigaciones.md)) |

## 4. Cirugía: el minijuego del médico

**De dónde sale.** El minijuego de fabricación de *Final Fantasy XIV* (ver [Fabricación](../07-economia/fabricacion.md)), aplicado a un paciente, con el riesgo de las cirugías de *RimWorld*.

**Las barras:**
- **Progreso de la operación:** cuando se llena, la operación terminó.
- **Estabilidad del paciente:** baja con cada acción agresiva; si llega a 0, el paciente queda en estado crítico y hay que estabilizarlo o abortar.
- **Limpieza:** si baja, sube el riesgo de infección posterior.
- **Dolor:** si sube demasiado, el paciente se agita y cada acción rinde menos (un analgésico lo baja).
- **Concentración del médico:** el recurso para las acciones especiales.

**Acciones:** Incisión, Suturar, Cauterizar, Limpiar, Anestesiar, Estabilizar, Extraer, Implantar (prótesis), Observar.

**Resultado:**
- **Éxito limpio:** herida resuelta, sin infección, recuperación rápida.
- **Éxito con complicaciones:** resuelta, pero con riesgo de infección o recuperación más lenta.
- **Fracaso:** no se resolvió; el paciente queda como estaba o algo peor (nunca muere, salvo en el Juramento de Hierro). El médico pierde reputación.

**Lo que ayuda:** el nivel de Medicina del médico, la calidad del instrumental (Herrería), la sala (una enfermería bien equipada en casa, en el gremio o en el sanatorio), los remedios que se usen (Alquimia) y las vendas limpias (Sastrería).

**Cómo se ve:**

```
🩺 Cirugía — Hemorragia interna (Bram, abdomen)
Progreso    ▓▓▓▓▓░░░░░  50 %
Estabilidad ▓▓▓▓▓▓▓░░░  ❤️ estable
Limpieza    ▓▓▓▓▓▓▓▓░░  🧼 buena
Dolor       ▓▓▓▓░░░░░░  😖 moderado
Concentración 140/220

[🔪 Incisión]      [🧵 Suturar]
[🔥 Cauterizar]    [🧼 Limpiar]
[💉 Anestesiar]    [❤️ Estabilizar]
[👁 Observar]      [⛔ Abortar]
```

## 5. Dónde curarse

| Lugar | Qué ofrece | Costo | Velocidad |
|---|---|---|---|
| **En el campo** | Primeros auxilios y remedios que llevas | Tus objetos | Inmediato, limitado |
| **Consulta de un médico jugador** | Diagnóstico, tratamientos, cirugía; puede ser en su casa, en tu casa o en la sala del gremio | Lo que cobre (con garantía del bot) | Según su agenda |
| **Enfermería de tu casa** | Reposo ×3, sala para que un médico opere | Construirla (ver [Casa propia](../09-construccion/casa-propia.md)) | — |
| **Enfermería del gremio** | Igual, para todos los miembros, con mejor equipo | Del gremio | — |
| **Sanatorio del Castillo** | Todo: diagnóstico exacto, tratamientos, cirugía segura. Hay lista de espera en epidemias | Caro: sumidero de oro y **techo de precios** para los médicos jugadores | Rápido |
| **Templo** | Rituales, maldiciones, corrupción, estrés, Restauración | Donación | Según el caso |
| **Taberna** | Bardos y banquetes contra el estrés | Propina, comida | Una noche |
| **Refugio de forajidos** | Un matasanos que atiende a jugadores con karma rojo | Caro y riesgoso | Rápido |

## 6. Consulta médica entre jugadores en Telegram

1. El paciente escribe `/medico` y elige: diagnóstico, tratamiento o cirugía.
2. El bot muestra a los médicos disponibles con su rango, especialidad, reputación y precio, y dónde atienden.
3. El paciente elige. El pago queda **en custodia** del bot.
4. El médico acepta y hace el diagnóstico o la cirugía (minijuego). El paciente ve el progreso en su propio mensaje vivo.
5. Al terminar, el pago se libera. El paciente puede dar un 👍 que suma a la reputación del médico.
6. Si el médico no se presenta en el tiempo acordado, el pago vuelve.

## 7. Qué cura qué

| Problema | Primera respuesta | Cura completa |
|---|---|---|
| Sangrado | Venda, torniquete, magia | Sutura |
| Laceración, herida profunda | Venda limpia | Sutura; cirugía si es crítica |
| Fractura | Entablillar | Tiempo con férula; cirugía si es crítica o soldó mal |
| Quemadura | Ungüento | Injerto (cirugía) en grado 3 |
| Congelación | Calor gradual | Tratamiento; amputación limpia si hay necrosis |
| Conmoción | Reposo sin combate | Tiempo; tratamiento del médico |
| Hemorragia interna | Estabilizar (magia) | Cirugía |
| Infección de herida | Limpiar | Antiséptico y tratamiento; cirugía si es gangrena |
| Fiebre del Pantano | Corteza amarga | Tratamiento completo, o seguirá volviendo |
| Gripe, neumonía | Caldo y reposo | Remedios, reposo en cama |
| Disentería, parásitos | Carbón, agua hervida | Purga, dieta |
| Tos del Minero | Máscara | Tratamiento de pulmón (crónico, se alivia) |
| Temblor Arcano, Quemadura de Maná | Reposo mágico | Tratamiento; runas de protección |
| Veneno | Antídoto | Antídoto específico de ese veneno |
| Podredumbre Gris | Ungüento de plata | Tratamiento largo; cicatriz |
| Plaga (epidemia) | Aislarse, remedios de síntomas | La cura que investiga la comunidad, y después la vacuna |
| Fiebre de Sangre (vampirismo) | Ritual antes de 3 días | Si ya te transformaste: el ritual mayor con su misión |
| Licantropía | Ritual antes de la luna llena | El ritual mayor con su misión |
| Dolor | Analgésico | Curar la herida que lo causa |
| Estrés y aflicciones | Taberna, bardo | Descanso, templo |
| Corrupción | — | Misiones largas del templo |
| Toxicidad | Esperar | Desintoxicación |
| Dependencia | Dejar de consumir | Tratamiento del médico |
| Miembro perdido | — | Prótesis, ritual de regeneración, o paciencia (Trol) |
| Mal crónico | Tratamiento que alivia | Médico maestro o cadena de misiones |

## 8. Medicinas: calidad, caducidad y escasez

- Todo remedio tiene **calidad** (ver [Fabricación](../07-economia/fabricacion.md)): uno excelente sube la inmunidad mucho más que uno normal.
- Algunos **caducan**: los remedios frescos rinden más, así que siempre hay demanda.
- Algunos ingredientes son **escasos** y de temporada (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)). En una epidemia, los antibióticos suben de precio y aparecen falsificadores (misión y caso de [investigación](../06-contenido/investigaciones.md)).
- **Botiquín:** una ranura de mochila para 5 remedios de uso rápido en combate. Cada uno cuenta para la toxicidad (ver [Condiciones](condiciones.md)).

## 9. El médico como carrera completa

Se puede jugar dos años siendo médico:
- **Rangos de Medicina** con especialidades: Cirugía, Farmacia y Epidemiología (ver [Profesiones](../07-economia/profesiones.md)).
- **Reputación de médico**, visible en la consulta.
- **Consulta propia** en tu casa (construida y equipada) o en la sala del gremio.
- **Contratos con gremios:** médico de cabecera de un gremio de bandas, con sueldo.
- **Epidemias:** el momento de gloria del médico, con títulos para quienes más curaron.
- **Entrenadores** en el ala de oficios del Castillo (ver [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md)).

Ver P-20 a P-25 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
