# Ankeret

Entrenador de noruego bokmål para hispanohablantes rioplatenses. Cada palabra se
aprende atada a algo que ya se sabe en inglés, italiano, francés, portugués o
castellano.

**En vivo:** https://rcossio.github.io/norsk/

275 palabras en seis niveles · 121 conversaciones escritas a mano · 742 frases ·
1169 textos con grabación · 11 juegos.
Un solo archivo HTML, sin dependencias, sin build, sin servidor.

El detalle de **por qué la app es como es**, con el listado de decisiones y de las
correcciones que las originaron, está en [DECISIONES.md](DECISIONES.md).

---

## El método: anclas

La unidad de aprendizaje no es la palabra sino el **puente hacia algo ya conocido**.
Cada entrada del vocabulario lleva un campo `an` con ese puente:

| Palabra | Ancla |
|---|---|
| hund | inglés *hound* |
| kjøtt | *chota*: el pedazo de carne |
| trenger | necesito una *tregua* |
| heter | inglés *I hate*: I hate cómo me llamo |
| beklager | tiré la cerveza *lager*, lo siento |
| gammel | *camel*: el camello arrugado y viejo |

Criterios de una buena ancla, en orden de preferencia:

1. **Cognado real** hacia un idioma que el usuario ya habla (*fisk* → fish).
2. **Cognado fonético** aunque el significado no coincida (*ost* → hostia: la
   oblea blanca y redonda, como una feta de queso).
3. **Mnemotecnia inventada** cuando no hay puente: se ata a una escena concreta y
   preferentemente absurda, porque se recuerda mejor.

Las anclas se escriben **a mano**, una por una. No son automatizables y son el
cuello de botella real para crecer el vocabulario.

## Pronunciación

La columna `pron` es una respelling pensada para un lector **rioplatense**, no IPA.
Decisiones que la gobiernan:

- `j` = la h noruega, soplada como en el *house* inglés, no la jota de *jamón*.
- `ü` = la u francesa de *tu*. La `y` noruega siempre suena así.
- Nunca se usa `y` en la respelling: en rioplatense se leería *sh*. Por eso *gir*
  es **iir** y no *yir*.
- La `o` larga noruega se transcribe `u`: *bok* → buk, *stor* → stur.
- El diptongo `ei` se transcribe con **e**, no con **a**: *jeg* → iei. Escribir
  "jai" produce el acento de extranjero más reconocible.

El campo `sil` documenta las letras que se escriben y no se dicen (la d final de
*god*, la g de *og*, la h de *hvor*) y los falsos amigos peligrosos (*nå* suena
como nuestro "no" y significa "ahora").

## Niveles

El vocabulario está partido en seis niveles **anidados**. El nivel filtra a la vez
palabras, frases, señuelos de opción múltiple, categorías y la lista.

| Nivel | Palabras | Conversaciones | Frases |
|---|---|---|---|
| 1 | 25 | — | 150 |
| 2 | 61 | 40 | 325 |
| 3 | 120 | 81 | 509 |
| 4 | 170 | 121 | 742 |
| 5 | 226 | 121 | 742 |
| 6 | 275 | 121 | 742 |

**Los niveles 5 y 6 suman vocabulario y no suman frases.** Sus 105 palabras
completan el top-275 de frecuencia del bokmål según `wordfreq`: entran en las
tarjetas, la lista y los juegos de palabras, pero las frases de Sonido y las
conversaciones de Dúo siguen siendo las de 170. Es una decisión, no una deuda:
escribir el corpus de frases cuesta un orden de magnitud más que escribir las
anclas, y el vocabulario reconocido sirve antes que el producido.

Por qué 275 y no 200: de las 170 que ya estaban, 78 quedan fuera del top-200
(*hund*, *katt*, *ost*, *toalett*, *flyplass*). Son la concesión pedagógica que
hace que existan frases; con puros funcionales no se dice nada. La frecuencia sola
nunca da un nivel jugable.

