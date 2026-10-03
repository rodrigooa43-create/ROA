# -*- coding: utf-8 -*-
"""Apoio comum dos testes: importa o ROA.py de forma isolada e offscreen.

O ROA.py cria pastas em Documentos/EEG_Coletor e em <pasta do programa>/sessions
já na importação. Para os testes não sujarem a máquina de quem os roda (nem o
repositório), este módulo aponta HOME para uma pasta temporária ANTES de
importar e força QT_QPA_PLATFORM=offscreen, para a bateria rodar sem monitor.

Uso nos testes:
    from _roa import ROA, app          # ROA = módulo importado; app = QApplication
"""
import os
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pasta temporária por processo: config.json, cadastro e sessões vão para cá.
_TMP_HOME = tempfile.mkdtemp(prefix="roa_testes_home_")
os.environ["HOME"] = _TMP_HOME
os.environ["USERPROFILE"] = _TMP_HOME
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# Sem variação de fonte entre máquinas e sem pedir rede.
os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false;qt.qpa.*=false")

if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from PySide6 import QtWidgets  # noqa: E402

# Uma única QApplication por processo de teste (o Qt não aceita duas).
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv[:1])

import ROA  # noqa: E402  (importa o programa inteiro, sem rodar main())


def config_limpa(**kw):
    """Devolve um AppConfig novo com os valores padrão, sobrescritos por kw.

    Serve para montar a janela ou um widget com um estado conhecido, sem ler o
    config.json de quem roda os testes.
    """
    cfg = ROA.AppConfig()
    for k, v in kw.items():
        setattr(cfg, k, v)
    return cfg


def processar_eventos(ms=50):
    """Deixa o Qt processar eventos pendentes por alguns milissegundos.

    Necessário depois de criar/mostrar widgets: layouts e timers só assentam
    quando o loop de eventos roda.
    """
    from PySide6 import QtCore
    fim = QtCore.QDeadlineTimer(ms)
    while not fim.hasExpired():
        app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 10)


def sinal_sintetico(n_canais, n_amostras, fs=250, semente=1):
    """Gera sinais sintéticos (ruído + senoides) para os testes.

    Nunca usamos dados de pessoas nos testes: tudo aqui é gerado por fórmula,
    com semente fixa para o resultado ser reprodutível.
    """
    import numpy as np
    rng = np.random.default_rng(semente)
    t = np.arange(n_amostras) / float(fs)
    dados = rng.normal(0.0, 5.0, size=(n_canais, n_amostras))
    for c in range(n_canais):
        dados[c] += 20.0 * np.sin(2 * np.pi * (8.0 + c) * t)
    return dados.astype(np.float64)
