# -*- coding: utf-8 -*-
"""P8 — Replay dentro de "Rever uma gravação": botão, tocador único e as três
cenas (músculos, coração, olhos), nos dois níveis, com gravações sintéticas.

As gravações são escritas no formato nativo (data.csv + summary.json) numa
pasta temporária; nenhum dado de pessoa.
"""
import csv
import json
import os
import sys
import tempfile
import time
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA, app, processar_eventos  # noqa: E402
from PySide6 import QtCore, QtWidgets  # noqa: E402

FS = 250


def _ecg(dur_s, rng):
    """ECG sintético: pulsos gaussianos a ~72 bpm com uma batida adiantada e uma pausa."""
    n = int(dur_s * FS)
    t = np.arange(n) / FS
    y = rng.normal(0, 6.0, n)
    tb, batidas = 0.6, []
    while tb < dur_s - 0.5:
        batidas.append(tb)
        rr = 0.83
        if abs(tb - 12.0) < 0.5:
            rr = 0.52          # batida adiantada
        elif abs(tb - 24.0) < 0.5:
            rr = 1.70          # pausa
        tb += rr
    for b in batidas:
        y += 900.0 * np.exp(-((t - b) / 0.012) ** 2) - 150.0 * np.exp(-((t - b - 0.04) / 0.02) ** 2)
    return y


def _eog(dur_s, rng):
    """EOG sintético: piscadas no vertical e sacadas no horizontal."""
    n = int(dur_s * FS)
    t = np.arange(n) / FS
    h = rng.normal(0, 3.0, n)
    v = rng.normal(0, 3.0, n)
    for tp in (3.0, 12.0, 21.0):
        v += 240.0 * np.exp(-((t - tp) / 0.06) ** 2)
    # sacadas com rampa de 60 ms (um degrau instantâneo não tem velocidade
    # mensurável para o detector) e volta ao centro 1 s depois
    for ts_, sinal in ((6.0, 1), (9.0, -1), (15.0, 1), (18.0, -1)):
        sobe = np.clip((t - ts_) / 0.06, 0.0, 1.0)
        desce = np.clip((t - (ts_ + 1.0)) / 0.06, 0.0, 1.0)
        h += sinal * 240.0 * (sobe - desce)
    return h, v


def _emg(dur_s, rng, n_can=2):
    """EMG sintético: ruído com rajadas (contrações) em instantes fixos."""
    n = int(dur_s * FS)
    t = np.arange(n) / FS
    out = []
    for c in range(n_can):
        base = rng.normal(0, 4.0, n)
        for t0 in (4.0 + c * 1.0, 11.0 + c * 1.0, 19.0 + c * 1.0):
            m = (t >= t0) & (t < t0 + 2.0)
            base[m] += rng.normal(0, 60.0, int(m.sum()))
        out.append(base)
    return np.vstack(out)