Lo que estos dos niveles aportaron y faltaba de verdad: **å**, el marcador de
infinitivo, que estaba ausente y bloqueaba todo *jeg liker å lese*; las partículas
de dirección completas (*ut, opp, inn, ned, over, under, rundt, gjennom, tilbake*);
una docena de conectores de alta frecuencia — *da, for, om, jo, bra, alltid, hele,
samme* — que se echaban de menos al escribir las conversaciones y había que rodear;
y en el nivel 6, **dårlig**, que es el antónimo de *bra* y no estaba, más el registro
de matiz que hace que el habla suene humana: *faktisk, egentlig, virkelig, nesten,
gjerne, ganske, altså, sånn*.

Rendimiento decreciente, medido: el top-170 cubre el 58,6% del texto corrido, el
top-226 el 61,3% y el top-275 el 63,1%. Cada escalón cuesta lo mismo en anclas y
rinde menos. Por eso el 275 es el último de esta serie.

Dúo empieza en el nivel 2: abajo de 60 palabras no alcanza para una conversación
que no suene a ejercicio.

Reglas por nivel: 6, 13, 22, 26, 26 y 26 acumuladas.

Criterios de corte:

- **La frecuencia manda, la cobertura verifica.** El orden sale de listas de
  frecuencia reales (`wordfreq` sobre bokmål, contrastado con corpus de
  subtítulos). No se optimiza el vocabulario contra el generador de frases propio:
  eso sería circular, elegiría las palabras que las plantillas premian en lugar de
  las que el idioma premia.
- **Los niveles son paquetes, no un slider continuo.** Agregar una palabra suelta
  muchas veces desbloquea cero frases, y hay bloques gramaticales que no se pueden
  partir: *en* y *et* entran juntos, *denne* y *dette* también, *ikke* no sirve sin
  un verbo.
- **Piso técnico de 25 palabras**: por debajo de eso, Pares se queda sin fichas y
  Categorías sin cajones.
- Cada nivel se audita: se verifica que **toda palabra del nivel aparezca al menos
  en una frase del nivel**. El nivel 2 tiene cobertura total.

El nivel elegido viaja en el hash de la URL (`#n=60`) porque la app no usa
almacenamiento del navegador.

## Las frases

**Las frases del juego Sonido son las líneas de las conversaciones.** No hay dos
corpus: cada línea que alguien dice en Dúo es también una frase que se escucha en
Sonido, y una sola grabación sirve para las dos cosas. De ahí que 121
conversaciones de nueve turnos den 741 frases con 1067 textos grabados, contra
1757 de la versión anterior, que mantenía frases y diálogos por separado.

Reglas de la derivación:

- **Se descartan las líneas de menos de tres palabras.** «Ja», «Nå?» o «Melk» ya
  existen como palabras sueltas; como frase de opción múltiple no enseñan nada.
- **Ninguna traducción castellana se repite dentro de un nivel**, porque dos
  opciones idénticas romperían el multiple choice. La línea sí puede repetirse en
  varias conversaciones: comparte grabación.
- **El nivel de una frase es el más bajo en que aparece**, así que una línea
  escrita para el nivel 2 sigue estando disponible en el 3 y el 4.
- Los señuelos salen de la **familia estructural** de la frase: pregunta con
  *hvor*, pregunta con *hva*, inversión sí/no, respuesta con *ja*, respuesta con
  *nei*, subordinada, pasado, modal, cortesía, declarativa con pronombre,
  declarativa con sustantivo. Quince familias, calculadas de la frase misma. Sin
  esto, la respuesta correcta se adivina por la forma sin escuchar nada.

El nivel 1 es la excepción: como no tiene conversaciones, conserva sus 150 frases
generadas por plantillas con `scripts/generar_frases.py`.

### Trampas del noruego que la revisión corrigió

Las conversaciones se auditaron preposición por preposición contra el sentido con
que cada palabra está presentada en la lista. Lo que apareció:

- **En tren, avión y hotel se va *på*, no *i***. *i bilen* sí, porque en el auto
  entrás; en el tren vas encima. Eran once líneas.
- ***fra her* no existe**: en noruego es *herfra*, una sola palabra. Las dos líneas
  se reformularon en vez de agregar una palabra al vocabulario.
- **Concordancia**: *barnet er lite*, no *liten*, porque *barn* es neutro. Y con
  sustantivo femenino el posesivo es *mi*, no *min*: *boka mi*, *klokka mi*.
