# -*- coding: utf-8 -*-
"""P9 — lançador: cache de bytecode, execução como __main__ e tela de abertura.

Roda sem o ROA.py de verdade: usa um fonte pequeno numa pasta temporária, para
o teste ser rápido e independente do tamanho do programa.
"""
import os
import sys
import tempfile
import time
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import EEG_Data_Collector as L  # noqa: E402


class TestCacheBytecode(unittest.TestCase):
    """O .pyc em cache é criado, reaproveitado e invalidado quando o fonte muda."""

    def setUp(self):
        self.pasta = tempfile.mkdtemp(prefix="roa_p9_")
        self.alvo = os.path.join(self.pasta, "ROA.py")
        with open(self.alvo, "w", encoding="utf-8") as f:
            f.write("X = 41\nif __name__ == '__main__':\n    X = 42\n")

    def test_cria_e_reaproveita(self):
        pasta = L.pasta_cache(self.pasta)
        self.assertTrue(pasta.endswith(".roa_cache"), pasta)
        destino = L.caminho_cache(self.alvo, pasta)
        self.assertIsNone(L.ler_cache(self.alvo, destino))
        code = L.obter_codigo(self.alvo)
        self.assertTrue(os.path.exists(destino), "o cache não foi gravado")
        self.assertIsNotNone(code)
        # segunda leitura vem do cache e é quase instantânea
        t = time.time()
        code2 = L.ler_cache(self.alvo, destino)
        self.assertIsNotNone(code2)
        self.assertLess(time.time() - t, 0.5)

    def test_invalida_quando_fonte_muda(self):
        pasta = L.pasta_cache(self.pasta)
        destino = L.caminho_cache(self.alvo, pasta)
        L.obter_codigo(self.alvo)
        with open(self.alvo, "a", encoding="utf-8") as f:
            f.write("\n# mudou\n")
        self.assertIsNone(L.ler_cache(self.alvo, destino))
        # e recompila sozinho
        self.assertIsNotNone(L.obter_codigo(self.alvo))
        self.assertIsNotNone(L.ler_cache(self.alvo, destino))

    def test_cache_corrompido_nao_derruba(self):
        pasta = L.pasta_cache(self.pasta)
        destino = L.caminho_cache(self.alvo, pasta)
        L.obter_codigo(self.alvo)
        with open(destino, "wb") as f:
            f.write(b"lixo")
        self.assertIsNone(L.ler_cache(self.alvo, destino))
        self.assertIsNotNone(L.obter_codigo(self.alvo))

    def test_executa_como_main_com_file(self):
        code = L.obter_codigo(self.alvo)
        mod = L.executar(code, self.alvo, nome="roa_teste_modulo")
        self.assertEqual(mod.X, 41)            # guarda __main__ não disparou
        self.assertEqual(mod.__file__, self.alvo)
        mod = L.executar(code, self.alvo, nome="__main__")
        self.assertEqual(mod.X, 42)            # como `python ROA.py`
        self.assertEqual(sys.argv[0], self.alvo)

    def test_compila_em_subprocesso(self):
        pasta = L.pasta_cache(self.pasta)
        destino = L.caminho_cache(self.alvo, pasta)
        chamadas = []
        ok = L._compilar_em_subprocesso(self.alvo, destino, espera=lambda: chamadas.append(1))
        self.assertTrue(ok)
        self.assertIsNotNone(L.ler_cache(self.alvo, destino))
        self.assertGreater(len(chamadas), 0, "espera() mantém a animação viva")


class TestSplash(unittest.TestCase):
    """A tela de abertura pinta, fala os 9 idiomas e fecha ao ver outra janela."""

    def test_frases_nos_nove_idiomas(self):
        idiomas = {"pt", "en", "es", "it", "fr", "zh", "de", "ja", "ru"}
        for chave, frases in L._FRASES.items():
            self.assertEqual(set(frases), idiomas, chave)
            for lang, txt in frases.items():
                self.assertTrue(txt.strip(), (chave, lang))

    def test_pinta_e_fecha_ao_ver_janela(self):
        from PySide6 import QtWidgets
        app, sp = L.criar_splash(RAIZ)
        self.assertIsNotNone(sp)
        sp.progresso("abrindo")
        sp.repaint()
        img = sp.grab().toImage()
        self.assertFalse(img.isNull())
        # tempo de pintura: bem abaixo de um quadro de 16 ms
        t = time.time()
        for _ in range(20):
            sp.repaint()
        self.assertLess((time.time() - t) / 20.0, 0.016)
        api = L._ApiSplash(sp)
        api.progresso("texto vindo do ROA")
        self.assertEqual(sp._texto, "texto vindo do ROA")
        # aparece a "tela inicial" -> a splash começa a sair
        sp.vigiar_janela_principal()
        janela = QtWidgets.QWidget()
        janela.resize(600, 400)
        janela.show()
        fim = time.time() + 2.0
        while time.time() < fim and not sp._fechada:
            app.processEvents()
            time.sleep(0.01)
        self.assertTrue(sp._fechada, "a splash não fechou ao ver a janela")
        janela.close()


if __name__ == "__main__":
    unittest.main()
