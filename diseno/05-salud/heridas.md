# Heridas

> **Módulo** [05 · Salud](README.md) · **Depende de:** [Combate](../04-combate/README.md) (golpes, críticos, tipos de daño), [Equipamiento](../03-personaje/equipamiento.md) (protección por zona) · **Alimenta a:** [Profesiones](../07-economia/profesiones.md) (Medicina), [Secuelas](secuelas-y-muerte.md) · **Estado:** propuesta

**De dónde sale.**
- *Escape from Tarkov*: 7 zonas con vida propia, sangrado leve y grave, fracturas, y el miembro "negro" (inutilizado) que solo se arregla con cirugía.
- *Project Zomboid*: tipos de herida con riesgo de infección distinto, vendas limpias contra sucias, entablillar.
- *Dwarf Fortress*: el cuerpo por capas, y la piel como barrera contra la infección.
- *Battle Brothers*: heridas temporales que se curan en días.
- *Achaea* (un MUD de texto): aflicciones curadas con hierbas y ungüentos, cada uno con su enfriamiento. Demuestra que esto funciona en texto puro.

---

## 1. El mapa del cuerpo

Siete zonas, como en Tarkov: pocas para leerlas de un vistazo, suficientes para que importen.

| Zona | La protege (ver [Equipamiento](../03-personaje/equipamiento.md)) | Si está herida |
|---|---|---|
| **Cabeza** | Casco | Baja la precisión; los hechizos pueden fallar; riesgo de conmoción; se puede perder un ojo (nunca los dos) |
| **Torso** | Pecho, hombros | Baja el Aguante máximo; posible hemorragia interna. Zona vital |
| **Abdomen** | Cintura, pecho | El Sustento baja más rápido; se infecta con más facilidad. Zona vital |
| **Brazo izquierdo** | Muñecas, guantes | El escudo o el arma secundaria rinden menos |
| **Brazo derecho** | Muñecas, guantes | El arma principal rinde menos; con una fractura no se pueden usar armas a dos manos |
| **Pierna izquierda** | Piernas, botas | Baja la iniciativa; esquivar cuesta más Aguante |
| **Pierna derecha** | Piernas, botas | Igual. Con las dos piernas en estado grave no se puede huir ni cambiar de fila |

**Por qué conviene atarlo al equipo.** Cada ranura de armadura protege una zona concreta. Un casco ya no es "+12 de defensa": es lo que evita que un golpe de maza te deje una conmoción. Eso le da valor propio a cada pieza que fabrica un artesano.

**Cómo se ve (`/cuerpo`):**

```
🧍 Estado del cuerpo — Bram (Enano, Guerrero)

        🟢 Cabeza
🟡 Brazo izq.   🟢 Torso   🔴 Brazo der.
        🟢 Abdomen
   🟠 Pierna izq.     🟢 Pierna der.

🔴 Brazo der. — Fractura (grave)
   Entablillada · sana en 2 d 6 h · sin armas a dos manos
🟠 Pierna izq. — Laceración (moderada) · ⚠️ vendaje sucio
   Riesgo de infección: ALTO · cámbialo pronto
🟡 Brazo izq. — Contusión (leve) · sana en 3 h

🤒 Fiebre del Pantano (día 2)
   Gravedad ▓▓▓▓░░░░░░  Inmunidad ▓▓▓▓▓▓░░░░  → vas ganando
🧠 Estrés 38/100 · 🧪 Toxicidad 20 % · 🍖 Bien alimentado
```

## 2. Tipos de herida

