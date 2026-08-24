# Ankeret

Entrenador de noruego bokmål para hispanohablantes rioplatenses. Cada palabra se
aprende atada a algo que ya se sabe en inglés, italiano, francés, portugués o
castellano.

**En vivo:** https://rcossio.github.io/norsk/

120 palabras en tres niveles · 1050 frases generadas · 1086 grabaciones · 10 juegos.
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

El vocabulario está partido en tres niveles **anidados**. El nivel filtra a la vez
palabras, frases, señuelos de opción múltiple, categorías y la lista.

| Nivel | Palabras | Frases | Plantillas |
|---|---|---|---|
| 1 | 25 | 150 | 17 |
| 2 | 61 | 450 | 36 |
| 3 | 120 | 1050 | 50 |

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

Se generan por plantillas gramaticales, nunca a mano ni por muestreo libre del
modelo: así se garantiza que sean correctas. `scripts/generar_frases.py` produce
más de 20.000 frases posibles en nivel 3, de las que se seleccionan 1050.

Reglas de la selección:

- **Ninguna plantilla puede pasar del 10%** del corpus. Sin este tope, cinco
  estructuras de "pronombre + verbo transitivo" se comían el 46% del total.
- **Ninguna traducción castellana se repite**, porque dos opciones idénticas
  romperían el multiple choice.
- Se filtra por plausibilidad semántica además de gramatical: hay matrices de qué
  adjetivo admite qué sustantivo (nada de "el año está caliente"), qué se puede
  comprar y qué se puede poseer.

Las 50 plantillas cubren, entre otras: sujeto pronominal y **nominal**, objeto
definido e indefinido, negación, modales con infinitivo, adjetivo predicativo y
**atributivo** (incluida la forma en `-e`), **plurales** con sus irregulares,
**imperativo**, preguntas sí/no, preguntas con *hvor / hva / når*, **inversión
V2**, coordinación con *og / men / eller*, **subordinadas** con el verbo al final,
lugar y movimiento con *i / på / til / fra / med*, presentativo con *det er*, y
**cortesía dentro de la frase** (*Jeg vil ha en ost, vær så snill*).

### Trampas del castellano que el generador respeta

- **"a" personal** con objetos animados: *ver a la mujer*, no *ver la mujer*.
- **ser vs estar**: temperatura y comida vieja piden *estar*.
- ***må ikke* es prohibición**, no ausencia de obligación: "no debe", no "no tiene que".
- ***gustar* invierte el sujeto**: *Jeg liker fisken* → "a mí me gusta el pescado",
  y hay que decir "a él" / "a ella" o *han* y *hun* darían traducciones idénticas.
- **Movimiento pide *hit/dit*, no *her/der***: *kommer her* no existe.

## Audio

Generado con [Piper](https://github.com/rhasspy/piper), voz
`no_NO-talesyntese-medium`. Un mp3 por palabra y por frase, mono 22050 Hz a 48 kbps.

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
python3 scripts/generar_frases.py   # regenera el corpus de frases
python3 scripts/generar_audio.py    # sintetiza lo que falte y borra huérfanos
```

`generar_frases.py` lee el vocabulario directamente de `index.html`, así que
agregar una palabra ahí ya la hace elegible para las plantillas.

## Estructura

```
index.html                  toda la app: datos, lógica y estilos
DECISIONES.md               estado, y por qué la app es como es
audio/*.mp3                 una grabación por palabra y por frase
scripts/generar_frases.py   plantillas gramaticales y selección del corpus
scripts/generar_audio.py    síntesis con Piper y control de calidad
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

- **Pasado** (*var* es la palabra 24 en frecuencia y no está) y **posesivos**
  (*min*, *din*, con la particularidad de que el noruego los pone detrás:
  *bilen min*). Son los dos huecos gramaticales más grandes que quedan.
- Niveles 250 y 500, que exigen escribir unas 380 anclas nuevas a mano.
- Diálogo de dos turnos, única forma natural de practicar *tusen takk* y
  *vær så god*.
