# -*- coding: utf-8 -*-
"""Lancador de compatibilidade do ROA.

O codigo real fica em ROA.py (antes chamado OpenBionica.py, e antes disso
EEG_Data_Collector.py). Este arquivo existe porque o executavel ja compilado
inicia por ESTE nome, via runpy — e um .exe nao pode ser reconstruido a cada
troca de nome. Nao edite.

A ordem de busca abaixo e o que permite atualizar quem instalou versoes
antigas: se a maquina ainda tiver OpenBionica.py (e nao ROA.py), o programa
abre normalmente por ele.

Rodar o app: ROA.exe   (ou: python ROA.py)
"""
# O launcher do .exe le a versao local por regex NESTE arquivo; sem a
# constante ele reportaria 0.0.0 e pediria update a toda consulta.
# Mantenha em sincronia com APP_VERSION do ROA.py ao publicar.
APP_VERSION = "1.9.0"
import os, sys, runpy

CANDIDATOS = ("ROA.py", "OpenBionica.py", "EEG_Data_Collector_app.py")

if __name__ == "__main__":
    _base = (os.path.dirname(os.path.abspath(sys.executable))
             if getattr(sys, "frozen", False)
             else os.path.dirname(os.path.abspath(__file__)))
    for _nome in CANDIDATOS:
        _alvo = os.path.join(_base, _nome)
        if os.path.exists(_alvo):
            runpy.run_path(_alvo, run_name="__main__")
            break
    else:
        raise SystemExit(
            "Nao encontrei o codigo do programa ao lado deste arquivo.\n"
            "Esperado um destes: " + ", ".join(CANDIDATOS) + "\n"
            "Pasta: " + _base)
