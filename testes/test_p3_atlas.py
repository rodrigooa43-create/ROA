# -*- coding: utf-8 -*-
"""P3 — atlas muscular desenhado em código: API, snap SENIAM, conversão de
montagem antiga, áreas e tempo de pintura.

O AtlasCorpoWidget vive dentro do ROA.py.
Roda offscreen, sem janela.
"""
import os
import sys
import time
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA, app, processar_eventos  # noqa: E402  (o atlas vive dentro do ROA.py)
from PySide6 import QtCore, QtGui, QtWidgets  # noqa: E402

M = ROA
ROA._apply_theme_colors("ROA (azul clinico)")

# As 19 chaves antigas de ATLAS_MUSCLE_XY (todas de COMMON_MUSCLES menos
# "(não definido)" e "Outro / Custom").
ANTIGOS_19 = {
    "Deltoide Anterior":         ("front", 0.31, 0.235),
    "Deltoide Medio":            ("front", 0.275, 0.220),
    "Peitoral Maior":            ("front", 0.415, 0.275),
    "Bíceps Braquial":           ("front", 0.225, 0.350),
    "Flexor Carpi Radialis":     ("front", 0.165, 0.470),
    "Iliopsoas":                 ("front", 0.445, 0.500),
    "Quadríceps (Reto Femoral)": ("front", 0.430, 0.625),
    "Vasto Lateral":             ("front", 0.370, 0.640),
    "Vasto Medial":              ("front", 0.470, 0.700),
    "Tibial Anterior":           ("front", 0.440, 0.840),
    "Deltoide Posterior":        ("back",  0.310, 0.235),
    "Trapézio":                  ("back",  0.500, 0.195),
    "Latíssimo do Dorso":        ("back",  0.400, 0.330),
    "Tríceps Braquial":          ("back",  0.225, 0.350),
    "Extensor Carpi Radialis":   ("back",  0.165, 0.470),
    "Glúteo Máximo":             ("back",  0.430, 0.510),
    "Isquiotibiais (Bíceps F.)": ("back",  0.430, 0.650),
    "Gastrocnêmio (medial)":     ("back",  0.440, 0.820),
    "Sóleo":                     ("back",  0.440, 0.885),
}
ROSTO = ("Masseter", "Temporal", "Frontal", "Orbicular do olho", "Zigomático")
SENIAM_EXTRA = ("Trapézio superior", "Reto abdominal", "Eretor da espinha", "Glúteo médio",
                "Fibular longo", "Extensor dos dedos", "Flexor dos dedos",
                "Esternocleidomastóideo")


def _pinta(wdg, w, h, n=1):
    """Pinta o widget n vezes num QPixmap w x h e devolve o tempo médio (ms)."""
    wdg.resize(w, h)
    pm = QtGui.QPixmap(w, h)
    t0 = time.perf_counter()
    for _ in range(n):
        p = QtGui.QPainter(pm)
        wdg.pintar(p, w, h)
        p.end()
    return (time.perf_counter() - t0) / max(1, n) * 1000.0, pm


class TestTabelas(unittest.TestCase):
    """Constantes: vistas, áreas e pontos SENIAM com todas as chaves pedidas."""

    def test_vistas_e_areas(self):
        self.assertEqual(M.ATLAS_VISTAS, ("front", "back", "side"))
        esperadas = {"rosto", "pescoco", "peito_abdomen", "costas", "braco_D", "braco_E",
                     "antebraco_mao_D", "antebraco_mao_E", "mao_D", "mao_E", "perna_D",
                     "perna_E", "pe_D", "pe_E"}
        self.assertTrue(esperadas <= set(M.ATLAS_AREAS))
        for aid, a in M.ATLAS_AREAS.items():
            self.assertIn(a["vista"], M.ATLAS_VISTAS, aid)
            x0, y0, x1, y1 = a["recorte"]
            self.assertLess(x0, x1, aid); self.assertLess(y0, y1, aid)
            self.assertIn(a["lado"], ("D", "E", None), aid)
            self.assertTrue(a["titulo"])

    def test_seniam_tem_todas_as_chaves(self):
        for k in list(ANTIGOS_19) + list(ROSTO) + list(SENIAM_EXTRA):
            self.assertIn(k, M.ELETRODOS_SENIAM, k)
            e = M.ELETRODOS_SENIAM[k]
            self.assertIn(e["vista"], M.ATLAS_VISTAS)
            self.assertTrue(0.0 < e["x"] < 1.0 and 0.0 <= e["y"] <= 1.0, k)
            self.assertIn(e["area"], M.ATLAS_AREAS, k)
            self.assertTrue(e["nota"], k)
            self.assertIn(e["lado"], ("D", "E", "ambos"), k)

    def test_seniam_mesma_vista_dos_antigos(self):
        """Os 19 músculos antigos ficam na mesma vista para a conversão cair
        direto no ponto SENIAM."""
        for k, (v, _x, _y) in ANTIGOS_19.items():
            self.assertEqual(M.ELETRODOS_SENIAM[k]["vista"], v, k)

    def test_pontos_seniam_dentro_do_corpo(self):
        """Todo ponto SENIAM (dos dois lados e no perfil) cai dentro do contorno."""
        d = M.CorpoHumanoDesenho()
        for vista in M.ATLAS_VISTAS:
            corpo = d.caminho_corpo(vista, 400.0, 800.0)
            for m, lado, nx, ny in M.CorpoHumanoDesenho.pontos_seniam(vista):
                self.assertTrue(corpo.contains(QtCore.QPointF(nx * 400.0, ny * 800.0)),
                                f"{m} {lado} fora do corpo em {vista} ({nx:.3f}, {ny:.3f})")


