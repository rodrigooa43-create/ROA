# -*- coding: utf-8 -*-
"""Mede quanto tempo o ROA leva para mostrar a primeira tela (pedido P9).

Roda o programa N vezes de duas formas e imprime a mediana de cada uma:
  - "lançador": python EEG_Data_Collector.py   (cache de bytecode + splash)
  - "direto":   python ROA.py                  (compila o fonte a cada vez)

O ROA.py entende a variável de ambiente ROA_MEDIR_ARRANQUE=<time.time() do
início>: assim que a primeira tela está desenhada ele imprime
"ROA_ARRANQUE_PRONTO <segundos>" e encerra. Passamos --no-wizard para pular o
Termo de Uso; a tela medida é a tela inicial do programa.

Uso: python ferramentas/mede_arranque.py [repetições=3] [--sem-cache]
     --sem-cache apaga o cache do lançador antes de cada abertura (mede a
     primeira abertura, que compila).
"""
import os
import shutil
import statistics
import subprocess
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _uma(cmd, limpar_cache=False):
    """Uma abertura; devolve os segundos até a primeira tela (ou None)."""
    if limpar_cache:
        shutil.rmtree(os.path.join(RAIZ, ".roa_cache"), ignore_errors=True)
    env = dict(os.environ)
    env["ROA_MEDIR_ARRANQUE"] = repr(time.time())
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        out = subprocess.run(cmd, cwd=RAIZ, env=env, capture_output=True,
                             text=True, timeout=180).stdout
    except subprocess.TimeoutExpired:
        return None
    for linha in out.splitlines():
        if linha.startswith("ROA_ARRANQUE_PRONTO"):
            return float(linha.split()[1])
    return None


def medir(rep=3, sem_cache=False):
    """Mede as duas formas de abrir e devolve {nome: [segundos]}."""
    formas = {
        "lançador (EEG_Data_Collector.py)": [sys.executable, "EEG_Data_Collector.py", "--no-wizard"],
        "direto (python ROA.py)": [sys.executable, "ROA.py", "--no-wizard"],
    }
    res = {}
    for nome, cmd in formas.items():
        tempos = []
        for i in range(rep):
            t = _uma(cmd, limpar_cache=(sem_cache and "lançador" in nome))
            if t is not None:
                tempos.append(t)
        res[nome] = tempos
    return res


def main(argv):
    rep = 3
    for a in argv:
        if a.isdigit():
            rep = int(a)
    sem_cache = "--sem-cache" in argv
    res = medir(rep, sem_cache)
    print("Tempo até a primeira tela (%d repetições%s):" % (rep, ", sem cache" if sem_cache else ""))
    for nome, tempos in res.items():
        if tempos:
            print("  %-36s mediana %.2f s  (%s)" % (
                nome, statistics.median(tempos), ", ".join("%.2f" % t for t in tempos)))
        else:
            print("  %-36s sem medida" % nome)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