| Herida | Causa típica | Efecto mientras dura | Tratamiento | Si no se trata, puede… | Si se deja empeorar, puede terminar en (♾️) |
|---|---|---|---|---|---|
| **Contusión** | Contundente | Penalización leve en la zona | Tiempo (horas) | — | — |
| **Arañazo** | Garras, espinas | Casi nada | Limpiar y vendar | Infectarse (poco) | — |
| **Laceración** | Corte | Sangrado leve | Vendar; suturar si es moderada o peor | Infectarse o pasar a sangrado grave | Si la infección llega a gangrena: pierna o brazo perdido |
| **Herida profunda** | Perforación, crítico | Sangrado grave | Sutura (Medicina) | Hemorragia; infección seria | Gangrena: pierna o brazo perdido. En la cabeza: ojo perdido |
| **Mordida** | Bestias, no-muertos | Sangrado y **riesgo de la enfermedad de esa criatura** | Limpiar; antídoto o tratamiento específico | Contagiar la enfermedad de la criatura | Mordida sucia → gangrena: pierna o brazo perdido. Podredumbre Gris: piel marcada |
| **Esguince / luxación** | Caídas, derribos | Bajan la iniciativa y la esquiva | Vendaje compresivo; recolocar (Medicina) | Volverse crónico 🔁 | En la rodilla, si se sigue forzando: rodilla destrozada |
| **Fractura** | Contundente fuerte, caídas | La zona casi no sirve | **Entablillar** y tiempo (días) | Soldar mal: *Rodilla mala* u otro mal crónico 🔁 | Volver a romper la misma pierna sin operarla: rodilla destrozada. Fractura abierta que se infecta: miembro perdido |
| **Quemadura** (grados 1 a 3) | Fuego, rayo, ácido | Dolor; en grado 3 se pierde piel y la infección es fácil | Ungüento; injerto en grado 3 | Infectarse; dejar cicatriz | Grado 3 sin injerto: piel marcada. En la cara: cicatriz grave. Ácido en los ojos: ojo perdido |
| **Congelación** | Escarcha, clima | Dedos o extremidades torpes | Calor gradual, no brusco | Necrosis | Dedos u oreja perdidos; si es todo el pie o la mano, el miembro |
| **Conmoción** | Golpe en la cabeza | Fallan la precisión y los hechizos; confusión | Reposo sin combate | Empeorar con otro golpe | Otra conmoción sin el reposo indicado: sordera parcial |
| **Hemorragia interna** | Perforación o contundente en torso o abdomen | Pierde vida máxima poco a poco | **Cirugía** | Derribarte fuera de combate | — |
| **Nervio dañado** | Cortes graves en brazos o piernas | Temblor: fallan las acciones de precisión | Tratamiento y tiempo largo | Volverse crónico 🔁 | En un brazo, seguir peleando con él sin el tratamiento: nervio cortado |
| **Miembro inutilizado** | Una zona recibe demasiado daño | La zona no funciona | Cirugía | Pasar a peligro de secuela (🔴) | Sin cirugía antes del último aviso: miembro perdido |

**Hasta dónde puede llegar.** La última columna dice a qué secuela definitiva (♾️) puede llevar cada herida si se deja empeorar. Nunca pasa de golpe: hace falta la cadena entera (no tratarla, que se complique, ignorar el aviso 🔴 y el último aviso), con un aviso claro en cada paso y tiempo para volver a un médico. Los efectos de cada secuela en combate y fuera de él, y qué la compensa, están en [Secuelas y muerte](secuelas-y-muerte.md) (§3 y §5).

## 3. Gravedad y tiempos

Cada herida tiene uno de cuatro niveles: **leve · moderada · grave · crítica**. La gravedad decide la penalización, el tiempo de curación y qué hace falta para tratarla.

| Gravedad | Tiempo orientativo (real) | Quién la trata |
|---|---|---|
| Leve | 1 a 6 horas | Tú mismo (vendas, descanso) |
| Moderada | 6 a 24 horas | Primeros Auxilios o un sanador en combate |
| Grave | 1 a 3 días | Médico (oficio Medicina) o sanatorio |
| Crítica | 3 a 7 días | Cirujano (Medicina alta) o sanatorio caro |

## 4. Cuándo aparece una herida

