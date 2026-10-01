# -*- coding: utf-8 -*-
"""Coleta as chaves de tr() do ROA.py que ainda não têm tradução em cada idioma.

Pipeline de tradução (regra 7 do projeto):
    1. python ferramentas/coleta_faltantes.py --lote <nome>
         -> escreve ferramentas/trad/<nome>/<lang>.py com um dicionário TRAD
            {"chave em pt": ""} para cada idioma com chaves faltando;
    2. preenche os valores (à mão ou por script);
    3. python ferramentas/aplica_trad.py <nome>
         -> insere as traduções nos dicionários _en/_es/... da classe I18N;
    4. python testes/roda_todos.py test_vazamento_idioma
         -> confirma que nenhuma chave ficou de fora.

Como acha as chaves: percorre a árvore sintática (ast) do ROA.py e guarda o
texto de toda chamada tr("literal") ou I18N.tr("literal"). Chaves montadas em
tempo de execução (tr(variavel)) não aparecem aqui; para elas existe o arquivo
ferramentas/chaves_extras.txt (uma chave por linha), lido junto.

Também é importado pelos testes (funções chaves_tr, mapas_i18n, faltantes).
"""
import ast
import re
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROA_PY = os.path.join(RAIZ, "ROA.py")
EXTRAS = os.path.join(RAIZ, "ferramentas", "chaves_extras.txt")
IDIOMAS = ("en", "es", "it", "fr", "zh", "de", "ja", "ru")


def _ler_fonte(caminho=ROA_PY):
    """Lê o ROA.py (ou outro arquivo) em utf-8 preservando as quebras de linha."""
    with open(caminho, "r", encoding="utf-8", newline="") as f:
        return f.read()


def _arvore(fonte):
    """ast.parse do arquivo inteiro (1-2 s num ROA.py de 80 mil linhas)."""
    return ast.parse(fonte)


def chaves_tr(fonte=None, arvore=None):
    """Conjunto das chaves literais passadas a tr()/I18N.tr() no código.

    Devolve dict {chave: [linhas]} para o relatório apontar onde cada uma é
    usada. Só strings literais; f-strings e variáveis ficam de fora.
    """
    if arvore is None:
        arvore = _arvore(fonte if fonte is not None else _ler_fonte())
    achadas = {}
    for no in ast.walk(arvore):
        if not isinstance(no, ast.Call) or not no.args:
            continue
        f = no.func
        # tr("..."), I18N.tr("...") e atalhos locais como _p7_tr("...") (blocos
        # que embrulham tr() para ter fallback fora do ROA.py)
        eh_tr = (isinstance(f, ast.Name) and (f.id == "tr" or re.fullmatch(r"_\w*tr", f.id))) or (
            isinstance(f, ast.Attribute) and f.attr == "tr"
            and isinstance(f.value, ast.Name) and f.value.id == "I18N")
        if not eh_tr:
            continue
        arg = no.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            achadas.setdefault(arg.value, []).append(no.lineno)
    return achadas


def chaves_extras(caminho=EXTRAS):
    """Chaves listadas à mão (uma por linha) que tr() recebe por variável."""
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return [l.rstrip("\r\n") for l in f if l.strip() and not l.startswith("#")]


def mapas_i18n(fonte=None, arvore=None):
    """Dicionários de tradução da classe I18N, lidos do código: {lang: {pt: trad}}.

    Lê os literais `_en = {...}` etc. direto da árvore, sem importar o ROA.py
    (importar exigiria Qt). Chaves duplicadas no mesmo dicionário são
    devolvidas em `duplicadas` para o teste reclamar.
    """
    if arvore is None:
        arvore = _arvore(fonte if fonte is not None else _ler_fonte())
    classe = next(n for n in arvore.body
                  if isinstance(n, ast.ClassDef) and n.name == "I18N")
    mapas, duplicadas = {}, {}
    for no in classe.body:
        if not isinstance(no, ast.Assign) or len(no.targets) != 1:
            continue
        alvo = no.targets[0]
        if not isinstance(alvo, ast.Name) or not alvo.id.startswith("_"):
            continue
        lang = alvo.id[1:]
        if lang not in IDIOMAS or not isinstance(no.value, ast.Dict):
            continue
        d = {}
        for k, v in zip(no.value.keys, no.value.values):
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                if k.value in d:
                    duplicadas.setdefault(lang, []).append(k.value)
                d[k.value] = v.value if isinstance(v, ast.Constant) else None
        mapas[lang] = d
    mapas["_duplicadas"] = duplicadas
    return mapas


