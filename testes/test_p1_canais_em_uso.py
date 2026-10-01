# -*- coding: utf-8 -*-
"""P1 — "Só os canais em uso": listas, mapas e laços seguem os canais da placa.

Problema de origem: com 8 canais de EMG o mapa "Atividade muscular (canais x
tempo)" mostrava CH1 a CH64, porque o launcher marca os 64 canais como EMG e
os laços percorriam range(MAX_CHANNELS). Aqui conferimos, para os 5 exames x
(8, 16, 32, 64) canais x os dois níveis, que:

  * canais_por_tipo (função pura) e os helpers da janela cortam em num_channels;
  * os combos EMG (MDF/MNF, APDF, espectrograma), ECG, EOG, ERP e dos painéis
    do Layout listam só os canais do tipo em uso (ou um item "sem canal");
  * o mapa canais x tempo tem exatamente k linhas, com ticks CH1..CHk;
  * _update_emg_view não toca canais >= num_channels;
  * a tabela de Calibração esconde as linhas dos canais que a placa não tem;
  * a legenda do envelope EMG lista só os canais EMG em uso;
  * mudar o tipo ou o número de canais repopula tudo preservando a seleção,
    inclusive no mapa de co-contração aberto e nos combos do Atlas;
  * "Rever uma gravação" (aba ERP) segue os canais da gravação carregada.

Uma única EEGCollectorWindow por classe (ela é pesada). Só sinais sintéticos.
"""
import os
import sys
import tempfile
import unittest

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from _roa import ROA, app, processar_eventos, sinal_sintetico  # noqa: E402,F401

EXAMES = ("EEG", "EMG", "ECG", "EoG", "Hibrido")
NS = (8, 16, 32, 64)
NIVEIS = ("simples", "avancado")
MAX = ROA.MAX_CHANNELS
SR = ROA.SAMPLE_RATE


def escolha(exame, n):
    """Dicionário igual ao que a tela inicial entrega a apply_launcher_choice.

    mode="live" sem porta: não agenda _autostart_simulation (o modo "sim"
    liga a simulação 400 ms depois e poluiria os testes)."""
    return {"mode": "live", "port": None, "num_channels": n,
            "expansion_16ch": n > 8, "acquisition_type": exame,
            "volunteer_dir": None, "selected_csv": None}


def tipos_esperados(exame, n):
    """Lista de tipos que o launcher grava para o exame (espelha apply_launcher_choice)."""
    if exame == "EoG":
        return ["EoG"] * 2 + ["off"] * (MAX - 2)
    if exame == "Hibrido":
        return ROA.layout_multimodal(n)
    return [exame] * MAX


def dados_combo(combo):
    """userData de todos os itens de um QComboBox."""
    return [combo.itemData(i) for i in range(combo.count())]


class TestCanaisPorTipo(unittest.TestCase):
    """Função pura canais_por_tipo(tipos, n_em_uso, tipo)."""

    def test_corta_em_n_em_uso(self):
        tipos = ["EMG"] * MAX
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, "EMG"), list(range(8)))
        self.assertEqual(ROA.canais_por_tipo(tipos, 64, "EMG"), list(range(64)))
        self.assertEqual(ROA.canais_por_tipo(tipos, 0, "EMG"), [])

    def test_lista_menor_que_n_completa_com_eeg(self):
        tipos = ["EMG", "ECG", "EMG"]          # só 3 tipos para 8 canais
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, "EMG"), [0, 2])
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, "ECG"), [1])
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, "EEG"), [3, 4, 5, 6, 7])
        self.assertEqual(ROA.canais_por_tipo([], 4, "EEG"), [0, 1, 2, 3])
        self.assertEqual(ROA.canais_por_tipo(None, 4, "EMG"), [])

    def test_off_e_tipo_none(self):
        tipos = ["EoG", "EoG"] + ["off"] * (MAX - 2)
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, "EoG"), [0, 1])
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, "off"), [2, 3, 4, 5, 6, 7])
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, "EEG"), [])
        self.assertEqual(ROA.canais_por_tipo(tipos, 8, None), list(range(8)))

    def test_n_invalido_nao_quebra(self):
        self.assertEqual(ROA.canais_por_tipo(["EMG"] * 8, None, "EMG"), [])
        self.assertEqual(ROA.canais_por_tipo(["EMG"] * 8, "x", "EMG"), [])
        self.assertEqual(ROA.canais_por_tipo(["EMG"] * 8, -3, "EMG"), [])
        self.assertEqual(ROA.canais_por_tipo(["EMG"] * 8, "8", "EMG"), list(range(8)))


