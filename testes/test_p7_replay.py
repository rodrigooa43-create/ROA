# -*- coding: utf-8 -*-
"""P7 (dentro do ROA.py) — protótipo do replay do coração e dos olhos (fora do ROA.py).

Importa o módulo do protótipo pelo caminho absoluto (ou por P7_REPLAY_PATH) e
confere: as detecções da gravação inteira acham as batidas, a batida
adiantada e a pausa do ECG sintético; as correções manuais; a ida e volta de
batidas.json/olhos.json; piscadas e sacadas com a direção certa (e a
inversão); as frases; o olhar no instante; os widgets pintam rápido e a
faixa responde ao clique. Roda offscreen.
"""
import math
import os
import sys
import tempfile
import time
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA, app  # noqa: E402  (o bloco P7 vive dentro do ROA.py)
from PySide6 import QtCore, QtGui, QtWidgets  # noqa: E402
from PySide6.QtTest import QTest  # noqa: E402


class _Sinteticos:
    """Geradores de ECG/EOG sintéticos do protótipo (só para os testes), com
    acesso a tudo o mais pelo próprio ROA.py."""

    def __getattr__(self, nome):
        return getattr(ROA, nome)


# ---- geradores sintéticos copiados do harness do protótipo P7 ----
def _tabela_ecg(n):
    """Complexo PQRST normalizado (pico R = 1,0) em n pontos."""
    f = np.linspace(0.0, 1.0, n, endpoint=False)
    def g(c, a, w):
        return a * np.exp(-0.5 * ((f - c) / w) ** 2)
    return (g(0.16, 0.12, 0.022) + g(0.26, -0.09, 0.006)
            + g(0.29, 1.00, 0.007) + g(0.32, -0.22, 0.008)
            + g(0.50, 0.28, 0.035))

def _tabela_piscada(n):
    return np.sin(np.pi * np.linspace(0.0, 1.0, n)) ** 2

def _tabela_sacada(n):
    return 0.5 - 0.5 * np.cos(np.pi * np.linspace(0.0, 1.0, n))

def ecg_sintetico(fs=250, dur_s=60.0, t_adiantada=20.0, t_pausa=40.0, ruido_uV=6.0,
                  semente=20260920):
    """ECG sintético: PQRST da tabela do GeradorSimulado (_tabela_ecg), ganho
    600 µV e ruído N(0, 6) como lá, ~70 bpm com arritmia sinusal respiratória
    discreta, UMA batida adiantada (RR de 0,52 s) logo após t_adiantada e UMA
    pausa (RR de 1,70 s) logo após t_pausa. Devolve (sinal, tempos_R,
    t_da_adiantada, t_fim_da_pausa)."""
    rng = np.random.default_rng(semente)
    tempos = []
    t = 0.6
    t_ad = t_pa = None
    while t < dur_s - 0.6:
        tempos.append(t)
        rr = 60.0 / (70.0 + 2.5 * np.sin(2 * np.pi * 0.25 * t))
        if t_ad is None and t >= t_adiantada:
            rr = 0.52
            t_ad = t + rr
        elif t_pa is None and t >= t_pausa:
            rr = 1.70
            t_pa = t + rr
        t += rr
    tab = _tabela_ecg(1024)
    n = int(dur_s * fs)
    x = np.zeros(n)
    ciclo = 0.85                               # forma do PQRST não estica com o RR
    for tr_ in tempos:
        i0 = int((tr_ - 0.29 * ciclo) * fs)
        i1 = int((tr_ + 0.71 * ciclo) * fs)
        idx = np.arange(max(0, i0), min(n, i1))
        fase = (idx / fs - tr_) / ciclo + 0.29
        x[idx] += 600.0 * tab[np.clip((fase * 1024).astype(int), 0, 1023)]
    x += rng.normal(0.0, ruido_uV, n)
    return x, np.asarray(tempos), t_ad, t_pa