Nunca por un golpe cualquiera. Solo cuando:
1. **Recibes un crítico:** se tira una herida en la zona golpeada.
2. **Cruzas el 50 % y el 25 % de vida** en una misma pelea: una tirada en cada umbral, como en *Battle Brothers*.
3. **Te derriban:** herida garantizada, al menos moderada.
4. **Lo dice un movimiento de jefe:** "Aplastar" rompe huesos, "Mordisco Pútrido" contagia.
5. **Fuera de combate:** trampas, caídas durante la exploración, el clima.

La armadura de la zona reduce la probabilidad y la gravedad. El tipo de daño decide el tipo de herida (ver [Daño y estados](../04-combate/dano-y-estados.md)).

## 5. Tratar

| Nivel | Qué se puede hacer | Quién |
|---|---|---|
| **De campo** | Vendar, torniquete, analgésico, entablillado de emergencia | Cualquiera que tenga el objeto |
| **Primeros Auxilios** (oficio menor) | Limpiar, suturar heridas leves y moderadas, entablillar bien | Cualquiera que lo aprenda |
| **Medicina** (oficio mayor) | Suturar heridas graves, recolocar, cirugía, tratar enfermedades, amputar si hace falta | Jugadores médicos |
| **Sanatorio** (PNJ en las capitales) | Todo, rápido | Cobra caro: es un **sumidero de oro** |
| **Magia** | Ver §6 | Sanadores |
| **Descanso** | Acelera cualquier curación | En una posada o en casa propia |

**El descanso corre en tiempo real y también fuera de línea.** Dormir en una posada o en tu casa duplica la velocidad de curación, y una casa con enfermería la triplica. Encaja con Telegram: quien se va a trabajar deja al héroe "internado" y vuelve con él curado. Es el descanso de WoW (experiencia extra por estar fuera) aplicado al cuerpo.

**Los materiales cuentan.** Una venda sin desinfectar sube el riesgo de infección, como en Project Zomboid; una de lino limpio hecha por un sastre lo baja. Una férula de madera noble cura más rápido que una improvisada con un palo. Cada consumible médico tiene calidad (ver [Fabricación](../07-economia/fabricacion.md)).

## 6. La magia no lo arregla todo

Si un sacerdote pudiera borrar una fractura con un botón, el sistema no existiría. Las reglas:
- La curación mágica devuelve **vida**, frena el **sangrado** y puede **estabilizar**: una herida crítica deja de empeorar.
- Solo algunas habilidades, con enfriamiento largo, **bajan un nivel** a una herida leve o moderada: el Sacerdote Sagrado en combate y ciertos rituales fuera de él.
- Las heridas graves y críticas **siempre** necesitan tratamiento físico o el templo.
- El milagro mayor, **Restauración**, cura una herida de cualquier gravedad. Cada sanador puede hacerlo una vez al día, cuesta un reactivo raro y lo deja agotado.
- **Estabilizar también gana tiempo:** congela durante 10 pasos el reloj de una herida que va camino a una secuela, una vez por herida (ver [Secuelas y muerte](secuelas-y-muerte.md) §5).
- **Ninguna magia devuelve lo perdido.** Restauración cura la herida, no la secuela definitiva: no hace crecer una pierna ni un ojo.

**Por qué conviene.** Los sanadores siguen siendo imprescindibles en combate, y además nace una economía de servicios (médicos, alquimistas, sastres, sacerdotes) que un juego de dos años necesita.

## 7. Límites

- **Como máximo 2 heridas graves o críticas a la vez.** Una tercera se convierte en **agotamiento** (una penalización general) en lugar de otra herida.
- **Protección de novato:** hasta el nivel 10 solo hay heridas leves, así que ninguna herida puede volverse crónica ni definitiva.
- **Nunca los dos de un par:** no se pierden las dos piernas, los dos brazos ni los dos ojos (ver [Secuelas y muerte](secuelas-y-muerte.md) §5.5).
