# -*- coding: utf-8 -*-
"""Genera las conversaciones orquestadas de la pestaña Dúo.

Cada conversación es un esqueleto coherente con huecos: se instancia varias veces
cambiando el objeto, la bebida o el lugar. Así hay variedad sin perder el sentido,
que es lo que se pierde si se generan turnos sueltos por plantilla.

Salida: /home/claude/dialogos.json  →  [{lvl, titulo, lineas:[[quien, no, es], ...]}]
"""
import json, re, itertools, random

RAIZ = "/home/claude/norsk"
_html = open(f"{RAIZ}/index.html", encoding="utf-8").read()
_w = _html[_html.index("const W = ["):_html.index("const SENT = [")]
NIV = {m.group(1): int(m.group(2)) for m in re.finditer(r'\{no:"([^"]+)"[^}]*?lvl:(\d)', _w)}

# formas de superficie que no son entrada de la lista pero se derivan de una
FORMAS = {
 "huset":"hus","bilen":"bil","boka":"bok","toget":"tog","flyet":"fly","hotellet":"hotell",
 "toalettet":"toalett","billetten":"billett","tingen":"ting","gaten":"gate","byen":"by",
 "mannen":"mann","kvinnen":"kvinne","barnet":"barn","hunden":"hund","katten":"katt",
 "fisken":"fisk","osten":"ost","brødet":"brød","egget":"egg","eplet":"eple","melken":"melk",
 "vannet":"vann","kjøttet":"kjøtt","maten":"mat","dagen":"dag","natten":"natt","året":"år",
 "kaffen":"kaffe","jobben":"jobb","telefonen":"telefon","pengene":"penger","tiden":"tid",
 "hjemme":"hjem","klokka":"klokka",
 "spise":"spiser","drikke":"drikker","kjøpe":"kjøper","se":"ser","ha":"har","ta":"tar",
 "finne":"finner","betale":"betaler","hjelpe":"hjelper","komme":"kommer","gå":"går",
 "reise":"reiser","snakke":"snakker","forstå":"forstår","lese":"leser","skrive":"skriver",
 "jobbe":"jobber","sove":"sover","vente":"venter","huske":"husker","glemme":"glemmer",
 "skjønne":"skjønner","bo":"bor","gi":"gir","høre":"hører","si":"sier","vite":"vet",
 "nytt":"ny","godt":"god","stort":"stor","lite":"liten","gammelt":"gammel","varmt":"varm",
 "kaldt":"kald","store":"stor","lille":"liten","nye":"ny","gode":"god","gamle":"gammel",
 "mitt":"min","ditt":"din","biler":"bil","bøker":"bok","katter":"katt","hunder":"hund",
 "epler":"eple","billetter":"billett","var":"var","hadde":"hadde","så":"ser","tok":"tar",
 "kjøpte":"kjøper","drakk":"drikker","spiste":"spiser","leste":"leser","skrev":"skriver",
 "husket":"husker","glemte":"glemmer","betalte":"betaler","fant":"finner","hørte":"hører",
}
def base(t):
    t = t.lower().strip("?!.,")
    return FORMAS.get(t, t)

NOMBRES = {"maria","rodrigo","anna","erik"}
MULTI = sorted([w for w in NIV if " " in w], key=len, reverse=True)

def nivel_de(texto):
    """nivel mínimo que hace falta para decir esta línea"""
    t = " " + texto.lower().replace("?"," ").replace("."," ").replace(","," ") + " "
    n = 1
    # primero las entradas de varias palabras: vær så god, tusen takk, god morgen…
    for w in MULTI:
        marca = " " + w.lower().replace("?","") + " "
        while marca in t:
            n = max(n, NIV[w]); t = t.replace(marca, " ", 1)
    for tok in t.split():
        b = base(tok)
        if b in NIV: n = max(n, NIV[b])
        elif b in NOMBRES: pass
        else: return 99          # palabra desconocida: la línea no sirve
    return n

