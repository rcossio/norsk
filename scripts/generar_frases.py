# -*- coding: utf-8 -*-
"""Genera frases por nivel (25 / 60 / 120), con plantillas variadas."""
import random, json
from collections import Counter, defaultdict

# ---------------- niveles ----------------
NUEVAS_3 = ["meg","deg","på","til","med","fra"]
import re as _re
_html = open("/home/claude/norsk/index.html", encoding="utf-8").read()
_wblock = _html[_html.index("const W = ["):_html.index("const SENT = [")]
_todas = _re.findall(r'\{no:"([^"]+)"', _wblock)
# los niveles salen del campo lvl de index.html, que es la fuente de verdad
import re as _re
_html = open("/home/claude/norsk/index.html", encoding="utf-8").read()
_w = _html[_html.index("const W = ["):_html.index("const SENT = [")]
_NIV = {m.group(1): int(m.group(2)) for m in _re.finditer(r'\{no:"([^"]+)"[^}]*?lvl:(\d)', _w)}
L1     = [w for w,l in _NIV.items() if l == 1]
L2_ADD = [w for w,l in _NIV.items() if l == 2]
L3_ADD = [w for w,l in _NIV.items() if l == 3]
L4_ADD = [w for w,l in _NIV.items() if l == 4]

def nivel(w):
    if w in L1: return 1
    if w in L2_ADD: return 2
    return 3

# sustantivo: (indef, gen, def, es_gen, es_indef, es_def, masa)
N = [
 ("mann","en","mannen","m","un hombre","el hombre",0),
 ("kvinne","en","kvinnen","f","una mujer","la mujer",0),
 ("hus","et","huset","f","una casa","la casa",0),
 ("bil","en","bilen","m","un auto","el auto",0),
 ("vann","et","vannet","f",None,"el agua",1),
 ("brød","et","brødet","m","un pan","el pan",0),
 ("barn","et","barnet","m","un niño","el niño",0),
 ("hund","en","hunden","m","un perro","el perro",0),
 ("katt","en","katten","m","un gato","el gato",0),
 ("fisk","en","fisken","m","un pescado","el pescado",0),
 ("bok","en","boka","m","un libro","el libro",0),
 ("dag","en","dagen","m","un día","el día",0),
 ("tog","et","toget","m","un tren","el tren",0),
 ("eple","et","eplet","f","una manzana","la manzana",0),
 ("melk","en","melken","f",None,"la leche",1),
 ("ting","en","tingen","f","una cosa","la cosa",0),
 ("ost","en","osten","m","un queso","el queso",0),
 ("egg","et","egget","m","un huevo","el huevo",0),
 ("kjøtt","et","kjøttet","f",None,"la carne",1),
 ("natt","en","natten","f","una noche","la noche",0),
 ("by","en","byen","f","una ciudad","la ciudad",0),
 ("gate","en","gaten","f","una calle","la calle",0),
 ("fly","et","flyet","m","un avión","el avión",0),
 ("billett","en","billetten","m","un boleto","el boleto",0),
 ("hotell","et","hotellet","m","un hotel","el hotel",0),
 ("toalett","et","toalettet","m","un baño","el baño",0),
 ("år","et","året","m","un año","el año",0),
 ("hånd","en","hånden","f","una mano","la mano",0),
 ("fot","en","foten","m","un pie","el pie",0),
 ("øye","et","øyet","m","un ojo","el ojo",0),
 ("munn","en","munnen","f","una boca","la boca",0),
 ("mat","en","maten","f",None,"la comida",1),
 ("penger","en","pengene","m",None,"el dinero",1),
 ("tid","en","tiden","m",None,"el tiempo",1),
 ("jobb","en","jobben","m","un trabajo","el trabajo",0),
 ("kaffe","en","kaffen","m",None,"el café",1),
 ("telefon","en","telefonen","m","un teléfono","el teléfono",0),
]
NX = {n[0]: n for n in N}
PLURAL = {'mann': ('menn', 'hombres'), 'kvinne': ('kvinner', 'mujeres'), 'hus': ('hus', 'casas'), 'bil': ('biler', 'autos'), 'brød': ('brød', 'panes'), 'barn': ('barn', 'niños'), 'hund': ('hunder', 'perros'), 'katt': ('katter', 'gatos'), 'fisk': ('fisker', 'pescados'), 'bok': ('bøker', 'libros'), 'dag': ('dager', 'días'), 'tog': ('tog', 'trenes'), 'eple': ('epler', 'manzanas'), 'ting': ('ting', 'cosas'), 'ost': ('oster', 'quesos'), 'egg': ('egg', 'huevos'), 'natt': ('netter', 'noches'), 'by': ('byer', 'ciudades'), 'gate': ('gater', 'calles'), 'fly': ('fly', 'aviones'), 'billett': ('billetter', 'boletos'), 'hotell': ('hoteller', 'hoteles'), 'toalett': ('toaletter', 'baños'), 'år': ('år', 'años'), 'hånd': ('hender', 'manos'), 'fot': ('føtter', 'pies'), 'øye': ('øyne', 'ojos')}
ANIM   = {"mann","kvinne","barn","hund","katt"}
COMIDA = ["fisk","ost","brød","egg","eple","kjøtt"]
BEBIDA = ["melk","vann"]
COSAS  = ["bil","bok","billett","ting","hus","fly","tog","eple","brød","ost","fisk","egg"]
LUGAR  = ["hus","by","gate","hotell","tog","fly","bil","toalett"]

