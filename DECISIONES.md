# Estado y decisiones

Este archivo explica **por qué la app es como es**. El README explica los criterios;
este explica el origen de cada uno.

## Estado actual

| | |
|---|---|
| Vocabulario | 275 palabras, seis niveles anidados (25 / 61 / 120 / 170 / 226 / 275) |
| Conversaciones | 121 escritas a mano (40 / 41 / 40 en los niveles 2, 3 y 4) |
| Frases | 742, derivadas de las líneas de las conversaciones; el nivel 1 conserva 150 generadas |
| Audio | 3507 mp3 sobre 1169 textos: Piper normal y lenta, más la voz de Google, 37 MB |
| Juegos | 11, más Reglas y la Lista |
| Dependencias | ninguna; un archivo HTML |
| Persistencia | ninguna; el nivel viaja en el hash de la URL |
| Externo | solo la pestaña Hablá (voz del navegador + Google) |

**Funciona:** todo lo listado, verificado en producción.
**Sabido y aceptado:** el contador de práctica se pierde al recargar; los endpoints
de Google no son oficiales y pueden caerse (hay respaldo local).
**Pendiente:** frases para los niveles 5 y 6, flexiones, conversaciones para el nivel 1.

---

## Solicitudes, en orden

Cada línea es una petición del usuario y lo que produjo. Las marcadas con ⚑ son
correcciones del usuario a errores del modelo.

### Contenido inicial

1. 50 palabras comunes ancladas a inglés, italiano, francés, portugués o castellano → método de anclas.
2. Las mismas separadas por comas, para pegar en un traductor.
3. Tabla de tres columnas: noruego, pronunciación, castellano → nace la estructura de datos.
4. 50 palabras más, orientadas a verbos, cortesía y viaje → vocabulario de 100.

### La app

5. Sitio con ~10 pestañas, un juego por pestaña, publicado en GitHub Pages → nace Ankeret.
6. Token entregado, repo `norsk`, hacerlo directamente.
7. No insistir con la seguridad del token → se deja de mencionar.
8. Audio con botón de play → 115 grabaciones con Piper, no TTS del navegador.

### Anclas propuestas por el usuario

9. *kjøtt* → chota, el pedazo de carne.
10. *trenger* → necesito una tregua.
11. *heter* → inglés *I hate*.
12. *spiser* → inglés *spice*.
13. *bor* → Boris la re vivía.
14. *kjøper* → sumar *shopper* al *cheap* existente.
15. *beklager* → tiré la cerveza *lager*.

Las anclas del usuario resultaron mejores que las del modelo. Por eso el README
las documenta como trabajo manual y no automatizable.

### Pronunciación

16. ¿*morgen* debería ser "morgn"? → se verifica: *morn* es correcto, no se cambia.
17. Pedido de revisar la escritura fonética, con la instrucción de **no tocar si hay dudas** → se corrigen solo dos: *gir* (yir se leería *shir* en rioplatense) y *penger*.
18. Idea de marcar las letras mudas → campo `sil`, en línea aparte para no romper la lectura de la fonética.
19. ⚑ *jeg* suena más "iei" que "iai" → correcto: el diptongo *ei* es [æi] y "jai" es el acento de extranjero típico. Se corrigen *jeg*, *hei* y *nei*.
20. ⚑ *sier* suena a "si" → se mide: el archivo tenía un artefacto de 0.4 s. Se regenera y se documenta que la *-er* es genuinamente débil.

### Ajustes de interfaz

21. En Elegí, botón de play en la pregunta.
22. En Escribí, esperar a que el usuario pulse Siguiente en vez de avanzar solo.
23. ⚑ En Pares se oyen dos voces → el mp3 se cortaba a sí mismo y el `AbortError` disparaba el sintetizador del navegador.
24. En Sonido, ocultar la transcripción tras un botón de revelado.
25. Eliminar el juego Ancla.
26. Banderas 🇳🇴 🇪🇸 en vez de "no" y "es"… ⚑ pero solo en esos dos botones: *mezclado* vuelve a su etiqueta.
27. En Escribí, quitar la dirección noruego → castellano.
28. Botón Siguiente neutro, sin color de acento.
29. Botón de velocidad lenta también en Sonido → se generaliza `playBtn` en vez de duplicar código.

### Muestreo

30. Las palabras se repiten demasiado → se propone mazo.
31. ⚑ No quiero mazo ni azar puro → rechazo con tope, O(1), sin tabla.
32. Tope de 3 en vez de 2… y después de 2 otra vez.
33. ⚑ "Vi cuatro repeticiones" → se auditan dos fugas reales: un off-by-one y una escapatoria tras 40 intentos.

### Hablá

