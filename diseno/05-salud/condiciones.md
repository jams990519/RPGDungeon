# Condiciones: dolor, fatiga, sustento, temperatura y toxicidad

> **Módulo** [05 · Salud](README.md) · **Depende de:** [Heridas](heridas.md), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (clima) · **Alimenta a:** [Profesiones](../07-economia/profesiones.md) (Cocina, Sastrería, Alquimia) · **Estado:** propuesta

**De dónde sale.**
- *Project Zomboid*: los "moodles", indicadores de estado por niveles.
- *Red Dead Redemption 2*: cada barra tiene un **núcleo** que baja con el tiempo, con la ropa inadecuada o con el hambre, y decide cuánto regeneras.
- *Vintage Story*: la variedad de la dieta sube la vida máxima.
- *The Witcher 3*: la toxicidad de las pociones.
- *RimWorld*: tolerancia, adicción y abstinencia.
- *Don't Starve*: ropa según el clima.

---

## 1. Las condiciones

| Condición | Qué la sube | Qué hace | Qué la baja |
|---|---|---|---|
| 😖 **Dolor** | Heridas | Baja la precisión y la iniciativa; tiene 4 niveles, como los moodles | Analgésicos, ungüentos, linaje (Orco) |
| 🩸 **Sangrado activo** | Heridas abiertas | Pierde vida por ronda en combate, o por minuto fuera | Vendar, torniquete, curación |
| 😴 **Fatiga** | Muchas horas seguidas de actividad, combates largos | Baja el Aguante máximo | Dormir |
| 🍖 **Sustento** | Pasa el tiempo activo; comer lo sube | Ver §2 | Comida |
| 🌡️ **Temperatura** | Bioma, clima, ropa | Frío: baja la iniciativa, riesgo de congelación y gripe. Calor: baja el Aguante, deshidratación, insolación | Ropa adecuada, fogatas, pociones |
| 🧪 **Toxicidad** | Pociones y elixires | Ver §4 | El tiempo; más rápido descansando |

## 2. Sustento: positivo primero

Nada de morirse de hambre por no entrar dos días.
- El Sustento tiene 5 estados: *Famélico · Hambriento · Normal · Bien alimentado · Banquete*.
- Solo los dos primeros penalizan, y solo se llega a ellos pasando mucho tiempo **activo** sin comer. **El tiempo fuera de línea no baja el Sustento.**
- **Variedad** (idea de *Vintage Story*): la dieta tiene 5 grupos (carnes, pescado, vegetales, granos, frutas). Cada grupo cubierto en las últimas horas sube un poco la vida máxima.
- *Banquete* da además un bonus al grupo y baja el estrés.
- El Trol come el doble; el Renacido casi no come, pero no se cura descansando (ver [Creación de personaje](../03-personaje/creacion-de-personaje.md)).

**Por qué conviene.** La Cocina tiene sentido sin ser una obligación que castiga.

## 3. Temperatura y aclimatación

- **Por bioma:** los Picos Helados piden abrigo de piel; el Desierto Ardiente pide telas ligeras y agua. Un sastre que fabrica ropa de abrigo tiene mercado en el tramo VI.
- **La capa** es la ranura de clima: una capa de piel contra el frío, una capa de lino blanco contra el sol (ver [Equipamiento](../03-personaje/equipamiento.md)).
- **Aclimatación:** al subir a un piso con clima nuevo hay una penalización pequeña durante las primeras horas, el **Mal del Piso**. El Humano se aclimata en la mitad del tiempo. Es el mal de altura aplicado a la Torre.

## 4. Toxicidad y dependencia

- Cada poción y elixir suma **Toxicidad**. Por encima del 75 % empiezas a perder vida; al 100 % no puedes beber más.
- La toxicidad baja con el tiempo, más rápido descansando.
- **Esto es lo que impide abusar de las pociones** en combate, un problema clásico del balance de los MMO. Las pociones pueden ser fuertes precisamente porque no puedes tomarte diez.
- Algunas sustancias (analgésicos fuertes, elixires de furia, la "polvareda" de ciertos pisos) generan **tolerancia**: cada uso rinde menos. El uso continuo trae **dependencia**, con abstinencia (una penalización hasta que pasa). Un médico la trata, pero hay que querer.
- El Renacido tolera más toxicidad.

## 5. Principio

Todas las condiciones se leen en la línea final de `/cuerpo` (ver [Heridas](heridas.md)). Ninguna castiga por no jugar; todas premian prepararse.
