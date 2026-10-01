# -*- coding: utf-8 -*-
"""Vazamento de idioma: toda chave literal de tr() precisa existir nos 8 idiomas.

Sem isso, uma tela em japonês mostraria a frase em português (fallback do
I18N.tr). O teste lê o ROA.py pela árvore sintática, sem importar Qt, por isso
é rápido e roda em qualquer máquina.

Também confere que nenhum dicionário tem chave repetida (a segunda ocorrência
venceria em silêncio) e que os placeholders {0}, {1}... da tradução batem com
os da chave em português (um {1} a mais quebra o .format em tempo de execução).
"""
import os
import re
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "ferramentas"))
import coleta_faltantes as cf  # noqa: E402

_PLACEHOLDER = re.compile(r"\{(\d*)(?::[^}]*)?\}")


class TestVazamentoIdioma(unittest.TestCase):
    """Chaves de tr() x dicionários da classe I18N."""

    @classmethod
    def setUpClass(cls):
        cls.fonte = cf._ler_fonte()
        cls.arvore = cf._arvore(cls.fonte)
        cls.usadas = cf.chaves_tr(arvore=cls.arvore)
        cls.mapas = cf.mapas_i18n(arvore=cls.arvore)

    def test_todas_as_chaves_traduzidas(self):
        """Nenhuma chave de tr() fica sem tradução em idioma algum."""
        falt = cf.faltantes(self.fonte)
        problemas = []
        for lang in cf.IDIOMAS:
            for k in falt[lang]:
                linhas = self.usadas.get(k, ["extra"])[:3]
                problemas.append("%s: %r (linhas %s)" % (lang, k[:80], linhas))
        self.assertEqual(problemas, [],
                         "Chaves sem tradução:\n" + "\n".join(problemas[:80]))

    def test_sem_chaves_duplicadas(self):
        """Chave repetida no mesmo dicionário é erro: a segunda vence em silêncio."""
        dup = self.mapas.get("_duplicadas", {})
        self.assertEqual(dup, {}, "Chaves duplicadas: %r" % dup)

    def test_placeholders_batem(self):
        """Os {n} da tradução são os mesmos da chave em português."""
        erros = []
        for lang in cf.IDIOMAS:
            for k, v in self.mapas.get(lang, {}).items():
                if not isinstance(v, str):
                    continue
                a = sorted(_PLACEHOLDER.findall(k))
                b = sorted(_PLACEHOLDER.findall(v))
                if a != b:
                    erros.append("%s: %r -> %r" % (lang, k[:60], v[:60]))
        self.assertEqual(erros, [], "Placeholders diferentes:\n" + "\n".join(erros[:40]))

    def test_oito_idiomas_presentes(self):
        """A classe I18N continua com os 8 dicionários além do pt."""
        for lang in cf.IDIOMAS:
            self.assertIn(lang, self.mapas)
            self.assertGreater(len(self.mapas[lang]), 1000)


if __name__ == "__main__":
    unittest.main()
