# -*- coding: utf-8 -*-
"""P5 (1.10.0): a ajuda interna conhece o que entrou nesta versão.

Confere que o assistente offline responde sobre Replay, perfis de uso,
gavetas, atlas, abertura rápida e canais em uso; que as entradas só do
Completo (gavetas, edição de movimentos) ficam fora do nível Simples; que
o glossário tem os verbetes novos; e que a base de conhecimento embutida
ganhou as seções correspondentes. Roda offscreen, sem dado de pessoa."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _roa import ROA  # noqa: E402


def _titulos(resps):
    return [t for t, _a, _r, _k in resps]


class TestFaqEGuias(unittest.TestCase):
    """Perguntas em palavras comuns chegam às entradas novas."""

    def _busca(self, pergunta, nivel="completo", limit=5):
        return ROA.help_answer(pergunta, limit=limit, nivel=nivel)

    def test_replay_na_faq_e_no_guia(self):
        titulos = " | ".join(_titulos(self._busca("como vejo o replay da gravação")))
        self.assertIn("Replay", titulos)

    def test_perfil_de_uso(self):
        titulos = " | ".join(_titulos(self._busca("uma aba sumiu, perfil de uso")))
        self.assertTrue("Perfil de uso" in titulos or "perfil de uso" in titulos, titulos)

    def test_atlas_eletrodo(self):
        titulos = " | ".join(_titulos(self._busca("onde coloco o eletrodo no desenho do corpo")))
        self.assertIn("eletrodo", titulos.lower())

    def test_abertura_lenta(self):
        titulos = " | ".join(_titulos(self._busca("o programa demora para abrir")))
        self.assertIn("demora para abrir", titulos)

    def test_canais_em_uso(self):
        titulos = " | ".join(_titulos(self._busca("um canal sumiu da lista")))
        self.assertIn("canais em uso", titulos.lower())

    def test_gavetas_so_no_completo(self):
        """A entrada das gavetas existe no Completo e não aparece no Simples,
        onde as gavetas não existem."""
        completo = " | ".join(_titulos(self._busca("um painel sumiu, gaveta, botão painéis")))
        self.assertIn("gavetas", completo)
        simples = " | ".join(_titulos(self._busca("um painel sumiu, gaveta, botão painéis",
                                                  nivel="simples")))
        self.assertNotIn("gavetas", simples)

    def test_editar_movimentos_so_no_completo(self):
        simples = _titulos(self._busca("trocar o movimento, dividir, tarefa pronta",
                                       nivel="simples"))
        self.assertFalse(any("Marcar ou corrigir os movimentos" in t for t in simples), simples)
        completo = _titulos(self._busca("trocar o movimento, dividir, tarefa pronta"))
        self.assertTrue(any("Marcar ou corrigir os movimentos" in t for t in completo), completo)

    def test_replay_no_simples(self):
        """O Replay existe nos dois níveis: o guia de ver o Replay fica no Simples."""
        titulos = _titulos(self._busca("ver o replay da gravação do coração", nivel="simples"))
        self.assertTrue(any("Replay" in t for t in titulos), titulos)

    def test_guia_tem_passos_e_erros(self):
        g = [g for g in ROA.HELP_GUIAS if g["t"].startswith("Ver o Replay")][0]
        self.assertGreaterEqual(len(g["passos"]), 4)
        self.assertTrue(g["erros"])
        html = ROA._guia_html(g)
        self.assertIn("<ol>", html)
        self.assertIn("simula", html)

    def test_faq_canais_tem_resposta_do_simples(self):
        e = [e for e in ROA.HELP_FAQ if e["t"] == "Só os canais em uso aparecem nas listas"][0]
        self.assertIn("a_simples", e)
        self.assertNotIn("Filtros e Canais", e["a_simples"])


class TestGlossarioEBase(unittest.TestCase):
    def test_verbetes_novos(self):
        self.assertIn("replay", ROA.HELP_GLOSSARIO)
        self.assertIn("seniam", ROA.HELP_GLOSSARIO)
        nome, oque, onde = ROA.HELP_GLOSSARIO["seniam"]
        self.assertIn("SENIAM".lower()[:3], nome.lower() + oque.lower())

    def test_o_que_e_seniam(self):
        titulos = " | ".join(_titulos(ROA.help_answer("o que é SENIAM?", limit=3)))
        self.assertIn("SENIAM", titulos)

    def test_base_de_conhecimento(self):
        secoes = [t for t, _b in ROA._help_read_kb()]
        for esperado in ("Replay de uma gravação", "Perfis de uso", "Painéis em gavetas",
                         "Atlas muscular", "Abertura rápida", "Canais em uso"):
            self.assertTrue(any(esperado in t for t in secoes), esperado)

    def test_textos_sem_tom_de_laudo(self):
        """Regra 8: nada que pareça diagnóstico; o Replay diz que simula."""
        for e in ROA.HELP_FAQ:
            if "Replay" in e["t"]:
                self.assertIn("simula", e["a"])
                self.assertIn("laudo", e["a"])


class TestTraducao(unittest.TestCase):
    """Os textos novos passam pelo tr() e existem nos 8 idiomas."""

    def test_titulos_traduzidos(self):
        novos = ["Replay: ver a gravação como uma animação",
                 "Perfil de uso: Cérebro, Músculos, Coração, Olhos ou Tudo",
                 "O programa demora para abrir",
                 "Ver o Replay de uma gravação de músculos, coração ou olhos",
                 "Colocar os eletrodos no desenho do corpo"]
        for lang in ("en", "es", "it", "fr", "zh", "de", "ja", "ru"):
            d = getattr(ROA.I18N, "_" + lang)
            for k in novos:
                self.assertIn(k, d, (lang, k))
                self.assertTrue(d[k].strip() and d[k] != k, (lang, k))

    def test_corpus_por_idioma(self):
        """O corpus se refaz ao trocar o idioma e traz o título traduzido."""
        atual = ROA.I18N.current
        try:
            ROA.I18N.current = "en"
            titulos = " | ".join(_titulos(ROA.help_answer("program takes long to open", limit=5)))
            self.assertIn("takes long to open", titulos)
        finally:
            ROA.I18N.current = atual
            ROA._help_corpus()


if __name__ == "__main__":
    unittest.main(verbosity=1)
