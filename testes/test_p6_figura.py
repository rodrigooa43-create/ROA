# -*- coding: utf-8 -*-
"""P6 — figura articulada que SIMULA o movimento marcado (replay de EMG), dentro do ROA.py.

Roda offscreen.
"""
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA, app  # noqa: E402  (a figura vive dentro do ROA.py)
from PySide6 import QtCore, QtGui, QtWidgets  # noqa: E402

COMMON_MUSCLES = list(ROA.COMMON_MUSCLES)
TEMA_CLARO = dict(ROA.THEMES["ROA (azul clinico)"])
TEMA_ESCURO = dict(ROA.THEMES["ROA Escuro"])
M = ROA
ROA._apply_theme_colors("ROA (azul clinico)")
CHAVES_POSE = set(M.POSE_REPOUSO.keys())


class TestPose(unittest.TestCase):
    """pose_do_movimento: chaves válidas, repouso nas pontas, sinais da rotação."""

    def test_chaves_validas_e_volta_ao_repouso(self):
        for mov in M.MOVIMENTOS:
            for fase in (0.0, 0.5, 1.0):
                d = M.pose_do_movimento(mov, fase)
                self.assertEqual(set(d.keys()), CHAVES_POSE, mov)
            for fase in (0.0, 1.0):
                for k, v in M.pose_do_movimento(mov, fase).items():
                    self.assertAlmostEqual(v, 0.0, places=6, msg="%s/%s em fase %s" % (mov, k, fase))
                pose = M.pose_mesclada([(mov, fase)])
                for k in CHAVES_POSE:
                    self.assertAlmostEqual(pose[k], M.POSE_REPOUSO[k], places=6, msg="%s/%s" % (mov, k))
        # faixa longa (sustentada) também volta ao repouso
        for k, v in M.pose_do_movimento("pinca", 1.0, duracao_s=8.0).items():
            self.assertAlmostEqual(v, 0.0, places=6)
        self.assertAlmostEqual(M.perfil_movimento(0.5, duracao_s=8.0), 1.0, places=6)

    def test_pico_move_alguma_coisa(self):
        for mov in M.MOVIMENTOS:
            if mov in ("repouso", "a_definir"):
                continue
            d = M.pose_do_movimento(mov, 0.5)
            self.assertTrue(any(abs(v) > 1e-6 for v in d.values()), mov)

    def test_supinacao_e_pronacao_opostas(self):
        sup = M.pose_do_movimento("supinacao", 0.5)["pronacao"]
        pro = M.pose_do_movimento("pronacao", 0.5)["pronacao"]
        self.assertLess(sup, -0.5)
        self.assertGreater(pro, 0.5)
        self.assertLess(sup * pro, 0.0)
        # e na pose final (com repouso somado) o sinal se mantém
        self.assertLess(M.pose_mesclada([("supinacao", 0.5)])["pronacao"], -0.5)
        self.assertGreater(M.pose_mesclada([("pronacao", 0.5)])["pronacao"], 0.5)

    def test_mesclada_soma_e_clampa(self):
        um = M.pose_mesclada([("flexao_ombro", 0.5)])["ombro"]
        meio = M.pose_mesclada([("flexao_ombro", 0.5, 0.5)])["ombro"]
        self.assertAlmostEqual(meio - M.POSE_REPOUSO["ombro"], (um - M.POSE_REPOUSO["ombro"]) / 2.0, places=6)
        dois = M.pose_mesclada([("flexao_ombro", 0.5), ("flexao_ombro", 0.5)])["ombro"]
        self.assertGreater(dois, um)           # somou
        for k, (lo, hi) in M.LIMITES_POSE.items():
            self.assertLessEqual(dois if k == "ombro" else M.POSE_REPOUSO[k], hi)
        cot = M.pose_mesclada([("flexao_cotovelo", 0.5), ("flexao_cotovelo", 0.5)])["cotovelo"]
        self.assertAlmostEqual(cot, M.LIMITES_POSE["cotovelo"][1], places=6)   # clampou
        for pose in (M.pose_mesclada([("supinacao", 0.5), ("supinacao", 0.5), ("fechar_mao", 0.5)]),
                     M.pose_mesclada([("extensao_ombro", 0.5), ("extensao_ombro", 0.5)])):
            for k, (lo, hi) in M.LIMITES_POSE.items():
                self.assertGreaterEqual(pose[k], lo, k)
                self.assertLessEqual(pose[k], hi, k)
        # faixa de mão junto com gesto de braço não levanta o cotovelo por conta própria
        so_ombro = M.pose_mesclada([("flexao_ombro", 0.5, 0.36)])["cotovelo"]
        com_mao = M.pose_mesclada([("flexao_ombro", 0.5, 0.36), ("fechar_mao", 0.5)])["cotovelo"]
        self.assertAlmostEqual(so_ombro, com_mao, places=6)


