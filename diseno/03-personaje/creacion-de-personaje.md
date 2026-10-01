# Creación de personaje

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Clases y especializaciones](clases-y-especializaciones.md), [Talentos](talentos.md) · **Alimenta a:** [Progresión](progresion.md), [Equipamiento](equipamiento.md), [Salud](../05-salud/README.md), [Profesiones](../07-economia/profesiones.md), [Misiones](../06-contenido/misiones-y-exploracion.md) · **Estado:** §1 y §2 están en el juego (0.9.2); §3 a §6 son propuesta

Crear un héroe tiene que tomar menos de un minuto. Hoy son tres pasos: **nombre → clase → confirmación**. La especialización no se elige al crear: se gana con el primer punto de talento (D-68, D-74). Linaje, trasfondo y apariencia quedan como capa profunda opcional para más adelante (D-44).

---

## 1. El flujo de hoy

### 1.1 Paso 1 · El nombre

- Al tocar /start, el bot muestra **🌅 Lost Realms · El despertar**: despiertas junto a una fogata en el Claro, sin recuerdos y sin nada.
- Escribes el nombre del héroe. Debe tener de 2 a 16 caracteres y empezar con una letra.
- **El nombre es único en el mundo.** Si otro héroe ya lo usa, el bot pide otro. No importan las mayúsculas, las tildes ni los espacios: "José Luis" y "joseluis" son el mismo nombre. Mientras alguien elige su clase, su nombre queda apartado.
- Mientras eliges la clase, puedes escribir otro nombre y el bot lo cambia.

### 1.2 Paso 2 · La clase, en páginas de 3

- El bot pregunta "¿cómo peleas?" y muestra **3 clases por página**, cada una con una frase: su armadura, su recurso y su estilo.
- Son 15 clases, así que hay 5 páginas. **▶️ Ver más clases** pasa a la siguiente y, después de la última, vuelve a la primera.
- Así el mensaje nunca pasa de 4 botones (D-75): 3 clases y ▶️.
- El texto recuerda que **todas valen lo mismo**: la diferencia la hacen los oficios y lo que aprendas (D-49).

### 1.3 Paso 3 · La confirmación

- Al tocar una clase, el bot muestra su descripción y **sus 3 especializaciones**, cada una con su rol (⚔ Ataque, 🛡 Defensa, ✚ Curación o ✦ Soporte) y su función.
- Aviso: "La clase es para siempre. La especialización la vas eligiendo nivel a nivel y la puedes cambiar más adelante".
- Dos botones: **✅ Elegir [clase]** y **↩️ Volver a las clases**. Volver te deja en la misma página donde estaba esa clase.
- Al confirmar, el bot revisa otra vez que el nombre siga libre. Si alguien lo tomó en el medio, vuelve al paso 1.

### 1.4 Con qué empiezas

| Qué | Cuánto | Dónde se ajusta |
|---|---|---|
| Lugar | El Claro, coordenadas (0, 0) | — |
| Nivel | 1, sin puntos de talento | `hero` |
| Energía | Llena: 50 ⚡ | `energy.max` |
| Monedas | 10 🥉 | `hero.start_gold` |
| Cinturón | 2 pociones de vida y 1 venda | `hero.start_belt` |
| Mochila | 2 pociones de vida y 2 vendas | `hero.start_backpack` |
| Equipo | Un arma y una armadura de nivel 1 de tu tipo, ya puestas | `gear.start_tier` |
| Combate | ⚔️ Atacar y la respuesta básica de tu clase (bloquear, esquivar o escudo) | `engine/classes/talents.py` |

- Todos los números están en `content/balance.yaml`.
- En la ficha, la clase aparece como "sin especialización todavía" y con el ícono de la clase (D-70, D-86).
- Si entraste con el enlace de un amigo, él gana energía apenas creas tu héroe (D-65).
- El tutorial empieza solo, con pistas y sin instrucciones (D-56): explorar el Claro, recolectar, vender lo que sobra al mercader (antes: aportar a la obra común, quitada por D-98), salir del Claro, ganar una pelea, curarte y usar 📒 Lugares. Cada paso cumplido da 5 🥉 y 20 de experiencia (`tutorial`).

