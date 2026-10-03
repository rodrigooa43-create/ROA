# -*- coding: utf-8 -*-
"""Lançador do ROA: abre rápido, com a logo animada, e roda o ROA.py.

O código real fica em ROA.py (antes chamado OpenBionica.py, e antes disso
EEG_Data_Collector.py). Este arquivo existe porque o executável já compilado
inicia por ESTE nome — e um .exe não pode ser reconstruído a cada troca de
nome. A ordem de busca em CANDIDATOS é o que permite atualizar quem instalou
versões antigas: se a máquina ainda tiver OpenBionica.py (e não ROA.py), o
programa abre normalmente por ele.

O que este lançador faz (1.10.0):
1. CACHE DE BYTECODE. Antes, runpy.run_path("ROA.py") recompilava os 80 mil
   linhas do fonte a cada abertura (6,7 s medidos no Windows). Agora o ROA.py é
   compilado UMA vez para um .pyc guardado em cache (na pasta do programa ou,
   se ela não for gravável, em %LOCALAPPDATA%\\ROA\\cache); o cache é descartado
   sozinho quando o ROA.py muda (tamanho ou data) ou quando muda a versão do
   Python. Carregar o .pyc pronto custa centésimos de segundo.
2. TELA DE ABERTURA. Enquanto as bibliotecas carregam, uma janela leve mostra a
   logo do ROA entrando com um fade e uma linha de sinal se desenhando por
   baixo, com o progresso em palavras. Ela some com um fade assim que a
   primeira janela do programa aparece; nada é atrasado de propósito. Com
   --sem-splash (ou ROA_SEM_SPLASH=1) ela não é mostrada.
3. COMPATIBILIDADE. Um ROA.py antigo roda igual: ele não precisa saber que a
   tela de abertura existe (o lançador a fecha sozinho ao ver a primeira
   janela). Um ROA.py novo pode escrever o progresso nela por
   sys.modules["roa_splash"].progresso(texto).

Rodar o app: ROA.exe   (ou: python ROA.py, ou python EEG_Data_Collector.py)
"""
# O launcher do .exe lê a versão local por regex NESTE arquivo; sem a
# constante ele reportaria 0.0.0 e pediria update a toda consulta.
# Mantenha em sincronia com APP_VERSION do ROA.py ao publicar.
APP_VERSION = "1.9.0"

import importlib
import importlib.util
import json
import marshal
import os
import struct
import subprocess
import sys
import tempfile
import threading
import time

CANDIDATOS = ("ROA.py", "OpenBionica.py", "EEG_Data_Collector_app.py")

# Cabeçalho do arquivo de cache: número mágico do bytecode desta versão do
# Python + data (ns) e tamanho do fonte. Se qualquer um mudar, o cache é refeito.
_FORMATO_CABECALHO = "<QQ"
_TAM_CABECALHO = len(importlib.util.MAGIC_NUMBER) + struct.calcsize(_FORMATO_CABECALHO)

# Bibliotecas pesadas que o ROA.py importa logo no topo. Importá-las numa thread
# enquanto a tela de abertura anima deixa a animação fluida; se alguma falhar
# aqui, o import de verdade dentro do ROA.py mostra o erro normalmente.
_PRE_IMPORTS = ("numpy", "PySide6.QtWidgets", "pyqtgraph", "serial.tools.list_ports",
                "scipy.fft")

