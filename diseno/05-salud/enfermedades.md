# Enfermedades

> **Módulo** [05 · Salud](README.md) · **Depende de:** [Heridas](heridas.md), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (clima, estaciones) · **Alimenta a:** [Profesiones](../07-economia/profesiones.md) (Medicina, Alquimia), [Eventos](../06-contenido/eventos.md) · **Estado:** propuesta

**De dónde sale.**
- *RimWorld*: enfermedad como **carrera entre gravedad e inmunidad**.
- *Crusader Kings III*: epidemias con intensidad menor, mayor o apocalíptica, y el médico de corte que se dedica a controlarlas.
- *Pathologic 2*: plaga sin cura total, en la que solo se controlan los síntomas.
- *DayZ*: enfermedades por agua sucia y carne cruda.
- *Skyrim*: enfermedades contagiadas por criaturas, y **vampirismo y licantropía** como enfermedades con ventajas.
- *World of Warcraft*: el incidente de la **Sangre Corrupta** (septiembre de 2005). Un debuff contagioso escapó de una banda y arrasó las capitales; lo estudiaron epidemiólogos en revistas científicas. Aquí se hace **a propósito**, como evento.

---

## 1. El modelo: carrera entre gravedad e inmunidad

Al contraer una enfermedad aparecen dos barras:
- **Gravedad:** sube cada hora, según la enfermedad.
- **Inmunidad:** sube cada hora según tu descanso, tu alimentación, el tratamiento que recibes y tu linaje.

Si la inmunidad llega a 100 primero, te curas y quedas inmune un tiempo. Si la gravedad llega primero, la enfermedad pasa a su **desenlace**: normalmente una fase crónica o una secuela, **nunca la muerte del personaje** fuera del modo Juramento de Hierro.

Tratar una enfermedad no la borra: **acelera la inmunidad** o **frena la gravedad**. Un buen médico con buenos medicamentos convierte una carrera perdida en ganada.

**Fases:** incubación (no sabes que la tienes, pero ya contagias) → síntomas → pico → recuperación o desenlace.

## 2. Contagio

- **De criatura a jugador:** mordidas, heridas infectadas, comer carne cruda, beber agua de pantano.
- **De jugador a jugador:** algunas enfermedades se contagian dentro del grupo (mazmorras, bandas) o en asentamientos concurridos. El Licántropo huele la enfermedad en otros, y un médico la puede diagnosticar.
- **Cuarentena:** durante una epidemia, los asentamientos pueden declararla. La declara el alcalde PNJ, o el gremio si el territorio es suyo. Hay menos comercio y menos contagio.
- **Máscaras y ropa** fabricadas por sastres y médicos bajan el contagio.

## 3. Catálogo inicial