def eog_sintetico(fs=250, dur_s=32.0, ruido_uV=3.0, semente=7):
    """H e V sintéticos: piscadas (tabela _tabela_piscada, 240 µV, 300 ms) em
    t = 3, 12 e 21 s no vertical; sacadas (rampa _tabela_sacada de 60 ms)
    para a direita em 5 s (volta em 8), esquerda em 14 (volta em 17) no
    horizontal; para cima em 24 (volta em 26) e para baixo em 27 (volta em
    29) no vertical. Deriva lenta + ruído N(0, 3). Devolve (h, v, esperados)
    com esperados = {"piscadas": [t...], "sacadas": [(t, direcao), ...]}."""
    rng = np.random.default_rng(semente)
    n = int(dur_s * fs)
    tt = np.arange(n) / fs
    h = np.zeros(n)
    v = np.zeros(n)
    rampa = _tabela_sacada(max(2, int(0.06 * fs)))
    pisc = _tabela_piscada(max(2, int(0.30 * fs)))

    def degrau(sinal, t0, de, para):
        i0 = int(t0 * fs)
        for k, r in enumerate(rampa):
            if i0 + k < n:
                sinal[i0 + k] = de + (para - de) * r
        sinal[min(n, i0 + len(rampa)):] = para

    piscadas = [3.0, 12.0, 21.0]
    sac_h = [(5.0, 0.0, 240.0, "direita"), (8.0, 240.0, 0.0, "esquerda"),
             (14.0, 0.0, -240.0, "esquerda"), (17.0, -240.0, 0.0, "direita")]
    sac_v = [(24.0, 0.0, 200.0, "cima"), (26.0, 200.0, 0.0, "baixo"),
             (27.0, 0.0, -200.0, "baixo"), (29.0, -200.0, 0.0, "cima")]
    for t0, de, para, _d in sac_h:
        degrau(h, t0, de, para)
    for t0, de, para, _d in sac_v:
        degrau(v, t0, de, para)
    for tp in piscadas:
        i0 = int((tp - 0.15) * fs)
        idx = np.arange(i0, min(n, i0 + len(pisc)))
        v[idx] += 240.0 * pisc[:idx.size]
    deriva = np.cumsum(rng.normal(0.0, 0.6, n))
    deriva -= np.linspace(deriva[0], deriva[-1], n)
    h += 0.3 * deriva + rng.normal(0.0, ruido_uV, n)
    v += 0.3 * deriva[::-1] + rng.normal(0.0, ruido_uV, n)
    esperados = {"piscadas": piscadas,
                 "sacadas": [(s[0], s[3]) for s in sac_h] + [(s[0], s[3]) for s in sac_v],
                 "t_axis": tt}
    return h, v, esperados


def _carrega():
    """Devolve o "módulo" P7: o ROA.py mais os geradores sintéticos acima."""
    m = _Sinteticos()
    for nome in _NOMES_SINTETICOS:
        setattr(m, nome, globals()[nome])
    return m


_NOMES_SINTETICOS = ['_tabela_ecg', '_tabela_piscada', '_tabela_sacada', 'ecg_sintetico', 'eog_sintetico']


class TestP7(unittest.TestCase):
    """Base: carrega o módulo e os sinais sintéticos uma vez."""

    @classmethod
    def setUpClass(cls):
        cls.p7 = _carrega()
        cls.fs = 250
        cls.ecg, cls.tempos_r, cls.t_ad, cls.t_pa = cls.p7.ecg_sintetico(cls.fs)
        cls.det = cls.p7.detectar_batidas_gravacao(cls.ecg, cls.fs)
        cls.h, cls.v, cls.esperados = cls.p7.eog_sintetico(cls.fs)
        cls.olhos = cls.p7.detectar_eventos_olhos(cls.h, cls.v, cls.fs, 80.0)