# Frases do progresso nos 9 idiomas do programa (o lançador não tem tr()).
_FRASES = {
    "preparando": {
        "pt": "Preparando o programa pela primeira vez…",
        "en": "Preparing the program for the first time…",
        "es": "Preparando el programa por primera vez…",
        "it": "Preparazione del programma per la prima volta…",
        "fr": "Préparation du programme pour la première fois…",
        "zh": "正在首次准备程序…", "de": "Das Programm wird zum ersten Mal vorbereitet…",
        "ja": "初回のためプログラムを準備しています…", "ru": "Первая подготовка программы…",
    },
    "bibliotecas": {
        "pt": "Carregando as bibliotecas…", "en": "Loading the libraries…",
        "es": "Cargando las bibliotecas…", "it": "Caricamento delle librerie…",
        "fr": "Chargement des bibliothèques…", "zh": "正在加载库…",
        "de": "Bibliotheken werden geladen…", "ja": "ライブラリを読み込んでいます…",
        "ru": "Загрузка библиотек…",
    },
    "abrindo": {
        "pt": "Abrindo o programa…", "en": "Opening the program…",
        "es": "Abriendo el programa…", "it": "Apertura del programma…",
        "fr": "Ouverture du programme…", "zh": "正在打开程序…",
        "de": "Das Programm wird geöffnet…", "ja": "プログラムを開いています…",
        "ru": "Открытие программы…",
    },
    "tela": {
        "pt": "Montando a tela inicial…", "en": "Building the home screen…",
        "es": "Montando la pantalla inicial…", "it": "Preparazione della schermata iniziale…",
        "fr": "Préparation de l'écran d'accueil…", "zh": "正在生成初始界面…",
        "de": "Startbildschirm wird aufgebaut…", "ja": "ホーム画面を準備しています…",
        "ru": "Подготовка начального экрана…",
    },
}


