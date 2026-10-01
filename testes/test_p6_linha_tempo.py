# -*- coding: utf-8 -*-
"""P6 — linha do tempo de movimentos (modelo, JSON, widgets) dentro do ROA.py.


Rodar: cd /home/user/ROA && QT_QPA_PLATFORM=offscreen python -m unittest testes/test_p6_linha_tempo.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA, app  # noqa: E402  (o bloco P6 vive dentro do ROA.py)
from PySide6 import QtCore, QtGui, QtWidgets  # noqa: E402

P6 = ROA


def _aplicar_tema(nome):
    """Troca a paleta global do ROA para "claro" ou "escuro" (tema do programa)."""
    ROA._apply_theme_colors("ROA Escuro" if nome == "escuro" else "ROA (azul clinico)")



# Rótulos tal como ficam gravados pelos presets sEMG do ROA.py
# (PROTOCOL_PRESETS "sEMG MS — Calibração MVC" e "sEMG MS — Exercícios"),
# com os marcadores de controle que _proto_iniciar/_proto_parar injetam.
def _marcadores_preset_calibracao():
    ms = [(0.0, "PROTOCOLO_INICIO:sEMG MS — Calibração MVC (35 s)")]
    fases = ["Baseline", "Contração máxima"] * 3 + ["Baseline"]
    ms += [(0.1 + 5 * i, f) for i, f in enumerate(fases)]
    ms.append((35.1, "PROTOCOLO_FIM:concluído"))
    return ms


def _marcadores_preset_exercicios():
    ms = [(0.0, "PROTOCOLO_INICIO:sEMG MS — Exercícios (55 s)")]
    for i in range(11):
        rot = "Baseline" if i % 2 == 0 else "Movimento %d" % ((i + 1) // 2)
        ms.append((0.1 + 5 * i, rot))
    ms.append((55.1, "PROTOCOLO_FIM:concluído"))
    return ms


def _modelo_base():
    """Modelo de 30 s com dois trechos na faixa 1 e um na faixa 2."""
    m = P6.ModeloMovimentos("grav", 30.0, n_faixas=2)
    m.adicionar_trecho(0, 5.0, 10.0, "flexao_cotovelo", registrar=False)
    m.adicionar_trecho(0, 12.0, 15.0, "extensao_cotovelo", registrar=False)
    m.adicionar_trecho(1, 7.0, 9.0, "fechar_mao", registrar=False)
    m.modificado = False
    return m


class TestMovimentoDoRotulo(unittest.TestCase):
    """Rótulos variados (acentos, maiúsculas, '#n', inglês) viram a chave certa."""

    CASOS = [
        ("Flexão", "flexao_cotovelo"),
        ("FLEXÃO #2", "flexao_cotovelo"),
        ("Flexão do punho", "flexao_punho"),
        ("wrist extension #3", "extensao_punho"),
        ("Extensão", "extensao_cotovelo"),
        ("Shoulder flexion", "flexao_ombro"),
        ("Extensão do ombro", "extensao_ombro"),
        ("Supinação", "supinacao"),
        ("pronacao #1", "pronacao"),
        ("Pinça", "pinca"),
        ("pinch grip", "pinca"),          # "pinc" vem antes de "grip"
        ("Open hand", "abrir_mao"),
        ("Abrir a mão", "abrir_mao"),
        ("Fechar a mão", "fechar_mao"),
        ("Preensão palmar", "fechar_mao"),
        ("Baseline", "repouso"),
        ("REPOUSO #10", "repouso"),
        ("Rest", "repouso"),
        ("Descanso", "repouso"),
        ("Contração máxima #2", "a_definir"),
        ("MVC Bíceps", "a_definir"),
        ("Isométrica", "a_definir"),
        ("Movimento 1", None),
        ("Aviso", None),
        ("", None),
        ("PROTOCOLO_INICIO:sEMG MS — Exercícios (55 s)", None),
        ("PROTOCOLO_FIM:interrompido", None),
    ]

    def test_casos(self):
        for rotulo, esperado in self.CASOS:
            with self.subTest(rotulo=rotulo):
                self.assertEqual(P6.movimento_do_rotulo(rotulo), esperado)

    def test_chaves_canonicas_batem_com_titulos(self):
        self.assertEqual(set(P6.MOVIMENTOS_ORDEM), set(P6.MOVIMENTOS_TITULOS))
        self.assertEqual(set(P6.MOVIMENTOS_ORDEM), set(P6.MUSCULOS_ESPERADOS))
        self.assertEqual(set(P6.MOVIMENTOS_ORDEM), set(P6.MOVIMENTOS_CORES))
        self.assertEqual(set(P6.MOVIMENTOS_ORDEM), set(P6.MOVIMENTOS_TITULOS_CURTOS))
        for chave in P6.PALAVRAS_MOVIMENTO.values():
            self.assertIn(chave, P6.MOVIMENTOS_TITULOS)


class TestTrechosIniciais(unittest.TestCase):
    """Marcadores e contrações viram o modelo inicial esperado."""

    def test_preset_calibracao(self):
        m = P6.trechos_de_marcadores(_marcadores_preset_calibracao(), 40.0, "g")
        self.assertEqual(m.origem, "marcadores")
        self.assertEqual(m.n_faixas(), 2)
        ts = m.trechos(0)
        # PROTOCOLO_INICIO (0,0) e Baseline (0,1) estão a 0,1 s: o primeiro
        # cai por ser mais curto que o mínimo. Sobram 7 fases + PROTOCOLO_FIM.
        self.assertEqual(len(ts), 8)
        self.assertEqual([t["movimento"] for t in ts],
                         ["repouso", "a_definir"] * 3 + ["repouso", "a_definir"])
        self.assertAlmostEqual(ts[0]["t0"], 0.1)
        self.assertAlmostEqual(ts[0]["t1"], 5.1)
        self.assertAlmostEqual(ts[1]["t1"], 10.1)
        # o último (PROTOCOLO_FIM) vai até +3 s
        self.assertAlmostEqual(ts[-1]["t0"], 35.1)
        self.assertAlmostEqual(ts[-1]["t1"], 38.1)
        self.assertEqual(m.trechos(1), [])
        self.assertFalse(m.modificado)

    def test_preset_exercicios_movimento_n_vira_a_definir(self):
        m = P6.trechos_de_marcadores(_marcadores_preset_exercicios(), 56.0)
        movs = [t["movimento"] for t in m.trechos(0)]
        self.assertEqual(movs[:4], ["repouso", "a_definir", "repouso", "a_definir"])
        # o último marcador (55,1) é preso ao fim da gravação (56)
        self.assertAlmostEqual(m.trechos(0)[-1]["t1"], 56.0)

    def test_rotulos_reconhecidos(self):
        ms = [(0.0, "Repouso"), (3.0, "Flexão"), (8.0, "Repouso"), (11.0, "Extensão #2")]
        m = P6.trechos_de_marcadores(ms, 20.0)
        self.assertEqual([t["movimento"] for t in m.trechos(0)],
                         ["repouso", "flexao_cotovelo", "repouso", "extensao_cotovelo"])
        self.assertAlmostEqual(m.trechos(0)[-1]["t1"], 14.0)

    def test_contracoes(self):
        m = P6.trechos_de_contracoes([(2.0, 3.5), (6.0, 6.1), (9.0, 10.0)], 12.0, "g")
        self.assertEqual(m.origem, "contracoes")
        ts = m.trechos(0)
        self.assertEqual(len(ts), 2)            # a de 0,1 s é curta demais
        self.assertTrue(all(t["movimento"] == "a_definir" for t in ts))
        self.assertAlmostEqual(ts[0]["t0"], 2.0)
        self.assertAlmostEqual(ts[1]["t1"], 10.0)

    def test_modelo_inicial_escolhe(self):
        onsets = [(1.0, 2.0)]
        self.assertEqual(P6.modelo_inicial([(0.0, "Flexão")], onsets, 10.0).origem, "marcadores")
        self.assertEqual(P6.modelo_inicial([(0.0, "Fase A"), (4.0, "Fase B")], onsets, 10.0).origem,
                         "marcadores")
        self.assertEqual(P6.modelo_inicial([(0.0, "Fase A")], onsets, 10.0).origem, "contracoes")
        self.assertEqual(P6.modelo_inicial([], [], 10.0).origem, "vazio")
        # só marcadores de controle, quase no mesmo instante: nada sobra -> contrações
        ms = [(0.0, "PROTOCOLO_INICIO:x"), (0.05, "PROTOCOLO_FIM:y")]
        self.assertEqual(P6.modelo_inicial(ms, onsets, 0.1).origem, "contracoes")

    def test_contracoes_da_gravacao_usa_detector_pelo_nome(self):
        import numpy as np
        fs = 250.0
        sinal = np.random.default_rng(0).normal(0, 1.0, int(10 * fs))
        sinal[int(3 * fs):int(5 * fs)] *= 12.0        # contração de 3 a 5 s
        ativ = P6.contracoes_da_gravacao(sinal, fs)
        self.assertTrue(ativ)
        self.assertTrue(any(a <= 3.3 and b >= 4.7 for a, b in ativ), ativ)
        m = P6.trechos_de_contracoes(ativ, 10.0)
        self.assertGreaterEqual(m.total_trechos(), 1)


class TestOperacoes(unittest.TestCase):
    """Mover, esticar, dividir, trocar, apagar, faixas e desfazer/refazer."""

    def test_mover_para_no_vizinho(self):
        m = _modelo_base()
        real = m.mover(0, 0, +4.0)              # 5–10 -> quer 9–14, mas o vizinho começa em 12
        self.assertAlmostEqual(real, 2.0)
        self.assertAlmostEqual(m.trecho(0, 0)["t0"], 7.0)
        self.assertAlmostEqual(m.trecho(0, 0)["t1"], 12.0)
        real = m.mover(0, 1, +100.0)            # 12–15 -> bate no fim (30)
        self.assertAlmostEqual(m.trecho(0, 1)["t1"], 30.0)
        self.assertAlmostEqual(real, 15.0)
        real = m.mover(0, 0, -100.0)            # bate no começo
        self.assertAlmostEqual(m.trecho(0, 0)["t0"], 0.0)
        self.assertEqual(m.mover(0, 0, -1.0), 0.0)   # já no limite: nada muda

    def test_esticar_para_no_vizinho_e_no_minimo(self):
        m = _modelo_base()
        self.assertAlmostEqual(m.esticar(0, 0, "t1", 14.0), 12.0)   # para em 12 (vizinho)
        self.assertAlmostEqual(m.esticar(0, 1, "t0", 5.0), 12.0)    # para em 12 (vizinho)
        self.assertAlmostEqual(m.esticar(0, 0, "t0", 11.95), 12.0 - m.DURACAO_MINIMA)
        self.assertAlmostEqual(m.esticar(1, 0, "t1", 99.0), 30.0)    # fim da gravação
        self.assertAlmostEqual(m.esticar(1, 0, "t0", -5.0), 0.0)

    def test_dividir(self):
        m = _modelo_base()
        self.assertIsNone(m.dividir(0, 0, 5.05))     # metade menor que o mínimo
        novo = m.dividir(0, 0, 7.5)
        self.assertEqual(novo, 1)
        ts = m.trechos(0)
        self.assertEqual(len(ts), 3)
        self.assertAlmostEqual(ts[0]["t1"], 7.5)
        self.assertAlmostEqual(ts[1]["t0"], 7.5)
        self.assertAlmostEqual(ts[1]["t1"], 10.0)
        self.assertEqual(ts[1]["movimento"], "flexao_cotovelo")
        self.assertEqual(ts[2]["movimento"], "extensao_cotovelo")

    def test_trocar_e_apagar(self):
        m = _modelo_base()
        self.assertTrue(m.trocar_movimento(0, 0, "supinacao"))
        self.assertEqual(m.trecho(0, 0)["movimento"], "supinacao")
        self.assertFalse(m.trocar_movimento(0, 0, "supinacao"))     # igual: nada
        self.assertTrue(m.trocar_movimento(0, 0, "nao_existe"))
        self.assertEqual(m.trecho(0, 0)["movimento"], "a_definir")
        self.assertTrue(m.apagar(0, 0))
        self.assertEqual(len(m.trechos(0)), 1)
        self.assertFalse(m.apagar(0, 7))

    def test_adicionar_trecho_cabe_na_lacuna(self):
        m = _modelo_base()
        idx = m.adicionar_trecho(0, 8.0, 13.0, "pinca")       # invade 5–10 e 12–15
        self.assertEqual(idx, 1)
        self.assertAlmostEqual(m.trecho(0, 1)["t0"], 10.0)
        self.assertAlmostEqual(m.trecho(0, 1)["t1"], 12.0)
        self.assertIsNone(m.adicionar_trecho(0, 6.0, 7.0, "pinca"))   # sem lacuna
        self.assertIsNone(m.adicionar_trecho(5, 0.0, 1.0))             # faixa inexistente

    def test_faixas(self):
        m = _modelo_base()
        self.assertFalse(m.remover_faixa(0))                 # mínimo 2
        self.assertEqual(m.adicionar_faixa(), 2)
        self.assertEqual(m.adicionar_faixa(), 3)
        self.assertIsNone(m.adicionar_faixa())               # máximo 4
        self.assertTrue(m.remover_faixa(0))
        self.assertEqual([f["nome"] for f in m.faixas], ["Faixa 1", "Faixa 2", "Faixa 3"])
        self.assertEqual(m.trecho(0, 0)["movimento"], "fechar_mao")

    def test_desfazer_refazer_restauram_exatamente(self):
        m = _modelo_base()
        antes = json.dumps(m.para_dict()["faixas"], sort_keys=True)
        m.mover(0, 0, 1.0)
        m.dividir(0, 1, 13.5)
        m.trocar_movimento(1, 0, "pinca")
        m.apagar(0, 0)
        m.adicionar_faixa()
        depois = json.dumps(m.para_dict()["faixas"], sort_keys=True)
        self.assertNotEqual(antes, depois)
        for _ in range(5):
            self.assertTrue(m.desfazer())
        self.assertFalse(m.desfazer())
        self.assertEqual(json.dumps(m.para_dict()["faixas"], sort_keys=True), antes)
        for _ in range(5):
            self.assertTrue(m.refazer())
        self.assertFalse(m.refazer())
        self.assertEqual(json.dumps(m.para_dict()["faixas"], sort_keys=True), depois)
        # uma edição nova apaga o refazer
        m.desfazer()
        m.trocar_movimento(1, 0, "abrir_mao")
        self.assertFalse(m.pode_refazer())

    def test_limite_da_pilha(self):
        m = _modelo_base()
        for i in range(150):
            m.trocar_movimento(0, 0, P6.MOVIMENTOS_ORDEM[i % 12])
        self.assertLessEqual(len(m._desfazer), m.LIMITE_DESFAZER)

    def test_gesto_com_registrar_false_vale_um_desfazer(self):
        m = _modelo_base()
        m.marcar_desfazer()
        for _ in range(10):
            m.mover(0, 0, 0.1, registrar=False)
        self.assertAlmostEqual(m.trecho(0, 0)["t0"], 6.0)
        self.assertTrue(m.desfazer())
        self.assertAlmostEqual(m.trecho(0, 0)["t0"], 5.0)
        self.assertFalse(m.pode_desfazer())

    def test_movimentos_em_mescla_faixas(self):
        m = _modelo_base()
        self.assertEqual(m.movimentos_em(8.0),
                         [("flexao_cotovelo", 0.6), ("fechar_mao", 0.5)])
        self.assertEqual(m.movimentos_em(6.0), [("flexao_cotovelo", 0.2)])
        self.assertEqual(m.movimentos_em(11.0), [])
        self.assertEqual(m.movimentos_em(12.0), [("extensao_cotovelo", 0.0)])  # [t0, t1)
        self.assertEqual(m.movimentos_em(15.0), [])


class TestArquivo(unittest.TestCase):
    """movimentos.json: ida-e-volta e carga tolerante."""

    def setUp(self):
        self.pasta = tempfile.mkdtemp(prefix="roa_p6_")

    def test_caminho(self):
        self.assertEqual(P6.caminho_movimentos("/x/grav"), os.path.join("/x/grav", "movimentos.json"))
        self.assertEqual(P6.caminho_movimentos("/x/grav/data.csv"),
                         os.path.join("/x/grav", "movimentos.json"))

    def test_salvar_carregar_ida_e_volta(self):
        m = _modelo_base()
        m.adicionar_faixa()
        caminho = P6.caminho_movimentos(self.pasta)
        m.salvar(caminho)
        self.assertFalse(m.modificado)
        self.assertFalse(os.path.exists(caminho + ".tmp"))
        with open(caminho, encoding="utf-8") as f:
            bruto = json.load(f)
        self.assertEqual(bruto["versao"], 1)
        self.assertEqual(bruto["gravacao"], "grav")
        self.assertEqual(bruto["duracao_s"], 30.0)
        self.assertEqual(bruto["origem"], "manual")     # editado a partir de "vazio"
        self.assertEqual(len(bruto["faixas"]), 3)
        self.assertEqual(set(bruto["faixas"][0]["trechos"][0]), {"t0", "t1", "movimento"})
        m2 = P6.ModeloMovimentos.carregar(caminho)
        self.assertEqual(m2.para_dict(), m.para_dict())
        self.assertFalse(m2.modificado)
        self.assertFalse(m2.pode_desfazer())

    def test_carga_tolerante(self):
        caminho = os.path.join(self.pasta, "movimentos.json")
        lixo = {
            "versao": 1, "gravacao": "g", "duracao_s": 20.0, "origem": "qualquer",
            "faixas": [
                {"nome": "Faixa 1", "trechos": [
                    {"t0": 1.0, "t1": 4.0, "movimento": "polichinelo"},   # chave inválida
                    {"t0": 3.0, "t1": 6.0, "movimento": "pinca"},         # sobrepõe: é aparado
                    {"t0": 18.0, "t1": 50.0, "movimento": "repouso"},     # fora: preso em 20
                    {"t0": 7.0, "t1": 7.05, "movimento": "repouso"},      # curto demais
                    {"t0": "x", "t1": 9.0, "movimento": "repouso"},       # inválido
                    "nem é dict",
                ]},
            ],
        }
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(lixo, f)
        m = P6.ModeloMovimentos.carregar(caminho)
        self.assertEqual(m.origem, "vazio")
        self.assertEqual(m.n_faixas(), 2)               # completa até o mínimo
        ts = m.trechos(0)
        self.assertEqual([t["movimento"] for t in ts], ["a_definir", "pinca", "repouso"])
        self.assertAlmostEqual(ts[1]["t0"], 4.0)
        self.assertAlmostEqual(ts[2]["t1"], 20.0)
        # a duração da gravação manda sobre a do arquivo
        m2 = P6.ModeloMovimentos.carregar(caminho, duracao_s=5.0)
        self.assertEqual(len(m2.trechos(0)), 2)
        self.assertAlmostEqual(m2.trechos(0)[1]["t1"], 5.0)

    def test_de_dict_com_lixo_total(self):
        m = P6.ModeloMovimentos.de_dict("isso não é um dicionário")
        self.assertEqual(m.n_faixas(), 2)
        self.assertEqual(m.total_trechos(), 0)


class TestAvisoEIntensidade(unittest.TestCase):
    """Aviso de incompatibilidade e intensidade por músculo."""

    def test_nada_ativo(self):
        self.assertEqual(P6.aviso_incompatibilidade(
            "flexao_cotovelo", {"Bíceps Braquial": 0.1, "Tríceps Braquial": 0.2}), "")
        self.assertEqual(P6.aviso_incompatibilidade("flexao_cotovelo", {}), "")

    def test_esperado_ativo(self):
        self.assertEqual(P6.aviso_incompatibilidade(
            "flexao_cotovelo", {"Bíceps Braquial": 0.8, "Tríceps Braquial": 0.5}), "")
        self.assertEqual(P6.aviso_incompatibilidade(
            "flexao_ombro", {"Peitoral Maior": 0.4}), "")

    def test_so_antagonista_ativo(self):
        txt = P6.aviso_incompatibilidade(
            "flexao_cotovelo", {"Tríceps Braquial": 0.6, "Bíceps Braquial": 0.1})
        self.assertIn("Tríceps Braquial", txt)
        self.assertIn("Flexão do cotovelo", txt)
        self.assertIn("esperado: Bíceps Braquial", txt)
        self.assertNotIn("Bíceps Braquial)", txt.split(";")[0])   # o bíceps não é "ativo"
        txt2 = P6.aviso_incompatibilidade(
            "extensao_ombro", {"Deltoide Anterior": 0.9, "Bíceps Braquial": 0.4})
        self.assertTrue(txt2.startswith("Os músculos ativos (Deltoide Anterior, Bíceps Braquial)"))
        self.assertIn("Deltoide Posterior, Latíssimo do Dorso", txt2)

    def test_sem_referencia_nao_avisa(self):
        self.assertEqual(P6.aviso_incompatibilidade("repouso", {"Bíceps Braquial": 0.9}), "")
        self.assertEqual(P6.aviso_incompatibilidade("a_definir", {"Bíceps Braquial": 0.9}), "")

    def test_intensidade_no_instante(self):
        import numpy as np
        fs = 100.0
        env = np.zeros(int(10 * fs))
        env[int(3 * fs):int(4 * fs)] = 2.0
        env[int(6 * fs):int(7 * fs)] = 1.0
        envs = {"Bíceps Braquial": env, "Tríceps Braquial": np.zeros_like(env)}
        r = P6.intensidade_no_instante(envs, fs, 3.5)
        self.assertAlmostEqual(r["Bíceps Braquial"], 1.0)      # percentil 95 = 2 -> 1,0
        self.assertAlmostEqual(r["Tríceps Braquial"], 0.0)
        r = P6.intensidade_no_instante(envs, fs, 6.5)
        self.assertAlmostEqual(r["Bíceps Braquial"], 0.5)
        r = P6.intensidade_no_instante(envs, fs, 6.5, mvc={"Bíceps Braquial": 4.0})
        self.assertAlmostEqual(r["Bíceps Braquial"], 0.25)
        r = P6.intensidade_no_instante(envs, fs, 1.0)
        self.assertAlmostEqual(r["Bíceps Braquial"], 0.0)
        r = P6.intensidade_no_instante(envs, fs, 99.0)          # fora do sinal
        self.assertEqual(r["Bíceps Braquial"], 0.0)
        self.assertEqual(P6.intensidade_no_instante({}, fs, 1.0), {})


class TestWidgets(unittest.TestCase):
    """Os widgets pintam sem erro nos dois modos e nos dois temas, e as
    interações básicas alteram o modelo."""

    def _processar(self, ms=30):
        fim = QtCore.QDeadlineTimer(ms)
        while not fim.hasExpired():
            app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 10)

    def _widget(self, somente_leitura=False, modelo=None):
        w = P6.LinhaDoTempoMovimentosWidget()
        w.set_somente_leitura(somente_leitura)
        w.set_modelo(modelo or _modelo_base())
        w.set_marcadores([(0.0, "PROTOCOLO_INICIO:x"), (5.0, "Flexão"), (12.0, "Extensão")])
        w.set_cursor(8.0)
        w.resize(800, w.sizeHint().height())
        w.show()
        self._processar()
        return w

    def test_pinta_edicao_e_leitura_nos_dois_temas(self):
        for tema in ("claro", "escuro"):
            _aplicar_tema(tema)
            for ro in (False, True):
                with self.subTest(tema=tema, somente_leitura=ro):
                    w = self._widget(ro)
                    pix = w.grab()
                    self.assertFalse(pix.isNull())
                    self.assertEqual(pix.width(), 800)
                    self.assertEqual(w.height(), w.sizeHint().height())
                    w.close()
        _aplicar_tema("claro")

    def test_pinta_sem_modelo_e_sem_marcadores(self):
        w = P6.LinhaDoTempoMovimentosWidget()
        w.resize(400, w.sizeHint().height())
        w.show(); self._processar()
        self.assertFalse(w.grab().isNull())
        w.set_modelo(_modelo_base())
        self.assertFalse(w.grab().isNull())

    def test_altura_acompanha_faixas(self):
        w = self._widget()
        h2 = w.height()
        w.modelo().adicionar_faixa()
        w._apos_mudanca()
        self._processar()
        self.assertGreater(w.height(), h2)

    def test_clique_no_fundo_move_cursor(self):
        w = self._widget()
        recebidos = []
        w.cursorMovido.connect(recebidos.append)
        x = w._x_de_t(20.0)
        y = w._y_faixa(1) + 10          # faixa 2 em 20 s: vazio
        QtTest = _qt_test()
        QtTest.QTest.mouseClick(w, QtCore.Qt.MouseButton.LeftButton,
                                QtCore.Qt.KeyboardModifier.NoModifier, QtCore.QPoint(int(x), y))
        self.assertEqual(len(recebidos), 1)
        self.assertAlmostEqual(recebidos[0], 20.0, places=1)
        self.assertAlmostEqual(w.cursor(), 20.0, places=1)

    def test_arrastar_bloco_move_e_vale_um_desfazer(self):
        w = self._widget()
        mudou = []
        w.modeloMudou.connect(lambda: mudou.append(1))
        QtTest = _qt_test()
        y = w._y_faixa(0) + 17
        x_ini = int(w._x_de_t(7.5))                      # meio do bloco 5–10
        QtTest.QTest.mousePress(w, QtCore.Qt.MouseButton.LeftButton,
                                QtCore.Qt.KeyboardModifier.NoModifier, QtCore.QPoint(x_ini, y))
        self.assertEqual(w.selecionado(), (0, 0))
        for x in range(x_ini, int(w._x_de_t(12.5)), 6):
            local = QtCore.QPointF(x, y)
            ev = QtGui.QMouseEvent(QtCore.QEvent.Type.MouseMove, local,
                                   QtCore.QPointF(w.mapToGlobal(local.toPoint())),
                                   QtCore.Qt.MouseButton.NoButton, QtCore.Qt.MouseButton.LeftButton,
                                   QtCore.Qt.KeyboardModifier.NoModifier)
            app.sendEvent(w, ev)
        QtTest.QTest.mouseRelease(w, QtCore.Qt.MouseButton.LeftButton,
                                  QtCore.Qt.KeyboardModifier.NoModifier,
                                  QtCore.QPoint(int(w._x_de_t(12.5)), y))
        m = w.modelo()
        self.assertEqual(mudou, [1])
        self.assertAlmostEqual(m.trecho(0, 0)["t1"], 12.0, places=2)   # parou no vizinho
        self.assertTrue(m.desfazer())
        self.assertAlmostEqual(m.trecho(0, 0)["t0"], 5.0)
        self.assertFalse(m.pode_desfazer())                              # gesto = 1 passo

    def test_somente_leitura_nao_edita(self):
        w = self._widget(somente_leitura=True)
        QtTest = _qt_test()
        y = w._y_faixa(0) + 17
        x = int(w._x_de_t(7.5))
        antes = json.dumps(w.modelo().para_dict())
        QtTest.QTest.mouseDClick(w, QtCore.Qt.MouseButton.LeftButton,
                                 QtCore.Qt.KeyboardModifier.NoModifier,
                                 QtCore.QPoint(int(w._x_de_t(20.0)), y))
        QtTest.QTest.keyClick(w, QtCore.Qt.Key.Key_Delete)
        self.assertEqual(json.dumps(w.modelo().para_dict()), antes)
        self.assertIsNone(w.selecionado())
        # mas o clique num bloco posiciona o cursor
        QtTest.QTest.mouseClick(w, QtCore.Qt.MouseButton.LeftButton,
                                QtCore.Qt.KeyboardModifier.NoModifier, QtCore.QPoint(x, y))
        self.assertAlmostEqual(w.cursor(), 7.5, places=1)

    def test_duplo_clique_cria_e_ctrl_z_desfaz(self):
        w = self._widget()
        QtTest = _qt_test()
        y = w._y_faixa(1) + 17
        QtTest.QTest.mouseDClick(w, QtCore.Qt.MouseButton.LeftButton,
                                 QtCore.Qt.KeyboardModifier.NoModifier,
                                 QtCore.QPoint(int(w._x_de_t(20.0)), y))
        m = w.modelo()
        self.assertEqual(len(m.trechos(1)), 2)
        novo = m.trechos(1)[1]
        self.assertEqual(novo["movimento"], "a_definir")
        self.assertAlmostEqual(novo["t1"] - novo["t0"], 1.0, places=2)
        QtTest.QTest.keyClick(w, QtCore.Qt.Key.Key_Z, QtCore.Qt.KeyboardModifier.ControlModifier)
        self.assertEqual(len(m.trechos(1)), 1)
        QtTest.QTest.keyClick(w, QtCore.Qt.Key.Key_Y, QtCore.Qt.KeyboardModifier.ControlModifier)
        self.assertEqual(len(m.trechos(1)), 2)

    def test_menu_de_contexto(self):
        w = self._widget()
        pos = QtCore.QPoint(int(w._x_de_t(7.5)), w._y_faixa(0) + 17)
        menu = w.criar_menu(pos)
        textos = [a.text() for a in menu.actions() if not a.isSeparator()]
        self.assertEqual(textos, ["Trocar o movimento", "Dividir aqui", "Apagar",
                                  "Desfazer", "Refazer", "Adicionar faixa", "Remover faixa"])
        sub = menu.actions()[0].menu()
        self.assertEqual(len(sub.actions()), len(P6.MOVIMENTOS_ORDEM))
        self.assertTrue([a for a in sub.actions() if a.isChecked()][0].text()
                        .startswith("Flexão do cotovelo"))
        # Desfazer está desligado (nada feito); Remover faixa também (só 2 faixas)
        self.assertFalse(textos and menu.actions()[4].isEnabled())
        self.assertFalse(menu.actions()[-1].isEnabled())
        # "Dividir aqui" divide no instante do clique
        [a for a in menu.actions() if a.text() == "Dividir aqui"][0].trigger()
        self.assertEqual(len(w.modelo().trechos(0)), 3)
        self.assertAlmostEqual(w.modelo().trechos(0)[1]["t0"], 7.5, places=1)
        # trocar pelo submenu
        sub.actions()[P6.MOVIMENTOS_ORDEM.index("pinca")].trigger()
        self.assertEqual(w.modelo().trecho(0, 0)["movimento"], "pinca")
        # menu no fundo vazio oferece "Novo trecho aqui"
        menu2 = w.criar_menu(QtCore.QPoint(int(w._x_de_t(25.0)), w._y_faixa(1) + 17))
        self.assertEqual(menu2.actions()[0].text(), "Novo trecho aqui")

    def test_roda_zoom_e_rolagem(self):
        w = self._widget()
        pos = QtCore.QPointF(w._x_de_t(15.0), w._y_faixa(0) + 10)
        ev = QtGui.QWheelEvent(pos, w.mapToGlobal(pos.toPoint()), QtCore.QPoint(),
                               QtCore.QPoint(0, 120), QtCore.Qt.MouseButton.NoButton,
                               QtCore.Qt.KeyboardModifier.ControlModifier,
                               QtCore.Qt.ScrollPhase.NoScrollPhase, False)
        app.sendEvent(w, ev)
        self.assertLess(w._v1 - w._v0, 30.0)                 # ampliou
        v0 = w._v0
        ev = QtGui.QWheelEvent(pos, w.mapToGlobal(pos.toPoint()), QtCore.QPoint(),
                               QtCore.QPoint(0, -120), QtCore.Qt.MouseButton.NoButton,
                               QtCore.Qt.KeyboardModifier.NoModifier,
                               QtCore.Qt.ScrollPhase.NoScrollPhase, False)
        app.sendEvent(w, ev)
        self.assertGreater(w._v0, v0)                         # rolou para a direita
        self.assertFalse(w.grab().isNull())
        w.ajustar_tudo()
        self.assertEqual((w._v0, w._v1), (0.0, 30.0))

    def test_lista_de_trechos(self):
        lista = P6.ListaTrechosWidget()
        lista.set_modelo(_modelo_base())
        self.assertEqual(lista.count(), 3)
        self.assertEqual(lista.item(0).text(), "0:05–0:10  Flexão do cotovelo (faixa 1)")
        self.assertEqual(lista.item(1).text(), "0:07–0:09  Fechar a mão (faixa 2)")
        recebidos = []
        lista.cursorMovido.connect(recebidos.append)
        sel = []
        lista.trechoSelecionado.connect(lambda f, i: sel.append((f, i)))
        lista.itemClicked.emit(lista.item(1))
        self.assertEqual(recebidos, [7.0])
        self.assertEqual(sel, [(1, 0)])
        lista.set_modelo(P6.ModeloMovimentos("g", 10.0))
        self.assertEqual(lista.count(), 1)          # aviso de lista vazia
        self.assertFalse(lista.item(0).flags() & QtCore.Qt.ItemFlag.ItemIsSelectable)
        lista.resize(400, 200); lista.show(); self._processar()
        self.assertFalse(lista.grab().isNull())


def _qt_test():
    """Importa QtTest sob demanda (não é usado fora dos testes de widget)."""
    from PySide6 import QtTest
    return QtTest


if __name__ == "__main__":
    unittest.main()
