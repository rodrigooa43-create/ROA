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
| P2 Painéis em gavetas | **feito** | `testes/test_p2_gavetas.py`; imagens em `revisao/p2_gavetas/` |
| P4 Perfis de uso | **feito** (página "Escolha os gráficos" liga ao catálogo do P2 quando ele entrar) | `testes/test_p4_perfis.py`; imagens em `revisao/p4_perfis/` |
| P3 Atlas muscular | **feito** | `testes/test_p3_atlas.py`; propostas e comparação em `revisao/p3_atlas/` |
| P6 Replay do movimento (EMG) | **feito** | figura + linha do tempo; `test_p6_figura`, `test_p6_linha_tempo` |
| P7 Replay coração e olhos | **feito** | mesmas detecções do PDF; `test_p7_replay` |
| P8 Replay integrado em "Rever uma gravação" | **feito** | botão ▶ Replay nos dois níveis; `test_p8_replay`; imagens em `revisao/p8_replay/` |
| P5 Documentação | em curso | CHANGELOG, `docs/manual_1.10/`, ajuda interna |
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

- **Fotos do guia de imagens a refazer no Windows** (as capturas offscreen de
  `revisao/` servem de referência):
  1. Tela de abertura (splash) — `revisao/p9_abertura/`.
  2. Tela inicial Simples e Completo com a linha/painel "Perfil" — `revisao/p4_perfis/`.
  3. Assistente de primeiro uso, página "Com o que você trabalha?" e, no Completo,
     "Escolha os gráficos" — `revisao/p4_perfis/`.
  4. Sistema → Tema e Cores → grupo "Perfil de uso".
  5. Aba Músculos no Completo (gavetas + atlas novo), Coração e Olhos — `revisao/p2_gavetas/`.
  6. Atlas: vistas Frente/Costas/Lado e uma área (ex.: Rosto) — `revisao/p3_atlas/`.
  7. Menu "Painéis ▾" aberto e o menu "⋯" de uma gaveta — `revisao/p2_gavetas/`.
  8. "Rever uma gravação" (Simples) com o botão ▶ Replay — `revisao/p8_replay/`.
  9. Replay dos músculos, do coração e dos olhos, nos dois níveis — `revisao/p8_replay/`.
  10. Mapa "Atividade muscular (canais × tempo)" com 8 canais (P1).
- PDFs finais dos manuais (textos-fonte atualizados em `docs/manual_1.10/`).
- `.exe`, empacotamento e `publicar_update.py`.
- Conferir no Windows a fonte Inter/JetBrains Mono nos textos curtos das gavetas
  e da linha do tempo (aqui as capturas usaram DejaVu/Noto, ~8 % mais largas).

## Decisões que o autor precisa tomar

1. **Manifesto padrão sem update_config.json** (P9): instalações sem o arquivo
   passam a consultar `VERSION_URL_PADRAO` (raw do repositório ROA) quando a
   pessoa clica em "Verificar atualizações". Antes mostravam "não configurada".
   Continua manual e opcional; reverter é apagar 3 linhas em `_check_updates_manual`.
2. **Cache do lançador na pasta do programa** (`.roa_cache/`): fica ao lado do
   `.exe` quando a pasta é gravável, senão em `%LOCALAPPDATA%\ROA\cache`.
   Se preferir sempre em LOCALAPPDATA, inverter a ordem em `pasta_cache()`.
3. **Replay do coração** segue os números do relatório PDF (`ecg_pan_tompkins` +
   `correct_ectopic_rr` 30 %), não os do painel ao vivo (que filtra RR 300–2000 ms
   e usa outro detector). Com pausa > 2 s os contadores divergem da tela de
   propósito. Idem para sacadas (`eog_sacadas`, do PDF; a tela usa dH > 0,6·limiar).
4. **Movimentos: PROTOCOLO_FIM** abre um trecho "a definir" de até 3 s (como o
   pedido manda); pode ser ignorado se preferir. Trechos < 0,2 s são descartados.
5. **Gavetas**: painéis-núcleo (canais EMG, traçado ECG/EOG, modo do exame,
   parâmetros de conexão) não fecham; estado é por aba e global (não por
   paciente); cada arranjo grava o config.json após 0,5 s parado. Topografia e
   ERS/ERD ficaram fora (QGroupBox dentro de splitters).
6. **Atlas**: "Outro / Custom" e "(não definido)" ficam como ponto livre;
   `ATLAS_GROUP_LABELS` deixou de ser desenhado (continua no arquivo); músculo
   ativo sem eletrodo na vista acende nos dois lados (D e E).
7. **Figura do movimento**: no neutro a mão fica em 3/4 (licença visual para a
   supinação/pronação ser inconfundível); faixas > 2,5 s viram platô (sobe,
   sustenta, desce) em vez de repetição em câmera lenta.

## Resultados dos testes

Etapa P9+P1+P4 (`python testes/roda_todos.py`): test_p1_canais_em_uso 12/12,
test_p4_perfis 16/16, test_p9_lancador 7/7, test_vazamento_idioma 4/4.

Etapa P2+P3+P6+P7+P8 (`python testes/roda_todos.py`, 56 s): test_p1 12/12,
test_p2_gavetas 22/22, test_p3_atlas 27/27, test_p4_perfis 16/16,
test_p6_figura 11/11, test_p6_linha_tempo 37/37, test_p7_replay 18/18,
test_p8_replay 6/6, test_p9_lancador 7/7, test_vazamento_idioma 4/4
(0 chaves de tr() sem tradução nos 8 idiomas).