class TestDesenho(unittest.TestCase):
    """Motor de desenho: caminhos cacheados, áreas inversas, calor."""

    def test_caminho_cacheado(self):
        d = M.CorpoHumanoDesenho()
        a = d.caminho_corpo("front", 200, 400)
        b = d.caminho_corpo("front", 200, 400)
        self.assertIs(a, b)
        self.assertGreater(a.elementCount(), 100)
        for vista in M.ATLAS_VISTAS:
            self.assertGreater(d.caminho_corpo(vista, 300, 600).elementCount(), 50)

    def test_para_area_de_area_inversas(self):
        for aid in M.ATLAS_AREAS:
            for (x, y) in ((0.1, 0.2), (0.5, 0.5), (0.93, 0.98)):
                ax, ay = M.CorpoHumanoDesenho.para_area(x, y, aid)
                x2, y2 = M.CorpoHumanoDesenho.de_area(ax, ay, aid)
                self.assertAlmostEqual(x, x2, places=9, msg=aid)
                self.assertAlmostEqual(y, y2, places=9, msg=aid)
            # o canto da área é (0,0) e (1,1)
            x0, y0, x1, y1 = M.ATLAS_AREAS[aid]["recorte"]
            self.assertEqual(M.CorpoHumanoDesenho.para_area(x0, y0, aid), (0.0, 0.0))
            ax, ay = M.CorpoHumanoDesenho.para_area(x1, y1, aid)
            self.assertAlmostEqual(ax, 1.0); self.assertAlmostEqual(ay, 1.0)

    def test_recorte_area_espelha_nas_costas(self):
        r_f = M.CorpoHumanoDesenho.recorte_area("braco_D", "front")
        r_b = M.CorpoHumanoDesenho.recorte_area("braco_D", "back")
        self.assertAlmostEqual(r_f[0], 1.0 - r_b[2]); self.assertAlmostEqual(r_f[2], 1.0 - r_b[0])
        r_s = M.CorpoHumanoDesenho.recorte_area("braco_D", "side")
        self.assertAlmostEqual((r_s[0] + r_s[2]) * 0.5, 0.5)

    def test_cor_calor_e_pintura(self):
        c0, c1 = M.atlas_cor_calor(0.0), M.atlas_cor_calor(1.0)
        self.assertGreater(c0.blue(), c0.red())      # frio
        self.assertGreater(c1.red(), c1.blue())      # quente
        pm = QtGui.QPixmap(100, 100); pm.fill(QtGui.QColor("white"))
        p = QtGui.QPainter(pm)
        rec = QtGui.QPainterPath(); rec.addEllipse(10, 10, 80, 80)
        M.CorpoHumanoDesenho.pintar_calor(p, [(50, 50, 1.0, 40)], rec)
        p.end()
        img = pm.toImage()
        self.assertNotEqual(img.pixelColor(50, 50).name(), "#ffffff")   # pintou no centro
        self.assertEqual(img.pixelColor(2, 2).name(), "#ffffff")        # recortado fora