class TestECG(TestP7):
    """Detecção, classificação e correção das batidas."""

    def test_acha_todas_as_batidas(self):
        ts = [b["t"] for b in self.det["batidas"]]
        self.assertEqual(len(ts), len(self.tempos_r))
        for t_ref, t in zip(self.tempos_r, ts):
            self.assertLess(abs(t_ref - t), 0.040, (t_ref, t))
        self.assertEqual(self.det["versao"], 1)
        self.assertEqual(self.det["fs"], 250.0)
        self.assertIsNone(self.det["batidas"][0]["rr_ms"])
        self.assertTrue(all(b["origem"] == "auto" for b in self.det["batidas"]))

    def test_classifica_adiantada_e_pausa(self):
        self.assertEqual(self.det["n_adiantadas"], 1)
        self.assertEqual(self.det["n_pausas"], 1)
        ad = [b for b in self.det["batidas"] if b["tipo"] == "adiantada"][0]
        pa = [b for b in self.det["batidas"] if b["tipo"] == "pausa"][0]
        self.assertLess(abs(ad["t"] - self.t_ad), 0.040)
        self.assertLess(abs(pa["t"] - self.t_pa), 0.040)
        self.assertLess(abs(ad["rr_ms"] - 520.0), 40.0)
        self.assertLess(abs(pa["rr_ms"] - 1700.0), 40.0)
        self.assertAlmostEqual(self.det["bpm_medio"], 69.4, delta=1.5)

    def test_mesmo_criterio_do_painel(self):
        """Os ectópicos contados pela mesma chamada da tela são exatamente
        as batidas não regulares do replay."""
        import numpy as np
        rr = np.diff([b["t"] for b in self.det["batidas"]]) * 1000.0
        _c, idx = self.p7.correct_ectopic_rr(rr, threshold=0.30)
        nao_regulares = [i for i, b in enumerate(self.det["batidas"]) if b["tipo"] != "normal"]
        self.assertEqual(sorted(int(i) + 1 for i in idx), nao_regulares)

    def test_corrige_adicionar_no_meio_da_pausa(self):
        pa = [b for b in self.det["batidas"] if b["tipo"] == "pausa"][0]
        meio = pa["t"] - pa["rr_ms"] / 2000.0
        novas = self.p7.aplicar_correcoes(self.det["batidas"], [{"acao": "adicionar", "t": meio}])
        self.assertEqual(len(novas), len(self.det["batidas"]) + 1)
        r = self.p7.resumo_batidas(novas)
        self.assertEqual(r["n_pausas"], 0)
        self.assertEqual(r["n_adiantadas"], 1)
        add = [b for b in novas if abs(b["t"] - meio) < 1e-6][0]
        self.assertEqual(add["origem"], "manual")
        self.assertEqual(add["tipo"], "normal")
        # a lista original não mudou
        self.assertEqual(self.p7.resumo_batidas(self.det["batidas"])["n_pausas"], 1)

    def test_corrige_remover_cria_pausa_nos_vizinhos(self):
        b10 = self.det["batidas"][10]
        novas = self.p7.aplicar_correcoes(self.det["batidas"], [{"acao": "remover", "t": b10["t"] + 0.02}])
        self.assertEqual(len(novas), len(self.det["batidas"]) - 1)
        r = self.p7.resumo_batidas(novas)
        self.assertEqual(r["n_pausas"], 2)         # o buraco vira "pausa" pelo mesmo critério
        self.assertLess(abs(novas[10]["rr_ms"] - 2 * 857.0), 120.0)

    def test_corrige_tipo_fica_fixo(self):
        ad = [b for b in self.det["batidas"] if b["tipo"] == "adiantada"][0]
        novas = self.p7.aplicar_correcoes(self.det["batidas"],
                                          [{"acao": "tipo", "t": ad["t"], "tipo": "normal"}])
        r = self.p7.resumo_batidas(novas)
        self.assertEqual(r["n_adiantadas"], 0)
        b = [x for x in novas if abs(x["t"] - ad["t"]) < 1e-6][0]
        self.assertTrue(b.get("tipo_fixo"))
        self.assertEqual(b["origem"], "manual")
        # e sobrevive a uma segunda rodada de correções em outro ponto
        novas2 = self.p7.aplicar_correcoes(novas, [{"acao": "remover", "t": novas[3]["t"]}])
        self.assertEqual(self.p7.resumo_batidas(novas2)["n_adiantadas"], 0)

    def test_salvar_carregar_batidas(self):
        pasta = tempfile.mkdtemp(prefix="p7_bat_")
        corr = [{"acao": "tipo", "t": 1.0, "tipo": "normal"}]
        caminho = self.p7.salvar_batidas(pasta, self.det, corr)
        self.assertEqual(caminho, self.p7.caminho_batidas(pasta))
        self.assertTrue(caminho.endswith("batidas.json"))
        lido = self.p7.carregar_batidas(pasta)
        self.assertEqual(lido["versao"], 1)
        self.assertEqual(lido["fs"], 250.0)
        self.assertEqual(lido["correcoes"], corr)
        self.assertIn("gerado_em", lido)
        self.assertEqual(len(lido["batidas"]), len(self.det["batidas"]))
        self.assertEqual(lido["n_adiantadas"], 1)
        self.assertEqual(lido["n_pausas"], 1)
        self.assertAlmostEqual(lido["bpm_medio"], self.det["bpm_medio"], places=6)
        self.assertIsNone(self.p7.carregar_batidas(pasta + "_nao_existe"))


