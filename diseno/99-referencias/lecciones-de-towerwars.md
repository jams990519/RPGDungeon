# Lecciones de TowerWars

> **Módulo** [99 · Referencias](README.md)

**TowerWars (@TowerWarsBot) es otro juego y no se toca.** Pero lleva meses en producción en Telegram, con cerca de 1.190 héroes registrados a septiembre de 2026, y lo que aprendió vale oro para este diseño. Aquí van las lecciones que se aplican, cada una con dónde se usa. Salen de sus documentos de estado, reglas de trabajo y registro de cambios (repositorio `jams990519/towerwars`, solo lectura).

---

## Sobre Telegram

| Lección | Dónde se aplica |
|---|---|
| Telegram corta en 4.096 caracteres, y pasarse significa que **no sale nada**, no que sale cortado | [Telegram](../01-plataforma/telegram.md) |
| El costo nunca va en un botón: en pantallas chicas se trunca | [Telegram](../01-plataforma/telegram.md) |
| Las rondas simultáneas de 90 s en grupo funcionan | [Ronda y acciones](../04-combate/ronda-y-acciones.md) |
| El chat dentro de la pelea y el parte `.txt` por corrida funcionan | [Telegram](../01-plataforma/telegram.md), [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md) |
| El reenvío de mensajes sirve como mecánica: los vales del gremio se cobran reenviando | [Economía](../07-economia/economia.md), [Gremios](../08-social/gremios-y-social.md) |
| El menú persistente abajo, al estilo Chat Wars, es mejor que repetir botones en cada mensaje | [Telegram](../01-plataforma/telegram.md) |

## Sobre arquitectura

| Lección | Dónde se aplica |
|---|---|
| **Motor puro y adaptadores:** "nada en el motor importa nada de los adaptadores". Es lo que permite otro adaptador sin reescribir reglas | [Arquitectura](../01-plataforma/arquitectura-modular.md) |
| Los códigos de habilidad asignados por orden de aparición se rompen cuando se inserta algo en el medio: **identificadores estables, solo se agregan** | [Arquitectura](../01-plataforma/arquitectura-modular.md) |
| En SQLite, agregar una columna tocaba seis lugares, y "Incorrect number of bindings" apareció dos veces: **migraciones desde el día uno** | [Arquitectura](../01-plataforma/arquitectura-modular.md) |
| "Que un módulo importe no significa que arranque": antes de cada subida, pruebas **y** arrancar el bot | Hoja de ruta (proceso) |
| Los `.pyc` viejos confunden al depurar | Proceso |
| Credenciales: nombres de variables sí, valores jamás | [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md) |

## Sobre balance

| Lección | Dónde se aplica |
|---|---|
| **"La ropa no contaba":** la guerra calculaba el poder por su lado y el equipo no sumaba (cinco defensores con 259 de armadura aportaban 12). **Una sola fuente de verdad para el poder** | [PvP](../06-contenido/pvp.md), [Arquitectura](../01-plataforma/arquitectura-modular.md) |
| El nivel mínimo de cada pieza estaba declarado, pero no se comprobaba al equiparse (el mercado y el almacén no preguntaban). **Las reglas se validan en el motor, en un solo lugar**, no en cada pantalla | [Arquitectura](../01-plataforma/arquitectura-modular.md) |
| +1 de vida no es una elección real al lado de +1 de ataque: **nada de puntos de estadística sueltos** | [Balance](../03-personaje/balance.md) |
| Después de un reinicio, los jugadores recibieron repartos distintos según la fecha: **nada que dependa de cuándo llegaste** | [Balance](../03-personaje/balance.md) |
| **Registro de dificultad:** cada número que se mueve, con su antes → después y la medición. "Si un número de balance se movió y no está ahí, se movió a ciegas" | [Balance](../03-personaje/balance.md) |
| "Un diagnóstico de segunda mano no es un hecho": varias discusiones se cerraron recién con una herramienta para mirar el motor (`/admin_castillo`) | [Arquitectura](../01-plataforma/arquitectura-modular.md) (radiografías) |
| El jefe que busca primero al sanador y después al más débil crea presión real | [Ronda y acciones](../04-combate/ronda-y-acciones.md), [Jefes](../06-contenido/jefes.md) |
| Provocar repartido entre tanques | [Ronda y acciones](../04-combate/ronda-y-acciones.md) |
| No dejar entrar con menos del 25 % de vida hace que caer cueste algo | [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) |
| La "mordida" (daño mínimo que ignoraba la armadura) se revirtió: la armadura tiene que contar siempre | [Daño y estados](../04-combate/dano-y-estados.md) |

## Sobre la guerra y la comunidad

| Lección | Dónde se aplica |
|---|---|
| Solo cuentan en la guerra los activos de los últimos 3 días | [PvP](../06-contenido/pvp.md), [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md) |
| El que ataca no defiende | [PvP](../06-contenido/pvp.md) |
| Un castillo vacío no paga experiencia | [PvP](../06-contenido/pvp.md) |
| El límite de saturación por castillo | [Facciones](../02-mundo/facciones.md) |
| El parte narrado de la batalla al canal engancha | [PvP](../06-contenido/pvp.md) |
| **Carriles de contenido:** cada actividad lidera en algo distinto | [Progresión](../03-personaje/progresion.md) |
| La cola de misiones con temporizador es el mejor sistema de "toque" | [Misiones](../06-contenido/misiones-y-exploracion.md) |
| La cola de feedback clasificada por tema, sistema y gravedad | [Arquitectura](../01-plataforma/arquitectura-modular.md) |

## Sobre la comunicación con los jugadores

| Lección | Dónde se aplica |
|---|---|
| Notas de versión en **idioma de resultado**, no de mecánica; sin porcentajes ni fórmulas; en español y en inglés | [Gremios y social](../08-social/gremios-y-social.md) (canal de novedades) |
| La documentación vieja miente: la wiki describía 6 clases de un modelo anterior. **El diseño se actualiza con el código** | Este documento de diseño |
| Un registro de cambios en orden (el de TowerWars quedó desordenado) | Proceso |