class TestWidgetAPI(unittest.TestCase):
    """API pública igual à do MuscleAtlasWidget, mais vista lateral e áreas."""

    def setUp(self):
        self.w = M.AtlasCorpoWidget()
        self.w.resize(300, 470)

    def test_api_existe(self):
        for nome in ("set_view", "get_view", "set_show_labels", "set_place_mode",
                     "set_muscle_activations", "set_live_channel_data", "set_electrodes",
                     "get_electrodes", "selected_id", "select", "add_electrode",
                     "remove_selected", "clear_all", "rename", "set_channel", "set_zoom",
                     "zoom_regiao", "render_highres", "muscle_side", "_nearest_muscle",
                     "set_area", "areas_disponiveis", "_find", "_quality_color"):
            self.assertTrue(callable(getattr(self.w, nome, None)), nome)
        for sig in ("sigElectrodesChanged", "sigElectrodeSelected", "sigZoomChanged"):
            self.assertTrue(hasattr(self.w, sig), sig)
        self.assertEqual(len(self.w.REGIOES[0]), 4)       # compat com o combo da aba EMG

    def test_vistas(self):
        self.w.set_view("back"); self.assertEqual(self.w.get_view(), "back")
        self.w.set_view("side"); self.assertEqual(self.w.get_view(), "side")
        self.w.set_view("xyz"); self.assertEqual(self.w.get_view(), "front")

    def test_add_electrode_em_cada_vista(self):
        recebidos = []
        self.w.sigElectrodesChanged.connect(lambda: recebidos.append("mudou"))
        for i, vista in enumerate(M.ATLAS_VISTAS):
            e = self.w.add_electrode(0.4, 0.3, view=vista, channel=i)
            self.assertEqual(e["view"], vista)
            self.assertEqual(e["channel"], i)
            self.assertEqual(e["atlas"], 2)
            self.assertEqual(self.w.selected_id(), e["id"])
        self.assertEqual(len(self.w.get_electrodes()), 3)
        self.assertEqual(len(recebidos), 3)
        self.w.rename(1, "Teste"); self.assertEqual(self.w._find(1)["name"], "Teste")
        self.w.set_channel(1, 5, "Bíceps Braquial")
        self.assertEqual(self.w._find(1)["channel"], 5)
        self.w.select(2); self.w.remove_selected()
        self.assertEqual(len(self.w.get_electrodes()), 2)
        self.w.clear_all(); self.assertEqual(self.w.get_electrodes(), [])

    def test_snap_ao_ponto_seniam(self):
        pt = M.CorpoHumanoDesenho.ponto_seniam("Bíceps Braquial", "D")
        e = self.w.add_electrode_snap(pt[0] + 0.01, pt[1] + 0.01, "front")
        self.assertEqual(e["muscle"], "Bíceps Braquial")
        self.assertAlmostEqual(e["x"], pt[0], places=6)
        self.assertAlmostEqual(e["y"], pt[1], places=6)
        self.assertEqual(self.w.muscle_side(e["x"]), "D")
        # espelho = lado E
        e2 = self.w.add_electrode_snap(1.0 - pt[0], pt[1], "front")
        self.assertEqual(e2["muscle"], "Bíceps Braquial")
        self.assertEqual(self.w.muscle_side(e2["x"]), "E")
        # longe de qualquer ponto: fica livre e sem músculo
        e3 = self.w.add_electrode_snap(0.02, 0.98, "front")
        self.assertEqual(e3["muscle"], "")
        self.assertAlmostEqual(e3["x"], 0.02)
        # perfil
        self.w.set_view("side")
        lat = M.CorpoHumanoDesenho.ponto_seniam("Vasto Lateral", "E", "side")
        e4 = self.w.add_electrode_snap(lat[0], lat[1])
        self.assertEqual(e4["muscle"], "Vasto Lateral")
        self.assertEqual(self.w.muscle_side(e4["x"]), "E")

    def test_nearest_muscle_usa_seniam(self):
        for m, e in M.ELETRODOS_SENIAM.items():
            if e.get("alias_de"):
                continue
            self.assertEqual(self.w._nearest_muscle(e["x"], e["y"], e["vista"]), m, m)

    def test_areas(self):
        ids = [a for a, _t, _l in self.w.areas_disponiveis()]
        self.assertEqual(ids, list(M.ATLAS_AREAS))
        self.w.set_area("costas"); self.assertEqual(self.w.get_view(), "back")
        self.assertEqual(self.w.get_area(), "costas")
        self.w.set_area("rosto"); self.assertEqual(self.w.get_view(), "front")
        self.w.set_area(None); self.assertIsNone(self.w.get_area())
        self.w.set_area("nao_existe"); self.assertIsNone(self.w.get_area())
        # eletrodo colocado na área tem coordenadas do corpo inteiro
        self.w.set_area("braco_D")
        pt = M.CorpoHumanoDesenho.ponto_seniam("Bíceps Braquial", "D")
        e = self.w.add_electrode(pt[0], pt[1])
        ax, ay = M.CorpoHumanoDesenho.para_area(e["x"], e["y"], "braco_D")
        self.assertTrue(0.0 <= ax <= 1.0 and 0.0 <= ay <= 1.0)
        self.w.set_area(None)
        self.assertEqual(self.w.get_electrodes()[0]["x"], e["x"])

    def test_zoom_e_regioes(self):
        zs = []
        self.w.sigZoomChanged.connect(zs.append)
        self.w.set_zoom(3.0, (0.3, 0.3)); self.assertAlmostEqual(self.w._zoom, 3.0)
        self.assertTrue(self.w.zoom_regiao("Antebraço e mão"))
        self.assertFalse(self.w.zoom_regiao("não existe"))
        self.assertTrue(self.w.zoom_regiao("Corpo inteiro"))
        self.assertTrue(zs)
        self.assertAlmostEqual(zs[-1], 1.0)

    def test_tela_e_de_tela_inversas(self):
        self.w.set_zoom(2.5, (0.4, 0.6))
        for (nx, ny) in ((0.2, 0.3), (0.5, 0.5), (0.9, 0.95)):
            sx, sy = self.w._tela(nx, ny, 300, 470)
            nx2, ny2 = self.w._de_tela(sx, sy, 300, 470)
            self.assertAlmostEqual(nx, nx2, places=6); self.assertAlmostEqual(ny, ny2, places=6)

    def test_set_electrodes_converte_antigos(self):
        """Montagem antiga (sem atlas=2) entra pelo set_electrodes já convertida."""
        antigos = [{"id": 1, "name": "B", "x": 0.225, "y": 0.35, "view": "front",
                    "channel": 0, "muscle": "Bíceps Braquial"}]
        self.w.set_electrodes(antigos)
        e = self.w.get_electrodes()[0]
        pt = M.CorpoHumanoDesenho.ponto_seniam("Bíceps Braquial", "D")
        self.assertAlmostEqual(e["x"], pt[0]); self.assertAlmostEqual(e["y"], pt[1])
        self.assertEqual(e["atlas"], 2)
        # já convertido: passa intacto
        self.w.set_electrodes([{"id": 3, "name": "X", "x": 0.33, "y": 0.44, "view": "side",
                                "channel": 2, "muscle": "", "atlas": 2}])
        e = self.w.get_electrodes()[0]
        self.assertEqual((e["x"], e["y"], e["view"], e["channel"]), (0.33, 0.44, "side", 2))

    def test_tempo_de_pintura(self):
        """Média de 30 pinturas em 300x470 abaixo de 12 ms (meta 8 ms)."""
        for i, m in enumerate(("Bíceps Braquial", "Peitoral Maior", "Tibial Anterior",
                               "Reto abdominal", "Quadríceps (Reto Femoral)", "Deltoide Medio")):
            pt = M.CorpoHumanoDesenho.ponto_seniam(m, "D" if i % 2 else "E")
            self.w.add_electrode(pt[0], pt[1], "front", channel=i, muscle=m)
        self.w.set_live_channel_data({i: (15 * (i + 1), 80) for i in range(6)})
        _pinta(self.w, 300, 470, 2)             # aquece caches
        ms, _ = _pinta(self.w, 300, 470, 30)
        self.assertLess(ms, 12.0, f"pintura média de {ms:.2f} ms")
        ms2, _ = _pinta(self.w, 600, 900, 10)
        self.assertLess(ms2, 24.0, f"pintura 600x900 média de {ms2:.2f} ms")

    def test_render_highres(self):
        self.w.add_electrode(0.4, 0.3)
        pm = self.w.render_highres(2.0, "Título")
        self.assertEqual((pm.width(), pm.height()), (600, 940))
        pm = self.w.render_highres(1.0)
        self.assertEqual((pm.width(), pm.height()), (300, 470))

    def test_miniatura_pinta(self):
        self.w.set_miniatura(True)
        self.w.add_electrode(0.4, 0.3, channel=0)
        self.w.set_live_channel_data({0: (80, 90)})
        for vista in M.ATLAS_VISTAS:
            self.w.set_view(vista)
            _ms, pm = _pinta(self.w, 90, 140, 1)
            self.assertEqual((pm.width(), pm.height()), (90, 140))
            img = pm.toImage()
            # o corpo foi pintado (algum pixel do meio difere do fundo)
            fundo = img.pixelColor(1, 1)
            self.assertNotEqual(img.pixelColor(45, 70), fundo, vista)


