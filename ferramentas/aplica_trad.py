# -*- coding: utf-8 -*-
"""Insere no ROA.py as traduções de um lote (ferramentas/trad/<lote>/<lang>.py).

Cada idioma tem na classe I18N um dicionário `_en = {`, `_es = {`, ... As
traduções novas entram logo abaixo dessa linha de abertura, sob um cabeçalho
"# ===== <lote> (1.10.0) =====", na mesma forma dos lotes anteriores.

Segue a regra de edição do projeto: troca por texto exato (a linha de abertura
de cada dicionário é única), ast.parse antes de gravar, utf-8 e newline="".
Chaves que já existem no dicionário do idioma são puladas (rodar duas vezes não
duplica), e valores vazios são ignorados com aviso.

Uso: python ferramentas/aplica_trad.py <lote> [--versao 1.10.0]
"""
import ast
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "ferramentas"))
import coleta_faltantes as cf  # noqa: E402


def aplicar(lote, versao="1.10.0", roa_py=cf.ROA_PY, pasta_trad=None):
    """Aplica o lote no arquivo e devolve {lang: n_inseridas}."""
    pasta = os.path.join(pasta_trad or os.path.join(RAIZ, "ferramentas", "trad"), lote)
    fonte = cf._ler_fonte(roa_py)
    mapas = cf.mapas_i18n(fonte=fonte)
    inseridas = {}
    for lang in cf.IDIOMAS:
        caminho = os.path.join(pasta, lang + ".py")
        if not os.path.exists(caminho):
            continue
        trad = cf.ler_lote_idioma(caminho)
        novas = []
        for k, v in trad.items():
            if not v:
                print("aviso: %s sem tradução para %r" % (lang, k[:60]))
                continue
            if k in mapas.get(lang, {}):
                continue
            novas.append((k, v))
        if not novas:
            inseridas[lang] = 0
            continue
        ancora = "\n    _%s = {\n" % lang
        assert fonte.count(ancora) == 1, "âncora do dicionário %s não é única" % lang
        bloco = ["        # ===== %s (%s) =====" % (lote, versao)]
        for k, v in novas:
            bloco.append("        %s: %s," % (cf._literal_py(k), cf._literal_py(v)))
        fonte = fonte.replace(ancora, ancora + "\n".join(bloco) + "\n", 1)
        inseridas[lang] = len(novas)
    ast.parse(fonte)  # garante que o arquivo continua válido antes de gravar
    with open(roa_py, "w", encoding="utf-8", newline="") as f:
        f.write(fonte)
    return inseridas


def main(argv):
    """Linha de comando."""
    if not argv:
        print(__doc__)
        return 1
    versao = "1.10.0"
    if "--versao" in argv:
        versao = argv[argv.index("--versao") + 1]
    res = aplicar(argv[0], versao)
    for lang, n in res.items():
        print("%s: %d tradução(ões) inserida(s)" % (lang, n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