# ---------------------------------------------------------------- esqueletos
# A y B se alternan. {x} son huecos.
ESQ = [
{"id":"cafe","t":"En el café","slots":{
   "beb":[("kaffe","kaffen","el café"),("melk","melken","la leche"),("vann","vannet","el agua")],
   "com":[("brød","brødet","el pan"),("eple","eplet","la manzana"),("ost","osten","el queso")]},
 "l":[
  ("A","Hei","Hola"),
  ("B","Hei, hvordan går det?","Hola, ¿cómo andás?"),
  ("A","Det er godt","Todo bien"),
  ("B","Vil du ha {beb1}?","¿Querés {beb2}?"),
  ("A","Ja takk, jeg vil ha {beb1}","Sí gracias, quiero {beb2}"),
  ("B","Vil du ha {com1} også?","¿Querés {com2} también?"),
  ("A","Nei takk, bare {beb1}","No gracias, solo {beb2}"),
  ("B","Hvor mye koster {beb0}?","¿Cuánto cuesta {beb2}?"),
  ("A","Jeg vet ikke","No sé"),
  ("B","Jeg spør","Yo pregunto"),
  ("A","Takk","Gracias"),
  ("B","Vær så god","De nada"),
  ("A","{beb0} er veldig god","{beb2} está muy bueno"),
  ("B","Ja, den er god","Sí, está bueno"),
  ("A","Jeg betaler","Yo pago"),
  ("B","Nei, jeg betaler","No, pago yo"),
  ("A","Takk, du er god","Gracias, sos buena persona"),
  ("B","Vi kommer igjen","Volvemos otra vez"),
  ("A","Ja, vi kommer igjen","Sí, volvemos"),
  ("B","Ha det","Chau"),
 ]},
{"id":"n2casa","t":"Mirando la casa","slots":{
   "obj":[("bok","boka","el libro"),("bil","bilen","el auto"),("hund","hunden","el perro")]},
 "l":[
  ("A","Hei","Hola"),
  ("B","Hei","Hola"),
  ("A","Hva er dette?","¿Qué es esto?"),
  ("B","Det er {obj1}","Es {obj2}"),
  ("A","Er {obj1} ny?","¿{obj2} es nuevo?"),
  ("B","Ja, {obj1} er ny","Sí, es nuevo"),
  ("A","Jeg liker {obj1}","Me gusta {obj2}"),
  ("B","Vil du ha {obj1}?","¿Lo querés?"),
  ("A","Ja takk","Sí, gracias"),
  ("B","Det er godt","Está bien"),
  ("A","Hvor er huset?","¿Dónde está la casa?"),
  ("B","Huset er her","La casa está acá"),
  ("A","Huset er stort","La casa es grande"),
  ("B","Ja, men det er gammelt","Sí, pero es vieja"),
  ("A","Jeg bor her nå","Vivo acá ahora"),
  ("B","Jeg kommer nå","Vengo ahora"),
  ("A","Vi spiser her","Comemos acá"),
  ("B","Ja, vi spiser brødet","Sí, comemos el pan"),
  ("A","Takk","Gracias"),
  ("B","Hei","Chau"),
 ]},
{"id":"n2animal","t":"El perro y el gato","slots":{
   "ani":[("hund","hunden","el perro"),("katt","katten","el gato")],
   "com":[("fisk","fisken","el pescado"),("brød","brødet","el pan"),("eple","eplet","la manzana")]},
 "l":[
  ("A","Hei, hva ser du?","Hola, ¿qué ves?"),
  ("B","Jeg ser {ani1}","Veo {ani2}"),
  ("A","Er {ani1} stor?","¿Es grande?"),
  ("B","Nei, {ani1} er liten","No, es chico"),
  ("A","Jeg liker {ani1}","Me gusta {ani2}"),
  ("B","{ani1} spiser {com1}","{ani2} come {com2}"),
  ("A","Spiser {ani1} {com1}?","¿Come {com2}?"),
  ("B","Ja, {ani1} spiser","Sí, come"),
  ("A","Har du en {ani0}?","¿Tenés {ani2}?"),
  ("B","Ja, jeg har en {ani0}","Sí, tengo uno"),
  ("A","Hvor er {ani1} nå?","¿Dónde está ahora?"),
  ("B","{ani1} er der","Está allá"),
  ("A","{ani1} drikker vannet","{ani2} toma el agua"),
  ("B","Ja, det er godt","Sí, está bien"),
  ("A","Vil du gå?","¿Querés ir?"),
  ("B","Ja, vi går nå","Sí, vamos ahora"),
  ("A","Kommer {ani1}?","¿Viene?"),
  ("B","Ja, {ani1} kommer","Sí, viene"),
  ("A","Takk","Gracias"),
  ("B","Hei","Chau"),
 ]},
{"id":"n3calle","t":"Perdidos en la calle","slots":{
   "lug":[("hotell","hotellet","el hotel"),("toalett","toalettet","el baño"),("tog","toget","el tren")]},
 "l":[
  ("A","Unnskyld","Disculpe"),
  ("B","Ja?","¿Sí?"),
  ("A","Hvor er {lug1}?","¿Dónde está {lug2}?"),
  ("B","{lug1} er der, til høyre","{lug2} está allá, a la derecha"),
  ("A","Tusen takk","Muchas gracias"),
  ("B","Vær så god","De nada"),
  ("A","Snakker du engelsk?","¿Hablás inglés?"),
  ("B","Nei, beklager","No, lo siento"),
  ("A","Jeg forstår ikke norsk","No entiendo noruego"),
  ("B","Jeg snakker norsk","Yo hablo noruego"),
  ("A","Takk, nå forstår jeg","Gracias, ahora entiendo"),
  ("B","Reiser du i dag?","¿Viajás hoy?"),
  ("A","Ja, jeg tar toget","Sí, tomo el tren"),
  ("B","Hvor mye koster billetten?","¿Cuánto cuesta el boleto?"),
  ("A","Jeg vet ikke","No sé"),
  ("B","Du kan betale her","Podés pagar acá"),
  ("A","Jeg har penger","Tengo dinero"),
  ("B","Det er godt","Está bien"),
  ("A","Tusen takk","Muchas gracias"),
  ("B","Ha det","Chau"),
 ]},
{"id":"n3cafe","t":"Pidiendo en el mostrador","slots":{
   "com":[("ost","osten","el queso"),("egg","egget","el huevo"),("fisk","fisken","el pescado")],
   "beb":[("vann","vannet","el agua"),("melk","melken","la leche")]},
 "l":[
  ("A","God morgen","Buen día"),
  ("B","God morgen","Buen día"),
  ("A","Jeg vil ha {com1}, vær så snill","Quiero {com2}, por favor"),
  ("B","Vil du ha {beb1}?","¿Querés {beb2}?"),
  ("A","Ja, vær så snill","Sí, por favor"),
  ("B","Vær så god","Aquí tiene"),
  ("A","Tusen takk","Muchas gracias"),
  ("B","Hvor mye vil du ha?","¿Cuánto querés?"),
  ("A","Ikke mye","No mucho"),
  ("B","{com1} er varm","{com2} está caliente"),
  ("A","Det er godt","Está bien"),
  ("A","Hvor mye koster det?","¿Cuánto cuesta?"),
  ("B","Du kan betale her","Podés pagar acá"),
  ("A","Jeg betaler nå","Pago ahora"),
  ("B","Takk","Gracias"),
  ("A","Hvor er toalettet?","¿Dónde está el baño?"),
  ("B","Toalettet er til venstre","El baño está a la izquierda"),
  ("A","Tusen takk","Muchas gracias"),
  ("B","Ha det","Chau"),
  ("A","Ha det","Chau"),
 ]},
{"id":"tren","t":"En la estación","slots":{
   "veh":[("tog","toget","el tren"),("fly","flyet","el avión"),("bil","bilen","el auto")],
   "lug":[("by","byen","la ciudad"),("hotell","hotellet","el hotel"),("hus","huset","la casa")]},
 "l":[
  ("A","Unnskyld, hvor er {veh0}?","Disculpe, ¿dónde está {veh2}?"),
  ("B","{veh1} er der","{veh2} está allá"),
  ("A","Takk. Når kommer {veh1}?","Gracias. ¿Cuándo viene {veh2}?"),
  ("B","Jeg vet ikke","No sé"),
  ("A","Jeg venter her","Espero acá"),
  ("B","Reiser du til {lug1}?","¿Viajás a {lug2}?"),
  ("A","Ja, jeg reiser til {lug1}","Sí, viajo a {lug2}"),
  ("B","Jeg reiser også","Yo también viajo"),
  ("A","Har du en billett?","¿Tenés un boleto?"),
  ("B","Nei, jeg må kjøpe en billett","No, tengo que comprar un boleto"),
  ("A","Hvor mye koster billetten?","¿Cuánto cuesta el boleto?"),
  ("B","Jeg spør","Pregunto"),
  ("A","Jeg har penger","Tengo dinero"),
  ("B","Takk, men jeg betaler","Gracias, pero pago yo"),
  ("A","{veh1} kommer nå","{veh2} viene ahora"),
  ("B","Ja, jeg ser {veh1}","Sí, veo {veh2}"),
  ("A","Vi tar {veh1}","Tomamos {veh2}"),
  ("B","Jeg er her","Estoy acá"),
  ("A","Vi kommer til {lug1} i dag","Llegamos a {lug2} hoy"),
  ("B","Ha det","Chau"),
 ]},
{"id":"casa","t":"Buscando algo en casa","slots":{
   "obj":[("bok","boka","el libro"),("telefon","telefonen","el teléfono"),("billett","billetten","el boleto")],
   "sitio":[("hus","huset","la casa"),("bil","bilen","el auto"),("jobb","jobben","el trabajo")]},
 "l":[
  ("A","Hei, hvor er {obj1} min?","Hola, ¿dónde está mi {obj2}?"),
  ("B","Jeg vet ikke","No sé"),
  ("A","Jeg husker ikke","No me acuerdo"),
  ("B","Var {obj1} i {sitio1}?","¿{obj2} estaba en {sitio2}?"),
  ("A","Ja, {obj1} var der","Sí, estaba ahí"),
  ("B","Jeg ser ikke {obj1}","No veo {obj2}"),
  ("A","Jeg glemte {obj1}","Me olvidé {obj2}"),
  ("B","Hvorfor glemte du {obj1}?","¿Por qué te olvidaste?"),
  ("A","Fordi jeg jobber mye","Porque trabajo mucho"),
  ("B","Jeg hjelper deg","Te ayudo"),
  ("A","Takk, du er veldig god","Gracias, sos muy buena"),
  ("B","Er {obj1} her?","¿Está acá?"),
  ("A","Nei, {obj1} er ikke her","No, no está acá"),
  ("B","Jeg finner {obj1}","Yo lo encuentro"),
  ("A","Hvor var {obj1}?","¿Dónde estaba?"),
  ("B","{obj1} var i {sitio1}","Estaba en {sitio2}"),
  ("A","Tusen takk","Muchas gracias"),
  ("B","Vær så god","De nada"),
  ("A","Nå kan vi gå","Ahora podemos ir"),
  ("B","Ja, vi går","Sí, vamos"),
 ]},
{"id":"comida","t":"Preparando la comida","slots":{
   "com":[("fisk","fisken","el pescado"),("kjøtt","kjøttet","la carne"),("egg","egget","el huevo")],
   "beb":[("vann","vannet","el agua"),("melk","melken","la leche"),("kaffe","kaffen","el café")]},
 "l":[
  ("A","Er du her?","¿Estás acá?"),
  ("B","Ja, jeg er her","Sí, estoy acá"),
  ("A","Jeg spiser ikke nå","No como ahora"),
  ("B","Hvorfor ikke?","¿Por qué no?"),
  ("A","Fordi jeg venter","Porque estoy esperando"),
  ("B","Vi har {com1}","Tenemos {com2}"),
  ("A","Er {com1} god?","¿Está bueno?"),
  ("B","Ja, {com1} er veldig god","Sí, está muy bueno"),
  ("A","Jeg vil ha {com1}","Quiero {com2}"),
  ("B","Vil du ha {beb1} også?","¿Querés {beb2} también?"),
  ("A","Ja takk","Sí, gracias"),
  ("B","{beb1} er kald","{beb2} está fría"),
  ("A","Det er godt","Está bien"),
  ("B","Spiser du {com1}?","¿Comés {com2}?"),
  ("A","Nei, jeg spiser aldri {com1}","No, nunca como {com2}"),
  ("B","Jeg spiser {com1} igjen","Yo como {com2} otra vez"),
  ("A","Tusen takk","Muchas gracias"),
  ("B","Vær så god","De nada"),
  ("A","Nå er jeg god","Ahora estoy bien"),
  ("B","Ja, det er godt","Sí, está bien"),
 ]},
{"id":"hotel","t":"En el hotel","slots":{
   "cosa":[("bok","boka","el libro"),("telefon","telefonen","el teléfono"),("billett","billetten","el boleto")]},
 "l":[
  ("A","God morgen","Buen día"),
  ("B","God morgen. Hvordan er hotellet?","Buen día. ¿Cómo es el hotel?"),
  ("A","Hotellet er stort og godt","El hotel es grande y bueno"),
  ("B","Er toalettet her?","¿El baño está acá?"),
  ("A","Nei, toalettet er der","No, el baño está allá"),
  ("B","Takk","Gracias"),
  ("A","Har du {cosa1} din?","¿Tenés tu {cosa2}?"),
  ("B","Nei, jeg glemte {cosa1}","No, me olvidé {cosa2}"),
  ("A","Hvor var {cosa1}?","¿Dónde estaba?"),
  ("B","{cosa1} var i bilen","Estaba en el auto"),
  ("A","Jeg finner {cosa1}","Lo encuentro yo"),
  ("B","Tusen takk","Muchas gracias"),
  ("A","Vi går i byen","Vamos a la ciudad"),
  ("B","Ja, jeg vil gå","Sí, quiero ir"),
  ("A","Vi tar toget","Tomamos el tren"),
  ("B","Hvor mye koster billetten?","¿Cuánto cuesta el boleto?"),
  ("A","Jeg vet ikke, jeg spør","No sé, pregunto"),
  ("B","Vi har penger","Tenemos dinero"),
  ("A","Vi kommer hjem i natt","Volvemos a casa esta noche"),
  ("B","Det er godt","Está bien"),
 ]},
{"id":"idioma","t":"Practicando el idioma","slots":{
   "obj":[("bok","boka","el libro"),("telefon","telefonen","el teléfono")]},
 "l":[
  ("A","Hei, snakker du norsk?","Hola, ¿hablás noruego?"),
  ("B","Ja, litt","Sí, un poco"),
  ("A","Jeg snakker ikke norsk","Yo no hablo noruego"),
  ("B","Snakker du engelsk?","¿Hablás inglés?"),
  ("A","Ja, jeg snakker engelsk","Sí, hablo inglés"),
  ("B","Jeg skjønner","Entiendo"),
  ("A","Hva heter du?","¿Cómo te llamás?"),
  ("B","Jeg heter Maria","Me llamo María"),
  ("A","Hvor bor du?","¿Dónde vivís?"),
  ("B","Jeg bor i byen","Vivo en la ciudad"),
  ("A","Jobber du her?","¿Trabajás acá?"),
  ("B","Ja, jeg jobber her","Sí, trabajo acá"),
  ("A","Jeg leser {obj1}","Yo leo {obj2}"),
  ("B","Er {obj1} god?","¿Está bueno?"),
  ("A","Ja, men jeg forstår ikke alt".replace("alt","alle"),"Sí, pero no entiendo a todos"),
  ("B","Jeg hjelper deg","Te ayudo"),
  ("A","Tusen takk","Muchas gracias"),
  ("B","Vær så god","De nada"),
  ("A","Vi snakker igjen","Hablamos otra vez"),
  ("B","Ja, ha det","Sí, chau"),
 ]},
{"id":"compras","t":"De compras","slots":{
   "obj":[("bok","boka","el libro"),("bil","bilen","el auto"),("telefon","telefonen","el teléfono")]},
 "l":[
  ("A","Hei, hva gjør du?","Hola, ¿qué hacés?"),
  ("B","Jeg kjøper {obj1}","Compro {obj2}"),
  ("A","Hvorfor kjøper du {obj1}?","¿Por qué comprás {obj2}?"),
  ("B","Fordi {obj1} er veldig god","Porque {obj2} es muy bueno"),
  ("A","Hvor mye koster {obj1}?","¿Cuánto cuesta {obj2}?"),
  ("B","Jeg vet ikke","No sé"),
  ("A","Har du penger?","¿Tenés dinero?"),
  ("B","Ja, jeg har litt","Sí, tengo un poco"),
  ("A","Jeg har også penger","Yo también tengo dinero"),
  ("B","Takk, men jeg betaler","Gracias, pero pago yo"),
  ("A","Er {obj1} ny?","¿{obj2} es nuevo?"),
  ("B","Nei, {obj1} er gammel","No, es viejo"),
  ("A","Jeg ser mange biler","Veo muchos autos"),
  ("B","Ja, det er mange biler her","Sí, hay muchos autos acá"),
  ("A","Jeg vil se {obj1} din","Quiero ver tu {obj2}"),
  ("B","Vær så god","Aquí tenés"),
  ("A","{obj1} er veldig stor","{obj2} es muy grande"),
  ("B","Ja, jeg liker {obj1}","Sí, me gusta {obj2}"),
  ("A","Vi går hjem nå","Vamos a casa ahora"),
  ("B","Ja, vi går","Sí, vamos"),
 ]},
{"id":"ayer","t":"Contando lo de ayer","slots":{
   "obj":[("bok","boka","el libro"),("fisk","fisken","el pescado"),("kaffe","kaffen","el café")],
   "lug":[("by","byen","la ciudad"),("hotell","hotellet","el hotel"),("gate","gaten","la calle")]},
 "l":[
  ("A","Hei, hvor var du?","Hola, ¿dónde estabas?"),
  ("B","Jeg var i {lug1}","Estaba en {lug2}"),
  ("A","Hva gjør du?","¿Qué hacés?"),
  ("B","Jeg jobber","Trabajo"),
  ("A","Hadde du tid?","¿Tenías tiempo?"),
  ("B","Nei, jeg hadde ikke tid","No, no tenía tiempo"),
  ("A","Jeg venter","Yo espero"),
  ("B","Unnskyld, jeg glemte det","Perdón, me olvidé"),
  ("A","Det er godt","Está bien"),
  ("B","Jeg kjøpte {obj1}","Compré {obj2}"),
  ("A","Var {obj1} god?","¿Estaba bueno?"),
  ("B","Ja, {obj1} var veldig god","Sí, estaba muy bueno"),
  ("A","Jeg så {lug1}","Yo vi {lug2}"),
  ("B","Hvordan var {lug1}?","¿Cómo era {lug2}?"),
  ("A","{lug1} var stor og gammel","Era grande y vieja"),
  ("B","Jeg husker {lug1}","Me acuerdo de {lug2}"),
  ("A","Vi var der i natt","Estuvimos ahí anoche"),
  ("B","Ja, jeg husker","Sí, me acuerdo"),
  ("A","Vi kommer igjen","Volvemos"),
  ("B","Ha det","Chau"),
 ]},
]