P = [("jeg","yo"),("du","vos"),("han","él"),("hun","ella"),("vi","nosotros"),("de","ellos")]
VT = {
 "spiser":  ("spise","comer", ["como","comés","come","come","comemos","comen"], COMIDA+["mat"]),
 "drikker": ("drikke","beber",["bebo","bebés","bebe","bebe","bebemos","beben"], BEBIDA),
 "kjøper":  ("kjøpe","comprar",["compro","comprás","compra","compra","compramos","compran"], COSAS),
 "ser":     ("se","ver",    ["veo","ves","ve","ve","vemos","ven"], COSAS+list(ANIM)+["by","gate","hotell"]),
 "har":     ("ha","tener",  ["tengo","tenés","tiene","tiene","tenemos","tienen"], COSAS+list(ANIM)),
 "tar":     ("ta","tomar",  ["tomo","tomás","toma","toma","tomamos","toman"], ["tog","bil","fly","bok","billett","eple"]),
 "finner":  ("finne","encontrar",["encuentro","encontrás","encuentra","encuentra","encontramos","encuentran"], COSAS+["toalett","hotell","gate","penger"]),
 "åpner":   ("åpne","abrir", ["abro","abrís","abre","abre","abrimos","abren"], ["bok","hus","bil","øye","toalett"]),
 "lukker":  ("lukke","cerrar",["cierro","cerrás","cierra","cierra","cerramos","cierran"], ["bok","hus","bil","øye"]),
 "betaler": ("betale","pagar",["pago","pagás","paga","paga","pagamos","pagan"], ["billett","bil","hotell","bok","fisk","ost","mat"]),
 "trenger": ("trenge","necesitar",["necesito","necesitás","necesita","necesita","necesitamos","necesitan"], COSAS+["vann","melk","mat","penger","tid"]),
 "hører":   ("høre","oír",  ["oigo","oís","oye","oye","oímos","oyen"], ["hund","katt","barn","tog","fly","mann","kvinne"]),
 "skjønner":("skjønne","entender",["entiendo","entendés","entiende","entiende","entendemos","entienden"], ["bok","mann","kvinne","barn","telefon"]),
 "leser":   ("lese","leer",  ["leo","leés","lee","lee","leemos","leen"], ["bok","telefon"]),
 "skriver": ("skrive","escribir",["escribo","escribís","escribe","escribe","escribimos","escriben"], ["bok","telefon"]),
 "husker":  ("huske","recordar",["recuerdo","recordás","recuerda","recuerda","recordamos","recuerdan"], ["mann","kvinne","barn","by","gate","dag","natt"]),
 "glemmer": ("glemme","olvidar",["olvido","olvidás","olvida","olvida","olvidamos","olvidan"], ["bok","billett","telefon","jobb","dag"]),
 "forstår": ("forstå","entender",["entiendo","entendés","entiende","entiende","entendemos","entienden"], ["bok","mann","kvinne","barn"]),
}
VI = {
 "kommer": ("komme","venir", ["vengo","venís","viene","viene","venimos","vienen"]),
 "går":    ("gå","ir",       ["camino","caminás","camina","camina","caminamos","caminan"]),
 "reiser": ("reise","viajar",["viajo","viajás","viaja","viaja","viajamos","viajan"]),
 "bor":    ("bo","vivir",    ["vivo","vivís","vive","vive","vivimos","viven"]),
 "jobber": ("jobbe","trabajar",["trabajo","trabajás","trabaja","trabaja","trabajamos","trabajan"]),
 "sover":  ("sove","dormir",  ["duermo","dormís","duerme","duerme","dormimos","duermen"]),
 "venter": ("vente","esperar",["espero","esperás","espera","espera","esperamos","esperan"]),
}
MOD = {
 "vil": ["quiero","querés","quiere","quiere","queremos","quieren"],
 "kan": ["puedo","podés","puede","puede","podemos","pueden"],
 "må":  ["tengo que","tenés que","tiene que","tiene que","tenemos que","tienen que"],
}
MOD_NEG = {
 "vil": ["no quiero","no querés","no quiere","no quiere","no queremos","no quieren"],
 "kan": ["no puedo","no podés","no puede","no puede","no podemos","no pueden"],
 "må":  ["no debo","no debés","no debe","no debe","no debemos","no deben"],
}
ADJ = [("ny","nytt","nuevo","nueva"),("god","godt","bueno","buena"),("stor","stort","grande","grande"),
       ("liten","lite","pequeño","pequeña"),("gammel","gammelt","viejo","vieja"),
       ("varm","varmt","caliente","caliente"),("kald","kaldt","frío","fría")]
ADV = [("i dag","hoy",2),("i natt","esta noche",3),("nå","ahora",2),("her","acá",2),("der","allá",2)]
LG  = [("norsk","noruego"),("engelsk","inglés")]
CUERPO = {"hånd","fot","øye","munn"}
SOLO_PLURAL = {"penger"}          # no tiene singular: ni artículo ni adjetivo en singular
NO_TAM  = {"dag","natt","år","melk","vann","kjøtt"}
NO_TEMP = ANIM | {"år","bok","billett","ting","by","gate","fly","tog","toalett","hotell"}
COMIDA_N = {"melk","vann","kjøtt","brød","ost","fisk","egg","eple"}

def cap(t):
    i = 1 if t[0] == "¿" else 0
    return t[:i] + t[i].upper() + t[i+1:]