def precisa_traducao(chave):
    """False para chaves sem letra nenhuma ("{0} µV", "—", "CH{0}"): iguais em
    todo idioma, não vale a pena traduzir nem reclamar delas."""
    return any(c.isalpha() for c in chave)


def faltantes(fonte=None):
    """{lang: [chaves sem tradução]} para as chaves literais de tr() + extras."""
    fonte = fonte if fonte is not None else _ler_fonte()
    arvore = _arvore(fonte)
    # I18N.tr() aceita chave com espaço/quebra de linha nas pontas e traduz o
    # miolo; por isso os lotes guardam a chave já sem as pontas.
    usadas = {k.strip() for k in chaves_tr(arvore=arvore)} | {k.strip() for k in chaves_extras()}
    mapas = mapas_i18n(arvore=arvore)
    saida = {}
    for lang in IDIOMAS:
        m = mapas.get(lang, {})
        saida[lang] = sorted(k for k in usadas if k and precisa_traducao(k) and k not in m)
    return saida


def _literal_py(s):
    """String em forma de literal Python de aspas duplas (json.dumps serve:
    os escapes \\n, \\" e \\\\ são os mesmos)."""
    return json.dumps(s, ensure_ascii=False)


def escrever_lote(nome, falt, pasta_base=None):
    """Grava ferramentas/trad/<nome>/<lang>.py com TRAD = {chave: ""}.

    Se o arquivo já existe, mantém as traduções já preenchidas e só acrescenta
    as chaves novas (dá para rodar várias vezes durante o desenvolvimento).
    """
    pasta = os.path.join(pasta_base or os.path.join(RAIZ, "ferramentas", "trad"), nome)
    os.makedirs(pasta, exist_ok=True)
    escritos = []
    for lang in IDIOMAS:
        chaves = falt.get(lang) or []
        if not chaves:
            continue
        caminho = os.path.join(pasta, lang + ".py")
        existentes = ler_lote_idioma(caminho) if os.path.exists(caminho) else {}
        linhas = ["# -*- coding: utf-8 -*-",
                  '"""Lote "%s": traduções pt -> %s. Preencha os valores vazios."""' % (nome, lang),
                  "TRAD = {"]
        for k in chaves:
            linhas.append("    %s: %s," % (_literal_py(k), _literal_py(existentes.get(k, ""))))
        linhas.append("}")
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(linhas) + "\n")
        escritos.append(caminho)
    return escritos


def ler_lote_idioma(caminho):
    """Lê o dicionário TRAD de um arquivo de lote sem executar nada além dele."""
    with open(caminho, "r", encoding="utf-8") as f:
        arvore = ast.parse(f.read())
    for no in arvore.body:
        if isinstance(no, ast.Assign) and isinstance(no.targets[0], ast.Name) \
                and no.targets[0].id == "TRAD":
            return ast.literal_eval(no.value)
    return {}


def main(argv):
    """Linha de comando: relatório no terminal e, com --lote, grava os arquivos."""
    lote = None
    if "--lote" in argv:
        lote = argv[argv.index("--lote") + 1]
    falt = faltantes()
    total = 0
    for lang in IDIOMAS:
        n = len(falt[lang])
        total += n
        print("%s: %d chave(s) sem tradução" % (lang, n))
        if "--mostrar" in argv:
            for k in falt[lang][:50]:
                print("    ", repr(k))
    if lote:
        for c in escrever_lote(lote, falt):
            print("escrito", os.path.relpath(c, RAIZ))
    return 0 if total == 0 else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