class TestTarefas(unittest.TestCase):
    """TAREFAS: chaves válidas, objeto conhecido, duração coberta sem buracos."""

    def test_trechos_validos_e_sem_buracos(self):
        for nome, t in M.TAREFAS.items():
            self.assertIn(t["objeto"], ("halter", "chave", "copo"), nome)
            self.assertTrue(t["titulo"], nome)
            dur = float(t["duracao_s"])
            self.assertGreater(dur, 0.0)
            for trecho in t["trechos"]:
                self.assertIn(trecho[0], M.MOVIMENTOS_INFO, "%s: %s" % (nome, trecho[0]))
                self.assertTrue(0.0 <= trecho[1] < trecho[2] <= 1.0, (nome, trecho))
            passo = 0.05 / dur                      # 50 ms
            buraco, maior = 0.0, 0.0
            k = 0
            while k * passo <= 1.0:
                tf = k * passo
                if M.movimentos_da_tarefa(nome, tf):
                    buraco = 0.0
                else:
                    buraco += passo * dur
                    maior = max(maior, buraco)
                k += 1
            self.assertLessEqual(maior, 1.0, "%s: buraco de %.2f s" % (nome, maior))
            for tf in (0.0, 0.25, 0.5, 0.75, 1.0):
                pose = M.pose_da_tarefa(nome, tf)
                self.assertEqual(set(pose.keys()), CHAVES_POSE)
                for kk, (lo, hi) in M.LIMITES_POSE.items():
                    self.assertTrue(lo <= pose[kk] <= hi, (nome, tf, kk))

    def test_musculos_esperados_so_do_common_muscles(self):
        self.assertEqual(set(M.MUSCULOS_ESPERADOS.keys()), set(M.MOVIMENTOS_INFO.keys()))
        for mov, ms in M.MUSCULOS_ESPERADOS.items():
            for m in ms:
                self.assertIn(m, COMMON_MUSCLES, "%s -> %s" % (mov, m))
        self.assertEqual(M.MUSCULOS_ESPERADOS["repouso"], [])
        self.assertEqual(M.MUSCULOS_ESPERADOS["a_definir"], [])
        self.assertEqual(M.MUSCULOS_ESPERADOS["flexao_cotovelo"], ["Bíceps Braquial"])
        self.assertEqual(set(M.MUSCULOS_ESPERADOS["flexao_ombro"]), {"Deltoide Anterior", "Peitoral Maior"})
        for m in M.MUSCULOS_FIGURA:
            self.assertIn(m, COMMON_MUSCLES)

    def test_chaves_canonicas(self):
        esperadas = {"repouso", "flexao_cotovelo", "extensao_cotovelo", "supinacao", "pronacao",
                     "flexao_punho", "extensao_punho", "abrir_mao", "fechar_mao", "pinca",
                     "flexao_ombro", "extensao_ombro", "a_definir"}
        self.assertEqual(set(M.MOVIMENTOS_INFO.keys()), esperadas)


class TestWidget(unittest.TestCase):
    """O widget pinta cada movimento e objeto sem erro e rápido, nos dois temas."""

    def _pintar(self, w, larg=480, alt=360):
        pm = QtGui.QPixmap(larg, alt)
        pm.fill(QtGui.QColor("#ffffff"))
        pt = QtGui.QPainter(pm)
        try:
            w.pintar(pt, QtCore.QRect(0, 0, larg, alt))
        finally:
            pt.end()
        return pm

    def test_pinta_tudo_sem_erro_e_rapido(self):
        w = M.FiguraMovimentoWidget()
        w.resize(480, 360)
        self._pintar(w)                       # aquece fontes
        n, total = 0, 0.0
        for objeto in (None, "halter", "chave", "copo"):
            w.set_objeto(objeto)
            for mov in M.MOVIMENTOS:
                for fase in (0.0, 0.5, 0.8):
                    w.set_pose(M.pose_mesclada([(mov, fase)]))
                    w.set_ativacao({m: 0.9 for m in M.MUSCULOS_ESPERADOS[mov]})
                    w.set_rotulo_movimento(M.MOVIMENTOS_INFO[mov]["titulo"])
                    t0 = time.perf_counter()
                    self._pintar(w)
                    total += time.perf_counter() - t0
                    n += 1
        media_ms = total / n * 1000.0
        self.assertLess(media_ms, 12.0, "pintura média %.2f ms" % media_ms)

    def test_ativacao_ignora_musculos_fora_da_figura(self):
        w = M.FiguraMovimentoWidget()
        w.set_ativacao({m: 0.7 for m in COMMON_MUSCLES})
        w.set_ativacao({"Sóleo": 1.0, "Bíceps Braquial": 2.0, "Trapézio": "x", "Inexistente": 0.5})
        self.assertEqual(w._ativacao, {"Bíceps Braquial": 1.0})
        self._pintar(w)
        w.set_objeto("coisa")                 # objeto desconhecido vira None
        self.assertIsNone(w._objeto)
        w.set_pose({"cotovelo": 999, "pronacao": -5, "lixo": 1})
        self.assertEqual(w.pose()["cotovelo"], M.LIMITES_POSE["cotovelo"][1])
        self.assertEqual(w.pose()["pronacao"], -1.0)
        self._pintar(w)

    def test_tamanhos_e_tema_escuro(self):
        w = M.FiguraMovimentoWidget()
        w.set_objeto("copo")
        w.set_pose(M.pose_da_tarefa("copo_a_boca", 0.5))
        w.set_ativacao({"Bíceps Braquial": 0.8})
        for larg, alt in ((240, 200), (800, 600), (1200, 300), (300, 900)):
            pm = self._pintar(w, larg, alt)
            self.assertFalse(pm.isNull())
        M.COLORS.clear()
        M.COLORS.update(TEMA_ESCURO)
        try:
            pm = self._pintar(w)
            # fundo do tema escuro foi usado de verdade
            self.assertEqual(QtGui.QColor(pm.toImage().pixel(2, 2)).name(), TEMA_ESCURO["surface"])
        finally:
            M.COLORS.clear()
            M.COLORS.update(TEMA_CLARO)

    def test_widget_de_verdade_render(self):
        w = M.FiguraMovimentoWidget()
        w.resize(480, 360)
        w.set_pose(M.pose_mesclada([("supinacao", 0.5)]))
        pm = QtGui.QPixmap(480, 360)
        w.render(pm)                           # caminho do paintEvent
        self.assertFalse(pm.isNull())


if __name__ == "__main__":
    unittest.main()