- ***Det er godt* es «está bueno», no «está bien»**. Para asentir, el noruego usa
  *bra* o *greit*, que recién aparecen en el nivel 5. Donde el castellano decía
  «está bien» se corrigió la traducción; donde hacía falta asentir de verdad se usó
  *som du vil*.
- **Giros que no se dicen así**: *det gjør ikke noe* y no *det er ikke noe*;
  *det er det jeg sier* y no *jeg sier det*.
- **Traducciones que decían de más**: «siempre» donde el noruego decía *igjen*
  (otra vez), «nada» donde solo había una negación, «todo el día» donde solo decía
  *i dag*.

*før* (antes) y *for* (para) se escriben casi igual y ahora conviven en la lista;
la entrada de *før* lo advierte.

### Trampas del castellano que las traducciones respetan

- **"a" personal** con objetos animados: *ver a la mujer*, no *ver la mujer*.
- **ser vs estar**: temperatura y comida vieja piden *estar*.
- ***må ikke* es prohibición**, no ausencia de obligación: "no debe", no "no tiene que".
- ***gustar* invierte el sujeto**: *Jeg liker fisken* → "a mí me gusta el pescado".
- **Movimiento pide *hit/dit*, no *her/der***: *kommer her* no existe.

## Dúo

Conversaciones para dos personas y un solo teléfono. El chat se apila arriba, el
turno actual abajo con su traducción al castellano siempre a la vista, audio en
las dos voces y la versión lenta.

No hay opciones que elegir: cada turno se desbloquea **diciendo la línea en voz
alta**. El reconocedor compara lo escuchado con lo esperado y basta con acertar el
**80% de las palabras**, así que la pronunciación imperfecta no traba el juego.
Siempre hay un botón para seguir sin hablar, por si el micrófono no está disponible.

Las 121 conversaciones están **escritas a mano, una por una**, de ocho a diez
turnos cada una. La versión anterior las instanciaba desde doce esqueletos con
huecos y se notaba: doce formas repetidas sesenta veces. Un esqueleto no sabe
interrumpir, contradecir ni dejar algo sin resolver.

Criterios de escritura:

- **No todas terminan en despedida.** Muchas cierran con un comentario al pasar,
  una contradicción o algo que queda picando. *Ha det* es un final entre otros.
- **No todas son pregunta y respuesta.** Hay desacuerdos, insistencias, alguien
  que no contesta lo que le preguntaron y remates secos.
- **Cada nivel usa solo su vocabulario**, verificado token por token contra la
  lista con el mismo reductor de flexiones que usa la app.
- **Cobertura completa**: toda palabra de un nivel aparece al menos en una línea
  de ese nivel.

Lo que el nivel deja afuera se nota en el tono, y está bien que así sea. El nivel 2
no tiene preposiciones más allá de *i*, ni *meg* ni *deg*, así que sus
conversaciones son cortas y concretas. El nivel 4 ya tiene pasado, subordinadas y
posesivos, y puede permitirse ironía.

## Reglas

Pestaña aparte con 22 reglas de gramática y pronunciación, repartidas por nivel
(6 / 13 / 22 acumuladas). Cada una trae enunciado, ejemplos con audio y preguntas
de opción múltiple con la explicación del porqué. Hay además un modo de práctica
que sortea preguntas de todas las reglas del nivel.

Las reglas de pronunciación que antes vivían como leyenda al pie de la Lista se
mudaron acá.

## Dos voces

Cada texto tiene grabación de **Piper** (local, generada) y de **Google Translate**
(bajada una vez y guardada, no pedida en vivo). En Sonido hay tres botones:
**▶₁** voz principal (Google), **▶₂** segunda voz (Piper) y **½×** la lenta con
pausas, que solo existe en Piper. El resto de los juegos usa la voz principal.

La descarga de la voz de Google se hizo en cinco etapas con `scripts/voz_google.py`,
espaciando los pedidos medio segundo: el endpoint es interno y el uso intenso puede
devolver 429 o bloquear la IP. Guardarla evita depender de la red en cada carta.

## Audio