class TestEOG(TestP7):
    """Piscadas, sacadas, direção, inversão, frases e olhar."""

    def test_acha_piscadas_e_sacadas(self):
        pisc = [e for e in self.olhos["eventos"] if e["tipo"] == "piscada"]
        self.assertEqual(len(pisc), 3)
        self.assertEqual(self.olhos["n_piscadas"], 3)
        for t_ref, e in zip(self.esperados["piscadas"], pisc):
            self.assertLess(abs(e["t"] - t_ref), 0.060, (t_ref, e["t"]))
            self.assertIsNone(e["direcao"])
            self.assertGreater(e["dur_s"], 0.05)
        sac = [e for e in self.olhos["eventos"] if e["tipo"] == "sacada"]
        self.assertEqual(len(sac), 8)
        self.assertEqual(self.olhos["n_sacadas"], 4)     # horizontais, como o PDF
        self.assertEqual(self.olhos["n_sacadas_v"], 4)
        for t_ref, d_ref in self.esperados["sacadas"]:
            cand = [e for e in sac if abs(e["t"] - t_ref) < 0.1]
            self.assertEqual(len(cand), 1, (t_ref, d_ref))
            self.assertEqual(cand[0]["direcao"], d_ref, (t_ref, d_ref))
        self.assertAlmostEqual(self.olhos["taxa_piscadas_min"], 3 / (32.0 / 60.0), places=3)

    def test_inverter_horizontal_troca_direita_esquerda(self):
        inv = self.p7.detectar_eventos_olhos(self.h, self.v, self.fs, 80.0, inverter_h=True)
        oposta = {"direita": "esquerda", "esquerda": "direita"}
        for e0, e1 in zip(self.olhos["eventos"], inv["eventos"]):
            self.assertAlmostEqual(e0["t"], e1["t"])
            if e0["direcao"] in oposta:
                self.assertEqual(e1["direcao"], oposta[e0["direcao"]])
            else:
                self.assertEqual(e1["direcao"], e0["direcao"])
        self.assertTrue(inv["inverter_h"])
        # inverter_direcoes dá o mesmo sem detectar de novo
        inv2 = self.p7.inverter_direcoes(self.olhos, True, False)
        self.assertEqual([e["direcao"] for e in inv2["eventos"]],
                         [e["direcao"] for e in inv["eventos"]])
        inv3 = self.p7.inverter_direcoes(inv2, False, True)
        for e0, e3 in zip(self.olhos["eventos"], inv3["eventos"]):
            if e0["direcao"] == "cima":
                self.assertEqual(e3["direcao"], "baixo")
            if e0["direcao"] == "direita":
                self.assertEqual(e3["direcao"], "direita")

    def test_sem_limiar_usa_detector_do_pdf(self):
        d = self.p7.detectar_eventos_olhos(self.h, self.v, self.fs, None)
        self.assertEqual(d["n_piscadas"], 3)
        self.assertIsNone(d["limiar_uV"])

    def test_texto_evento_e_fmt_mmss(self):
        f = self.p7.fmt_mmss
        self.assertEqual(f(3), "0:03")
        self.assertEqual(f(65), "1:05")
        self.assertEqual(f(11.99), "0:12")
        self.assertEqual(f(3725), "1:02:05")
        self.assertEqual(f(None), "0:00")
        te = self.p7.texto_evento
        self.assertEqual(te({"t": 3.0, "tipo": "piscada"}), "0:03 piscou")
        self.assertEqual(te({"t": 5.0, "tipo": "sacada", "direcao": "direita"}), "0:05 olhou para a direita")
        self.assertEqual(te({"t": 5.0, "tipo": "sacada", "direcao": "esquerda"}), "0:05 olhou para a esquerda")
        self.assertEqual(te({"t": 65.0, "tipo": "sacada", "direcao": "cima"}), "1:05 olhou para cima")
        self.assertEqual(te({"t": 65.0, "tipo": "sacada", "direcao": "baixo"}), "1:05 olhou para baixo")
        self.assertEqual(te({"t": 9.0, "tipo": "fixacao", "direcao": "cima", "dur_s": 1.2}),
                         "0:09 ficou olhando para cima por 1,2 s")

    def test_fmt_num_virgula_por_idioma(self):
        p7 = self.p7
        anterior = p7.I18N.current
        try:
            p7.I18N.current = "pt"
            self.assertEqual(p7.fmt_num(1.8, 1), "1,8")
            p7.I18N.current = "en"
            self.assertEqual(p7.fmt_num(1.8, 1), "1.8")
            p7.I18N.current = "de"
            self.assertEqual(p7.fmt_num(2.25, 2), "2,25")
            self.assertEqual(p7.fmt_num(None, 1), "—")
        finally:
            p7.I18N.current = anterior

    def test_olhar_no_instante_com_inversao(self):
        o = self.p7.olhar_no_instante
        gx, gy = o(self.h, self.v, self.fs, 6.5, False, False, 160.0)
        self.assertGreater(gx, 0.5)
        self.assertLess(abs(gy), 0.3)
        gx_i, gy_i = o(self.h, self.v, self.fs, 6.5, True, False, 160.0)
        self.assertLess(gx_i, -0.5)
        self.assertAlmostEqual(gy_i, gy)
        gx, gy = o(self.h, self.v, self.fs, 25.0, False, False, 160.0)
        self.assertGreater(gy, 0.5)
        _, gy_i = o(self.h, self.v, self.fs, 25.0, False, True, 160.0)
        self.assertLess(gy_i, -0.5)
        gx, gy = o(self.h, self.v, self.fs, 1.0, False, False, 160.0)
        self.assertLess(abs(gx), 0.3)
        self.assertLess(abs(gy), 0.3)
        self.assertEqual(self.p7.direcao_do_olhar(0.9, 0.1), "direita")
        self.assertEqual(self.p7.direcao_do_olhar(0.9, 0.8), "cima")   # vertical primeiro, como a tela
        self.assertEqual(self.p7.direcao_do_olhar(0.1, 0.1), "centro")

    def test_correcoes_e_json_olhos(self):
        ev = self.olhos["eventos"]
        novos = self.p7.aplicar_correcoes_olhos(ev, [
            {"acao": "remover", "t": ev[0]["t"]},
            {"acao": "adicionar", "t": 30.0, "tipo": "piscada"},
            {"acao": "tipo", "t": 5.0, "tipo": "sacada", "direcao": "esquerda"}])
        self.assertEqual(len(novos), len(ev))
        self.assertEqual(novos[-1]["t"], 30.0)
        self.assertEqual(novos[-1]["origem"], "manual")
        e5 = [e for e in novos if abs(e["t"] - 5.0) < 0.1][0]
        self.assertEqual(e5["direcao"], "esquerda")
        pasta = tempfile.mkdtemp(prefix="p7_olhos_")
        d2 = dict(self.olhos)
        d2["eventos"] = novos
        caminho = self.p7.salvar_olhos(pasta, d2, [{"acao": "remover", "t": 3.0}], dur_s=32.0)
        self.assertEqual(caminho, self.p7.caminho_olhos(pasta))
        lido = self.p7.carregar_olhos(pasta)
        self.assertEqual(lido["versao"], 1)
        self.assertEqual(lido["limiar_uV"], 80.0)
        self.assertEqual(len(lido["eventos"]), len(novos))
        self.assertEqual(lido["n_piscadas"], 3)
        self.assertEqual(lido["n_sacadas"], 4)
        self.assertEqual(lido["correcoes"], [{"acao": "remover", "t": 3.0}])
        self.assertIn("gerado_em", lido)


