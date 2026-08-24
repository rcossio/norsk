# -*- coding: utf-8 -*-
"""Baja una segunda voz (Google Translate) para cada texto de la app.

Uso:  python3 scripts/voz_google.py <etapa 1-5>

Se hace por etapas para no golpear el endpoint de una: es interno y no
documentado, y el uso intenso puede devolver 429 o bloquear la IP. Cada etapa
salta lo que ya existe, así que se puede repetir sin duplicar trabajo.

Salida: audio/<slug>-g.mp3, recodificado a mono 22050 Hz 48 kbps para que pese
lo mismo que las grabaciones de Piper.
"""
import os, re, subprocess, sys, time, random, urllib.parse, urllib.request

RAIZ   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETAPAS = 5
ESPERA = 0.5
UA     = ("Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/120.0.0.0 Mobile Safari/537.36")

def slug(t):
    t = t.lower().replace("å","a").replace("ø","o").replace("æ","ae")
    return re.sub(r"\s+", "-", re.sub(r"[^a-z0-9 ]", "", t).strip())

def textos():
    html = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
    out  = re.findall(r'no:"([^"]+)"', html)
    out += re.findall(r'\["([^"]+)","[^"]*",\d+,\d+\]', html)
    for m in re.finditer(r"ej:\[([^\]]*)\]", html):
        out += re.findall(r'"([^"]+)"', m.group(1))
    vistos, limpio = set(), []
    for t in out:
        if slug(t) in vistos: continue
        vistos.add(slug(t)); limpio.append(t)
    return sorted(limpio, key=slug)          # orden estable entre etapas

def bajar(texto):
    url = ("https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=no&q="
           + urllib.parse.quote(texto))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        if r.status != 200: raise RuntimeError(f"HTTP {r.status}")
        datos = r.read()
    if len(datos) < 1000: raise RuntimeError("respuesta demasiado corta")
    return datos

def main():
    etapa = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    todos = textos()
    tanda = [t for i, t in enumerate(todos) if i % ETAPAS == etapa - 1]
    destino = os.path.join(RAIZ, "audio")
    hechos = saltados = fallos = 0
    t0 = time.time()
    for t in tanda:
        salida = os.path.join(destino, slug(t) + "-g.mp3")
        if os.path.exists(salida):
            saltados += 1; continue
        try:
            datos = bajar(t)
        except Exception as e:
            fallos += 1
            print(f"  falló: {t[:40]} → {e}", flush=True)
            if fallos >= 5:
                print("cinco fallos seguidos: se corta para no insistir"); break
            time.sleep(3); continue
        open("/tmp/_g.mp3", "wb").write(datos)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/_g.mp3",
                        "-ac","1","-ar","22050","-codec:a","libmp3lame","-b:a","48k",
                        salida], check=True)
        hechos += 1
        time.sleep(ESPERA + random.uniform(0, 0.25))
    print(f"etapa {etapa}/{ETAPAS}: {hechos} nuevos, {saltados} ya estaban, "
          f"{fallos} fallos, {len(tanda)} en la tanda, {time.time()-t0:.0f} s")

if __name__ == "__main__":
    main()
