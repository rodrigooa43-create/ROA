# -*- coding: utf-8 -*-
"""P4 — Perfis de uso: funções puras, config, tela inicial, assistente e janela.

Tudo offscreen e com sinais/configs sintéticos. A janela principal é pesada,
por isso é construída uma vez só (setUpClass) e reaproveitada.
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA, app, processar_eventos  # noqa: E402


class _Cfg:
    """Config mínima (só os atributos que as funções puras leem)."""

    def __init__(self, perfil="Tudo", perfis=None):
        self.usage_profile = perfil
        self.usage_profiles = perfis or {}


class TestFuncoesPuras(unittest.TestCase):
    """perfil_para_exames, exames_do_perfil, perfil_valido, perfis_disponiveis."""

    def test_perfil_para_exames(self):
        self.assertEqual(ROA.perfil_para_exames(["EEG"]), "Cérebro (EEG)")
        self.assertEqual(ROA.perfil_para_exames(["EMG"]), "Músculos (EMG)")
        self.assertEqual(ROA.perfil_para_exames(["ECG"]), "Coração (ECG)")
        self.assertEqual(ROA.perfil_para_exames(["EoG"]), "Olhos (EOG)")
        self.assertEqual(ROA.perfil_para_exames(["EoG", "EMG", "EEG", "ECG"]), "Tudo")
        self.assertEqual(ROA.perfil_para_exames(["EMG", "ECG"]), "Minha bancada")

    def test_exames_do_perfil(self):
        self.assertEqual(ROA.exames_do_perfil(None), ["EEG", "EMG", "ECG", "EoG", "Hibrido"])
        self.assertEqual(ROA.exames_do_perfil(_Cfg("Cérebro (EEG)")), ["EEG"])
        self.assertEqual(ROA.exames_do_perfil(_Cfg("Tudo")), ["EEG", "EMG", "ECG", "EoG", "Hibrido"])
        cfg = _Cfg("Minha bancada", {"Minha bancada": {"exames": ["ECG", "EMG"], "paineis": {}}})
        # ordem dos cartões e Multimodal por último
        self.assertEqual(ROA.exames_do_perfil(cfg), ["EMG", "ECG", "Hibrido"])

    def test_perfil_valido_cai_em_tudo(self):
        self.assertEqual(ROA.perfil_valido(_Cfg("não existe")), "Tudo")
        self.assertEqual(ROA.perfil_valido(_Cfg(None)), "Tudo")
        self.assertEqual(ROA.perfil_valido(_Cfg("Olhos (EOG)")), "Olhos (EOG)")

    def test_perfis_disponiveis_ignora_lixo(self):
        cfg = _Cfg("Tudo", {"Ok": {"exames": ["EMG", "xx"]}, "": {"exames": ["EEG"]},
                            "Tudo": {"exames": ["EEG"]}, "Ruim": "texto"})
        p = ROA.perfis_disponiveis(cfg)
        self.assertEqual(p["Ok"]["exames"], ["EMG"])
        self.assertFalse(p["Ok"]["pronto"])
        self.assertNotIn("", p)
        self.assertEqual(p["Tudo"]["exames"], ["EEG", "EMG", "ECG", "EoG"])  # pronto não é sobrescrito
        self.assertEqual(p["Ruim"]["exames"], ["EEG", "EMG", "ECG", "EoG"])


class TestAppConfig(unittest.TestCase):
    """As chaves novas gravam, voltam, e um config antigo fica em "Tudo"."""

    def setUp(self):
        self.pasta = tempfile.mkdtemp(prefix="roa_p4_cfg_")
        self.caminho = os.path.join(self.pasta, "config.json")

    def test_padrao_e_ida_e_volta(self):
        cfg = ROA.AppConfig(path=self.caminho)
        self.assertEqual(cfg.usage_profile, "Tudo")
        self.assertEqual(cfg.usage_profiles, {})
        cfg.usage_profile = "Minha bancada"
        cfg.usage_profiles = {"Minha bancada": {"exames": ["EMG", "ECG"], "paineis": {"emg_mdf": False}}}
        cfg.save()
        d = json.load(open(self.caminho, encoding="utf-8"))
        self.assertEqual(d["usage_profile"], "Minha bancada")
        cfg2 = ROA.AppConfig(path=self.caminho)
        self.assertEqual(cfg2.usage_profile, "Minha bancada")
        self.assertEqual(cfg2.usage_profiles["Minha bancada"]["exames"], ["EMG", "ECG"])
        self.assertEqual(cfg2.usage_profiles["Minha bancada"]["paineis"], {"emg_mdf": False})

    def test_config_antigo_sem_chave(self):
        # um config.json da 1.9.0 não tem a chave: continua vendo tudo
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump({"theme": "ROA (azul clinico)", "language": "pt"}, f)
        cfg = ROA.AppConfig(path=self.caminho)
        self.assertEqual(cfg.usage_profile, "Tudo")
        self.assertEqual(ROA.exames_do_perfil(cfg), ["EEG", "EMG", "ECG", "EoG", "Hibrido"])

    def test_lixo_no_arquivo(self):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump({"usage_profile": 7, "usage_profiles": {"A": {"exames": ["nada"]},
                                                                "B": {"exames": ["EEG"]}}}, f)
        cfg = ROA.AppConfig(path=self.caminho)
        self.assertEqual(cfg.usage_profile, "Tudo")
        self.assertEqual(list(cfg.usage_profiles), ["B"])


class TestTelaInicial(unittest.TestCase):
    """A tela inicial só oferece os exames do perfil e troca de perfil na hora."""

    def _cfg(self, perfil, nivel):
        pasta = tempfile.mkdtemp(prefix="roa_p4_launch_")
        cfg = ROA.AppConfig(path=os.path.join(pasta, "config.json"))
        cfg.usage_profile = perfil
        cfg.ui_level = nivel
        cfg.acquisition_mode = "EEG"
        return cfg

    def test_simples_so_exames_do_perfil(self):
        cfg = self._cfg("Músculos (EMG)", "simples")
        tela = ROA.LauncherScreen(config=cfg, volunteers_mgr=None)
        try:
            chaves = [k for k, _l, _t in tela._tipos_de_exame()]
            self.assertEqual(chaves, ["EMG"])
            # o exame salvo (EEG) saiu do perfil: cai no primeiro oferecido
            self.assertEqual(tela._exame_atual(), "EMG")
            self.assertIn("EMG", tela.exame_lbl.text())
            self.assertTrue(hasattr(tela, "perfil_combo"))
            self.assertGreaterEqual(tela.perfil_combo.count(), 5)
            # trocar para "Tudo" devolve os 5 exames
            tela.perfil_combo.setCurrentIndex(tela.perfil_combo.findData("Tudo"))
            processar_eventos(20)
            self.assertEqual(cfg.usage_profile, "Tudo")
            self.assertEqual(len(tela._tipos_de_exame()), 5)
        finally:
            tela.close()

    def test_completo_esconde_radios(self):
        cfg = self._cfg("Coração (ECG)", "avancado")
        tela = ROA.LauncherScreen(config=cfg, volunteers_mgr=None)
        try:
            self.assertEqual(set(tela._acq_radios), {"EEG", "EMG", "ECG", "EoG", "Hibrido"})
            self.assertFalse(tela._acq_radios["ECG"].isHidden())
            for k in ("EEG", "EMG", "EoG", "Hibrido"):
                self.assertTrue(tela._acq_radios[k].isHidden(), k)
            self.assertTrue(tela._acq_radios["ECG"].isChecked())
            tela.perfil_combo.setCurrentIndex(tela.perfil_combo.findData("Olhos (EOG)"))
            processar_eventos(20)
            self.assertTrue(tela._acq_radios["EoG"].isChecked())
            self.assertFalse(tela._acq_radios["EoG"].isHidden())
            self.assertTrue(tela._acq_radios["ECG"].isHidden())
        finally:
            tela.close()


class TestAssistente(unittest.TestCase):
    """Página "Com o que você trabalha?" decide o perfil."""

    def _wiz(self, nivel="simples"):
        pasta = tempfile.mkdtemp(prefix="roa_p4_wiz_")
        cfg = ROA.AppConfig(path=os.path.join(pasta, "config.json"))
        cfg.ui_level = nivel
        return ROA.FirstRunWizard(cfg), cfg

    def test_um_cartao_vira_perfil_pronto(self):
        wiz, cfg = self._wiz()
        try:
            self.assertEqual(wiz.stack.count(), 6)
            for code, bt in wiz._cartoes_trabalho.items():
                bt.setChecked(code == "EMG")
            self.assertEqual(wiz._exames_marcados(), ["EMG"])
            wiz._aplicar_perfil_escolhido()
            self.assertEqual(cfg.usage_profile, "Músculos (EMG)")
            self.assertEqual(cfg.acquisition_mode, "EMG")
        finally:
            wiz.close()

    def test_pagina_graficos_vem_do_catalogo_de_paineis(self):
        """No caminho Pesquisa, "Escolha os gráficos" lista os painéis do
        catálogo do P2 para os exames marcados; desmarcar um deles vira um
        perfil personalizado com esse painel fechado."""
        wiz, cfg = self._wiz("completo")
        try:
            wiz.rb_uso_pesquisa.setChecked(True)
            for code, bt in wiz._cartoes_trabalho.items():
                bt.setChecked(code == "EMG")
            wiz._atualiza_pagina_graficos()
            chks = wiz._graficos_chks
            esperados = {it["id"] for it in ROA.CATALOGO_PAINEIS.itens()
                         if not it["exames"] or "EMG" in it["exames"]}
            self.assertTrue(esperados)
            self.assertEqual(set(chks), esperados)
            # nenhum painel de outro exame (ECG/EoG) entra na lista
            self.assertFalse([i for i in chks if i.startswith(("ecg.", "eog."))])
            alvo = sorted(i for i in chks if i.startswith("emg."))[0]
            chks[alvo].setChecked(False)
            wiz._aplicar_perfil_escolhido()
            self.assertEqual(cfg.usage_profile, "Minha bancada")
            self.assertEqual(cfg.usage_profiles["Minha bancada"]["paineis"], {alvo: False})
        finally:
            wiz.close()

    def test_rotulos_dos_perfis_traduzidos(self):
        """Os nomes dos perfis prontos e da aba Bio passam por tr() via
        variável (a coleta não os via): existem nos 8 idiomas e saem
        traduzidos na tela."""
        chaves = ["Cérebro (EEG)", "Músculos (EMG)", "Coração (ECG)", "Olhos (EOG)",
                  "Tudo", "Minha bancada", "Músculos", "Coração", "Olhos"]
        for lang in ("en", "es", "it", "fr", "zh", "de", "ja", "ru"):
            d = getattr(ROA.I18N, "_" + lang)
            for k in chaves:
                self.assertIn(k, d, (lang, k))
                self.assertNotEqual(d[k].strip(), "", (lang, k))
        atual = ROA.I18N.current
        try:
            ROA.I18N.current = "en"
            self.assertEqual(ROA.rotulo_perfil("Cérebro (EEG)"), "Brain (EEG)")
            self.assertEqual(ROA.rotulo_perfil("Tudo"), "Everything")
            # perfil do usuário não passa por tr(): sai como foi escrito
            self.assertEqual(ROA.rotulo_perfil("Bancada do João"), "Bancada do João")
        finally:
            ROA.I18N.current = atual

    def test_dois_cartoes_viram_minha_bancada(self):
        wiz, cfg = self._wiz()
        try:
            for code, bt in wiz._cartoes_trabalho.items():
                bt.setChecked(code in ("EMG", "ECG"))
            wiz._aplicar_perfil_escolhido()
            self.assertEqual(cfg.usage_profile, "Minha bancada")
            self.assertEqual(cfg.usage_profiles["Minha bancada"]["exames"], ["EMG", "ECG"])
            self.assertEqual(ROA.exames_do_perfil(cfg), ["EMG", "ECG", "Hibrido"])
        finally:
            wiz.close()

    def test_quatro_cartoes_e_tudo_e_nenhum_trava(self):
        wiz, cfg = self._wiz()
        try:
            wiz._aplicar_perfil_escolhido()
            self.assertEqual(cfg.usage_profile, "Tudo")
            wiz.stack.setCurrentIndex(2)
            for bt in wiz._cartoes_trabalho.values():
                bt.setChecked(False)
            wiz._refresh_nav()
            self.assertFalse(wiz.btn_next.isEnabled())
            self.assertTrue(wiz._aviso_trabalho.isVisibleTo(wiz))
            wiz._cartoes_trabalho["EEG"].setChecked(True)
            wiz._refresh_nav()
            self.assertTrue(wiz.btn_next.isEnabled())
        finally:
            wiz.close()

    def test_navegacao_pula_paginas_de_pesquisa(self):
        wiz, _cfg = self._wiz("simples")
        try:
            wiz.stack.setCurrentIndex(2)
            wiz._go_next()
            self.assertEqual(wiz.stack.currentIndex(), 5)   # direto ao Termo
            wiz._go_back()
            self.assertEqual(wiz.stack.currentIndex(), 2)
            wiz.rb_uso_pesquisa.setChecked(True)
            wiz._go_next()
            self.assertEqual(wiz.stack.currentIndex(), 3)   # gráficos
            wiz._go_next()
            self.assertEqual(wiz.stack.currentIndex(), 4)   # layout
        finally:
            wiz.close()


class TestJanela(unittest.TestCase):
    """Abas fora do perfil somem; CRUD de perfis em Sistema vale na hora."""

    @classmethod
    def setUpClass(cls):
        cls.win = ROA.EEGCollectorWindow()
        processar_eventos(100)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.win.close()
        except Exception:
            pass

    def _bio_visivel(self):
        sub = self.win._sub_tabs["view"]
        pos = self.win._pos_aba("view", 3)      # "Bio (EMG/ECG/EoG)"
        return sub.isTabVisible(pos)

    def _modo(self, code):
        combo = self.win.mode_visibility_combo
        idx = combo.findData(code)
        if combo.currentIndex() == idx:
            self.win._on_mode_visibility_apply()
        else:
            combo.setCurrentIndex(idx)
        processar_eventos(30)

    def test_perfil_eeg_esconde_bio_mesmo_no_multimodal(self):
        win = self.win
        win.config.ui_level = "avancado"
        win._definir_nivel("avancado")
        win._perfil_definir("Tudo")
        self._modo("Hibrido")
        self.assertTrue(self._bio_visivel())
        win._perfil_definir("Cérebro (EEG)")
        processar_eventos(30)
        # o modo saiu do perfil: a janela muda para EEG e a aba Bio some
        self.assertEqual(win._signal_mode, "EEG")
        self.assertFalse(self._bio_visivel())
        modelo = win.mode_visibility_combo.model()
        for i in range(win.mode_visibility_combo.count()):
            code = win.mode_visibility_combo.itemData(i)
            self.assertEqual(modelo.item(i).isEnabled(), code == "EEG", code)
        win._perfil_definir("Tudo")
        processar_eventos(30)
        for i in range(win.mode_visibility_combo.count()):
            self.assertTrue(modelo.item(i).isEnabled())

    def test_crud_de_perfis_em_sistema(self):
        win = self.win
        pede_original = ROA.pede_texto
        pergunta_original = ROA.QtWidgets.QMessageBox.question
        try:
            ROA.pede_texto = lambda *a, **k: ("Bancada teste", True)
            win._perfil_definir("Tudo")
            win._perfil_novo()
            self.assertEqual(win.config.usage_profile, "Bancada teste")
            self.assertIn("Bancada teste", win.config.usage_profiles)
            # exames editáveis só no personalizado
            self.assertTrue(win._perfil_exame_chks["EMG"].isEnabled())
            win._perfil_exame_chks["EEG"].setChecked(False)
            win._perfil_exame_chks["EoG"].setChecked(False)
            processar_eventos(30)
            self.assertEqual(win.config.usage_profiles["Bancada teste"]["exames"], ["EMG", "ECG"])
            self.assertEqual(ROA.exames_do_perfil(win.config), ["EMG", "ECG", "Hibrido"])
            # renomear
            ROA.pede_texto = lambda *a, **k: ("Bancada 2", True)
            win._perfil_renomear()
            self.assertEqual(win.config.usage_profile, "Bancada 2")
            self.assertNotIn("Bancada teste", win.config.usage_profiles)
            # duplicar um pronto vira personalizado
            win._perfil_definir("Olhos (EOG)")
            ROA.pede_texto = lambda *a, **k: ("Copia olhos", True)
            win._perfil_duplicar()
            self.assertEqual(win.config.usage_profiles["Copia olhos"]["exames"], ["EoG"])
            # excluir volta para Tudo
            ROA.QtWidgets.QMessageBox.question = staticmethod(
                lambda *a, **k: ROA.QtWidgets.QMessageBox.StandardButton.Yes)
            win._perfil_excluir()
            self.assertEqual(win.config.usage_profile, "Tudo")
            self.assertNotIn("Copia olhos", win.config.usage_profiles)
            # pronto não se exclui nem renomeia
            win._perfil_excluir()
            self.assertEqual(win.config.usage_profile, "Tudo")
            self.assertFalse(win.perfil_del_btn.isEnabled())
        finally:
            ROA.pede_texto = pede_original
            ROA.QtWidgets.QMessageBox.question = pergunta_original

    def test_simples_continua_simples(self):
        win = self.win
        win._perfil_definir("Tudo")
        win.config.ui_level = "simples"
        win._definir_nivel("simples")
        processar_eventos(30)
        # o grupo de perfil está na página Tema e Cores, que o Simples mostra;
        # nada novo aparece nas telas do exame
        self.assertTrue(hasattr(win, "perfil_cfg_combo"))
        win.config.ui_level = "avancado"
        win._definir_nivel("avancado")


if __name__ == "__main__":
    unittest.main()