class TestCanaisEmUsoJanela(unittest.TestCase):
    """Janela inteira: combos, mapa canais x tempo, laços e tabela."""

    @classmethod
    def setUpClass(cls):
        cls.win = ROA.EEGCollectorWindow()
        processar_eventos(100)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.win.close()
            cls.win.deleteLater()
        except Exception:
            pass
        processar_eventos(50)

    # ------------------------------------------------------------------
    def _aplicar(self, exame, n, nivel="avancado"):
        """Põe a janela no nível e no exame pedidos, com n canais."""
        win = self.win
        win.config.ui_level = nivel
        win._definir_nivel(nivel)
        win.apply_launcher_choice(escolha(exame, n))
        processar_eventos(5)
        self.assertEqual(win.num_channels, n)
        return win

    def _confere_combo_tipo(self, combo, canais, tipo, ctx):
        """Combo de canal por tipo: um item por canal em uso do tipo (userData =
        índice do canal) ou um único item "sem canal" com data -1."""
        if canais:
            self.assertEqual(dados_combo(combo), canais, ctx)
            for i, ch in enumerate(canais):
                self.assertTrue(combo.itemText(i).startswith("CH%d" % (ch + 1)),
                                ctx + " texto %r" % combo.itemText(i))
        else:
            self.assertEqual(combo.count(), 1, ctx)
            self.assertEqual(combo.itemData(0), -1, ctx)
            self.assertEqual(combo.itemText(0), self.win._msg_sem_canal(tipo), ctx)

    def _mapa_atividade(self, ctx):
        """Alimenta _emg_update_advanced com sinal sintético nos 64 canais e
        confere que o mapa canais x tempo tem só os canais EMG em uso."""
        win = self.win
        emg = win._canais_em_uso_tipo("EMG")
        data = sinal_sintetico(MAX, 2 * SR)
        env_map = {ch: np.abs(data[ch]) for ch in range(MAX)}   # 64 "envelopes"
        rects = []
        original = win.emg_activity_img.setRect
        win.emg_activity_img.setRect = lambda r: (rects.append(r), original(r))
        try:
            win._emg_update_advanced(data, env_map, data.shape[1])
        finally:
            win.emg_activity_img.setRect = original
        eixo = win.emg_activity_widget.getAxis("left")
        ticks = [lbl for _pos, lbl in (eixo._tickLevels or [[]])[0]]
        if emg:
            self.assertTrue(rects, ctx + " setRect não foi chamado")
            self.assertEqual(rects[-1].height(), float(len(emg)), ctx)
            self.assertEqual(ticks, ["CH%d" % (ch + 1) for ch in emg], ctx)
            self.assertEqual(win.emg_activity_img.image.shape[1], len(emg), ctx)
        else:
            self.assertEqual(ticks, [], ctx)
            self.assertIsNone(win.emg_activity_img.image, ctx)

    # ------------------------------------------------------------------
    def test_matriz_exames_canais_niveis(self):
        """5 exames x 4 tamanhos de placa x 2 níveis."""
        win = self.win
        for nivel in NIVEIS:
            for exame in EXAMES:
                for n in NS:
                    ctx = "[%s %s %dch]" % (nivel, exame, n)
                    self._aplicar(exame, n, nivel)
                    tipos = tipos_esperados(exame, n)
                    self.assertEqual(list(win.config.channel_signal_types), tipos, ctx)
                    # helpers
                    self.assertEqual(win._canais_em_uso(), list(range(n)), ctx)
                    for t in ("EEG", "EMG", "ECG", "EoG", "off"):
                        self.assertEqual(win._canais_em_uso_tipo(t),
                                         ROA.canais_por_tipo(tipos, n, t), ctx + t)
                    emg = win._canais_em_uso_tipo("EMG")
                    ecg = win._canais_em_uso_tipo("ECG")
                    eog = win._canais_em_uso_tipo("EoG")
                    # combos EMG
                    for nome in ("emg_mnfdf_channel", "emg_apdf_channel", "emg_spec_channel"):
                        self._confere_combo_tipo(getattr(win, nome), emg, "EMG", ctx + nome)
                    # ECG / EOG (já respeitavam n; continuam)
                    self._confere_combo_tipo(win.ecg_channel_combo, ecg, "ECG", ctx + "ecg")
                    if eog:
                        self.assertEqual(dados_combo(win.eog_h_combo), eog, ctx + "eog_h")
                    else:
                        self.assertEqual(win.eog_h_combo.count(), 1, ctx + "eog_h")
                    # ERP sem gravação carregada: canais em uso
                    self.assertIsNone(getattr(win, "_erp_data", None))
                    self.assertEqual(dados_combo(win.erp_channel_combo), list(range(n)), ctx + "erp")
                    # painéis do Layout
                    for i, slot in enumerate(win.layout_slots):
                        self.assertEqual(dados_combo(slot["ch_combo"]), list(range(n)),
                                         ctx + " layout slot %d" % i)
                    # Calibração: linhas >= n escondidas
                    for ch in range(MAX):
                        self.assertEqual(win.imp_table.isRowHidden(ch), ch >= n,
                                         ctx + " imp_table linha %d" % ch)
                    # legenda do envelope EMG
                    legenda = [lbl.text for _s, lbl in win.emg_plot.plotItem.legend.items]
                    self.assertEqual(legenda, ["CH%d" % (ch + 1) for ch in emg], ctx + "legenda")
                    # mapa canais x tempo
                    self._mapa_atividade(ctx)

    def test_update_emg_view_nao_toca_canais_fora_de_uso(self):
        """Com 8 canais EMG, os canais 9-64 (também marcados EMG) ficam de fora
        do envelope, da co-contração e do atlas."""
        win = self._aplicar("EMG", 8)
        N = 3 * SR
        win.buffer[:, :N] = sinal_sintetico(MAX, N)
        win.samples_total = N
        win.buffer_pos = N
        for cur in win.emg_curves:
            cur.setData([], [])
        win._update_emg_view()
        self.assertEqual(sorted(win._emg_env_atual), list(range(8)))
        for ch in range(MAX):
            tam = len(win.emg_curves[ch].xData) if win.emg_curves[ch].xData is not None else 0
            if ch < 8:
                self.assertEqual(tam, N, "CH%d sem curva" % (ch + 1))
            else:
                self.assertEqual(tam, 0, "CH%d fora de uso recebeu dados" % (ch + 1))
        self.assertIn("8", win.emg_active_count_lbl.text())
        # com 16 canais o laço cresce junto
        win._set_num_channels(16)
        win._update_emg_view()
        self.assertEqual(sorted(win._emg_env_atual), list(range(16)))
        self.assertIn("16", win.emg_active_count_lbl.text())

    def test_mudar_tipo_repopula_e_preserva_selecao(self):
        """_on_channel_signal_type_changed repopula os combos e mantém o canal
        escolhido (pela identidade do canal, não pela posição)."""
        win = self._aplicar("EMG", 16)
        for nome in ("emg_mnfdf_channel", "emg_apdf_channel", "emg_spec_channel"):
            cb = getattr(win, nome)
            cb.setCurrentIndex(cb.findData(5))              # CH6
        win._on_channel_signal_type_changed(2, "ECG")       # CH3 vira ECG
        self.assertEqual(win._canais_em_uso_tipo("EMG"), [c for c in range(16) if c != 2])
        for nome in ("emg_mnfdf_channel", "emg_apdf_channel", "emg_spec_channel"):
            cb = getattr(win, nome)
            self.assertEqual(cb.count(), 15, nome)
            self.assertNotIn(2, dados_combo(cb), nome)
            self.assertEqual(cb.currentData(), 5, nome + " perdeu a seleção")
        self.assertEqual(dados_combo(win.ecg_channel_combo), [2])
        legenda = [lbl.text for _s, lbl in win.emg_plot.plotItem.legend.items]
        self.assertNotIn("CH3", legenda)
        self.assertEqual(len(legenda), 15)
        # o canal escolhido some: cai no primeiro, sem quebrar
        win._on_channel_signal_type_changed(5, "EEG")
        self.assertEqual(win.emg_spec_channel.currentData(), 0)
        # volta
        win._on_channel_signal_type_changed(2, "EMG")
        win._on_channel_signal_type_changed(5, "EMG")
        self.assertEqual(dados_combo(win.emg_mnfdf_channel), list(range(16)))
        self.assertEqual(win.ecg_channel_combo.itemData(0), -1)

    def test_imp_table_altura_segue_canais(self):
        win = self._aplicar("EEG", 8)
        tbl = win.imp_table
        row_h = tbl.verticalHeader().defaultSectionSize()
        self.assertEqual(tbl.minimumHeight(), row_h * 8 + 28 + 4)
        self.assertEqual(sum(not tbl.isRowHidden(r) for r in range(tbl.rowCount())), 8)
        win._set_num_channels(32)
        self.assertEqual(tbl.minimumHeight(), row_h * 32 + 28 + 4)
        self.assertEqual(sum(not tbl.isRowHidden(r) for r in range(tbl.rowCount())), 32)

    def test_atlas_combos_so_canais_emg_em_uso(self):
        """Combo "Canal" de cada eletrodo do Atlas: canais EMG em uso + o canal
        já gravado no eletrodo (para a montagem salva não mudar sozinha)."""
        win = self._aplicar("EMG", 8)
        montagem_antes = win.emg_atlas.get_electrodes()
        try:
            win.emg_atlas.set_electrodes([
                {"id": 1, "name": "E1", "x": 0.4, "y": 0.4, "view": "front",
                 "channel": 1, "muscle": ""},
                {"id": 2, "name": "E2", "x": 0.6, "y": 0.6, "view": "front",
                 "channel": 40, "muscle": ""},          # gravado com outra placa
            ])
            win._emg_atlas_rebuild_table()
            cb0 = win.emg_atlas_table.cellWidget(0, 2)
            cb1 = win.emg_atlas_table.cellWidget(1, 2)
            self.assertEqual(dados_combo(cb0), [-1] + list(range(8)))
            self.assertEqual(cb0.currentData(), 1)
            self.assertEqual(dados_combo(cb1), [-1] + list(range(8)) + [40])
            self.assertEqual(cb1.currentData(), 40)
            # mudou o número de canais: a tabela acompanha
            win._set_num_channels(64)
            cb0 = win.emg_atlas_table.cellWidget(0, 2)
            cb1 = win.emg_atlas_table.cellWidget(1, 2)
            self.assertEqual(dados_combo(cb0), [-1] + list(range(64)))
            self.assertEqual(dados_combo(cb1), [-1] + list(range(64)))
            self.assertEqual(cb1.currentData(), 40)
            # e o tipo também
            win._on_channel_signal_type_changed(0, "ECG")
            cb0 = win.emg_atlas_table.cellWidget(0, 2)
            self.assertEqual(dados_combo(cb0), [-1] + list(range(1, 64)))
            self.assertEqual(cb0.currentData(), 1)
        finally:
            win.emg_atlas.set_electrodes(montagem_antes)
            win._emg_atlas_rebuild_table()

    def test_cocontracao_dialogo_acompanha_canais(self):
        """Mapa de co-contração aberto: repopula ao mudar n ou tipo, sem perder o par."""
        win = self._aplicar("EMG", 8)
        dlg = ROA.CoContractionMapDialog(win)
        try:
            self.assertIs(win._cocontr_dialog, dlg)
            self.assertEqual(dados_combo(dlg.cb_flex), list(range(8)))
            self.assertEqual(dlg.cb_ext.currentData(), 1)
            win._set_num_channels(16)
            self.assertEqual(dados_combo(dlg.cb_flex), list(range(16)))
            self.assertEqual(dados_combo(dlg.cb_ext), list(range(16)))
            dlg.cb_flex.setCurrentIndex(dlg.cb_flex.findData(2))
            dlg.cb_ext.setCurrentIndex(dlg.cb_ext.findData(4))
            win._on_channel_signal_type_changed(0, "ECG")
            self.assertEqual(dlg.cb_flex.count(), 15)
            self.assertEqual(dlg.cb_flex.currentData(), 2)
            self.assertEqual(dlg.cb_ext.currentData(), 4)
            # músculo definido aparece no rótulo
            win.config.emg_channel_muscle[4] = "Bíceps Braquial"
            dlg._popular_canais()
            self.assertIn("—", dlg.cb_ext.itemText(dlg.cb_ext.findData(4)))
            self.assertEqual(dlg.cb_ext.currentData(), 4)
        finally:
            win.config.emg_channel_muscle[4] = "(não definido)"
            dlg.close()
            dlg.deleteLater()
            win._cocontr_dialog = None
            processar_eventos(20)

    def test_erp_segue_canais_da_gravacao(self):
        """Rever uma gravação: o combo do ERP lista os canais do data.csv
        carregado (3 canais com nomes próprios), não os da placa, e abrir a
        gravação não mexe em num_channels nem no config."""
        win = self._aplicar("EEG", 16)
        tipos_antes = list(win.config.channel_signal_types)
        pasta = tempfile.mkdtemp(prefix="roa_p1_erp_")
        caminho = os.path.join(pasta, "data.csv")
        n_amostras = 5 * SR
        sinal = sinal_sintetico(3, n_amostras)
        marcas = {2 * SR: "alvo", 3 * SR: "alvo", 4 * SR: "outro"}
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            f.write("timestamp,Fp1_uV,Cz_uV,O1_uV,marker\n")
            for i in range(n_amostras):
                f.write("%.4f,%.3f,%.3f,%.3f,%s\n" % (
                    i / SR, sinal[0, i], sinal[1, i], sinal[2, i], marcas.get(i, "")))
        win._pick_session_csv = lambda: (caminho, pasta)
        try:
            win._erp_load_csv()
            self.assertIsNotNone(win._erp_data)
            self.assertEqual(dados_combo(win.erp_channel_combo), [0, 1, 2])
            self.assertEqual([win.erp_channel_combo.itemText(i) for i in range(3)],
                             ["Fp1", "Cz", "O1"])
            self.assertEqual(win.num_channels, 16)
            self.assertEqual(list(win.config.channel_signal_types), tipos_antes)
            # a gravação manda: mudar a placa não troca a lista do ERP
            win._refresh_listas_canais()
            win._set_num_channels(32)
            self.assertEqual(dados_combo(win.erp_channel_combo), [0, 1, 2])
            # calcular no 3º canal da gravação funciona e usa o nome dele
            win.erp_channel_combo.setCurrentIndex(2)
            win._erp_compute()
            self.assertIn("O1", win.erp_info_label.text())
        finally:
            del win._pick_session_csv
            win._erp_data = None
            win.erp_compute_btn.setEnabled(False)
        # sem gravação carregada, volta aos canais em uso
        win._refresh_listas_canais()
        self.assertEqual(dados_combo(win.erp_channel_combo), list(range(32)))

    def test_rotulo_com_musculo(self):
        """Combos EMG mostram "CHn — músculo" quando o músculo está definido."""
        win = self._aplicar("EMG", 8)
        musculo = "Bíceps Braquial"              # chave de COMMON_MUSCLES
        self.assertIn(musculo, ROA.COMMON_MUSCLES)
        try:
            win.config.emg_channel_muscle[3] = musculo
            win._refresh_listas_canais()
            txt = win.emg_mnfdf_channel.itemText(win.emg_mnfdf_channel.findData(3))
            self.assertTrue(txt.startswith("CH4 — "), txt)
            self.assertEqual(win.emg_mnfdf_channel.itemText(0), "CH1")
        finally:
            win.config.emg_channel_muscle[3] = "(não definido)"
            win._refresh_listas_canais()


if __name__ == "__main__":
    unittest.main()
