# Instrucciones del proyecto para la IA

Toda sesión de IA que trabaje en este repositorio lee esto primero. Una orden nueva del dueño manda sobre este archivo; si la orden cambia una regla de aquí, se actualiza este archivo en el mismo cambio.

## 1. Qué es y dónde está todo

- ***Ascendentes*** (nombre provisional): un MMORPG **por turnos y en texto**. Un solo motor y un solo mundo, con tres clientes: el bot de Telegram **@thetowerwarbot**, la web y una app móvil de texto (D-40, D-41).
- **Estado:** diseño. **Todavía no hay código del juego.**
- **Punto de entrada:** [diseno/README.md](diseno/README.md), con el mapa de los módulos.
- **Lo decidido:** [decisiones.md](diseno/00-vision/decisiones.md) (D-xx). Solo la tabla "Confirmadas por el dueño" es ley; lo demás es provisional o propuesta.
- **Lo que falta decidir:** [preguntas-abiertas.md](diseno/00-vision/preguntas-abiertas.md) (P-xx, cada una con recomendación).
- **Antes de la beta:** el cuestionario de beta, `diseno/00-vision/cuestionario-beta.md` (D-39).
- **Cómo se parte el juego:** [arquitectura-modular.md](diseno/01-plataforma/arquitectura-modular.md) (25 módulos, M1 a M25) y [web-y-multiplataforma.md](diseno/01-plataforma/web-y-multiplataforma.md).
- **Qué aprendimos de otro juego:** [lecciones-de-towerwars.md](diseno/99-referencias/lecciones-de-towerwars.md).

Antes de proponer algo, buscar si ya está decidido o preguntado: `grep -rn "palabra" diseno/`.

## 2. Reglas fijas del dueño (no se negocian)

1. **TowerWars no se toca.** Ni el bot @TowerWarsBot, ni el repositorio `jams990519/towerwars`, ni su carpeta local, ni su base de datos, ni sus servicios (D-01). De TowerWars solo se toman lecciones, y ya están resumidas en el diseño.
2. **El juego se monta en @thetowerwarbot** (D-02), que es otro bot.
3. **Nada en Railway ni ningún despliegue sin permiso explícito del dueño** (D-03). Ni crear servicios, ni cambiar variables, ni desplegar, ni volver a desplegar. Si la sesión tiene herramientas de Railway, no se usan hasta que el dueño lo pida.
4. **Todo en texto y por turnos** (D-05).
5. **Modular para Telegram, web y app móvil:** un solo motor y las mismas reglas para los tres. Ningún cliente da ventaja. El motor no sabe desde qué cliente juega cada jugador (D-40, D-41).
6. **No se escribe código del juego hasta que el dueño lo autorice** (D-04). Los ejemplos de código dentro del diseño sí se permiten.
7. **Los archivos `RPG-0.1` a `RPG-0.9`** eran un proyecto viejo del dueño. Por su pedido, el repositorio se dedicó por completo al juego nuevo y esos archivos se quitaron (siguen en el historial de git).

## 3. Cómo hablar con el dueño

- **Siempre en español.**
- **Habla por voz.** Las transcripciones llegan revueltas: palabras cambiadas, frases cortadas, muletillas. Se interpreta la intención **sin pedirle que repita**. Si la interpretación cambia algo importante, se dice cuál se tomó y se registra como decisión provisional (como D-25).
- **Respuestas en lenguaje de resultado:** qué quedó hecho, qué falta y qué necesita de él. Sin relleno, sin repetir lo que pidió y sin jerga técnica que no haga falta.
- **Cuando una decisión es suya,** se pregunta con opciones cortas y una recomendación: "Recomiendo X porque Y. ¿Sigo?". Si queda abierta, se registra como P-xx.
- Nunca se trata una propuesta como si el dueño la hubiera confirmado.

## 4. Convenciones de código (para cuando haya código)

Lo que pidió el dueño: que, si le pide a la IA cambiar una sola línea, la IA pueda responder **"ok, pero esto también va a romper esto, esto y esto, o puede afectar esto otro"**. Para eso existen estas reglas (D-42). El detalle está en [convenciones-de-codigo.md](diseno/01-plataforma/convenciones-de-codigo.md).