34. Grabar la voz del usuario, transcribir y traducir → Web Speech API + desglose local + Google.
35. Play de la versión modelo para comparar.
36. Versión lenta y botón de palabra al azar para improvisar.
37. ⚑ "Volviste a las palabras sueltas" → no; el modo lento de Google inserta pausas.
38. ⚑ "El normal suena igual que el lento" → cierto: `ttsspeed` frena solo 18% y el `playbackRate` se perdía al cargar el recurso. Se pasa a `playbackRate` con `defaultPlaybackRate`.
39. ⚑ "Están sonando tus mp3, no Google" → cierto: una regla del modelo prefería la grabación local si el texto coincidía. Se elimina y se avisa en pantalla cuando entra el respaldo.
40. ⚑ "Google no responde" → cierto: 404 por `Referer`. Se agrega `<meta name="referrer" content="no-referrer">`.

### Frases

41. En Sonido, submodo de frases con ~500 frases generadas.
42. ⚑ "¿Las revisaste una por una?" → no. La auditoría encuentra siete defectos, entre ellos *må ikke* mal traducido y *kommer her*, que no existe.
43. ⚑ "¿Agregaste a la lista las palabras que usaste en las frases?" → no. Faltaban *ikke* (en 104 frases), *i* y *nå*.
44. ⚑ "Las frases tienen sesgo: nunca el sujeto es un sustantivo" → cierto y medible: 0 de 500 tenían sujeto nominal, 346 empezaban con pronombre, 36 palabras no aparecían nunca.
45. ⚑ "La cortesía sí entra en oraciones" → cierto. Siete plantillas nuevas con sus ejemplos: *Jeg vil ha en ost, vær så snill*.
46. Dos rondas de scouting del modelo para diversificar → atributivos, plurales, imperativo, subordinadas, identificación, dos cláusulas con sujetos distintos.

### Niveles

47. Diagnóstico previo, sin tocar código, sobre cómo hacer niveles de vocabulario.
48. ⚑ "Elegir por cobertura es intratable" → parcialmente: el greedy es barato, pero **sería circular**. Se adopta la propuesta del usuario: la frecuencia manda, la cobertura verifica.
49. Implementar 25 / 60 / 120 conservando las palabras ya construidas → el nivel 3 son las 114 existentes más 6, así que hubo que escribir 6 anclas nuevas y no 120.

### Audio, segunda vuelta

52. ⚑ "Reproducir más lento no sirve; el problema son las pausas entre palabras. ¿Estás usando Google de verdad?" → **no**: en Sonido sonaban los mp3 de Piper; Google solo se usaba en Hablá. Y el diagnóstico era correcto: lo que cuesta al escuchar es segmentar, no la velocidad. Se genera una segunda grabación `-lento` por cada texto, con comas entre palabras para forzar pausas reales.
53. ⚑ "No te pedí que tocaras Hablá" → cierto, fue un cambio no pedido. Hablá se revierte: sigue yendo siempre a Google, porque ahí el texto lo inventa el usuario y no hay grabación propia; encadenar palabras sueltas no funciona.

54. Botón **G** en Sonido, a la izquierda del play y simétrico con el ½×, para pedir una segunda voz a Google bajo demanda → se mantiene el audio local por defecto y se evita depender de una API no oficial, pero queda la ayuda cuando hace falta contrastar.

### Reglas

55. Sección de reglas gramaticales y de pronunciación, con las de pronunciación mudadas desde la Lista, repartidas en tres niveles y **practicables, no solo enunciadas** → 22 reglas con 48 preguntas de opción múltiple; cada respuesta explica el porqué y suma al marcador general.

56. Segunda voz de Google, bajada en cinco etapas para verificar que no bloquee → 1128 archivos, 0 fallos. Después, a pedido, Google pasa a voz principal (▶₁) y Piper a segunda (▶₂).
57. ⚑ "El orden de la Lista desapareció y yo no lo pedí" → cierto: un borrado por rango se llevó el selector, y el JS huérfano cortaba la ejecución del script entero. El mismo error había borrado antes `playBtn`. Se restauran, `$()` se blinda y se agrega un simulador de DOM que corre el script completo, porque `node --check` solo valida sintaxis.
58. Poder escuchar la propia grabación en Hablá, sin que quede guardada → se intentó con MediaRecorder en paralelo al reconocimiento. **No funcionó**: en Android los dos consumidores del micrófono se pisan y el reconocedor aborta sin avisar. Serializar la toma del micrófono tampoco alcanzó. Revertido a pedido del usuario; queda pendiente hasta tener el error de consola.