def _grava_sessao(pasta, modo, canais, tipos, musculos=None, marcadores=None, report=None):
    """Escreve data.csv + summary.json no formato nativo do ROA."""
    os.makedirs(pasta, exist_ok=True)
    n_ch, n = canais.shape
    with open(os.path.join(pasta, "data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp_s"] + ["CH%d_uV" % (i + 1) for i in range(n_ch)]
                   + ["ax_g", "ay_g", "az_g", "marker"])
        marc = dict((int(round(t * FS)), lab) for t, lab in (marcadores or []))
        for i in range(n):
            w.writerow(["%.6f" % (i / FS)] + ["%.4f" % v for v in canais[:, i]]
                       + ["0", "0", "1", marc.get(i, "")])
    resumo = {"session_name": os.path.basename(pasta), "acquisition_mode": modo,
              "num_channels": n_ch, "sample_rate": FS,
              "hardware": {"channel_types": list(tipos),
                           "channel_muscles": list(musculos or [""] * n_ch),
                           "data_source": "synthetic"},
              "report_channels": report or {}}
    with open(os.path.join(pasta, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)
    return os.path.join(pasta, "data.csv")


class TestReplay(unittest.TestCase):
    """Uma janela para a classe toda; gravações sintéticas de cada exame."""

    @classmethod
    def setUpClass(cls):
        rng = np.random.default_rng(7)
        cls.raiz = tempfile.mkdtemp(prefix="roa_p8_")
        dur = 30.0
        emg = _emg(dur, rng)
        cls.csv_emg = _grava_sessao(os.path.join(cls.raiz, "emg"), "EMG", emg, ["EMG", "EMG"],
                                    ["Bíceps Braquial", "Tríceps Braquial"],
                                    marcadores=[(3.5, "Flexão"), (10.5, "Extensão"), (18.5, "Repouso")])
        ecg = _ecg(dur, rng)[None, :]
        cls.csv_ecg = _grava_sessao(os.path.join(cls.raiz, "ecg"), "ECG", ecg, ["ECG"],
                                    report={"ecg": 0})
        h, v = _eog(dur, rng)
        cls.csv_eog = _grava_sessao(os.path.join(cls.raiz, "eog"), "EoG", np.vstack([h, v]),
                                    ["EoG", "EoG"], report={"eog_h": 0, "eog_v": 1, "eog_threshold": 80.0})
        eeg = rng.normal(0, 10.0, (2, int(dur * FS)))
        cls.csv_eeg = _grava_sessao(os.path.join(cls.raiz, "eeg"), "EEG", eeg, ["EEG", "EEG"])
        cls.win = ROA.EEGCollectorWindow()
        cls.win.config.ui_level = "avancado"
        cls.win._definir_nivel("avancado")
        processar_eventos(50)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.win.close()
        except Exception:
            pass

    def _abre(self, csv_path):
        self.win._offline_load_csv(csv_path)
        processar_eventos(50)
        dlg = getattr(self.win, "_replay_dlg", None)
        if dlg is not None:
            try:
                dlg.close()
            except Exception:
                pass
        self.win._offline_abrir_replay()
        processar_eventos(50)
        return self.win._replay_dlg

    def test_botao_segue_o_exame(self):
        win = self.win
        win._offline_load_csv(self.csv_eeg)
        processar_eventos(30)
        self.assertFalse(win.offline_replay_btn.isEnabled())
        for c in (self.csv_emg, self.csv_ecg, self.csv_eog):
            win._offline_load_csv(c)
            processar_eventos(30)
            self.assertTrue(win.offline_replay_btn.isEnabled(), c)
        self.assertIn(win.offline_replay_btn, win._offline_botoes)
        # o botão não é "avançado": existe nos dois níveis
        self.assertNotIn(win.offline_replay_btn, win._detail_widgets.get("ui", []))

    def test_exame_da_gravacao(self):
        self.assertEqual(ROA.replay_exame_da_gravacao("EMG", []), "EMG")
        self.assertEqual(ROA.replay_exame_da_gravacao("Hibrido", ["EEG", "ECG", "ECG"]), "ECG")
        self.assertIsNone(ROA.replay_exame_da_gravacao("EEG", ["EEG", "EEG"]))
        self.assertIsNone(ROA.replay_exame_da_gravacao(None, []))

    def test_replay_musculos(self):
        dlg = self._abre(self.csv_emg)
        self.assertIsInstance(dlg, ROA.ReplayDialog)
        cena = dlg.cena
        self.assertIsInstance(cena, ROA.CenaReplayEMG)
        # trechos nasceram dos marcadores (Flexão/Extensão/Repouso)
        self.assertGreaterEqual(cena.modelo.total_trechos(), 3)
        movs = [tr["movimento"] for _f, _i, tr in cena.modelo.todos_trechos()]
        self.assertIn("flexao_cotovelo", movs)
        self.assertIn("extensao_cotovelo", movs)
        # o tocador anda e a cena acompanha
        dlg.tocador.set_velocidade(4.0)
        dlg.tocador.tocar()
        fim = time.time() + 0.6
        while time.time() < fim:
            app.processEvents()
            time.sleep(0.01)
        self.assertGreater(dlg.tocador.tempo(), 1.0)
        dlg.tocador.pausar()
        dlg.tocador.set_tempo(4.5)
        self.assertIn("Flexão", cena.lbl_mov.text())
        # intensidade: Bíceps acima do ruído durante a rajada
        ativ = ROA.intensidade_no_instante(cena.envelopes, cena.fs, 4.5)
        self.assertGreater(ativ.get("Bíceps Braquial", 0.0), 0.3)
        # salvar escreve movimentos.json ao lado da gravação
        cena.modelo.trocar_movimento(0, 0, "supinacao")
        self.assertTrue(cena.tem_alteracoes())
        self.assertTrue(cena.salvar())
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(self.csv_emg), "movimentos.json")))
        self.assertFalse(cena.tem_alteracoes())
        dlg.close()
        # reabrir lê o arquivo salvo
        dlg2 = self._abre(self.csv_emg)
        self.assertEqual(dlg2.cena.modelo.trecho(0, 0)["movimento"], "supinacao")
        dlg2.close()

    def test_replay_coracao(self):
        dlg = self._abre(self.csv_ecg)
        cena = dlg.cena
        self.assertIsInstance(cena, ROA.CenaReplayECG)
        bat = cena.deteccao["batidas"]
        self.assertGreater(len(bat), 25)
        tipos = [b["tipo"] for b in bat]
        self.assertIn("adiantada", tipos)
        self.assertIn("pausa", tipos)
        dlg.tocador.set_tempo(12.3)
        self.assertGreater(cena.coracao.pulso() if hasattr(cena.coracao, "pulso") else 1.0, -1.0)
        # correção no Completo: remover uma batida e salvar batidas.json
        t_rm = bat[5]["t"]
        cena._corrigir({"acao": "remover", "t": t_rm})
        self.assertEqual(len(cena.deteccao["batidas"]), len(bat) - 1)
        self.assertTrue(cena.tem_alteracoes())
        cena.salvar()
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(self.csv_ecg), "batidas.json")))
        dlg.close()
        dlg2 = self._abre(self.csv_ecg)
        self.assertEqual(len(dlg2.cena.deteccao["batidas"]), len(bat) - 1)
        dlg2.close()

    def test_replay_olhos(self):
        dlg = self._abre(self.csv_eog)
        cena = dlg.cena
        self.assertIsInstance(cena, ROA.CenaReplayEOG)
        ev = cena.deteccao["eventos"]
        self.assertEqual(sum(1 for e in ev if e["tipo"] == "piscada"), 3)
        dirs = [e.get("direcao") for e in ev if e["tipo"] == "sacada"]
        self.assertIn("direita", dirs)
        self.assertIn("esquerda", dirs)
        # inverter horizontal troca os lados sem redetectar
        n_antes = len(ev)
        cena.chk_h.setChecked(True)
        processar_eventos(20)
        ev2 = cena.deteccao["eventos"]
        self.assertEqual(len(ev2), n_antes)
        d1 = [e.get("direcao") for e in ev if e["tipo"] == "sacada" and e.get("direcao") in ("direita", "esquerda")]
        d2 = [e.get("direcao") for e in ev2 if e["tipo"] == "sacada" and e.get("direcao") in ("direita", "esquerda")]
        self.assertEqual(d2, ["esquerda" if d == "direita" else "direita" for d in d1])
        dlg.tocador.set_tempo(6.5)
        cena.salvar()
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(self.csv_eog), "olhos.json")))
        dlg.close()

    def test_simples_tem_so_o_essencial(self):
        win = self.win
        win.config.ui_level = "simples"
        win._definir_nivel("simples")
        try:
            dlg = self._abre(self.csv_emg)
            self.assertTrue(dlg.cena.linha.somente_leitura())
            self.assertFalse(hasattr(dlg.cena, "combo_tarefa"))
            self.assertFalse(dlg.tocador.combo_vel.isVisibleTo(dlg.tocador))
            dlg.close()
            dlg = self._abre(self.csv_ecg)
            # sem edição da faixa no Simples
            self.assertFalse(getattr(dlg.cena.faixa, "_edicao", False))
            dlg.close()
        finally:
            win.config.ui_level = "avancado"
            win._definir_nivel("avancado")


if __name__ == "__main__":
    unittest.main()