- **Código en inglés:** nombres, comentarios y docstrings.
- **Debajo, una nota `[ES]` en español:** para qué sirve, con qué se conecta y qué se rompe si cambia. Va en cada archivo (encabezado de 10 campos, §2), en cada clase y función pública (§3) y en cada archivo de datos (§4).
- **Los textos que ve el jugador** van en archivos de idiomas o de contenido, nunca en el motor.

**Antes de cambiar código:**
1. Leer el encabezado y las notas `[ES]` del archivo y de lo que se va a tocar.
2. Leer el mapa de impacto del módulo: `diseno/01-plataforma/mapa-de-impacto.md`.
3. Comprobar en el código quién lo usa de verdad, por los cinco caminos: importaciones, eventos, IDs de datos, números de balance y lo que el motor devuelve a los clientes. La nota puede estar vieja.
4. Avisar al dueño qué más se afecta, con el mensaje de impacto (plantilla en §6.3 de las convenciones). Si el riesgo es medio o alto, esperar su sí.

**Después de cambiar código,** en el mismo cambio: actualizar las notas `[ES]`, el mapa de impacto, el documento de diseño y el registro de balance (si se movió un número).

**Siempre:**
- **Diseño y código se actualizan juntos.** Si no coinciden, es un error: se le avisa al dueño, que decide, y se corrigen los dos.
- **IDs estables:** solo se agregan. Nunca se renombran, se borran ni se reutilizan; para retirar algo se marca `retired: true`.
- **Credenciales nunca en el repositorio:** solo los nombres de las variables, en un archivo de ejemplo. Los valores, jamás.
- **Antes de subir:** correr las pruebas **y** arrancar el motor con al menos un cliente.

## 5. Cómo se trabaja el diseño

- `diseno/` va en **español neutro y simple**. Los ejemplos de código, en inglés con notas `[ES]`.
- **Cada carpeta es un módulo** con su README: qué contiene, de qué depende, a qué alimenta y qué preguntas tiene abiertas. Un documento nuevo se agrega al README de su módulo.
- **Cada documento empieza con su línea de módulo**, así:
  `> **Módulo** [04 · Combate](README.md) · **Depende de:** ... · **Alimenta a:** ... · **Estado:** propuesta`
  Y casi siempre lleva una sección **"De dónde sale"**, que dice qué juego inspira cada idea.
- **Decisiones nuevas:** el siguiente número D-xx libre en [decisiones.md](diseno/00-vision/decisiones.md). Va como confirmada solo si el dueño lo dijo; si no, como provisional.
- **Preguntas nuevas:** el siguiente número P-xx libre en [preguntas-abiertas.md](diseno/00-vision/preguntas-abiertas.md), con recomendación. Cuando se resuelve, se marca `✅ Decidido (D-xx)`.
- Los números D-xx y P-xx nunca se reutilizan. Antes de elegir uno, buscar el más alto: `grep -o "D-[0-9]*" diseno/00-vision/decisiones.md | sort -t- -k2 -n | tail -1`.
- Todo sistema nuevo se conecta a la [red de sistemas](diseno/00-vision/red-de-sistemas.md): qué consume y qué produce (D-20, D-38). Y respeta "amplio pero ligero": capa simple por defecto, capa profunda opcional (D-44).
- Los términos propios nuevos van al [glosario](diseno/00-vision/glosario.md).
- **Verificar los enlaces internos antes de subir.** Este comando muestra los enlaces rotos; si no muestra nada, están bien:

```bash
python3 - <<'EOF'
import re, pathlib
for f in pathlib.Path('.').rglob('*.md'):
    for link in re.findall(r'\]\(([^)#\s]+)', f.read_text(encoding='utf-8')):
        if not link.startswith(('http', 'mailto:')) and not (f.parent / link).exists():
            print(f, '->', link)
EOF
```

## 6. Git

- Se trabaja en la **rama asignada a la sesión**. Nunca directo en `main` y nunca `push --force`.
- **Commits claros en español,** en lenguaje de resultado y un tema por commit. Ejemplo: "Registrar decisión: modular también para aplicación móvil de texto".
- Antes de cada commit, `git status`: no subir archivos ajenos al pedido ni pisar cambios de otras sesiones.
- **Pull requests en borrador.** El dueño decide cuándo se unen.