class TestConversao(unittest.TestCase):
    """converter_montagem_antiga preserva músculo/canal/nome/id e marca atlas=2."""

    def test_19_musculos_antigos(self):
        antigos = []
        for i, (m, (v, x, y)) in enumerate(ANTIGOS_19.items()):
            antigos.append({"id": i + 1, "name": f"E{i + 1}", "x": x, "y": y, "view": v,
                            "channel": i % 8, "muscle": m})
        novos = M.converter_montagem_antiga(antigos, ANTIGOS_19)
        self.assertEqual(len(novos), 19)
        for a, n in zip(antigos, novos):
            for k in ("id", "name", "channel", "muscle", "view"):
                self.assertEqual(a[k], n[k], k)
            self.assertEqual(n["atlas"], 2)
            # mesma regra do muscle_side de hoje; na linha média (Trapézio em
            # x=0.5) vale a convenção do módulo
            lado = M._atlas_lado_antigo(a["x"], a["view"])
            pt = M.CorpoHumanoDesenho.ponto_seniam(a["muscle"], lado)
            self.assertAlmostEqual(n["x"], pt[0], places=6, msg=a["muscle"])
            self.assertAlmostEqual(n["y"], pt[1], places=6, msg=a["muscle"])

    def test_lado_esquerdo_pelo_x(self):
        """Bíceps antigo à direita de quem olha (x>0.5, frontal) = lado E."""
        n = M.converter_montagem_antiga(
            [{"id": 1, "name": "b", "x": 0.775, "y": 0.35, "view": "front",
              "channel": 0, "muscle": "Bíceps Braquial"}], ANTIGOS_19)[0]
        pt = M.CorpoHumanoDesenho.ponto_seniam("Bíceps Braquial", "E")
        self.assertAlmostEqual(n["x"], pt[0]); self.assertGreater(n["x"], 0.5)
        # nas costas o x<0.5 é o lado E do paciente
        n = M.converter_montagem_antiga(
            [{"id": 2, "name": "t", "x": 0.225, "y": 0.35, "view": "back",
              "channel": 1, "muscle": "Tríceps Braquial"}], ANTIGOS_19)[0]
        pt = M.CorpoHumanoDesenho.ponto_seniam("Tríceps Braquial", "E")
        self.assertAlmostEqual(n["x"], pt[0])

    def test_sem_musculo_e_custom(self):
        antigos = [
            {"id": 7, "name": "livre", "x": 0.25, "y": 0.36, "view": "front", "channel": 3, "muscle": ""},
            {"id": 8, "name": "custom", "x": 0.44, "y": 0.83, "view": "front", "channel": 4,
             "muscle": "Outro / Custom"},
            {"id": 9, "name": "costas", "x": 0.60, "y": 0.40, "view": "back", "channel": -1, "muscle": ""},
        ]
        novos = M.converter_montagem_antiga(antigos, ANTIGOS_19)
        self.assertEqual(len(novos), 3)
        for a, n in zip(antigos, novos):
            for k in ("id", "name", "channel", "muscle", "view"):
                self.assertEqual(a[k], n[k], k)
            self.assertEqual(n["atlas"], 2)
            self.assertTrue(0.02 <= n["x"] <= 0.98 and 0.0 <= n["y"] <= 1.0)
        # o eletrodo livre perto do bíceps antigo acompanha o bíceps novo
        pt = M.CorpoHumanoDesenho.ponto_seniam("Bíceps Braquial", "D")
        self.assertLess(abs(novos[0]["x"] - pt[0]), 0.08)
        self.assertLess(abs(novos[0]["y"] - pt[1]), 0.04)

    def test_idempotente_e_tolerante(self):
        antigos = [{"id": 1, "name": "a", "x": 0.3, "y": 0.3, "view": "front", "channel": 0,
                    "muscle": "Peitoral Maior"}]
        uma = M.converter_montagem_antiga(antigos, ANTIGOS_19)
        duas = M.converter_montagem_antiga(uma, ANTIGOS_19)
        self.assertEqual(uma, duas)
        # tabela antiga vazia e item malformado não derrubam
        novos = M.converter_montagem_antiga([{"id": "x"}, "lixo", {"x": 0.5, "y": 0.5}], {})
        self.assertEqual(len(novos), 1)
        self.assertEqual(novos[0]["atlas"], 2)