def generar(vocab):
    """vocab: set de palabras permitidas. Devuelve [(no, es, tpl)]"""
    out = []
    # forma de superficie -> palabra de la lista
    FORMA = {}
    for n in N:
        FORMA[n[0]] = n[0]; FORMA[n[2]] = n[0]
        if n[0] in PLURAL: FORMA[PLURAL[n[0]][0]] = n[0]
    for a in ADJ:
        FORMA[a[0]] = a[0]; FORMA[a[1]] = a[0]
        FORMA["lille" if a[0]=="liten" else ("gamle" if a[0]=="gammel" else a[0]+"e")] = a[0]
    for v,(inf,ines,esf,objs) in VT.items():
        FORMA[v] = v; FORMA[inf] = v
    for v,(inf,ines,esf) in VI.items():
        FORMA[v] = v; FORMA[inf] = v
    def base(t):
        return FORMA.get(t, t)
    EXTRA_OK = {"vær","så","snill","morgen","ha","for","takk","hei","ja","nei",
                "unnskyld","beklager","god","det","hjelpe","meg"}
    def add(no, es, tpl):
        toks = no.lower().replace("?","").replace(",","").split()
        if all(base(t) in vocab or t in EXTRA_OK for t in toks):
            out.append((cap(no), cap(es), tpl))
    def obj(n, verbo, definido=True):
        t = n[5] if definido else n[4]
        if n[0] in ANIM and verbo not in ("har","liker"):
            return "al "+t[3:] if t.startswith("el ") else "a "+t
        return t
    def suj_nom(n):
        return n[2], n[5]                      # mannen / el hombre

    nombres = [n for n in N if n[0] in vocab]
    adjs    = [a for a in ADJ if a[0] in vocab]
    advs    = [a for a in ADV if all(x in vocab for x in a[0].split())]
    vts     = {k:v for k,v in VT.items() if k in vocab}
    vis     = {k:v for k,v in VI.items() if k in vocab}
    mods    = {k:v for k,v in MOD.items() if k in vocab}

    # ---------- sujeto pronominal ----------
    for pi,(pno,pes) in enumerate(P):
        for v,(inf,ines,esf,objs) in vts.items():
            for o in objs:
                if o not in NX or o not in vocab: continue
                n = NX[o]
                add(f"{pno} {v} {n[2]}", f"{pes} {esf[pi]} {obj(n,v)}", 0)
                if not n[6]: add(f"{pno} {v} {n[1]} {n[0]}", f"{pes} {esf[pi]} {obj(n,v,False)}", 1)
                add(f"{pno} {v} ikke {n[2]}", f"{pes} no {esf[pi]} {obj(n,v)}", 2)
        for m,mes in mods.items():
            for v,(inf,ines,esf,objs) in vts.items():
                if (m,v) in (("kan","trenger"),("må","trenger"),("kan","har"),("må","har"),
                             ("kan","hører"),("må","hører")): continue
                for o in objs:
                    if o not in NX or o not in vocab: continue
                    n = NX[o]
                    es3 = f"{pes} {mes[pi]} {obj(n,v)}" if (m,inf)==("vil","ha") else f"{pes} {mes[pi]} {ines} {obj(n,v)}"
                    add(f"{pno} {m} {inf} {n[2]}", es3, 3)
                    add(f"{pno} {m} ikke {inf} {n[2]}", f"{pes} {MOD_NEG[m][pi]} {ines} {obj(n,v)}", 4)
        for v,(inf,ines,esf) in vis.items():
            for a,aes,_ in advs:
                if v in ("kommer","reiser") and a in ("her","der"): continue
                if v == "bor" and a in ("i dag","i natt","nå"): continue
                add(f"{pno} {v} {a}", f"{pes} {esf[pi]} {aes}", 5)
        if "snakker" in vocab:
            for lg,lges in LG:
                if lg not in vocab: continue
                yo = {0:"yo hablo",1:"vos hablás",2:"él habla",3:"ella habla",4:"nosotros hablamos",5:"ellos hablan"}[pi]
                add(f"{pno} snakker {lg}", f"{yo} {lges}", 6)
                add(f"{pno} snakker ikke {lg}", yo.replace("hab","no hab",1) if False else
                    {0:"yo no hablo",1:"vos no hablás",2:"él no habla",3:"ella no habla",4:"nosotros no hablamos",5:"ellos no hablan"}[pi]+" "+lges, 6)
        if "liker" in vocab:
            for o in COMIDA+["bil","bok","by","hus","katt","hund","melk","vann"]:
                if o not in NX or o not in vocab: continue
                n = NX[o]
                g = ["a mí me","a vos te","a él le","a ella le","a nosotros nos","a ellos les"][pi]
                add(f"{pno} liker {n[2]}", f"{g} gusta {n[5]}", 7)

    # ---------- adjetivo predicativo ----------
    for n in nombres:
        if n[0] in SOLO_PLURAL: continue
        for a in adjs:
            if a[0] in ("stor","liten") and n[0] in NO_TAM: continue
            if a[0] in ("varm","kald") and n[0] in NO_TEMP: continue
            if a[0] in ("ny","gammel") and n[0] in {"vann"}|ANIM: continue
            if a[0] == "god" and n[0] == "år": continue
            adj  = a[1] if n[1]=="et" else a[0]
            ades = a[2] if n[3]=="m" else a[3]
            cop  = "está" if (a[0] in ("varm","kald") or (a[0]=="gammel" and n[0] in COMIDA_N)) else "es"
            add(f"{n[2]} er {adj}", f"{n[5]} {cop} {ades}", 8)
            dem = "denne" if n[1]=="en" else "dette"
            if dem in vocab:
                add(f"{dem} {n[2]} er {adj}", f"{'este' if n[3]=='m' else 'esta'} {n[5].split(' ',1)[1]} {cop} {ades}", 9)
            if "er" in vocab:   # T21 pregunta sí/no con er
                add(f"er {n[2]} {adj}?", f"¿{n[5]} {cop} {ades}?", 21)

    # ---------- preguntas fijas ----------
    COMPRABLE = {"bil","bok","billett","ting","hus","eple","brød","ost","fisk","egg","katt","hund"}
    for n in nombres:
        if n[0] in CUERPO: continue
        add(f"hvor er {n[2]}?", f"¿dónde está {n[5]}?", 10)
        if not n[6] and n[0] in COMPRABLE:
            add(f"hvor mye koster {n[2]}?", f"¿cuánto cuesta {n[5]}?", 11)
            add(f"kan jeg kjøpe {n[1]} {n[0]}?", f"¿puedo comprar {n[4]}?", 13)
            add(f"har du {n[1]} {n[0]}?", f"¿tenés {n[4]}?", 12)

    # ---------- NUEVAS: sujeto nominal ----------
    for s in nombres:
        if s[0] not in ANIM: continue
        ssuj, ses = suj_nom(s)
        for v,(inf,ines,esf,objs) in vts.items():
            for o in objs:
                if o not in NX or o not in vocab or o == s[0]: continue
                n = NX[o]
                add(f"{ssuj} {v} {n[2]}", f"{ses} {esf[2]} {obj(n,v)}", 14)
                if not n[6]: add(f"{ssuj} {v} {n[1]} {n[0]}", f"{ses} {esf[2]} {obj(n,v,False)}", 15)
                add(f"{ssuj} {v} ikke {n[2]}", f"{ses} no {esf[2]} {obj(n,v)}", 14)
    # sujeto nominal intransitivo (cualquier sustantivo que se mueva)
    for s in nombres:
        if s[0] not in ANIM|{"tog","fly","bil"}: continue
        ssuj, ses = suj_nom(s)
        for v,(inf,ines,esf) in vis.items():
            if v=="bor" and s[0] not in ANIM: continue
            for a,aes,_ in advs:
                if v in ("kommer","reiser") and a in ("her","der"): continue
                if v=="bor" and a in ("i dag","i natt","nå"): continue
                add(f"{ssuj} {v} {a}", f"{ses} {esf[2]} {aes}", 16)

    # ---------- NUEVAS: coordinación ----------
    if "og" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for v1,(i1,e1,f1,o1) in vts.items():
                for v2,(i2,e2,f2,o2) in vts.items():
                    if v1>=v2: continue
                    for a in o1[:3]:
                        for b in o2[:3]:
                            if a not in vocab or b not in vocab or a==b: continue
                            na,nb = NX[a],NX[b]
                            add(f"{pno} {v1} {na[2]} og {v2} {nb[2]}",
                                f"{pes} {f1[pi]} {obj(na,v1)} y {f2[pi]} {obj(nb,v2)}", 17)
    if "men" in vocab and "kan" in vocab and "vil" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for v,(inf,ines,esf,objs) in vts.items():
                for o in objs[:4]:
                    if o not in vocab: continue
                    n = NX[o]
                    add(f"{pno} vil {inf} {n[2]} men {pno} kan ikke",
                        f"{pes} {MOD['vil'][pi]} {ines} {obj(n,v)} pero no {MOD['kan'][pi]}", 18)
    if "eller" in vocab and "vil" in vocab and "har" in vocab:
        for a_ in COMIDA+["melk","vann","bok","bil"]:
            for b_ in COMIDA+["melk","vann","bok","bil"]:
                if a_>=b_ or a_ not in vocab or b_ not in vocab: continue
                na,nb = NX[a_],NX[b_]
                add(f"vil du ha {na[2]} eller {nb[2]}?", f"¿querés {na[5]} o {nb[5]}?", 27)

    # ---------- NUEVAS: inversión V2 ----------
    for a,aes,_ in advs:
        for pi,(pno,pes) in enumerate(P):
            for v,(inf,ines,esf,objs) in vts.items():
                for o in objs[:4]:
                    if o not in vocab: continue
                    n = NX[o]
                    add(f"{a} {v} {pno} {n[2]}", f"{aes} {pes} {esf[pi]} {obj(n,v)}", 19)
            for v,(inf,ines,esf) in vis.items():
                if v in ("kommer","reiser") and a in ("her","der"): continue
                if v=="bor" and a in ("i dag","i natt","nå"): continue
                add(f"{a} {v} {pno}", f"{aes} {pes} {esf[pi]}", 19)

    # ---------- NUEVAS: preguntas sí/no y de pregunta ----------
    for pi,(pno,pes) in enumerate(P):
        for v,(inf,ines,esf,objs) in vts.items():
            for o in objs[:5]:
                if o not in vocab: continue
                n = NX[o]
                add(f"{v} {pno} {n[2]}?", f"¿{pes} {esf[pi]} {obj(n,v)}?", 20)
            if "hva" in vocab:
                add(f"hva {v} {pno}?", f"¿qué {esf[pi]} {pes}?", 23)
    if "når" in vocab:
        for s in [n for n in nombres if n[0] in ANIM|{"tog","fly","bil"}]:
            for v,(inf,ines,esf) in vis.items():
                if v=="bor": continue
                add(f"når {v} {s[2]}?", f"¿cuándo {esf[2]} {s[5]}?", 22)

    # ---------- NUEVAS: lugar ----------
    ESTAR = ["estoy","estás","está","está","estamos","están"]
    VIVIR = ["vivo","vivís","vive","vive","vivimos","viven"]
    for prep,pes_prep in [("i","en"),("på","en")]:
        if prep not in vocab: continue
        for s in [("jeg","yo",0),("du","vos",1),("han","él",2),("hun","ella",3),("vi","nosotros",4),("de","ellos",5)]:
            for o in LUGAR:
                if o not in vocab: continue
                n = NX[o]
                if prep=="i" and o not in ("hus","by","bil","tog","fly"): continue
                if prep=="på" and o not in ("hotell","toalett","tog","fly","gate"): continue
                if "er" in vocab:
                    add(f"{s[0]} er {prep} {n[2]}", f"{s[1]} {ESTAR[s[2]]} {pes_prep} {n[5]}", 25)
                if "bor" in vocab and o in ("hus","by"):
                    add(f"{s[0]} bor {prep} {n[2]}", f"{s[1]} {VIVIR[s[2]]} {pes_prep} {n[5]}", 25)

    # ---------- NUEVAS: presentativo ----------
    if "det" in vocab and "er" in vocab:
        ABSTRACTO = {"år","dag","natt","tid","ting"}
        for n in nombres:
            if n[6] or n[0] in CUERPO or n[0] in ABSTRACTO: continue
            for a,aes,_ in advs:
                if a not in ("her","der"): continue
                add(f"det er {n[1]} {n[0]} {a}", f"hay {n[4]} {aes}", 26)
    # ---------- pregunta sí/no con intransitivo ----------
    for pi,(pno,pes) in enumerate(P):
        for v,(inf,ines,esf) in vis.items():
            add(f"{v} {pno}?", f"¿{pes} {esf[pi]}?", 34)
        if "snakker" in vocab:
            add(f"{pno} snakker ikke", {0:"yo no hablo",1:"vos no hablás",2:"él no habla",
                3:"ella no habla",4:"nosotros no hablamos",5:"ellos no hablan"}[pi], 35)
            add(f"snakker {pno}?", {0:"¿yo hablo?",1:"¿vos hablás?",2:"¿él habla?",
                3:"¿ella habla?",4:"¿nosotros hablamos?",5:"¿ellos hablan?"}[pi], 34)

    # ---------- til / fra con movimiento ----------
    DEST = ["by","hotell","hus","gate","flyplass","toalett"]
    for prep,pes_prep,verbos in [("til","a",["går","reiser","kommer"]),("fra","de",["kommer","reiser"])]:
        if prep not in vocab: continue
        for pi,(pno,pes) in enumerate(P):
            for v in verbos:
                if v not in vis: continue
                esf = vis[v][2]
                for o in DEST:
                    if o not in vocab or o not in NX: continue
                    add(f"{pno} {v} {prep} {NX[o][2]}", f"{pes} {esf[pi]} {pes_prep} {NX[o][5]}", 28)

    # ---------- med: medio de transporte y compañía ----------
    if "med" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for v in ("reiser","kommer"):
                if v not in vis: continue
                esf = vis[v][2]
                for o in ("tog","bil","fly"):
                    if o not in vocab: continue
                    add(f"{pno} {v} med {NX[o][2]}", f"{pes} {esf[pi]} en {NX[o][5]}", 29)

    # ---------- meg / deg ----------
    OBJ_PERS = [("meg","me","a mí"),("deg","te","a vos")]
    for op,cl,fuerte in OBJ_PERS:
        if op not in vocab: continue
        for pi,(pno,pes) in enumerate(P):
            if (pno,op) in (("jeg","meg"),("vi","meg"),("du","deg")): continue
            for v,es3 in (("ser","ve"),("hører","oye"),("hjelper","ayuda"),("forstår","entiende")):
                if v not in vocab: continue
                conj = {"ser":["veo","ves","ve","ve","vemos","ven"],
                        "hører":["oigo","oís","oye","oye","oímos","oyen"],
                        "hjelper":["ayudo","ayudás","ayuda","ayuda","ayudamos","ayudan"],
                        "forstår":["entiendo","entendés","entiende","entiende","entendemos","entienden"]}[v]
                add(f"{pno} {v} {op}", f"{pes} {cl} {conj[pi]}", 30)
                if "kan" in vocab:
                    inf = {"ser":"se","hører":"høre","hjelper":"hjelpe","forstår":"forstå"}[v]
                    infes = {"ser":"ver","hører":"oír","hjelper":"ayudar","forstår":"entender"}[v]
                    add(f"kan {pno} {inf} {op}?", f"¿{pes} {cl} {MOD['kan'][pi]} {infes}?", 30)
        if "gir" in vocab:
            for pi,(pno,pes) in enumerate(P):
                if (pno,op) in (("jeg","meg"),("vi","meg"),("du","deg")): continue
                for o in ("bok","billett","eple","penger","melk"):
                    if o not in vocab: continue
                    d = ["doy","das","da","da","damos","dan"][pi]
                    add(f"{pno} gir {op} {NX[o][2]}", f"{pes} {cl} {d} {NX[o][5]}", 31)

    # ---------- vet / sier / gjør / heter ----------
    if "det" in vocab:
        for pi,(pno,pes) in enumerate(P):
            if "vet" in vocab:
                add(f"{pno} vet det", f"{pes} {['sé','sabés','sabe','sabe','sabemos','saben'][pi]} eso", 32)
                add(f"{pno} vet ikke", f"{pes} no {['sé','sabés','sabe','sabe','sabemos','saben'][pi]}", 32)
            if "sier" in vocab:
                add(f"{pno} sier det", f"{pes} {['digo','decís','dice','dice','decimos','dicen'][pi]} eso", 32)
    if "hva" in vocab:
        for pi,(pno,pes) in enumerate(P):
            if "gjør" in vocab: add(f"hva gjør {pno}?", f"¿qué {['hago','hacés','hace','hace','hacemos','hacen'][pi]} {pes}?", 32)
            if "sier" in vocab: add(f"hva sier {pno}?", f"¿qué {['digo','decís','dice','dice','decimos','dicen'][pi]} {pes}?", 32)
            if "heter" in vocab: add(f"hva heter {pno}?", f"¿cómo {['me llamo','te llamás','se llama','se llama','nos llamamos','se llaman'][pi]} {pes}?", 32)

    # ---------- venstre / høyre ----------
    if "til" in vocab:
        for lado,les in (("høyre","a la derecha"),("venstre","a la izquierda")):
            if lado not in vocab: continue
            for o in ("toalett","hotell","gate","tog","hus","bil"):
                if o not in vocab: continue
                add(f"{NX[o][2]} er til {lado}", f"{NX[o][5]} está {les}", 33)

    # ---------- cortesía dentro de la frase ----------
    CORT = lambda w: w in vocab
    # petición + por favor
    if "vær så snill" in vocab and "vil" in vocab:
        for pi,(pno,pes) in enumerate(P):
            if pno not in ("jeg","vi"): continue
            for o in COMIDA+["melk","vann","billett","bok","bil","mat"]:
                if o not in vocab or o not in NX: continue
                n = NX[o]
                art = f"{n[1]} {n[0]}" if not n[6] else n[2]
                cual = n[4] if not n[6] else n[5]
                add(f"{pno} vil ha {art}, vær så snill", f"{pes} {MOD['vil'][pi]} {cual}, por favor", 36)
        if "kan" in vocab and "meg" in vocab and "hjelper" in vocab:
            add("kan du hjelpe meg, vær så snill?", "¿me podés ayudar, por favor?", 36)
    # disculpa por no poder
    if CORT("beklager"):
        for pi,(pno,pes) in enumerate(P):
            for v,(inf,ines,esf) in vis.items():
                for a,aes,_ in advs:
                    if a not in ("i dag","i natt","nå"): continue
                    if v=="bor": continue
                    add(f"{pno} {v} ikke {a}, beklager", f"{pes} no {esf[pi]} {aes}, lo siento", 38)
            if "forstår" in vocab:
                add(f"{pno} forstår ikke, beklager",
                    f"{pes} no {['entiendo','entendés','entiende','entiende','entendemos','entienden'][pi]}, lo siento", 38)
    # disculpe para abrir
    if CORT("unnskyld"):
        for n in [x for x in nombres if x[0] not in CUERPO]:
            add(f"unnskyld, hvor er {n[2]}?", f"disculpe, ¿dónde está {n[5]}?", 37)
        if "hva" in vocab and "dette" in vocab:
            add("unnskyld, hva er dette?", "disculpe, ¿qué es esto?", 37)
    # saludo para abrir
    if CORT("hei"):
        COMPRABLE2 = {"bil","bok","billett","hus","katt","hund","eple","brød","ost","fisk"}
        for n in nombres:
            if n[0] in CUERPO: continue
            if "har" in vocab and not n[6] and n[0] in COMPRABLE2:
                add(f"hei, har du {n[1]} {n[0]}?", f"hola, ¿tenés {n[4]}?", 39)
            if "hvor" in vocab:
                add(f"hei, hvor er {n[2]}?", f"hola, ¿dónde está {n[5]}?", 39)
    # respuestas sí/no
    if CORT("ja") and CORT("nei"):
        for o in ["bil","bok","katt","hund","hus","billett","eple","brød"]:
            if o not in vocab or o not in NX: continue
            n = NX[o]
            if "har" in vocab:
                add(f"ja, jeg har {n[1]} {n[0]}", f"sí, tengo {n[4]}", 40)
                add(f"nei, jeg har ikke {n[1]} {n[0]}", f"no, no tengo {n[4]}", 40)
        if CORT("takk"):
            add("ja takk", "sí, gracias", 40)
            add("nei takk", "no, gracias", 40)
    # cierre
    if CORT("takk"):
        for o in ["bok","billett","eple","melk","mat"]:
            if o not in vocab or o not in NX: continue
            add(f"takk for {NX[o][2]}", f"gracias por {NX[o][5]}", 41)
        if "ha det" in vocab:
            add("takk, ha det", "gracias, chau", 41)
    if "god morgen" in vocab:
        for pi,(pno,pes) in enumerate(P):
            if pno in ("jeg","vi"): continue
            if "kommer" in vis and "i" in vocab and "dag" in vocab:
                add(f"god morgen, kommer {pno} i dag?", f"buen día, ¿{pes} {vis['kommer'][2][pi]} hoy?", 42)

    # ================= RONDA 1: estructuras que faltaban =================
    # adjetivo atributivo indefinido: "en stor bil" / "et stort hus"
    for pi,(pno,pes) in enumerate(P):
        for v,(inf,ines,esf,objs) in vts.items():
            for o in objs:
                if o not in NX or o not in vocab: continue
                n = NX[o]
                if n[6]: continue
                if o in ANIM and v in ("har","liker","kjøper","betaler"): continue
                for a in adjs:
                    if a[0] in ("stor","liten") and n[0] in NO_TAM: continue
                    if a[0] in ("varm","kald") and n[0] in NO_TEMP: continue
                    if a[0] in ("ny","gammel") and n[0] in {"vann"}|ANIM: continue
                    adj  = a[1] if n[1]=="et" else a[0]
                    ades = a[2] if n[3]=="m" else a[3]
                    art_es = n[4].split(" ",1)[0]
                    add(f"{pno} {v} {n[1]} {adj} {n[0]}",
                        f"{pes} {esf[pi]} {art_es} {n[4].split(' ',1)[1]} {ades}", 43)
    # atributivo con demostrativo: la forma en -e
    for n in nombres:
        if n[0] in SOLO_PLURAL: continue
        dem = "denne" if n[1]=="en" else "dette"
        if dem not in vocab: continue
        for a in adjs:
            if a[0] in ("stor","liten") and n[0] in NO_TAM: continue
            if a[0] in ("varm","kald") and n[0] in NO_TEMP: continue
            if a[0] in ("ny","gammel") and n[0] in {"vann"}|ANIM: continue
            forma_e = "lille" if a[0]=="liten" else ("gamle" if a[0]=="gammel" else a[0]+"e")
            ades = a[2] if n[3]=="m" else a[3]
            det = "este" if n[3]=="m" else "esta"
            if a[0] != "god":
                otro = "godt" if n[1]=="et" else "god"
                otro_es = "bueno" if n[3]=="m" else "buena"
            else:
                otro = "stort" if n[1]=="et" else "stor"
                otro_es = "grande"
            cop = "es"
            add(f"{dem} {forma_e} {n[2]} er {otro}",
                f"{det} {n[5].split(' ',1)[1]} {ades} {cop} {otro_es}", 44)
    # plural desnudo
    for pi,(pno,pes) in enumerate(P):
        for v in ("liker","ser","kjøper","spiser","hører"):
            if v not in vts: continue
            esf = vts[v][2]
            for o,(pl,ples) in PLURAL.items():
                if o not in vocab or o not in NX: continue
                if pl == o: continue          # plural invariable: sería ambiguo
                if o not in vts[v][3]: continue
                if v=="liker":
                    g = ["a mí me","a vos te","a él le","a ella le","a nosotros nos","a ellos les"][pi]
                    add(f"{pno} liker {pl}", f"{g} gustan los {ples}" if True else "", 45)
                else:
                    add(f"{pno} {v} {pl}", f"{pes} {esf[pi]} {ples}", 45)
    if "det" in vocab and "er" in vocab:
        for o,(pl,ples) in PLURAL.items():
            if o not in vocab or pl == o: continue
            for a,aes,_ in advs:
                if a not in ("her","der"): continue
                add(f"det er {pl} {a}", f"hay {ples} {aes}", 45)
    # imperativo
    IMP = {"spise":"spis","drikke":"drikk","komme":"kom","se":"se","ta":"ta","gå":"gå",
           "kjøpe":"kjøp","lukke":"lukk","betale":"betal","hjelpe":"hjelp","åpne":"åpne","høre":"hør"}
    IMPES = {"spis":"comé","drikk":"tomá","kom":"vení","se":"mirá","ta":"tomá","gå":"andá",
             "kjøp":"comprá","lukk":"cerrá","betal":"pagá","hjelp":"ayudá","åpne":"abrí","hør":"escuchá"}
    for v,(inf,ines,esf,objs) in vts.items():
        if inf not in IMP: continue
        im = IMP[inf]
        for o in objs:
            if o not in NX or o not in vocab: continue
            add(f"{im} {NX[o][2]}", f"{IMPES[im]} {NX[o][5]}", 46)
    for a,aes,_ in advs:
        for inf in ("komme","se","gå"):
            if inf not in [t[0] for t in vis.values()] and inf not in [t[0] for t in vts.values()]: continue
            if a in ("i dag","i natt") and inf=="se": continue
            add(f"{IMP[inf]} {a}", f"{IMPES[IMP[inf]]} {aes}", 46)
    # identificación con det
    if "det" in vocab and "er" in vocab:
        for n in nombres:
            if n[6] or n[0] in CUERPO: continue
            add(f"det er {n[1]} {n[0]}", f"es {n[4]}", 47)
            add(f"det er ikke {n[1]} {n[0]}", f"no es {n[4]}", 47)
        if "hva" in vocab: add("hva er det?", "¿qué es eso?", 47)
    # subordinada: el verbo se va al final
    if "vet" in vocab and "hvor" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for n in nombres:
                if n[0] in CUERPO: continue
                add(f"{pno} vet ikke hvor {n[2]} er",
                    f"{pes} no {['sé','sabés','sabe','sabe','sabemos','saben'][pi]} dónde está {n[5]}", 49)

    # ================= RONDA 2: cierre de huérfanas y frases largas =================
    # dos cláusulas con sujetos distintos
    if "men" in vocab:
        for i1,(p1,e1) in enumerate(P):
            for i2,(p2,e2) in enumerate(P):
                if i1 == i2: continue
                for v1 in ("spiser","drikker","kjøper","ser"):
                    for v2 in ("spiser","drikker","kjøper","ser"):
                        if v1 == v2 or v1 not in vts or v2 not in vts: continue
                        for o1 in vts[v1][3][:2]:
                            for o2 in vts[v2][3][:2]:
                                if o1 not in vocab or o2 not in vocab or o1 == o2: continue
                                n1, n2 = NX[o1], NX[o2]
                                add(f"{p1} {v1} {n1[2]}, men {p2} {v2} ikke {n2[2]}",
                                    f"{e1} {vts[v1][2][i1]} {n1[5]}, pero {e2} no {vts[v2][2][i2]} {n2[5]}", 50)
    # partes del cuerpo con imperativo y con posesión
    for parte,pes_parte in (("munn","la boca"),("øye","el ojo"),("hånd","la mano")):
        if parte not in vocab: continue
        if "åpner" in vts: add(f"åpne {NX[parte][2]}", f"abrí {pes_parte}", 46)
        if "lukker" in vts: add(f"lukk {NX[parte][2]}", f"cerrá {pes_parte}", 46)
        for pi,(pno,pes) in enumerate(P):
            if "har" in vts:
                add(f"{pno} har en {parte}" if NX[parte][1]=="en" else f"{pno} har et {parte}",
                    f"{pes} {vts['har'][2][pi]} {NX[parte][4]}", 0)
    # do y flyplass
    if "do" in vocab and "hvor" in vocab: add("hvor er do?", "¿dónde está el baño?", 37)
    if "flyplass" in vocab:
        for pi,(pno,pes) in enumerate(P):
            if "på" in vocab and "er" in vocab:
                add(f"{pno} er på flyplassen", f"{pes} {['estoy','estás','está','está','estamos','están'][pi]} en el aeropuerto", 25)
            if "til" in vocab and "reiser" in vis:
                add(f"{pno} reiser til flyplassen", f"{pes} {vis['reiser'][2][pi]} al aeropuerto", 28)
    # tusen takk y vær så god, que necesitan un interlocutor
    if "tusen takk" in vocab:
        for o in ("mat","bok","billett","melk","hjelp"):
            if o in NX and o in vocab: add(f"tusen takk for {NX[o][2]}", f"muchas gracias por {NX[o][5]}", 41)
    if "vær så god" in vocab:
        for o in ("billett","bok","eple","melk","mat"):
            if o not in NX or o not in vocab: continue
            add(f"vær så god, her er {NX[o][2]}", f"aquí tiene, acá está {NX[o][5]}", 41)
    # snakker du engelsk? después de no entender
    if "snakker du engelsk?" in vocab and "forstår" in vts:
        for pi,(pno,pes) in enumerate(P):
            if pno != "jeg": continue
            add("jeg forstår ikke, snakker du engelsk?", "no entiendo, ¿hablás inglés?", 53)
            if "norsk" in vocab:
                add("jeg snakker ikke norsk, snakker du engelsk?", "no hablo noruego, ¿hablás inglés?", 53)

    # ================= NIVEL 4: pasado, posesivos, cantidad, subordinadas =================
    PAS = {"spiser":"spiste","drikker":"drakk","kjøper":"kjøpte","ser":"så","tar":"tok",
           "finner":"fant","betaler":"betalte","hører":"hørte","leser":"leste","skriver":"skrev",
           "husker":"husket","glemmer":"glemte"}
    PAS_ES = {"spiser":["comí","comiste","comió","comió","comimos","comieron"],
              "drikker":["bebí","bebiste","bebió","bebió","bebimos","bebieron"],
              "kjøper":["compré","compraste","compró","compró","compramos","compraron"],
              "ser":["vi","viste","vio","vio","vimos","vieron"],
              "tar":["tomé","tomaste","tomó","tomó","tomamos","tomaron"],
              "finner":["encontré","encontraste","encontró","encontró","encontramos","encontraron"],
              "betaler":["pagué","pagaste","pagó","pagó","pagamos","pagaron"],
              "hører":["oí","oíste","oyó","oyó","oímos","oyeron"],
              "leser":["leí","leíste","leyó","leyó","leímos","leyeron"],
              "skriver":["escribí","escribiste","escribió","escribió","escribimos","escribieron"],
              "husker":["recordé","recordaste","recordó","recordó","recordamos","recordaron"],
              "glemmer":["olvidé","olvidaste","olvidó","olvidó","olvidamos","olvidaron"]}
    ERA = ["era","eras","era","era","éramos","eran"]
    TUVE = ["tenía","tenías","tenía","tenía","teníamos","tenían"]
    # pasado con var y hadde
    if "var" in vocab:
        for n in nombres:
            if n[0] in CUERPO or n[0] in SOLO_PLURAL: continue
            for a in adjs:
                if a[0] in ("stor","liten") and n[0] in NO_TAM: continue
                if a[0] in ("varm","kald") and n[0] in NO_TEMP: continue
                if a[0] in ("ny","gammel") and n[0] in {"vann"}|ANIM: continue
                adj  = a[1] if n[1]=="et" else a[0]
                ades = a[2] if n[3]=="m" else a[3]
                cop  = "estaba" if (a[0] in ("varm","kald") or (a[0]=="gammel" and n[0] in COMIDA_N)) else "era"
                add(f"{n[2]} var {adj}", f"{n[5]} {cop} {ades}", 60)
        for pi,(pno,pes) in enumerate(P):
            for a,aes,_ in advs:
                if a not in ("her","der"): continue
                add(f"{pno} var {a}", f"{pes} {ERA[pi]} {aes}"if False else f"{pes} estuvo {aes}" if pi in (2,3) else f"{pes} estuve {aes}" if pi==0 else f"{pes} estuviste {aes}" if pi==1 else f"{pes} estuvimos {aes}" if pi==4 else f"{pes} estuvieron {aes}", 60)
    if "hadde" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for o in ["bil","bok","katt","hund","hus","billett","jobb","telefon","kaffe"]:
                if o not in vocab or o not in NX: continue
                n = NX[o]
                art = n[2] if n[6] else f"{n[1]} {n[0]}"
                cual = n[5] if n[6] else n[4]
                add(f"{pno} hadde {art}", f"{pes} {TUVE[pi]} {cual}", 61)
    # verbos en pasado
    for pi,(pno,pes) in enumerate(P):
        for v,pas in PAS.items():
            if v not in vts or "var" not in vocab: continue
            for o in vts[v][3][:4]:
                if o not in vocab or o not in NX: continue
                n = NX[o]
                add(f"{pno} {pas} {n[2]}", f"{pes} {PAS_ES[v][pi]} {obj(n,v)}", 62)
                add(f"{pno} {pas} ikke {n[2]}", f"{pes} no {PAS_ES[v][pi]} {obj(n,v)}", 62)
    # posesivos, que van detrás del sustantivo
    POS = [("min","mi","mitt"),("din","tu","ditt")]
    for pos,pes_pos,posn in POS:
        if pos not in vocab: continue
        for n in nombres:
            if n[6] or n[0] in SOLO_PLURAL: continue
            forma = posn if n[1]=="et" else pos
            add(f"{n[2]} {forma} er {'nytt' if n[1]=='et' else 'ny'}",
                f"{pes_pos} {n[5].split(' ',1)[1]} es {'nuevo' if n[3]=='m' else 'nueva'}", 63)
            for pi,(pno,pes) in enumerate(P):
                if "ser" in vts:
                    add(f"{pno} ser {n[2]} {forma}", f"{pes} {vts['ser'][2][pi]} {pes_pos} {n[5].split(' ',1)[1]}", 63)
    # cantidad
    if "mange" in vocab:
        for o,(pl,ples) in PLURAL.items():
            if o not in vocab or pl == o: continue
            add(f"det er mange {pl} her", f"hay muchos {ples} acá", 64)
            for pi,(pno,pes) in enumerate(P):
                if "ser" in vts: add(f"{pno} ser mange {pl}", f"{pes} {vts['ser'][2][pi]} muchos {ples}", 64)
    for num,nes in (("to","dos"),("tre","tres")):
        if num not in vocab: continue
        for o,(pl,ples) in PLURAL.items():
            if o not in vocab or pl == o: continue
            add(f"jeg har {num} {pl}", f"tengo {nes} {ples}", 64)
            add(f"det er {num} {pl} her", f"hay {nes} {ples} acá", 64)
    if "veldig" in vocab:
        for n in nombres:
            if n[0] in CUERPO or n[0] in SOLO_PLURAL: continue
            for a in adjs:
                if a[0] in ("stor","liten") and n[0] in NO_TAM: continue
                if a[0] in ("varm","kald") and n[0] in NO_TEMP: continue
                if a[0] in ("ny","gammel") and n[0] in {"vann"}|ANIM: continue
                adj  = a[1] if n[1]=="et" else a[0]
                ades = a[2] if n[3]=="m" else a[3]
                cop  = "está" if a[0] in ("varm","kald") else "es"
                add(f"{n[2]} er veldig {adj}", f"{n[5]} {cop} muy {ades}", 65)
    # subordinadas con at, fordi, hvis
    if "at" in vocab and "tror" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for n in nombres:
                if n[0] in CUERPO or n[0] in SOLO_PLURAL: continue
                for a in adjs[:3]:
                    if a[0] in ("stor","liten") and n[0] in NO_TAM: continue
                    if a[0] in ("varm","kald") and n[0] in NO_TEMP: continue
                    if a[0] in ("ny","gammel") and n[0] in {"vann"}|ANIM: continue
                    adj  = a[1] if n[1]=="et" else a[0]
                    ades = a[2] if n[3]=="m" else a[3]
                    add(f"{pno} tror at {n[2]} er {adj}",
                        f"{pes} {['creo','creés','cree','cree','creemos','creen'][pi]} que {n[5]} es {ades}", 66)
    if "fordi" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for o in ["kaffe","vann","melk"]:
                if o not in vocab or o not in NX or "drikker" not in vts: continue
                n = NX[o]
                add(f"{pno} drikker {n[2]} fordi {pno} er trøtt".replace(" trøtt"," her"),
                    f"{pes} {vts['drikker'][2][pi]} {n[5]} porque {pes} {['estoy','estás','está','está','estamos','están'][pi]} acá", 67)
    if "hvis" in vocab and "kan" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for o in ["billett","bok","kaffe","bil"]:
                if o not in vocab or o not in NX: continue
                n = NX[o]
                # la subordinada ocupa el primer lugar, así que la principal invierte
                add(f"hvis {pno} har penger, kan {pno} kjøpe {n[2]}",
                    f"si {pes} {['tengo','tenés','tiene','tiene','tenemos','tienen'][pi]} dinero, {MOD['kan'][pi]} comprar {n[5]}", 68)
    # preguntas nuevas
    if "hvorfor" in vocab:
        for pi,(pno,pes) in enumerate(P):
            for v in ("sover","jobber","venter"):
                if v not in vis: continue
                add(f"hvorfor {v} {pno}?", f"¿por qué {vis[v][2][pi]} {pes}?", 69)
    if "hvordan" in vocab:
        for n in nombres:
            if n[0] in CUERPO or n[0] in SOLO_PLURAL: continue
            add(f"hvordan er {n[2]}?", f"¿cómo es {n[5]}?", 69)
    if "hvem" in vocab:
        for v in ("spiser","kjøper","leser","skriver","husker"):
            if v not in vts: continue
            for o in vts[v][3][:3]:
                if o not in vocab or o not in NX: continue
                add(f"hvem {v} {NX[o][2]}?", f"¿quién {vts[v][2][2]} {obj(NX[o],v)}?", 69)
    # también, solo, nunca, otra vez
    for adv,aes,tpl in (("også","también",70),("bare","solo",70),("aldri","nunca",70),("igjen","otra vez",70)):
        if adv not in vocab: continue
        for pi,(pno,pes) in enumerate(P):
            for v in ("spiser","drikker","leser","jobber","sover"):
                if v in vts:
                    for o in vts[v][3][:2]:
                        if o not in vocab or o not in NX: continue
                        n = NX[o]
                        if adv == "aldri":
                            add(f"{pno} {v} aldri {n[2]}", f"{pes} nunca {vts[v][2][pi]} {obj(n,v)}", tpl)
                        elif adv == "igjen":
                            add(f"{pno} {v} {n[2]} igjen", f"{pes} {vts[v][2][pi]} {obj(n,v)} otra vez", tpl)
                        else:
                            add(f"{pno} {v} {adv} {n[2]}", f"{pes} {vts[v][2][pi]} {aes} {obj(n,v)}", tpl)
                elif v in vis:
                    add(f"{pno} {v} {adv}" if adv!="aldri" else f"{pno} {v} aldri",
                        f"{pes} {vis[v][2][pi]} {aes}" if adv!="aldri" else f"{pes} nunca {vis[v][2][pi]}", tpl)

    return out