Generado con [Piper](https://github.com/rhasspy/piper), voz
`no_NO-talesyntese-medium`. Un mp3 por texto, mono 22050 Hz a 48 kbps: 1169 textos,
3507 archivos, 37 MB.

Cada toma se valida midiendo su envolvente de amplitud: si tiene un silencio
interno mayor a 0.30 s se descarta y se vuelve a sintetizar, porque ese es el
artefacto típico del modelo (un chasquido, una pausa, y recién la palabra). Después
se recorta el silencio inicial y se deja 0.25 s de cola.

**Cada texto tiene dos grabaciones**: la normal y una `-lento`. La lenta no es la
normal estirada: se sintetiza aparte, con comas entre palabras (Piper las convierte
en pausas reales) y `length_scale` 1.35 en frases, 1.6 en palabras sueltas.

La razón: al escuchar, lo que cuesta no es la velocidad de los sonidos sino
**segmentar dónde termina una palabra y empieza la otra**. Bajar el `playbackRate`
estira todo por igual y no ayuda; las pausas sí. Si faltara un archivo lento, se
cae a estirar el normal a 0.62×.

## Servicios externos

Se usan lo mínimo posible y **nunca de forma automática**: el audio por defecto es
siempre local. En Sonido hay un botón **G** que pide esa palabra o frase a Google
como segunda voz, solo cuando el usuario lo toca. Si no responde, suena la
grabación propia.

Se evita depender de Google para el audio de los juegos porque `translate_tts` es
un endpoint interno, no documentado, que ante uso intenso devuelve 429 o directamente
bloquea la IP; además obligaría a un viaje de red por cada carta y rompería el modo
offline.

La pestaña **Hablá** es la única que necesita internet siempre:

- Reconocimiento de voz: Web Speech API del navegador (`nb-NO`). Chrome y Safari.
- Traducción y lectura de lo que dijiste: endpoints públicos de Google Translate.
  Ninguno de los dos es oficial y pueden dejar de funcionar; hay respaldo local.
- La página declara `<meta name="referrer" content="no-referrer">` porque Google
  devuelve 404 en `translate_tts` cuando la petición llega con `Referer` ajeno, y
  un `<audio>` no admite `referrerpolicy` propio.

El resto de la app funciona sin conexión una vez cargada.

## Reproducir

```bash
python3 scripts/generar_audio.py    # sintetiza lo que falte y borra huérfanos
python3 scripts/voz_google.py 1     # segunda voz, cinco etapas
```

Los dos leen los textos de `index.html`: palabras, frases, ejemplos de las reglas
y líneas de diálogo. Agregar una conversación y correrlos deja el audio al día.

`generar_frases.py` lee el vocabulario directamente de `index.html`, así que
agregar una palabra ahí ya la hace elegible para las plantillas.

## Estructura

```
index.html                  toda la app: datos, lógica y estilos
DECISIONES.md               estado, y por qué la app es como es
audio/*.mp3                 tres tomas por texto: Piper, Piper lenta y Google
scripts/generar_frases.py   plantillas gramaticales, hoy solo para el nivel 1
scripts/generar_audio.py    síntesis con Piper, toma lenta y control de calidad
scripts/voz_google.py       segunda voz, bajada por etapas
```

## Decisiones que se tomaron y por qué

- **Sin almacenamiento del navegador.** El contador de práctica y el nivel viven en
  memoria. Se pierde al recargar, y es una concesión consciente.
- **Un solo archivo.** No hay build ni dependencias: se puede editar desde
  cualquier lado y publicar copiándolo.
- **El contador de práctica resuelve flexiones al vuelo**, sin tabla escrita:
  reduce cada token a su entrada probando infinitivo, neutro del adjetivo, plural y
  sufijos de forma definida. Cubre el 99.8% de los tokens del corpus.
- **El muestreo no es azar puro ni un mazo.** Es rechazo con tope: se sortea al
  azar y se rechaza si esa palabra ya salió más de 2 veces por encima de la que
  menos salió. Mantiene la sensación de azar sin dejar palabras sin practicar.

## Pendiente

- Frases y conversaciones para los niveles 5 y 6, que hoy solo suman vocabulario.
- Las flexiones: comparativos, plurales irregulares y los pronombres de objeto
  completos (*ham* está, faltan *henne* y *dem*). No agrandan la lista pero
  desbloquean frases que hoy no se pueden escribir.
- Conversaciones para el nivel 1, si es que 25 palabras dan para alguna.