| Enfermedad | Dónde se contrae | Síntomas | Tratamiento | Si se pierde la carrera | Inspiración |
|---|---|---|---|---|---|
| **Fiebre del Pantano** | Tramo IV, picaduras | Fiebre, Aguante bajo; **vuelve** en brotes | Corteza amarga (Alquimia) | Crónica: un brote cada semana hasta tratarla | Malaria (RimWorld) |
| **Gripe de Escarcha** | Frío, tramo VI, invierno | Baja la iniciativa, tos | Reposo caliente, caldo | Neumonía, más grave y más larga | Resfriado (DayZ) |
| **Disentería** | Agua sucia, carne cruda | El Sustento cae en picada | Carbón, agua hervida | Varios días de debilidad | DayZ, *Oregon Trail* |
| **Gangrena** | Herida infectada sin tratar | La zona empeora sola | Limpiar, cirugía | **Amputación** del miembro | Project Zomboid, RimWorld |
| **Tétanos de Óxido** | Heridas de armas oxidadas | Rigidez: pierdes la acción rápida | Antitoxina | Espasmos crónicos | — |
| **Podredumbre Gris** | Criaturas pútridas | Daño lento; la piel se cae | Ungüento de plata | Cicatriz extensa | Podredumbre escarlata (Elden Ring) |
| **Tos del Minero** | **Oficio:** minar sin máscara mucho tiempo | Baja el Aguante máximo | Máscara, hierbas para el pulmón | Crónica leve | Enfermedad laboral |
| **Temblor Arcano** | **Oficio o clase:** abusar de la magia arcana | Los hechizos fallan | Reposo mágico | Quemadura de Maná crónica | — |
| **Fiebre del Vacío** | Tramo IX, criaturas del Vacío | El estrés sube solo | Templo, bardo | Corrupción permanente | Cordura de WoW |
| **Plaga Pálida** | **Evento de servidor** (§4) | Contagiosa, varias fases | Una cura que médicos y alquimistas fabrican en cadena | Semanas de debilidad | Sangre Corrupta (WoW), Peste Negra (CK3) |
| **Parásito de Río** | Pescado crudo | El Sustento baja más rápido | Purga (Alquimia) | Delgadez: baja la vida máxima | — |
| **Fiebre de Sangre** | Mordida de vampiro | Sed, rechazo al sol | Ritual antes de 3 días | **Vampirismo** (§5) | Sanguinare Vampiris (Skyrim) |
| **Mordida del Lobo Lunar** | Licántropos salvajes | Pesadillas, hambre | Ritual antes de la luna llena | **Licantropía** (§5) | Skyrim |
| **Mal del Piso** | Subir a un clima nuevo | Penalización pequeña | Tiempo | — | Mal de altura |

**Enfermedades laborales.** La Tos del Minero y el Temblor Arcano muestran que los oficios también dejan huella. La protección (máscaras, guantes, delantales) la fabrican otros artesanos: el cuerpo también mueve la economía.

## 4. Epidemias de servidor

Una vez por temporada llega una **Plaga** a la Torre. Es un evento con historia:
1. **Brote.** Aparece en un piso por culpa de una criatura, una caravana o un gremio que abrió una cripta.
2. **Propagación.** Los jugadores la llevan de un asentamiento a otro sin saberlo, porque la incubación ya contagia. La Gaceta publica el mapa de contagios.
3. **Respuesta.** Médicos y alquimistas investigan la cura: una receta que se descubre entre todos, aportando ingredientes. Los gremios declaran cuarentenas y aparecen curanderos falsos (misiones).
4. **Final.** La cura se fabrica en cadena, quienes ayudaron reciben recompensas y los médicos que más curaron ganan un título.

**Por qué conviene.** La Sangre Corrupta de 2005 fue un accidente que la gente recuerda veinte años después. Hecha a propósito, con salidas claras y sin matar personajes, es el tipo de evento que une a un servidor y le da trabajo a las profesiones de servicio.

## 5. Maldiciones con ventajas: vampirismo y licantropía

En Skyrim, contraer vampirismo o licantropía es una enfermedad que te transforma si no la curas a tiempo, con ventajas reales y costos reales.

| | Vampirismo | Licantropía |
|---|---|---|
| **Ventajas** | Visión nocturna, robo de vida, resistencia a enfermedades naturales | Forma bestial en combate (ráfaga), regeneración, olfato |
| **Costos** | Débil al sol en zonas abiertas de día; los asentamientos de luz lo rechazan; necesita sangre | Pierde el control en luna llena (evento); los cazadores de bestias lo persiguen; rompe equipo al transformarse |
| **Cura** | Ritual caro con misión propia | Ritual caro con misión propia |
| **Contagio** | Puede contagiar a otros jugadores, con su consentimiento o en PvP | Igual |

No tocan el presupuesto de poder en contenido clasificado: la forma bestial reemplaza habilidades, no las suma. Son **identidad**, no ventaja competitiva.

## 6. Límites

- **Protección de novato:** hasta el nivel 10 no hay enfermedades serias.
- **Tiempo fuera de línea:** la inmunidad sigue subiendo mientras no juegas (descansar ayuda). Quien no entra dos días vuelve mejor, no peor.
- **Una enfermedad seria a la vez**, salvo durante las epidemias.
