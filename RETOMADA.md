# RETOMADA — ROA 1.10.0 (branch `v1.10-nuvem`)

Arquivo de retomada do trabalho na nuvem (Linux). Atualizado a cada etapa, para
a sessão poder cair e ser retomada sem perder o fio. Tudo o que está aqui foi
feito **sem publicar nada**: publicar (APP_VERSION, version.json, .exe) é
decisão do autor, no Windows.

## Como retomar

```bash
git checkout v1.10-nuvem
python -m py_compile ROA.py                 # o arquivo compila?
python testes/roda_todos.py                 # bateria inteira, offscreen
python ferramentas/coleta_faltantes.py      # chaves de tr() sem tradução (deve dar 0)
```

Regras de edição do ROA.py (não quebrar): editar por script Python com troca de
texto exato (`assert fonte.count(antigo) == 1`), `ast.parse` antes de gravar,
`encoding="utf-8"`, `newline=""`; depois `python -m py_compile ROA.py`.

Tradução de textos novos: `python ferramentas/coleta_faltantes.py --lote <nome>`
→ preencher `ferramentas/trad/<nome>/<lang>.py` → `python ferramentas/aplica_trad.py <nome>`
→ `python testes/roda_todos.py test_vazamento_idioma`.

## Estado por pedido

| Pedido | Estado | Observações |
|---|---|---|
| Infra (branch, testes, ferramentas de tradução) | feito | `testes/`, `ferramentas/`, `revisao/`, `.gitignore` |
| P9 Abrir rápido + logo animada | **feito** | lançador com cache + splash; scipy adiado; medidas no CHANGELOG |
| P1 Só os canais em uso | **feito** | helpers + 16 locais; `testes/test_p1_canais_em_uso.py` |
| P2 Painéis em gavetas | a fazer | |
| P4 Perfis de uso | **feito** (página "Escolha os gráficos" liga ao catálogo do P2 quando ele entrar) | `testes/test_p4_perfis.py`; imagens em `revisao/p4_perfis/` |
| P3 Atlas muscular | a fazer | |
| P6 Replay do movimento (EMG) | a fazer | |
| P7 Replay coração e olhos | a fazer | |
| P8 Replay integrado em "Rever uma gravação" | a fazer | |
| P5 Documentação | ao longo + passada final | |
| Pendências antigas (URLs OpenBionica → ROA) | **feito** | CODE_URL, catálogo E308/E402-404 (9 idiomas), CITATION.cff; version.json não tocado |

## Medições (P9) — base, antes das mudanças

Máquina da nuvem (Linux, Python 3.11, disco rápido). No Windows do autor a
compilação do ROA.py custa 6,7 s e o import ~9 s; aqui os números são menores,
mas as proporções valem:

| Etapa | Tempo |
|---|---|
| compilar ROA.py (fonte → bytecode) | 0,79 s |
| carregar o .pyc pronto (marshal) | 0,02 s |
| `import scipy.signal` | 1,18 s |
| `import scipy.stats` (puxado pelo scipy.signal) | 0,98 s |
| `import pyqtgraph` | 0,37 s |
| `import scipy.fft` | 0,34 s |
| `import matplotlib` | 0,32 s |
| `import numpy` | 0,13 s |
| `import PySide6.QtWidgets` | 0,15 s |
| `import ROA` completo, sem .pyc | 2,64 s |
| `import ROA` completo, com .pyc | 1,35 s |

## O que fica para o Windows

- **P9**: medir o arranque no PC do autor (`python ferramentas/mede_arranque.py 5` e
  `--sem-cache`), conferir a splash em monitor real (DPI alto, dois monitores) e
  rebuildar o `.exe` com o novo `EEG_Data_Collector.py` (o exe antigo continua
  funcionando com o ROA.py novo, só sem cache nem splash). `publicar_update.py`
  pode passar a escrever `launcher_url` e `launcher_sha256` no `version.json`.
- **URLs**: `update_config.json` distribuído com o programa ainda aponta para
  `.../OpenBionica/main/version.json` (redireciona; trocar na próxima publicação).

- Fotos do guia de imagens (lista será preenchida por pedido).
- PDFs finais dos manuais (textos-fonte atualizados aqui).
- `.exe`, empacotamento e `publicar_update.py`.

## Decisões que o autor precisa tomar

1. **Manifesto padrão sem update_config.json** (P9): instalações sem o arquivo
   passam a consultar `VERSION_URL_PADRAO` (raw do repositório ROA) quando a
   pessoa clica em "Verificar atualizações". Antes mostravam "não configurada".
   Continua manual e opcional; reverter é apagar 3 linhas em `_check_updates_manual`.
2. **Cache do lançador na pasta do programa** (`.roa_cache/`): fica ao lado do
   `.exe` quando a pasta é gravável, senão em `%LOCALAPPDATA%\ROA\cache`.
   Se preferir sempre em LOCALAPPDATA, inverter a ordem em `pasta_cache()`.

## Resultados dos testes

Etapa P9+P1+P4 (`python testes/roda_todos.py`): test_p1_canais_em_uso 12/12,
test_p4_perfis 16/16, test_p9_lancador 7/7, test_vazamento_idioma 4/4.