## 2. La especialización llega después

- **El primer punto de talento llega al subir al nivel 2.** Después, 1 punto por nivel (D-68).
- En **👤 Héroe → 🌟 Talentos**, lo primero es escoger la especialización: tocas una y le pones tu punto (D-86).
- Con 1, 3, 6, 10, 16, 24, 34 y 46 puntos en una especialización se abren sus 8 habilidades (D-79).
- Tu especialización principal ⭐ es la que tiene más puntos. Su ícono te representa en todo el juego (D-70).
- **Cambiarla:** reiniciar los talentos cuesta 10 🥉 por nivel y devuelve todos los puntos para repartirlos de nuevo (D-74). La clase nunca cambia.
- **Doble especialización:** con 10 puntos en tu especialización principal y 3 💰 bolsas tienes dos repartos y cambias entre ellos fuera de combate con /doble (D-88).
- El detalle está en [Talentos](talentos.md) y en [Progresión](progresion.md).

**Por qué así.** Elegir clase, especialización, raza y origen de golpe, con nombres que todavía no dicen nada, asusta al jugador nuevo. Con un solo paso importante (la clase) se entra rápido. La especialización se elige cuando ya se peleó un poco y se sabe qué gusta.

## 3. Linajes (propuesta): 12 razas que cambian el cuerpo, no el daño

**Cómo entraría.** Como paso optativo entre el nombre y la clase, con un botón "elegir después". Mientras no se elija, el héroe es Humano. Encaja con "amplio pero ligero" (D-44): quien no quiere pensar, no piensa.

**El problema de WoW.** Las raciales de combate fueron una fuente constante de desequilibrio. *Every Man for Himself* (Humano) funcionaba como un segundo abalorio de PvP hasta que lo cambiaron en 2016. *Hardiness* (Orco) y *Will of the Forsaken* (No-muerto) se siguen discutiendo. La gente elegía raza por un número, no por gusto.

**La regla aquí.** Ninguna racial toca el daño, la curación ni el control en combate. Así se respetan las clases igualadas (D-49). Todas las razas tienen **el mismo presupuesto**:
- un rasgo de **cuerpo**: cómo interactúa con heridas, enfermedades y clima;
- un rasgo de **oficio o exploración**;
- un rasgo **social o de estilo**.

Como el juego tendrá un sistema de salud profundo (D-09), la raza importa donde se nota: **en cómo vive y se rompe tu cuerpo**. Cualquier linaje puede ser cualquier clase (P-15).

| Linaje | Inspiración | Cuerpo | Oficio / exploración | Social / estilo |
|---|---|---|---|---|
| **Humano** | Humano | Se aclimata a regiones nuevas en la mitad del tiempo | +10 % de reputación ganada | Puede tener dos trasfondos |
| **Enano** | Enano | Resiste enfermedades de mina y de frío; la Tos del Minero le avanza a la mitad | Ve la calidad de una veta sin prospectarla | Bebe sin penalización en la taberna |
| **Gnomo** | Gnomo | Tolera las prótesis mecánicas sin período de adaptación | Ingeniería: 10 % menos de fallos al inventar | Cabe por pasadizos que otros no |
| **Elfo del Alba** | Alto elfo / elfo de sangre | Resiste la Quemadura de Maná | Encantamiento: ve afijos ocultos | Los PNJ nobles le abren misiones propias |
| **Elfo Sombrío** | Elfo de la noche | Ve de noche sin penalización | Herboristería nocturna mejorada | Primera ronda con ventaja de sigilo fuera de ciudad |
| **Orco** | Orco | Las heridas leves no le penalizan | Desuello y curtido más rápidos | Su grito baja el estrés del grupo fuera de combate |
| **Trol** | Trol | Regenera heridas al doble de velocidad, e incluso un miembro perdido, muy despacio | Cocina: aprovecha partes de monstruo que otros tiran | Come el doble |
| **Renacido** | No-muerto | No sangra ni enferma de males naturales, pero no se cura descansando: necesita un remiendo | Alquimia: tolera más toxicidad | Precios algo peores con PNJ en ciudades de luz |
| **Taurino** | Tauren | Carga más peso sin penalización | Tala y agricultura mejoradas | Los animales salvajes no lo atacan primero |
| **Goblin** | Goblin | Resiste venenos y explosiones | Ve el precio medio de un objeto en otras ciudades | Negocia mejor con PNJ, nunca entre jugadores |
| **Licántropo** | Worgen | Olfato: detecta enfermedades en la comida y en otros. Portador latente de la licantropía (ver [Enfermedades](../05-salud/enfermedades.md)) | Rastreo: encuentra presas y jefes antes | Forma bestial para viajar más rápido fuera de combate |
| **Dracónido** | Dracthyr | Resiste frío y calor extremos | Vuelo corto: cruza zonas bloqueadas (precipicios, ríos) | Los monstruos débiles huyen |

