# -*- coding: utf-8 -*-
"""P2 — painéis em "gavetas" dentro do ROA.py: unidade do bloco e integração na janela.

Roda sem monitor:
    cd /home/user/ROA && QT_QPA_PLATFORM=offscreen python -m unittest testes/test_p2_gavetas.py
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA, app, processar_eventos  # noqa: E402  (o bloco P2 vive dentro do ROA.py)
from PySide6 import QtCore, QtWidgets  # noqa: E402

P2 = ROA
PALETA_CLARA = dict(ROA.THEMES["ROA (azul clinico)"])
PALETA_ESCURA = dict(ROA.THEMES["ROA Escuro"])
ROA._apply_theme_colors("ROA (azul clinico)")


def processar(ms=50):
    """Deixa o loop de eventos rodar por `ms` (timers, layouts)."""
    fim = QtCore.QDeadlineTimer(ms)
    while not fim.hasExpired():
        app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 10)


def grupo(titulo, altura_min=60):
    """QGroupBox falso com um rótulo dentro."""
    g = QtWidgets.QGroupBox(titulo)
    lay = QtWidgets.QVBoxLayout(g)
    lbl = QtWidgets.QLabel("conteúdo de " + titulo)
    lbl.setMinimumHeight(altura_min)
    lay.addWidget(lbl)
    return g


class _Dono:
    """Faz as vezes da janela: recebe _gavetas e guarda o "config"."""

    def __init__(self):
        self.config = {}
        self.gravacoes = 0


def montar_pilha(simples=False, aba_visivel=None, catalogo=None, dono=None):
    """Pilha de teste com três gavetas simples (a, b, c) e um pai mostrável."""
    pai = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(pai)
    pilha = P2.PilhaGavetas("teste", catalogo=catalogo, dono=dono,
                            simples=simples, aba_visivel=aba_visivel)
    ga = pilha.adicionar_painel("a", grupo("Painel A"), exames={"EMG"})
    gb = pilha.adicionar_painel("b", grupo("Painel B"), exames={"ECG"},
                                recolhido=True)
    gc = pilha.adicionar_painel("c", grupo("Painel C"), exames={"EMG", "EoG"},
                                altura=200)
    lay.addWidget(pilha)
    return pai, pilha, (ga, gb, gc)


class TestCatalogo(unittest.TestCase):
    """CatalogoPaineis: registro, consultas, serialização e API para o P4."""

    def setUp(self):
        self.cat = P2.CatalogoPaineis()
        self.cat.registrar("emg.atlas", "Atlas", "emg", {"EMG"})
        self.cat.registrar("emg.fadiga", "Fadiga", "emg", {"EMG"}, recolhido=True)
        self.cat.registrar("ecg.hrv", "HRV", "ecg", "ECG", visivel=True, altura=180)
        self.cat.registrar("ana.fft", "FFT", "analises", {"EEG"})

    def test_registrar_e_consultar(self):
        self.assertEqual(self.cat.ids_da_aba("emg"), ["emg.atlas", "emg.fadiga"])
        self.assertEqual(self.cat.ids_do_exame("ECG"), ["ecg.hrv"])
        self.assertEqual(set(self.cat.ids_do_exame("Hibrido")), set(self.cat.ids()))
        self.assertEqual(self.cat.estado_padrao("emg.fadiga"),
                         {"visivel": True, "recolhido": True, "altura": None})
        self.assertEqual(self.cat.estado_padrao("ecg.hrv")["altura"], 180)
        self.assertEqual(self.cat.exames_de("ecg.hrv"), {"ECG"})
        # altura absurda é saneada
        self.cat.registrar("x", "X", "emg", altura=10 ** 9)
        self.assertLessEqual(self.cat.estado_padrao("x")["altura"], 6000)
        self.cat.registrar("y", "Y", "emg", altura="lixo")
        self.assertIsNone(self.cat.estado_padrao("y")["altura"])

    def test_registrar_de_novo_preserva_estado(self):
        self.cat.definir_estado("emg.atlas", recolhido=True)
        self.cat.registrar("emg.atlas", "Atlas (novo título)", "emg", {"EMG"})
        self.assertTrue(self.cat.estado_atual("emg.atlas")["recolhido"])
        self.assertEqual(self.cat.titulo("emg.atlas"), "Atlas (novo título)")

    def test_serializar_ida_e_volta(self):
        self.cat.definir_estado("emg.atlas", visivel=False, altura=333)
        self.cat.definir_ordem("emg", ["emg.fadiga", "emg.atlas"])
        self.cat.definir_split("emg", "linha1", [400, 600])
        d = self.cat.para_config()
        texto = json.dumps(d, ensure_ascii=False)       # tem de ser JSON puro
        d2 = json.loads(texto)
        self.assertEqual(d2["emg"]["ordem"], ["emg.fadiga", "emg.atlas"])
        self.assertEqual(d2["emg"]["paineis"]["emg.atlas"],
                         {"visivel": False, "recolhido": False, "altura": 333})
        self.assertEqual(d2["emg"]["splits"], {"linha1": [400, 600]})
        # um catálogo novo com os mesmos registros lê de volta
        novo = P2.CatalogoPaineis()
        novo.registrar("emg.atlas", "Atlas", "emg", {"EMG"})
        novo.registrar("emg.fadiga", "Fadiga", "emg", {"EMG"}, recolhido=True)
        novo.registrar("ecg.hrv", "HRV", "ecg", {"ECG"}, altura=180)
        novo.registrar("ana.fft", "FFT", "analises", {"EEG"})
        novo.de_config(d2)
        self.assertEqual(novo.para_config(), d2)

    def test_de_config_tolerante(self):
        self.cat.de_config({
            "emg": {"ordem": ["nao.existe", "emg.fadiga", 42],
                    "paineis": {"emg.atlas": {"visivel": "sim", "recolhido": True,
                                              "altura": 0},
                                "fantasma": {"visivel": False}},
                    "splits": {"l": "errado", "m": [1, 2]}},
            "aba.inexistente": {"ordem": []},
            "ecg": "lixo",
        })
        # desconhecidos somem; o que faltava entra no fim na ordem padrão
        self.assertEqual(self.cat.ordem_da_aba("emg"), ["emg.fadiga", "emg.atlas"])
        e = self.cat.estado_atual("emg.atlas")
        self.assertTrue(e["visivel"])              # "sim" não é bool: ignorado
        self.assertTrue(e["recolhido"])
        self.assertEqual(e["altura"], P2._GAVETA_ALTURA_MIN)   # 0 vira o mínimo
        self.assertEqual(self.cat.splits_da_aba("emg"), {"m": [1, 2]})
        self.assertNotIn("aba.inexistente", self.cat.abas())
        self.cat.de_config(None)                   # não estoura

    def test_restaurar_padrao(self):
        self.cat.definir_estado("emg.atlas", visivel=False)
        self.cat.definir_ordem("emg", ["emg.fadiga", "emg.atlas"])
        self.cat.definir_split("emg", "l", [1, 2])
        self.cat.restaurar_padrao("emg")
        self.assertTrue(self.cat.estado_atual("emg.atlas")["visivel"])
        self.assertEqual(self.cat.ordem_da_aba("emg"), ["emg.atlas", "emg.fadiga"])
        self.assertEqual(self.cat.splits_da_aba("emg"), {})

    def test_api_p4(self):
        self.assertEqual(self.cat.recomendados_para("EMG"), ["emg.atlas", "emg.fadiga"])
        self.assertEqual(self.cat.recomendados_para({"EMG", "EEG"}),
                         ["emg.atlas", "emg.fadiga", "ana.fft"])
        self.assertEqual(len(self.cat.recomendados_para("Hibrido")), 4)
        perfil = self.cat.estado_para_perfil("ECG")
        self.assertFalse(perfil["emg"]["paineis"]["emg.atlas"]["visivel"])
        self.assertTrue(perfil["ecg"]["paineis"]["ecg.hrv"]["visivel"])
        self.assertEqual(perfil["ecg"]["paineis"]["ecg.hrv"]["altura"], 180)
        json.dumps(perfil)


class TestGavetas(unittest.TestCase):
    """PainelGaveta e PilhaGavetas no Completo."""

    def test_recolher_expandir(self):
        pai, pilha, (ga, gb, gc) = montar_pilha()
        pai.show()
        processar()
        self.assertFalse(ga.recolhido())
        self.assertTrue(gb.recolhido(), "o padrão recolhido=True do catálogo vale")
        self.assertFalse(gb.conteudo().isVisible())
        self.assertTrue(ga.conteudo().isVisible())
        ga.set_recolhido(True)
        processar()
        self.assertFalse(ga.conteudo().isVisible())
        self.assertEqual(ga._bt_seta.text(), "▸")
        self.assertEqual(ga.cabecalho().property("aberta"), "false")
        self.assertLess(ga.height(), 40, "recolhida, só o cabeçalho fica")
        ga.alternar_recolhido()
        processar()
        self.assertTrue(ga.conteudo().isVisible())
        self.assertEqual(ga._bt_seta.text(), "▾")
        pilha.recolher_todos()
        self.assertTrue(all(g.recolhido() for g in pilha.gavetas()))
        pilha.expandir_todos()
        self.assertFalse(any(g.recolhido() for g in pilha.gavetas()))
        pai.close()

    def test_titulo_do_groupbox_vai_para_o_cabecalho(self):
        pai, pilha, (ga, gb, gc) = montar_pilha()
        self.assertEqual(ga.titulo(), "Painel A")
        self.assertEqual(ga.conteudo().title(), "", "o QGroupBox perde o título próprio")
        self.assertEqual(ga.conteudo().property("emGaveta"), "true")
        self.assertEqual(ga._lbl_titulo.texto_cheio(), "Painel A")
        # "&&" do QGroupBox vira "&" no cabeçalho
        g2 = pilha.adicionar_painel("d", grupo("Atlas && Eletrodos"))
        self.assertEqual(g2.titulo(), "Atlas & Eletrodos")
        g2.set_titulo("Outro")
        self.assertEqual(g2._lbl_titulo.texto_cheio(), "Outro")

    def test_fechar_e_reabrir(self):
        pai, pilha, (ga, gb, gc) = montar_pilha()
        pai.show()
        processar()
        self.assertTrue(ga.isVisible())
        ga.fechar()
        processar()
        self.assertFalse(ga.visivel_painel())
        self.assertTrue(ga.isHidden(), "fechar esconde, não destrói")
        self.assertIs(ga.conteudo(), pilha.gaveta("a").conteudo())
        # um show() de fora (ex.: _apply_detail_level) não reabre
        ga.setVisible(True)
        self.assertTrue(ga.isHidden())
        ga.set_visivel_painel(True)
        processar()
        self.assertTrue(ga.isVisible())
        # fechavel=False: sem botão fechar e fechar() não faz nada
        gd = pilha.adicionar_painel("d", grupo("Fixo"), fechavel=False)
        self.assertFalse(gd._bt_fechar.isVisibleTo(gd))
        gd.fechar()
        self.assertTrue(gd.visivel_painel())
        pai.close()

    def test_mover_e_restaurar(self):
        pai, pilha, (ga, gb, gc) = montar_pilha()
        self.assertEqual(pilha.ordem(), ["a", "b", "c"])
        self.assertFalse(pilha.pode_mover("a", -1))
        self.assertTrue(pilha.pode_mover("a", +1))
        pilha.mover("a", +1)
        self.assertEqual(pilha.ordem(), ["b", "a", "c"])
        pilha.mover_para_baixo("a")
        self.assertEqual(pilha.ordem(), ["b", "c", "a"])
        pilha.mover_para_baixo("a")              # já é o último: nada muda
        self.assertEqual(pilha.ordem(), ["b", "c", "a"])
        pilha.mover_para_cima("c")
        self.assertEqual(pilha.ordem(), ["c", "b", "a"])
        # a ordem do layout acompanha
        posicoes = [pilha._lay.indexOf(pilha.gaveta(i)) for i in pilha.ordem()]
        self.assertEqual(posicoes, sorted(posicoes))
        self.assertEqual(pilha.catalogo().ordem_da_aba("teste"), ["c", "b", "a"])
        ga.set_recolhido(True)
        gc.set_visivel_painel(False)
        gb.set_altura(300)
        pilha.restaurar_padrao()
        self.assertEqual(pilha.ordem(), ["a", "b", "c"])
        self.assertFalse(ga.recolhido())
        self.assertTrue(gc.visivel_painel())
        self.assertTrue(gb.recolhido(), "padrão de b é recolhido")
        self.assertIsNone(gb.altura())
        self.assertEqual(gc.altura(), 200, "padrão de c tem altura 200")

    def test_altura(self):
        pai, pilha, (ga, gb, gc) = montar_pilha()
        pai.show()
        processar()
        self.assertEqual(gc.altura(), 200)
        self.assertEqual(gc._corpo.height(), 200)
        ga.set_altura(260)
        processar()
        self.assertEqual(ga._corpo.height(), 260)
        ga.set_altura(1)                          # abaixo do mínimo: sobe ao mínimo
        self.assertGreaterEqual(ga.altura(), ga.altura_minima())
        ga.tamanho_padrao()
        self.assertIsNone(ga.altura())
        # arraste pela alça: simula os sinais da alça
        ga._ao_iniciar_arrasto()
        h0 = ga._corpo.height()
        ga._ao_arrastar(+50)
        self.assertEqual(ga.altura(), max(ga.altura_minima(), h0 + 50))
        pai.close()

    def test_persistencia_ida_e_volta_e_debounce(self):
        dono = _Dono()
        pai, pilha, (ga, gb, gc) = montar_pilha(dono=dono)
        recebidos = []
        pilha.estadoMudou.connect(lambda d: recebidos.append(d))
        pai.show()
        processar()
        ga.set_recolhido(True)
        gb.set_visivel_painel(False)
        gc.set_altura(240)
        pilha.mover("c", -1)
        processar(100)
        self.assertEqual(recebidos, [], "ainda dentro do debounce: nada emitido")
        processar(700)
        self.assertEqual(len(recebidos), 1, "várias mudanças viram UMA gravação")
        est = recebidos[0]
        self.assertEqual(est["ordem"], ["a", "c", "b"])
        self.assertEqual(est["paineis"]["a"], {"visivel": True, "recolhido": True, "altura": None})
        self.assertEqual(est["paineis"]["b"]["visivel"], False)
        self.assertEqual(est["paineis"]["c"]["altura"], 240)
        self.assertEqual(est, pilha.estado())
        json.dumps(est)
        # volta: uma pilha nova (outro catálogo) recebe o dict e fica igual
        pai2, pilha2, (ga2, gb2, gc2) = montar_pilha()
        sinais2 = []
        pilha2.estadoMudou.connect(lambda d: sinais2.append(d))
        pilha2.aplicar_estado(json.loads(json.dumps(est)))
        processar(700)
        self.assertEqual(pilha2.ordem(), ["a", "c", "b"])
        self.assertTrue(ga2.recolhido())
        self.assertFalse(gb2.visivel_painel())
        self.assertEqual(gc2.altura(), 240)
        self.assertEqual(pilha2.estado(), est)
        self.assertEqual(sinais2, [], "aplicar um estado salvo não dispara gravação")
        pai.close()

    def test_linha_lado_a_lado(self):
        pai = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(pai)
        pilha = P2.PilhaGavetas("ana")
        split = pilha.adicionar_linha([("fft", grupo("FFT")), ("bandas", grupo("Bandas"))],
                                      nome="fft+bandas", tamanhos=[600, 400])
        lay.addWidget(pilha)
        pai.resize(1000, 600)
        pai.show()
        processar()
        self.assertIsInstance(split, QtWidgets.QSplitter)
        self.assertEqual(split.count(), 2)
        self.assertEqual(pilha.ordem(), ["fft", "bandas"])
        g1, g2 = pilha.gaveta("fft"), pilha.gaveta("bandas")
        larg_antes = g1.width()
        g2.set_visivel_painel(False)
        processar()
        self.assertGreater(g1.width(), larg_antes, "fechando a vizinha, a outra ocupa a linha")
        g2.set_visivel_painel(True)
        processar()
        # recolhida numa linha: a gaveta fica só com o cabeçalho, no alto da célula
        g2.set_recolhido(True)
        processar()
        self.assertLess(g2.height(), 40)
        self.assertEqual(g2.pos().y(), 0)
        # divisão movida é persistida em "splits"
        split.setSizes([300, 700])
        split.splitterMoved.emit(300, 1)
        est = pilha.estado()
        self.assertIn("fft+bandas", est["splits"])
        self.assertEqual(len(est["splits"]["fft+bandas"]), 2)
        # mover um membro move a linha inteira
        pilha.adicionar_painel("stats", grupo("Estatísticas"))
        pilha.mover("bandas", +1)
        self.assertEqual(pilha.ordem(), ["stats", "fft", "bandas"])
        pai.close()

    def test_esta_ativo_e_gaveta_ativa(self):
        aba = {"visivel": True}
        dono = _Dono()
        pai, pilha, (ga, gb, gc) = montar_pilha(aba_visivel=lambda: aba["visivel"], dono=dono)
        self.assertTrue(ga.esta_ativo())
        self.assertFalse(gb.esta_ativo(), "recolhido não está ativo")
        ga.set_visivel_painel(False)
        self.assertFalse(ga.esta_ativo(), "fechado não está ativo")
        self.assertFalse(P2.gaveta_ativa(dono, "a"))
        ga.set_visivel_painel(True)
        self.assertTrue(P2.gaveta_ativa(dono, "a"))
        aba["visivel"] = False
        self.assertFalse(ga.esta_ativo(), "aba fora de foco não está ativa")
        aba["visivel"] = True
        # id desconhecido ou dono sem registro: True (nunca bloqueia por engano)
        self.assertTrue(P2.gaveta_ativa(dono, "nao.existe"))
        self.assertTrue(P2.gaveta_ativa(object(), "a"))
        # com a janela na tela, um ancestral oculto também desativa
        pai.show()
        processar()
        self.assertTrue(ga.esta_ativo())
        pilha.hide()
        processar()
        self.assertFalse(ga.esta_ativo())
        pilha.show()
        pai.close()

    def test_botao_paineis(self):
        pai, pilha, (ga, gb, gc) = montar_pilha()
        bt = pilha.botao_paineis()
        self.assertIs(bt, pilha.botao_paineis(), "criado uma vez só")
        self.assertEqual(bt.objectName(), "botaoPaineis")
        self.assertFalse(bt.isHidden())
        gb.set_visivel_painel(False)
        bt.menu().aboutToShow.emit()
        acoes = bt.menu().actions()
        marcaveis = [a for a in acoes if a.isCheckable()]
        self.assertEqual([a.text() for a in marcaveis], ["Painel A", "Painel B", "Painel C"])
        self.assertEqual([a.isChecked() for a in marcaveis], [True, False, True])
        textos = [a.text() for a in acoes if not a.isSeparator() and not a.isCheckable()]
        self.assertEqual(textos, ["Recolher todos", "Expandir todos", "Restaurar o padrão"])
        marcaveis[1].setChecked(True)             # marcar reabre
        self.assertTrue(gb.visivel_painel())
        # menu "⋯" da gaveta
        ga.menu().aboutToShow.emit()
        textos = [a.text() for a in ga.menu().actions() if not a.isSeparator()]
        self.assertEqual(textos, ["Mover para cima", "Mover para baixo", "Tamanho padrão", "Fechar"])
        self.assertFalse(ga.menu().actions()[0].isEnabled(), "primeira não sobe")

    def test_qss_usa_so_cores_do_tema(self):
        for paleta in (PALETA_CLARA, PALETA_ESCURA):
            qss = P2.qss_gavetas(paleta)
            self.assertIn(paleta["accent"], qss)
            self.assertIn(paleta["surface_alt"], qss)
            self.assertNotIn("{c[", qss)
            self.assertNotIn("}}", qss)
            app.setStyleSheet(qss)             # o Qt aceita a folha sem reclamar
        app.setStyleSheet("")


class TestSimples(unittest.TestCase):
    """Com simples=True nada do cromo existe; set_simples alterna em tempo real."""

    def test_simples_sem_cabecalho(self):
        pai, pilha, (ga, gb, gc) = montar_pilha(simples=True)
        pai.show()
        processar()
        for g in (ga, gb, gc):
            self.assertIsNone(g.cabecalho())
            self.assertIsNone(g.menu())
            self.assertIsNone(g.findChild(QtWidgets.QFrame, "gavetaCabecalho"))
            self.assertIsNone(g.findChild(QtWidgets.QFrame, "gavetaAlca"))
            self.assertIsNone(g.findChild(QtWidgets.QToolButton))
            self.assertEqual(g.conteudo().property("emGaveta"), "false")
            self.assertTrue(g.conteudo().isVisible(), "no Simples o conteúdo sempre aparece")
        self.assertEqual(ga.conteudo().title(), "Painel A", "o QGroupBox mantém o título")
        self.assertTrue(gb.conteudo().isVisible(), "recolhido do catálogo não vale no Simples")
        self.assertTrue(pilha.botao_paineis().isHidden())
        self.assertIsNone(pai.findChild(QtWidgets.QFrame, "gavetaCabecalho"))
        # estado "fechado" não esconde no Simples
        ga.set_visivel_painel(False)
        processar()
        self.assertTrue(ga.isVisible())
        # esta_ativo no Simples segue só a visibilidade real
        self.assertTrue(gb.esta_ativo())
        pai.close()

    def test_alternar_nivel(self):
        pai, pilha, (ga, gb, gc) = montar_pilha(simples=True)
        pai.show()
        processar()
        ga.set_visivel_painel(False)
        pilha.set_simples(False)
        processar()
        self.assertIsNotNone(ga.cabecalho(), "o cromo é criado ao sair do Simples")
        self.assertEqual(ga.conteudo().title(), "")
        self.assertTrue(ga.isHidden(), "fechado volta a valer no Completo")
        self.assertFalse(gb.conteudo().isVisible(), "recolhido volta a valer")
        self.assertFalse(pilha.botao_paineis().isHidden())
        pilha.set_simples(True)
        processar()
        self.assertTrue(ga.cabecalho().isHidden())
        self.assertEqual(ga.conteudo().title(), "Painel A")
        self.assertTrue(ga.isVisible())
        self.assertTrue(gb.conteudo().isVisible())
        pai.close()




class TestIntegracaoJanela(unittest.TestCase):
    """As pilhas existem nas abas certas, o painel fechado não processa e o
    Simples não mostra nada das gavetas."""

    @classmethod
    def setUpClass(cls):
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

    def test_pilhas_e_catalogo(self):
        win = self.win
        for aba in ("emg", "ecg", "eog", "analises", "filtros", "rede"):
            self.assertIn(aba, win._pilhas, aba)
            self.assertTrue(win._pilhas[aba].gavetas(), aba)
        ids = {it["id"] for it in ROA.CATALOGO_PAINEIS.itens()}
        for pid in ("emg.atlas", "emg.tempo_freq", "ecg.tacograma", "eog.oculometria", "ana.fft"):
            self.assertIn(pid, ids)
        for it in ROA.CATALOGO_PAINEIS.itens():
            for campo in ("id", "titulo", "aba", "exames", "padrao"):
                self.assertIn(campo, it)
        self.assertIs(win._catalogo_paineis, ROA.CATALOGO_PAINEIS)

    def test_painel_fechado_nao_processa(self):
        win = self.win
        g = win._pilhas["emg"].gaveta("emg.tempo_freq")
        self.assertIsNotNone(g)
        g.set_visivel_painel(False)
        processar_eventos(20)
        self.assertFalse(ROA.gaveta_ativa(win, "emg.tempo_freq"))
        chamadas = []
        original = win.emg_spec_img.setImage
        win.emg_spec_img.setImage = lambda *a, **k: chamadas.append(1)
        try:
            # o laço principal pula o cálculo pesado do painel fechado
            win._set_num_channels(8)
            win.config.channel_signal_types[:8] = ["EMG"] * 8
            import numpy as np
            win.buffer[:, :] = np.random.default_rng(1).normal(0, 20, win.buffer.shape)
            win.samples_total = win.buffer.shape[1]
            for _ in range(3):
                win._update_emg_view()
        finally:
            win.emg_spec_img.setImage = original
        self.assertEqual(chamadas, [])
        g.set_visivel_painel(True)

    def test_estado_persiste_no_config(self):
        win = self.win
        pilha = win._pilhas["ecg"]
        g = pilha.gaveta("ecg.hrv_nao_linear")
        self.assertIsNotNone(g)
        g.set_recolhido(True)
        pilha.salvar_agora() if hasattr(pilha, "salvar_agora") else None
        processar_eventos(700)
        est = win.config.paineis.get("ecg", {})
        self.assertTrue(est.get("paineis", {}).get("ecg.hrv_nao_linear", {}).get("recolhido"))
        pilha.restaurar_padrao()

    def test_simples_sem_cromo(self):
        win = self.win
        win.config.ui_level = "simples"
        win._definir_nivel("simples")
        processar_eventos(50)
        try:
            for aba, pilha in win._pilhas.items():
                for g in pilha.gavetas():
                    # no Simples o cromo nem é criado (_cab fica None) ou fica oculto
                    cab = getattr(g, "_cab", None)
                    if cab is not None:
                        self.assertFalse(cab.isVisibleTo(g), aba)
                bt = pilha.botao_paineis()
                self.assertFalse(bt.isVisibleTo(bt.parentWidget() or bt), aba)
        finally:
            win.config.ui_level = "avancado"
            win._definir_nivel("avancado")
            processar_eventos(50)


if __name__ == "__main__":
    unittest.main()