class TestWidgets(TestP7):
    """Os widgets pintam sem erro e rápido, e a faixa responde ao clique."""

    def _mede(self, w, tamanho=(400, 300), n=50):
        w.resize(*tamanho)
        pix = QtGui.QPixmap(*tamanho)
        w.render(pix)
        t0 = time.perf_counter()
        for _ in range(n):
            w.render(pix)
        return (time.perf_counter() - t0) / n * 1000.0

    def test_coracao_pinta(self):
        w = self.p7.CoracaoReplayWidget()
        w.set_batidas(self.det["batidas"])
        for t in (0.0, self.det["batidas"][5]["t"] + 0.05, self.t_ad + 0.02, self.t_pa + 0.3):
            w.set_tempo(t)
            self.assertLess(self._mede(w), 12.0)
        w.set_tempo(self.det["batidas"][5]["t"] + 0.02)
        self.assertGreater(w.pulso(), 0.3)
        w.set_tempo(self.det["batidas"][5]["t"] + 0.7)
        self.assertLess(w.pulso(), 0.1)
        w.set_tempo(self.t_ad + 0.01)
        self.assertEqual(self.det["batidas"][w.batida_atual()]["tipo"], "adiantada")

    def test_olhos_pintam_e_piscam(self):
        w = self.p7.OlhosReplayWidget()
        w.set_eventos(self.olhos)
        w.set_olhar(0.8, 0.0)
        w.set_tempo(6.5)
        self.assertLess(self._mede(w), 12.0)
        self.assertEqual(w.fechamento(), 0.0)
        w.set_tempo(self.esperados["piscadas"][1])
        self.assertGreater(w.fechamento(), 0.9)
        self.assertLess(self._mede(w), 12.0)
        w.set_inverter(True, False)
        self.assertEqual(w.olhar_mostrado()[0], -0.8)
        self.assertEqual(w.contadores(), (2, 2, 0))

    def test_listas_pintam(self):
        for cls, dados in ((self.p7.ListaBatidasWidget, self.det["batidas"]),
                           (self.p7.LinhaDoTempoOlhosWidget, self.olhos)):
            w = cls()
            (w.set_batidas if cls is self.p7.ListaBatidasWidget else w.set_eventos)(dados)
            self.assertLess(self._mede(w), 12.0)
        lb = self.p7.ListaBatidasWidget()
        lb.set_batidas(self.det["batidas"])
        self.assertEqual(lb.count(), 3)                      # resumo + adiantada + pausa
        self.assertIn("68 batidas", lb.item(0).text())
        self.assertIn("batida adiantada", lb.item(1).text())
        self.assertIn("pausa maior (1,7 s)", lb.item(2).text())
        lt = self.p7.LinhaDoTempoOlhosWidget()
        lt.set_eventos(self.olhos)
        self.assertEqual(lt.count(), 11)
        self.assertEqual(lt.item(0).text(), "0:03 piscou")
        lt.set_tempo(15.5)
        self.assertEqual(lt.currentRow(), 4)

    def test_faixa_clique_emite_indice(self):
        w = self.p7.FaixaBatidasWidget()
        w.set_duracao(len(self.ecg) / self.fs)
        w.set_batidas(self.det["batidas"])
        w.resize(900, 80)
        w.show()
        QtWidgets.QApplication.processEvents()
        self.assertLess(self._mede(w, (900, 80)), 12.0)
        recebidos, tempos = [], []
        w.batidaClicada.connect(recebidos.append)
        w.cursorMovido.connect(tempos.append)
        alvo = 30
        x = int(round(w.tempo_para_x(self.det["batidas"][alvo]["t"])))
        QTest.mouseClick(w, QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.KeyboardModifier.NoModifier,
                         QtCore.QPoint(x, 30))
        self.assertEqual(recebidos, [alvo])
        self.assertAlmostEqual(tempos[-1], self.det["batidas"][alvo]["t"], places=6)
        # clique longe de qualquer marca: só move o cursor
        x_vazio = int(round(w.tempo_para_x(self.t_pa - 0.85)))
        QTest.mouseClick(w, QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.KeyboardModifier.NoModifier,
                         QtCore.QPoint(x_vazio, 30))
        self.assertEqual(recebidos, [alvo])
        self.assertLess(abs(tempos[-1] - (self.t_pa - 0.85)), 0.2)
        # menu de correção só em modo edição
        self.assertIsNone(w.menu_correcao(x))
        w.set_edicao(True)
        menu = w.menu_correcao(x)
        rotulos = [a.text() for a in menu.actions() if a.text()]
        self.assertIn("Remover batida", rotulos)
        pedidos = []
        w.correcaoPedida.connect(pedidos.append)
        menu.actions()[0].trigger()
        self.assertEqual(pedidos[0]["acao"], "remover")
        self.assertAlmostEqual(pedidos[0]["t"], self.det["batidas"][alvo]["t"])
        menu2 = w.menu_correcao(x_vazio)
        self.assertEqual([a.text() for a in menu2.actions()], ["Adicionar batida aqui"])
        w.close()


if __name__ == "__main__":
    unittest.main()