**Para más adelante:** Vulpinos (nómadas del desierto) y Úrsidos (monjes cerveceros), con nombres y cultura propios.

**Héroes que ya existen.** Si los linajes llegan, cada héroe guardado elige el suyo una vez, gratis, la próxima vez que entra. Nadie pierde nada (D-64).

## 4. Trasfondos (propuesta): de dónde viene tu héroe

**Cómo entraría.** Como paso optativo después del linaje, también con "elegir después". Cada trasfondo da:
- una **cadena corta de misiones propia** cerca del Claro (5-6 misiones);
- un **pequeño empujón**: un objeto de inicio o un oficio a nivel 5 cuando lleguen los oficios;
- **diálogos propios** con ciertos PNJ.

| Trasfondo | Empujón | Su historia |
|---|---|---|
| Soldado desertor | Primeros auxilios, espada gastada | Tu antiguo capitán te busca |
| Aprendiz de gremio | Un oficio a nivel 5 | Tu maestro desapareció en la Lejanía |
| Huérfano de las Ruinas | Ganzúa, sigilo en la ciudad | Conoces los túneles bajo el Claro |
| Noble caído | Unas monedas de 🥈 plata, anillo de familia | Tu casa perdió sus tierras en otra región |
| Curandero de aldea | Medicina a nivel 5, hierbas | Una plaga que no pudiste detener |
| Minero de las vetas | Minería a nivel 5, pico | Algo despertó en la mina |
| Juglar ambulante | Laúd, rumores | Sabes una canción que nadie más recuerda |
| Cazador de recompensas | Trampas, un contrato | Tu presa se adentró en la Lejanía antes que tú |

**Por qué conviene.** El segundo personaje empieza distinto y el primer oficio llega antes. Son cadenas cortas de texto: baratas de producir.

## 5. Apariencia (propuesta)

- **Descripción textual elegible:** complexión, rasgos, pelo, marcas y voz. Se muestra en el perfil y en el combate ("*Bram, con su barba trenzada, levanta el escudo…*").
- **Las cicatrices y las prótesis** que ganes se agregan solas, con el jefe y la zona donde las ganaste (ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md)).
- El equipo suma su propia descripción (ver [Equipamiento](equipamiento.md)).
- **Cambiar el nombre** del héroe costaría monedas. Hoy no se puede cambiar después de crearlo.

## 6. Dónde vivir

El diseño viejo pedía elegir un castillo al nivel 5. Ya no hace falta: hoy cada héroe empieza en el Claro y, cuando quiere, **pide unirse a un campamento** o funda el suyo (D-71, D-84). Un héroe pertenece a un solo campamento y puede salir. Ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md).

## 7. De dónde sale

- **World of Warcraft:** la clase se elige al crear y la especialización llega después, con puntos de talento por nivel. El paso de confirmación evita elegir por error una clase que es para siempre.
- **Juegos de Telegram** (Chat Wars, TowerWars): nombre y clase en dos toques, sin pantallas largas.
- **Linajes:** las razas de WoW, corrigiendo sus raciales de combate.
- **Trasfondos:** *Dragon Age: Origins* (orígenes jugables), *Cyberpunk 2077* (senderos de vida), *Kenshi* (inicios distintos), *Mount & Blade* (preguntas de infancia).

## 8. Preguntas

- P-15 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md): ¿cualquier linaje con cualquier clase? Recomendación: sí.