59. Escalón de 50 palabras → nivel 4 (170). El tamaño se eligió por el cuello de botella real, que son las anclas escritas a mano. Composición pensada para desbloquear estructura, no vocabulario suelto: **pasado** (var, hadde), **posesivos** (min, din, que van detrás del sustantivo), subordinantes (at, som, hvis, fordi), preguntas (hvordan, hvorfor, hvem) y cuantificadores (mange, veldig, litt, to, tre).

60. Actividad para aprender de a dos en un solo teléfono → **Dúo**. Se descartó la versión con tres opciones por turno: 50 conversaciones ramificadas son incombinables a mano. Queda una conversación orquestada de 20 mensajes que avanza por reconocimiento de voz con umbral del 80%.

### Conversaciones escritas a mano

61. ⚑ "Las conversaciones las hizo un script y no tienen ni cerca el poder de un
    LLM" → cierto y medible: las 61 salían de doce esqueletos con huecos, así que
    había doce formas repetidas sesenta veces, todas de pregunta y respuesta y casi
    todas terminadas en *ha det*. Se reemplazan por **121 escritas una por una**, de
    ocho a diez turnos, con desacuerdos, insistencias y finales que no son despedida.
    `scripts/generar_dialogos.py` se borra: dejarlo sería afirmar que las
    conversaciones son reproducibles desde él, y no lo son.

62. **La optimización de audio, pedida junto con lo anterior**: en vez de mantener
    un corpus de frases y otro de diálogos, las líneas de las conversaciones **son**
    las frases del juego Sonido. Una grabación sirve para las dos cosas y las líneas
    repetidas entre conversaciones comparten archivo. El corpus baja de 1450 frases a
    741, los textos grabados de 1757 a 1067 y el audio de 41 MB a 35.

    Lo que costó la derivación no fue el volumen sino tres detalles que la rompían:
    las líneas de una o dos palabras ("Ja", "Nå?") no sirven como opción múltiple
    y se descartan; dos frases distintas no pueden compartir traducción castellana
    dentro de un nivel; y los señuelos necesitan una **familia estructural** que
    reemplace a la plantilla que antes venía del generador, porque si salen al azar
    la respuesta se adivina por la forma sin escuchar.

63. **El nivel 1 no tiene conversaciones y Dúo queda deshabilitado abajo de 60.**
    Con 25 palabras no hay preposiciones, ni cortesía, ni pronombres de objeto: sale
    un ejercicio, no una conversación. El respaldo que hacía caer al nivel 2 se saca,
    porque contradecía el cartel de la propia pantalla. Las 150 frases generadas del
    nivel 1 se conservan: sin ellas, Sonido se queda sin submodo de frases.

64. Escribir a mano 983 líneas trae de vuelta el problema que las plantillas
    evitaban: **el modelo inventa palabras que suenan bien y no están en la lista**.
    En la primera pasada, 40 de 118 líneas usaban vocabulario de afuera (*da*, *bra*,
    *alltid*, *hjemme*, *selvfølgelig*). Se escribe un validador que replica en
    Python el reductor de flexiones de la app y se itera hasta cero. La lección es la
    de siempre acá: si no se midió, no está verificado.

### El top-200 de frecuencia

65. Pregunta por una lista oficial noruega de 350 palabras básicas → **no existe**.
    Lo único con ese número es Malimo, una editorial privada. HK-dir dice explícito
    que la Norskprøven no tiene temario, y el *Læreplan* define A1 por lo que el
    alumno puede hacer, no por qué palabras sabe. A diferencia del alemán, que sí
    tiene la *Wortliste* del Goethe-Institut, en noruego ese objeto no está. Queda
    `wordfreq` como criterio, que es el que ya se usaba.

66. "Agregá las palabras para llegar a un wordfreq de 200, pero para todo lo que no
    incluya frases" → **56 entradas nuevas, nivel 5, total 226**. El vocabulario
    cubría 118 de las 200; 21 de las que faltaban eran otra forma de una que ya
    estaba (*ble*, *vært*, *fikk*, *dem*, *bedre*) y 7 eran ruido (cifras, *Norge*,
    *Oslo*).

    **El nivel suma palabras y no suma frases, a pedido.** Es la primera vez que un
    nivel de la app hace eso, y hay que decirlo en pantalla o parece un bug: el
    selector muestra una nota cuando estás en 226.

67. ⚑ El validador propio daba por cubiertas tres palabras que no lo estaban: *så*
    (lo reducía al pasado de *se*), *enn* (le sacaba la n final y daba *en*) y
    *mener* (le sacaba *-er* y daba *men*). El reductor de flexiones acierta el
    99.8% de los tokens del corpus pero produce falsos positivos justo donde una
    palabra corta se parece a otra. Se detectaron comparando contra el top-200 por
    string exacto, no por resolución.