# ============================================================
# Cache de bytecode
# ============================================================
def _pasta_base():
    """Pasta onde o programa está (ao lado do .exe ou deste arquivo)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def _gravavel(pasta):
    """True se dá para criar e apagar um arquivo nessa pasta."""
    try:
        os.makedirs(pasta, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".w", dir=pasta)
        os.close(fd)
        os.remove(tmp)
        return True
    except OSError:
        return False


def pasta_cache(base):
    """Pasta do cache: <programa>/.roa_cache se gravável, senão a pasta do
    usuário (%LOCALAPPDATA%\\ROA\\cache no Windows, ~/.cache/ROA nos outros)."""
    candidatas = [os.path.join(base, ".roa_cache")]
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        candidatas.append(os.path.join(local, "ROA", "cache"))
    else:
        candidatas.append(os.path.join(os.path.expanduser("~"), ".cache", "ROA"))
    candidatas.append(os.path.join(tempfile.gettempdir(), "ROA_cache"))
    for c in candidatas:
        if _gravavel(c):
            return c
    return None


def caminho_cache(alvo, pasta):
    """Nome do .pyc: ROA.py.cpython-311.pyc (a tag separa versões do Python)."""
    tag = getattr(sys.implementation, "cache_tag", None) or "py"
    return os.path.join(pasta, "%s.%s.pyc" % (os.path.basename(alvo), tag))


def _assinatura(alvo):
    """(mtime_ns, tamanho) do fonte: é o que diz se o cache ainda vale."""
    st = os.stat(alvo)
    return int(st.st_mtime_ns), int(st.st_size)


def ler_cache(alvo, destino):
    """Devolve o code object do cache, ou None se não existe ou está vencido."""
    try:
        with open(destino, "rb") as f:
            dados = f.read()
    except OSError:
        return None
    if len(dados) <= _TAM_CABECALHO or dados[:len(importlib.util.MAGIC_NUMBER)] != importlib.util.MAGIC_NUMBER:
        return None
    mtime, tam = struct.unpack_from(_FORMATO_CABECALHO, dados, len(importlib.util.MAGIC_NUMBER))
    try:
        if (mtime, tam) != _assinatura(alvo):
            return None
        return marshal.loads(dados[_TAM_CABECALHO:])
    except Exception:
        return None


def compilar_para_cache(alvo, destino):
    """Compila o fonte e grava o cache de forma atômica (tmp + replace).

    Devolve o code object. Se não conseguir gravar (pasta só de leitura), ainda
    devolve o código compilado: o programa abre, só não ganha o cache.
    """
    with open(alvo, "rb") as f:
        fonte = f.read()
    mtime, tam = _assinatura(alvo)
    # dont_inherit: o bytecode não herda flags de __future__ deste lançador
    code = compile(fonte, alvo, "exec", dont_inherit=True)
    try:
        corpo = (importlib.util.MAGIC_NUMBER
                 + struct.pack(_FORMATO_CABECALHO, mtime, tam)
                 + marshal.dumps(code))
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".pyc", dir=os.path.dirname(destino))
        with os.fdopen(fd, "wb") as f:
            f.write(corpo)
        # mkstemp cria 0600; o cache pode ser lido por outro usuário da máquina
        try:
            os.chmod(tmp, 0o644)
        except OSError:
            pass
        os.replace(tmp, destino)
    except OSError:
        pass
    return code


def _compilar_em_subprocesso(alvo, destino, espera=None, limite_s=120.0):
    """Compila noutro processo para a tela de abertura não congelar.

    compile() segura o GIL por vários segundos num fonte de 6 MB; num processo
    à parte, a animação continua. `espera()` é chamada em laço enquanto o
    filho roda (processa os eventos do Qt). Devolve True se o cache ficou
    pronto. Com o .exe (frozen), sys.executable é o próprio exe, que entende
    --compilar-cache porque passa por este mesmo arquivo.
    """
    if getattr(sys, "frozen", False):
        cmd = [sys.executable, "--compilar-cache", alvo, destino]
    else:
        cmd = [sys.executable, os.path.abspath(__file__), "--compilar-cache", alvo, destino]
    try:
        flags = {}
        if sys.platform == "win32":
            flags["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, **flags)
    except OSError:
        return False
    inicio = time.time()
    while proc.poll() is None:
        if time.time() - inicio > limite_s:
            proc.kill()
            return False
        if espera is not None:
            espera()
        else:
            time.sleep(0.02)
    return proc.returncode == 0 and os.path.exists(destino)


def obter_codigo(alvo, progresso=None, espera=None):
    """Code object do ROA.py: do cache quando vale, senão compila e guarda.

    `progresso(chave)` avisa a tela de abertura; `espera()` mantém a animação
    viva enquanto o subprocesso compila.
    """
    pasta = pasta_cache(os.path.dirname(os.path.abspath(alvo)))
    destino = caminho_cache(alvo, pasta) if pasta else None
    if destino:
        code = ler_cache(alvo, destino)
        if code is not None:
            return code
        if progresso is not None:
            progresso("preparando")
        # Só vale a pena outro processo quando há tela para manter viva.
        if espera is not None and _compilar_em_subprocesso(alvo, destino, espera):
            code = ler_cache(alvo, destino)
            if code is not None:
                return code
        return compilar_para_cache(alvo, destino)
    # Sem pasta gravável nenhuma: compila em memória, como antes.
    with open(alvo, "rb") as f:
        return compile(f.read(), alvo, "exec", dont_inherit=True)


def executar(code, alvo, nome="__main__"):
    """Roda o código do ROA.py como se fosse `python ROA.py`.

    O módulo recebe __file__ = caminho do ROA.py: o atualizador grava no
    arquivo de onde o código foi carregado, e SCRIPT_DIR sai daí. sys.argv[0]
    e sys.path[0] seguem o que runpy.run_path fazia.
    """
    import types
    mod = types.ModuleType(nome)
    mod.__file__ = alvo
    mod.__cached__ = None
    mod.__package__ = None
    mod.__builtins__ = __builtins__
    pasta = os.path.dirname(os.path.abspath(alvo))
    if pasta not in sys.path:
        sys.path.insert(0, pasta)
    sys.argv[0] = alvo
    sys.modules[nome] = mod
    exec(code, mod.__dict__)
    return mod


def pre_importar(modulos, espera=None, limite_s=60.0):
    """Importa as bibliotecas pesadas numa thread, chamando espera() enquanto
    isso para a tela de abertura seguir animando. Falhas são ignoradas aqui:
    o import dentro do ROA.py repete e mostra o erro de verdade."""
    def alvo():
        for m in modulos:
            try:
                importlib.import_module(m)
            except Exception:
                pass
    th = threading.Thread(target=alvo, name="roa-pre-import", daemon=True)
    th.start()
    inicio = time.time()
    while th.is_alive() and time.time() - inicio < limite_s:
        if espera is not None:
            espera()
        th.join(0.016)


# ============================================================
# Tela de abertura
# ============================================================
def _config_rapida(base):
    """Lê só idioma e tema do config.json (sem importar o ROA.py), para a tela
    de abertura sair no idioma e no fundo certos. Qualquer erro -> padrões."""
    idioma, escuro = "pt", False
    casa = os.path.expanduser("~")
    candidatos = [os.path.join(casa, "Documents", "EEG_Coletor", "config.json"),
                  os.path.join(casa, "OneDrive", "Documentos", "EEG_Coletor", "config.json"),
                  os.path.join(casa, "OneDrive", "Documents", "EEG_Coletor", "config.json")]
    for c in candidatos:
        try:
            with open(c, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            continue
        idioma = str(cfg.get("language") or "pt")
        tema = str(cfg.get("theme") or "")
        escuro = any(p in tema for p in ("Escuro", "black", "Lime", "Sistema"))
        break
    if idioma not in _FRASES["abrindo"]:
        idioma = "pt"
    return idioma, escuro


def criar_splash(base):
    """Cria a QApplication e a tela de abertura; None se o Qt não carregar.

    A classe fica dentro da função porque PySide6 só pode ser importado depois
    de sabermos que a tela será usada (e para o fallback sem Qt continuar).
    """
    try:
        from PySide6 import QtCore, QtGui, QtWidgets
    except Exception:
        return None, None
    idioma, escuro = _config_rapida(base)

    class SplashROA(QtWidgets.QWidget):
        """Janela de abertura: logo com fade, linha de sinal se desenhando e
        o progresso em palavras. Pinta tudo à mão (sem widgets filhos), por
        isso o stylesheet que o ROA aplica depois não a altera."""

        DURACAO_LOGO_MS = 900     # fade da logo
        DURACAO_LINHA_MS = 1400   # a linha termina de se desenhar
        DURACAO_SAIDA_MS = 260    # fade de saída
        LIMITE_S = 90.0           # segurança: nunca fica aberta para sempre

        def __init__(self, base, idioma, escuro):
            super().__init__(None, QtCore.Qt.WindowType.FramelessWindowHint
                             | QtCore.Qt.WindowType.WindowStaysOnTopHint
                             | QtCore.Qt.WindowType.SplashScreen)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)
            self.idioma, self.escuro = idioma, escuro
            self.setFixedSize(560, 320)
            self._t0 = time.monotonic()
            self._saindo = None            # instante em que o fade de saída começou
            self._fechada = False
            self._texto = _FRASES["bibliotecas"][idioma]
            self._logo = self._carregar_logo(base)
            self._onda = self._gerar_onda()
            # cores da marca, as mesmas dos temas "ROA (azul clínico)"/"ROA Escuro"
            if escuro:
                self.cor_fundo, self.cor_texto = QtGui.QColor("#141a2b"), QtGui.QColor("#e8ecf7")
                self.cor_dim, self.cor_acento = QtGui.QColor("#98a2bd"), QtGui.QColor("#6b74ff")
                self.cor_borda = QtGui.QColor("#2b3550")
            else:
                self.cor_fundo, self.cor_texto = QtGui.QColor("#ffffff"), QtGui.QColor("#141a33")
                self.cor_dim, self.cor_acento = QtGui.QColor("#5a6480"), QtGui.QColor("#1a23e0")
                self.cor_borda = QtGui.QColor("#d6deef")
            tela = QtGui.QGuiApplication.primaryScreen()
            if tela is not None:
                g = tela.availableGeometry()
                self.move(g.center().x() - self.width() // 2,
                          g.center().y() - self.height() // 2)
            self._timer = QtCore.QTimer(self)
            self._timer.timeout.connect(self._tique)
            self._timer.start(16)

        # ---- conteúdo ----
        def _carregar_logo(self, base):
            """roa_logo.png ao lado do programa (ou em Documentos/EEG_Coletor);
            sem o arquivo, a marca é escrita em código."""
            casa = os.path.expanduser("~")
            for pasta in (base, os.path.join(casa, "Documents", "EEG_Coletor"),
                          getattr(sys, "_MEIPASS", "") or base):
                c = os.path.join(pasta, "roa_logo.png")
                if os.path.exists(c):
                    pm = QtGui.QPixmap(c)
                    if not pm.isNull():
                        return pm
            return None

        def _gerar_onda(self):
            """Pontos (0..1) de uma linha de sinal parecida com EEG/ECG: ondas
            lentas, um complexo rápido no meio e ondas lentas de novo."""
            import math
            pts = []
            n = 260
            for i in range(n):
                x = i / float(n - 1)
                y = 0.18 * math.sin(2 * math.pi * 3.0 * x) + 0.06 * math.sin(2 * math.pi * 11.0 * x + 1.0)
                # um "batimento" nítido perto do meio
                d = (x - 0.52) * 40.0
                y += 0.95 * math.exp(-d * d) - 0.25 * math.exp(-((x - 0.49) * 60.0) ** 2) \
                    - 0.18 * math.exp(-((x - 0.56) * 55.0) ** 2)
                pts.append((x, y))
            return pts

        def progresso(self, chave_ou_texto):
            """Troca a frase do progresso. Aceita uma chave de _FRASES ou um
            texto já traduzido vindo do ROA.py."""
            frases = _FRASES.get(chave_ou_texto)
            self._texto = frases[self.idioma] if frases else str(chave_ou_texto)
            self.update()

        def espera(self):
            """Processa os eventos pendentes do Qt (mantém a animação viva)."""
            QtWidgets.QApplication.processEvents(
                QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 20)

        # ---- ciclo de vida ----
        def vigiar_janela_principal(self):
            """Começa a observar: quando qualquer outra janela do programa
            ficar visível (a tela inicial), a splash sai com um fade."""
            self._vigiando = True

        def fechar(self):
            """Inicia o fade de saída (idempotente)."""
            if self._saindo is None and not self._fechada:
                self._saindo = time.monotonic()

        def _outra_janela_visivel(self):
            for w in QtWidgets.QApplication.topLevelWidgets():
                if w is self or not w.isVisible():
                    continue
                # tooltips/menus não contam como "a tela inicial pronta"
                if w.windowType() in (QtCore.Qt.WindowType.ToolTip, QtCore.Qt.WindowType.Popup):
                    continue
                if w.width() < 200 or w.height() < 120:
                    continue
                return True
            return False

        def _tique(self):
            agora = time.monotonic()
            if getattr(self, "_vigiando", False) and self._saindo is None and self._outra_janela_visivel():
                self.fechar()
            if self._saindo is None and agora - self._t0 > self.LIMITE_S:
                self.fechar()
            if self._saindo is not None and (agora - self._saindo) * 1000.0 >= self.DURACAO_SAIDA_MS:
                self._fechada = True
                self._timer.stop()
                self.hide()
                self.deleteLater()
                return
            self.update()

        # ---- pintura ----
        @staticmethod
        def _suave(x):
            """ease-out cúbico em 0..1."""
            x = max(0.0, min(1.0, x))
            return 1.0 - (1.0 - x) ** 3

        def paintEvent(self, _ev):
            agora = time.monotonic()
            ms = (agora - self._t0) * 1000.0
            opac_global = 1.0
            if self._saindo is not None:
                opac_global = 1.0 - min(1.0, (agora - self._saindo) * 1000.0 / self.DURACAO_SAIDA_MS)
            p = QtGui.QPainter(self)
            p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            p.setOpacity(opac_global)
            r = self.rect().adjusted(8, 8, -8, -8)
            # sombra leve + cartão
            sombra = QtGui.QColor(0, 0, 0, 60 if self.escuro else 28)
            p.setPen(QtCore.Qt.PenStyle.NoPen)
            p.setBrush(sombra)
            p.drawRoundedRect(r.translated(0, 3), 18, 18)
            p.setBrush(self.cor_fundo)
            p.setPen(QtGui.QPen(self.cor_borda, 1))
            p.drawRoundedRect(r, 18, 18)
            # logo com fade + leve subida
            k = self._suave(ms / self.DURACAO_LOGO_MS)
            p.setOpacity(opac_global * k)
            desloc = int((1.0 - k) * 14)
            cx = r.center().x()
            if self._logo is not None:
                pm = self._logo.scaledToWidth(240, QtCore.Qt.TransformationMode.SmoothTransformation)
                if self.escuro:
                    pm = self._tingir(pm, self.cor_acento)
                p.drawPixmap(cx - pm.width() // 2, r.top() + 48 + desloc, pm)
                y_sub = r.top() + 48 + pm.height() + 10
            else:
                f = QtGui.QFont()
                for fam in ("Inter", "Segoe UI", "Roboto", "Arial"):
                    f.setFamily(fam)
                    if QtGui.QFontInfo(f).family().lower().startswith(fam.lower()[:4]):
                        break
                f.setPointSize(56)
                f.setWeight(QtGui.QFont.Weight.Bold)
                f.setLetterSpacing(QtGui.QFont.SpacingType.PercentageSpacing, 108)
                p.setFont(f)
                p.setPen(self.cor_acento)
                p.drawText(QtCore.QRect(r.left(), r.top() + 40 + desloc, r.width(), 90),
                           QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter, "ROA")
                y_sub = r.top() + 134
            f2 = QtGui.QFont(p.font())
            f2.setPointSize(11)
            f2.setWeight(QtGui.QFont.Weight.Normal)
            f2.setLetterSpacing(QtGui.QFont.SpacingType.PercentageSpacing, 112)
            p.setFont(f2)
            p.setPen(self.cor_dim)
            p.drawText(QtCore.QRect(r.left(), y_sub + desloc, r.width(), 24),
                       QtCore.Qt.AlignmentFlag.AlignHCenter, "Research Open Analysis")
            # linha de sinal se desenhando (e depois correndo devagar)
            p.setOpacity(opac_global)
            frac = self._suave((ms - 250.0) / self.DURACAO_LINHA_MS)
            if frac > 0.0:
                x0, x1 = r.left() + 56, r.right() - 56
                yc, amp = r.bottom() - 92, 34.0
                caminho = QtGui.QPainterPath()
                n = max(2, int(frac * len(self._onda)))
                # depois de desenhada, a onda desliza devagar: sinal "vivo"
                corr = ((ms - 250.0 - self.DURACAO_LINHA_MS) / 9000.0) if frac >= 1.0 else 0.0
                for i in range(n):
                    x, y = self._onda[i]
                    if corr:
                        y = self._onda[(i + int(corr * len(self._onda))) % len(self._onda)][1]
                    px = x0 + x * (x1 - x0)
                    py = yc - y * amp
                    if i == 0:
                        caminho.moveTo(px, py)
                    else:
                        caminho.lineTo(px, py)
                caneta = QtGui.QPen(self.cor_acento, 2.4)
                caneta.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
                caneta.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
                p.setPen(caneta)
                p.setBrush(QtCore.Qt.BrushStyle.NoBrush)
                p.drawPath(caminho)
                # ponto na ponta da linha enquanto ela se desenha
                if frac < 1.0:
                    ponta = caminho.currentPosition()
                    p.setPen(QtCore.Qt.PenStyle.NoPen)
                    p.setBrush(self.cor_acento)
                    p.drawEllipse(ponta, 4.0, 4.0)
            # progresso em palavras
            f3 = QtGui.QFont(p.font())
            f3.setPointSize(10)
            f3.setLetterSpacing(QtGui.QFont.SpacingType.PercentageSpacing, 100)
            p.setFont(f3)
            p.setPen(self.cor_dim)
            p.drawText(QtCore.QRect(r.left(), r.bottom() - 52, r.width(), 22),
                       QtCore.Qt.AlignmentFlag.AlignHCenter, self._texto)
            f4 = QtGui.QFont(f3)
            f4.setPointSize(8)
            p.setFont(f4)
            cor_v = QtGui.QColor(self.cor_dim)
            cor_v.setAlpha(150)
            p.setPen(cor_v)
            p.drawText(QtCore.QRect(r.left(), r.bottom() - 28, r.width(), 18),
                       QtCore.Qt.AlignmentFlag.AlignHCenter, "v" + APP_VERSION)
            p.end()

        @staticmethod
        def _tingir(pm, cor):
            """Pinta o PNG da logo com a cor do acento (fundo escuro)."""
            out = QtGui.QPixmap(pm.size())
            out.setDevicePixelRatio(pm.devicePixelRatio())
            out.fill(QtCore.Qt.GlobalColor.transparent)
            pt = QtGui.QPainter(out)
            pt.drawPixmap(0, 0, pm)
            pt.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceIn)
            pt.fillRect(out.rect(), cor)
            pt.end()
            return out

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    splash = SplashROA(base, idioma, escuro)
    splash.show()
    splash.espera()
    return app, splash


class _ApiSplash:
    """O que o ROA.py enxerga em sys.modules["roa_splash"]: só progresso() e
    fechar(). Qualquer versão do ROA.py que não conheça isto segue ignorando."""

    def __init__(self, splash):
        self._splash = splash

    def progresso(self, texto):
        try:
            self._splash.progresso(texto)
            self._splash.espera()
        except Exception:
            pass

    def fechar(self):
        try:
            self._splash.fechar()
        except Exception:
            pass


# ============================================================
# Ponto de entrada
# ============================================================
def localizar_alvo(base):
    """Primeiro arquivo de CANDIDATOS que existir ao lado do lançador."""
    for nome in CANDIDATOS:
        alvo = os.path.join(base, nome)
        if os.path.exists(alvo):
            return alvo
    return None


def main():
    """Abre o ROA: cache de bytecode + tela de abertura + exec do programa."""
    if "--compilar-cache" in sys.argv:
        # processo filho: só compila e grava o cache
        i = sys.argv.index("--compilar-cache")
        compilar_para_cache(sys.argv[i + 1], sys.argv[i + 2])
        return 0
    base = _pasta_base()
    alvo = localizar_alvo(base)
    if alvo is None:
        raise SystemExit(
            "Nao encontrei o codigo do programa ao lado deste arquivo.\n"
            "Esperado um destes: " + ", ".join(CANDIDATOS) + "\n"
            "Pasta: " + base)
    sem_splash = ("--sem-splash" in sys.argv) or os.environ.get("ROA_SEM_SPLASH") == "1"
    if "--sem-splash" in sys.argv:
        sys.argv.remove("--sem-splash")
    splash = None
    if not sem_splash:
        _app, splash = criar_splash(base)
    espera = splash.espera if splash is not None else None
    progresso = splash.progresso if splash is not None else None
    code = obter_codigo(alvo, progresso=progresso, espera=espera)
    if splash is not None:
        splash.progresso("bibliotecas")
    pre_importar(_PRE_IMPORTS, espera=espera)
    if splash is not None:
        splash.progresso("abrindo")
        splash.vigiar_janela_principal()
        sys.modules["roa_splash"] = _ApiSplash(splash)
    executar(code, alvo)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