def construir(vocab, objetivo, semilla):
    bruto = generar(vocab)
    vistos, vistos_es, uniq = set(), set(), []
    for no,es,t in bruto:
        k,ke = no.lower(), es.lower()
        if k in vistos or ke in vistos_es: continue
        vistos.add(k); vistos_es.add(ke); uniq.append((no,es,t))
    random.seed(semilla)
    por = defaultdict(list)
    for r in uniq: por[r[2]].append(r)
    for t in por: random.shuffle(por[t])
    tope = max(6, int(objetivo*0.10))       # ninguna plantilla pasa del 10%
    sel, i = [], 0
    while len(sel) < objetivo:
        movio = False
        for t in sorted(por):
            usados = sum(1 for x in sel if x[2]==t)
            if i < len(por[t]) and usados < tope:
                sel.append(por[t][i]); movio = True
                if len(sel) >= objetivo: break
        if not movio: break
        i += 1
    random.shuffle(sel)
    return uniq, sel

if __name__ == "__main__":
    V1 = set(L1)
    V2 = V1 | set(L2_ADD)
    V3 = V2 | set(L3_ADD)
    print("vocabulario: N1=%d  N2=%d  N3=%d" % (len(V1),len(V2),len(V3)))
    todo = []
    V4 = V3 | set(L4_ADD)
    for lvl,(voc,obj) in enumerate([(V1,150),(V2,300),(V3,600),(V4,400)], start=1):
        uniq, sel = construir(voc, obj, 4200+lvl)
        c = Counter(r[2] for r in sel)
        print("\n=== NIVEL %d — producibles %d, elegidas %d, plantillas vivas %d"
              % (lvl, len(uniq), len(sel), len(c)))
        print("   reparto:", dict(sorted(c.items())))
        for r in sel: todo.append((r[0], r[1], r[2], lvl))
    json.dump(todo, open("/home/claude/frases2.json","w"), ensure_ascii=False)
    print("\ntotal frases:", len(todo))
