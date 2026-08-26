# -*- coding: utf-8 -*-
"""Sintetiza un mp3 por palabra, por frase y por línea de diálogo, y borra los huérfanos.

Uso:  python3 scripts/generar_audio.py
Requiere: pip install piper-tts, ffmpeg, y el modelo no_NO-talesyntese-medium.

De cada texto salen dos tomas: la normal y una `-lento` sintetizada aparte, con
comas entre palabras (Piper las convierte en pausas reales). Estirar la normal no
sirve: lo que cuesta al escuchar es segmentar, no la velocidad.

Criterios de calidad aplicados a cada toma:
  - se rechaza y se vuelve a sintetizar si hay un silencio interno > 0.30 s
    (artefacto típico del modelo: un chasquido, una pausa, y recién la palabra)
  - se recorta el silencio inicial y se deja 0.25 s de cola
  - mono 22050 Hz, mp3 48 kbps: suficiente para voz, ~7 KB por frase
"""
import json, os, re, subprocess, sys, wave
import numpy as np
from piper import PiperVoice, SynthesisConfig

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOZ  = os.environ.get("PIPER_VOICE", "voices/no.onnx")

def slug(t):
    t = t.lower().replace("å","a").replace("ø","o").replace("æ","ae")
    return re.sub(r"\s+", "-", re.sub(r"[^a-z0-9 ]", "", t).strip())

def perfil(path):
    raw = subprocess.run(["ffmpeg","-v","error","-i",path,"-f","s16le","-ac","1","-ar","22050","-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(float)/32768
    win = 441
    e = np.array([abs(x[i:i+win]).max() for i in range(0, len(x)-win, win)])
    idx = np.where(e > .02)[0]
    if len(idx) < 2: return 0, 9
    return (idx[-1]-idx[0]+1)*0.02, np.diff(idx).max()*0.02

def textos():
    html = open(os.path.join(RAIZ,"index.html"), encoding="utf-8").read()
    palabras = re.findall(r'no:"([^"]+)"', html)
    frases   = re.findall(r'\["([^"]+)","[^"]*",\d+,\d+\]', html)
    ejemplos = []
    for m in re.finditer(r'ej:\[([^\]]*)\]', html):
        ejemplos += re.findall(r'"([^"]+)"', m.group(1))
    dialogos = re.findall(r'\["[AB]","([^"]+)","[^"]*"\]', html)
    vistos, limpio = set(), []
    for t in palabras + frases + ejemplos + dialogos:
        if slug(t) in vistos: continue
        vistos.add(slug(t)); limpio.append(t)
    return limpio

FILTRO = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
          "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.25,areverse")

def codifica(wav, salida):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",wav,"-af",FILTRO,
        "-ac","1","-ar","22050","-codec:a","libmp3lame","-b:a","48k", salida], check=True)

def main():
    voz = PiperVoice.load(VOZ, config_path=VOZ + ".json")
    destino = os.path.join(RAIZ, "audio")
    os.makedirs(destino, exist_ok=True)
    usados, nuevos = set(), 0
    for t in textos():
        s = slug(t)
        usados.update([s, s + "-lento", s + "-g"])   # la voz de Google la baja voz_google.py
        out = os.path.join(destino, s + ".mp3")
        if not os.path.exists(out):
            for _ in range(6):
                with wave.open("/tmp/_p.wav","wb") as f: voz.synthesize_wav(t, f)
                neto, hueco = perfil("/tmp/_p.wav")
                if hueco <= 0.40 and neto > 0.15: break
            codifica("/tmp/_p.wav", out)
            nuevos += 1
        lento = os.path.join(destino, s + "-lento.mp3")
        if not os.path.exists(lento):
            pal = t.split()
            texto = ", ".join(pal) if len(pal) > 1 else t
            cfg = SynthesisConfig(length_scale=1.35 if len(pal) > 1 else 1.6)
            with wave.open("/tmp/_l.wav","wb") as f: voz.synthesize_wav(texto, f, syn_config=cfg)
            codifica("/tmp/_l.wav", lento)
            nuevos += 1
    borrados = 0
    for f in os.listdir(destino):
        if f.endswith(".mp3") and f[:-4] not in usados:
            os.remove(os.path.join(destino, f)); borrados += 1
    print(f"mp3 nuevos: {nuevos} | huérfanos borrados: {borrados}")

if __name__ == "__main__":
    main()