68. Cuatro pares quedaron homófonos: **og/å** (idénticos: la trampa ortográfica
    número uno del noruego nativo), *man/mann*, *for/får*, *hus/hos*. En Sonido eso
    haría preguntas sin respuesta posible, así que dos palabras con la misma
    escritura fonética ya no pueden ser señuelo una de otra. El par se documenta en
    el campo `sil`, que para eso está.

69. "Llevá las entradas a 275, solo palabras, frases inhabilitadas en ese nivel" →
    **49 entradas nuevas, nivel 6**. Cubren el top-275 salvo *videre* y los
    topónimos. La composición cambió respecto del escalón anterior: 11 verbos
    (*skjer, kjenner, viser, holder, ligger, lager, betyr, sitter, synes, prøver,
    håper*) y, sobre todo, un bloque de adverbios de matiz — *faktisk, egentlig,
    virkelig, nesten, gjerne, ganske, altså, sånn, kun, heller* — que es el registro
    que separa el habla de la lista de vocabulario. También entra **dårlig**, el
    antónimo de *bra*, que hasta ahora no existía.

70. Medido antes de decidir: el top-170 cubre 58,6% del texto corrido, el top-226
    61,3% y el top-275 63,1%. Cada escalón cuesta lo mismo en anclas escritas a mano
    y rinde la mitad que el anterior. Es la razón por la que 275 cierra la serie de
    vocabulario y lo que sigue son flexiones, no palabras.

71. Antes de aceptar el pedido se verificó qué significa "aparecer en las
    actividades": las cartas salen de `W`, así que una flexión como *større* no
    puede salir nunca; solo aparece dentro de una frase. De las 45 flexiones del
    top-260, **8 están en el corpus y 37 no**. Agregar flexiones no es tocar la
    lista: es escribir frases. Por eso el pedido fue de lemas y no de formas.

### La revisión de las frases

72. ⚑ "Cuando leo las frases detecto diferencia entre cómo me presentaste la palabra
    y cómo está usada" → auditoría preposición por preposición de las 983 líneas.
    **19 problemas reales, 40 líneas tocadas.** El ejemplo que traía era una lectura
    errónea suya (*før toget*, antes del tren, no *for*), pero el pedido era correcto
    y encontró cosas.

    Lo peor: **en tren, avión y hotel se va *på*, no *i***. Once líneas decían
    *i toget*, *i flyet*, *i hotellet*. Es el error clásico del hispanohablante, que
    traduce «en» por *i* siempre. Y ***fra her* no existe**: es *herfra*.

73. **La preposición no se puede validar con el validador de vocabulario.** *i* es
    una palabra del nivel 2 y *i toget* pasa todos los controles automáticos: cada
    token está en la lista y en el nivel. Lo que falla es la colocación, que ningún
    control de pertenencia detecta. Es el límite de la verificación que se venía
    haciendo, y hoy no tiene reemplazo automático.

74. ***Det er godt* apareció ocho veces traducido «está bien»**, y no significa eso:
    es «está bueno». Para asentir el noruego usa *bra* o *greit*, y las dos están
    recién en el nivel 5. Se corrigió el castellano en vez de forzar el noruego.
    Queda una inconsistencia anotada: *bra* es la palabra 123 por frecuencia y vive
    en el nivel 5, mientras que *eple* está en el 2. Bajarla al 2 arreglaría el
    problema de raíz, pero mueve niveles y no se hizo sin pedido.

75. El contador de práctica no sabía reducir los posesivos: *mitt*, *boka mi* y
    *huset mitt* estaban en el corpus desde antes y no sumaban. Se agregó un mapa
    `FORMAS` a `resolve()` con posesivos y plurales irregulares.

### Documentación

50. README con los criterios de construcción → se detecta que el generador de frases vivía fuera del repo y el corpus no era reproducible.
51. Este archivo.

---

## Lo que estas correcciones cambiaron en el diseño

- **El usuario audita mejor de oído que el modelo por medición.** Tres bugs de audio y pronunciación los detectó él escuchando; el modelo solo pudo confirmarlos midiendo después. De ahí que exista el botón lento y el aviso de cuándo entra el respaldo.
- **Nada se da por verificado si no se midió.** Las auditorías de cobertura y de tokens nacieron de dos preguntas del usuario que el modelo había contestado de memoria y mal.
- **Las decisiones de muestreo y de niveles son del usuario.** El modelo propuso mazo y cobertura óptima; ambas se descartaron por buenas razones y lo que quedó es más simple.
- **Nada de refactors grandes sin pedido.** Los cambios se hicieron incrementales y verificados en producción, uno por uno.