def instanciar(esq, valores):
    lineas = []
    for quien, no, es in esq["l"]:
        n, e = no, es
        for k,(indef, defi, esp) in valores.items():
            n = n.replace("{%s0}"%k, indef).replace("{%s1}"%k, defi)
            e = e.replace("{%s0}"%k, esp).replace("{%s1}"%k, esp).replace("{%s2}"%k, esp)
            n = n.replace("{%s2}"%k, defi)
        lineas.append([quien, n, e])
    return lineas

def main():
    random.seed(31415)
    salida = []
    for esq in ESQ:
        claves = list(esq["slots"])
        combos = list(itertools.product(*[esq["slots"][k] for k in claves]))
        random.shuffle(combos)
        for combo in combos[:7]:
            valores = dict(zip(claves, combo))
            lineas = instanciar(esq, valores)
            lvl = max(nivel_de(l[1]) for l in lineas)
            if lvl > 4:
                malas = [l[1] for l in lineas if nivel_de(l[1]) > 4]
                print("  descartada (%s): %s" % (esq["id"], malas[:2]))
                continue
            salida.append({"lvl":lvl, "titulo":esq["t"], "lineas":lineas})
    # deduplicar
    vistos, fin = set(), []
    for c in salida:
        k = "|".join(l[1] for l in c["lineas"])
        if k in vistos: continue
        vistos.add(k); fin.append(c)
    random.shuffle(fin)
    from collections import Counter
    print("conversaciones:", len(fin), "| por nivel:", dict(sorted(Counter(c["lvl"] for c in fin).items())))
    print("líneas totales:", sum(len(c["lineas"]) for c in fin))
    json.dump(fin, open("/home/claude/dialogos.json","w"), ensure_ascii=False)

if __name__ == "__main__":
    main()