class TestIntegracaoAbaMusculos(unittest.TestCase):
    """O atlas novo está na aba Músculos: vistas e áreas no combo, eletrodo,
    tabela, ativação ao vivo e conversão de montagem antiga."""

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

    def test_widget_e_combo(self):
        win = self.win
        self.assertIsInstance(win.emg_atlas, ROA.AtlasCorpoWidget)
        dados = [win.emg_atlas_view.itemData(i) for i in range(win.emg_atlas_view.count())]
        self.assertIn("view:side", dados)
        self.assertTrue(any(isinstance(d, str) and d.startswith("area:") for d in dados))
        win.emg_atlas_view.setCurrentIndex(dados.index("view:side"))
        processar_eventos(20)
        self.assertEqual(win.emg_atlas.get_view(), "side")
        idx_area = next(i for i, d in enumerate(dados) if isinstance(d, str) and d.startswith("area:"))
        win.emg_atlas_view.setCurrentIndex(idx_area)
        processar_eventos(20)
        self.assertEqual(win.emg_atlas.get_area(), dados[idx_area].split(":", 1)[1])
        win.emg_atlas_view.setCurrentIndex(dados.index("view:front"))
        processar_eventos(20)
        self.assertIsNone(win.emg_atlas.get_area())

    def test_eletrodo_tabela_e_ativacao(self):
        win = self.win
        win._set_num_channels(8)
        win.config.channel_signal_types[:8] = ["EMG"] * 8
        win.emg_atlas.clear_all()
        e = win.emg_atlas.add_electrode(0.5, 0.5, view="front", channel=0, muscle="Bíceps Braquial")
        self.assertIsNotNone(e)
        win._emg_atlas_rebuild_table()
        self.assertGreaterEqual(win.emg_atlas_table.rowCount(), 1)
        dados = ROA.np.random.default_rng(3).normal(0, 20, (ROA.MAX_CHANNELS, 2 * ROA.SAMPLE_RATE))
        env = {ch: ROA.np.abs(dados[ch]) for ch in range(8)}
        win._emg_atlas_update_live(dados, env)
        processar_eventos(20)
        win.emg_atlas.repaint()

    def test_montagem_antiga_converte_sem_perder_musculo(self):
        win = self.win
        antigos = [{"id": 1, "name": "E1", "x": 0.225, "y": 0.35, "view": "front", "channel": 0, "muscle": "Bíceps Braquial"},
                   {"id": 2, "name": "E2", "x": 0.44, "y": 0.82, "view": "back", "channel": 1, "muscle": "Gastrocnêmio (medial)"},
                   {"id": 3, "name": "E3", "x": 0.6, "y": 0.6, "view": "front", "channel": 2, "muscle": ""}]
        win.emg_atlas.set_electrodes(antigos)
        novos = win.emg_atlas.get_electrodes()
        self.assertEqual(len(novos), 3)
        por_id = {e["id"]: e for e in novos}
        self.assertEqual(por_id[1]["muscle"], "Bíceps Braquial")
        self.assertEqual(por_id[2]["muscle"], "Gastrocnêmio (medial)")
        self.assertEqual(por_id[1]["channel"], 0)
        for e in novos:
            self.assertEqual(e.get("atlas"), 2)
        # o carregador do config aceita a vista "side" e preserva "atlas"
        import tempfile, json
        pasta = tempfile.mkdtemp(prefix="roa_p3_cfg_")
        cfg = ROA.AppConfig(path=os.path.join(pasta, "config.json"))
        cfg.emg_electrode_montage = [dict(e) for e in novos] + [
            {"id": 9, "name": "E9", "x": 0.5, "y": 0.4, "view": "side", "channel": 3, "muscle": "Tríceps Braquial", "atlas": 2}]
        cfg.save()
        cfg2 = ROA.AppConfig(path=os.path.join(pasta, "config.json"))
        vistas = {e["view"] for e in cfg2.emg_electrode_montage}
        self.assertIn("side", vistas)
        self.assertTrue(all(e.get("atlas") == 2 for e in cfg2.emg_electrode_montage))


if __name__ == "__main__":
    unittest.main()
