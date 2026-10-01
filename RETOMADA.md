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
| P9 Abrir rápido + logo animada | a fazer | medição-base feita (abaixo) |
| P1 Só os canais em uso | a fazer | |
| P2 Painéis em gavetas | a fazer | |
| P4 Perfis de uso | a fazer | depende do catálogo do P2 |
| P3 Atlas muscular | a fazer | |
| P6 Replay do movimento (EMG) | a fazer | |
| P7 Replay coração e olhos | a fazer | |
| P8 Replay integrado em "Rever uma gravação" | a fazer | |
| P5 Documentação | ao longo + passada final | |
| Pendências antigas (URLs OpenBionica → ROA) | a fazer | |

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

- Fotos do guia de imagens (lista será preenchida por pedido).
- PDFs finais dos manuais (textos-fonte atualizados aqui).
- `.exe`, empacotamento e `publicar_update.py`.

## Decisões que o autor precisa tomar

(preenchido ao longo das etapas)

## Resultados dos testes

(preenchido a cada etapa)
