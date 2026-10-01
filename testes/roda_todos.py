# -*- coding: utf-8 -*-
"""Roda a bateria inteira de testes do ROA, offscreen, e resume o resultado.

Uso:  python testes/roda_todos.py            (todos)
      python testes/roda_todos.py test_p1    (só os arquivos cujo nome contém "test_p1")

Cada arquivo test_*.py roda num PROCESSO próprio: o ROA.py importa Qt e cria
uma QApplication, e um teste que trava não pode derrubar os demais. O código
de saída é 0 só quando todos passam.
"""
import glob
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))


def main(filtro=""):
    """Executa todos os testes (ou os filtrados) e imprime um quadro-resumo."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    arquivos = sorted(glob.glob(os.path.join(AQUI, "test_*.py")))
    if filtro:
        arquivos = [a for a in arquivos if filtro in os.path.basename(a)]
    if not arquivos:
        print("Nenhum teste encontrado.")
        return 1
    falhas = []
    inicio = time.time()
    for arq in arquivos:
        nome = os.path.basename(arq)
        t0 = time.time()
        proc = subprocess.run([sys.executable, "-m", "unittest", "-v", arq],
                              cwd=AQUI, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        dt = time.time() - t0
        ok = proc.returncode == 0
        # unittest escreve o sumário no stderr ("Ran N tests in ...")
        linhas = [l for l in proc.stderr.splitlines() if l.startswith("Ran ")]
        resumo = linhas[-1] if linhas else "(sem sumário)"
        print("%s  %-44s %s  (%.1f s)" % ("OK " if ok else "ERRO", nome, resumo, dt))
        if not ok:
            falhas.append(nome)
            print("-" * 72)
            print(proc.stdout[-4000:])
            print(proc.stderr[-6000:])
            print("-" * 72)
    print("\n%d arquivo(s) de teste, %d com falha, %.1f s no total."
          % (len(arquivos), len(falhas), time.time() - inicio))
    if falhas:
        print("Falharam: " + ", ".join(falhas))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
