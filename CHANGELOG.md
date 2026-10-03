# Changelog

Todas as mudanças notáveis deste projeto. Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e versionamento [SemVer](https://semver.org/lang/pt-BR/).

> **Controle de melhorias:** ao publicar, renomeie *Não lançado* para a versão+data,
> aumente `APP_VERSION` no código, rode `publicar_update.py` e faça push de
> `EEG_Data_Collector.py` + `version.json` (fluxo GitHub-pull). Bugs encontrados
> ficam registrados em `KNOWN_ISSUES.md`.

## [Não lançado]

### Adicionado
- **Replay dentro de "Rever uma gravação" (P6, P7, P8).** Botão **▶ Replay**
  na fileira da aba Offline (nos dois níveis), ligado quando a gravação aberta
  é de músculos, coração ou olhos; um tocador único (Tocar/Pausar, Início,
  linha do tempo arrastável, relógio; no Completo velocidade 0,25×–4× e
  Repetir) alimenta a cena do exame:
  - **Músculos**: figura articulada de perfil desenhada em código (tronco,
    ombro, cotovelo, antebraço, punho, mão com dedos e polegar) refaz o
    movimento marcado e cada músculo acende com a intensidade medida
    (envelope de 100 ms normalizado pelo percentil 95 da gravação).
    Movimentos: flexão/extensão do cotovelo, supinação e pronação
    (inconfundíveis: palma clara para cima × dorso para baixo, polegar de
    lado e o texto "palma para cima/baixo"), punho, abrir/fechar a mão,
    pinça, ombro, repouso, "a definir". Tarefas prontas com o objeto preso à
    mão: levantar o halter, abrir/fechar a porta com a chave, pegar o copo e
    levar à boca. Linha do tempo com 2 a 4 faixas (arrastar, esticar,
    dividir, trocar o movimento, apagar, desfazer/refazer; faixas no mesmo
    instante se somam), que nasce dos marcadores/fases da gravação ou, sem
    marcador, das contrações detectadas como "a definir"; aviso quando os
    músculos ativos não combinam com o movimento (e quando há músculo ativo
    num trecho de repouso). Salvo em `movimentos.json` ao lado do `data.csv`.
    No Simples: tocador, figura e lista de trechos (linha do tempo só exibe).
  - **Coração**: coração que bate no ritmo gravado, traçado com cursor, bpm,
    faixa com todas as batidas (adiantada = triângulo laranja, pausa maior =
    retângulo vazado vermelho: cor E forma) e lista em palavras simples. As
    batidas vêm das MESMAS funções do relatório PDF (`ecg_pan_tompkins`,
    `correct_ectopic_rr` com 30 %); no Completo, clique direito na faixa
    remove/adiciona/retipa batidas, salvas em `batidas.json`.
  - **Olhos**: olhos que piscam nas piscadas e olham para onde os sinais
    mandam (`eog_piscadas_tela`/`eog_sacadas`, as mesmas do PDF), "Inverter
    horizontal/vertical", linha do tempo em palavras ("0:03 piscou", "0:05
    olhou para a direita") e contadores; no Completo, clique direito na lista
    remove o evento ou troca a direção, salvo em `olhos.json`.
  Em toda cena um selo diz que a animação SIMULA o que foi gravado e que não
  é laudo nem diagnóstico. Testes: `test_p6_figura`, `test_p6_linha_tempo`,
  `test_p7_replay`, `test_p8_replay`.
- **Painéis em gavetas no Completo (P2).** Cada painel das abas Músculos,
  Coração, Olhos, Análises, Filtros e Canais e Rede e Eventos ganhou um
  cabeçalho fino (▾ recolher/expandir, ⋯ menu com Mover para cima/baixo,
  Tamanho padrão e Fechar, × fechar) e uma alça inferior para arrastar a
  altura; painéis lado a lado (Traçado ECG + Tacograma, FFT + Bandas) dividem
  a largura num divisor persistido. Botão **Painéis** em cada aba
  (mostrar/ocultar cada painel, Recolher todos, Expandir todos, Restaurar o
  padrão). O arranjo é salvo sozinho na chave nova `paineis` do
  `config.json` (debounce de 0,5 s) e restaurado; `CATALOGO_PAINEIS` guarda
  id, título, aba, exames e estado padrão de cada painel e serve ao perfil de
  uso (aba sem arranjo salvo nasce do perfil; painéis fora dos exames do
  perfil ou desmarcados nascem fechados). Painel fechado ou recolhido não
  gasta processamento (`gaveta_ativa()` nos laços de EMG/ECG/EOG/Análises;
  os acumuladores de série continuam). No Simples nada disso aparece. Painéis
  núcleo (canais EMG, traçado ECG/EOG, modo do exame) não fecham.
  Teste: `test_p2_gavetas` (unidade + janela real).
- **Atlas muscular desenhado em código (P3).** O boneco de retângulos deu
  lugar a um corpo em curvas de Bézier (ilustração médica limpa, linhas dos
  grupos musculares, volumes suaves) nas vistas Frente, Costas e **Lado**, e
  em 14 áreas recortadas (rosto, pescoço, peito e abdômen, costas, braço,
  antebraço e mão, mão, perna e pé, com lado direito/esquerdo). Eletrodos
  como pontos numerados que colam no ponto SENIAM do ventre do músculo (19
  músculos antigos, rosto: masseter, temporal, frontal, orbicular do olho,
  zigomático, e extras SENIAM); a ativação aparece NO ponto do eletrodo como
  mancha de calor que cresce e esquenta, recortada pelo corpo; eletrodo posto
  numa área aparece no corpo inteiro. Montagens antigas são convertidas sem
  perder músculo, canal nem nome (marca `atlas: 2`); o `config.json` aceita a
  vista `side`. Pintura ~3 ms em 300×470 (corpo em camada cacheada). Três
  propostas de estilo comparadas em `revisao/p3_atlas/COMPARACAO.md`.
  Teste: `test_p3_atlas` (27 testes).

- **Perfis de uso (P4).** Conceito novo: o perfil diz com o que a pessoa
  trabalha e decide o que a tela inicial oferece e quais abas aparecem.
  Prontos: "Cérebro (EEG)", "Músculos (EMG)", "Coração (ECG)", "Olhos (EOG)"
  e "Tudo"; personalizado: "Minha bancada" (criar, duplicar, renomear e
  excluir em Sistema → Tema e Cores → Perfil de uso, com os exames do perfil
  em caixas de marcar). No assistente de primeiro uso, a página "Com o que
  você trabalha?" tem quatro cartões grandes de marcar (um cartão = perfil
  pronto; dois ou três = "Minha bancada"; quatro = "Tudo"); no caminho
  Completo há a página opcional "Escolha os gráficos" (recomendados já
  marcados; lista vem do catálogo de painéis). Trocar de perfil na tela
  inicial (combo "Perfil:", nos dois níveis) ou em Sistema vale na hora: os
  exames fora do perfil somem da tela inicial, do diálogo "Trocar", do combo
  "Modo do exame" e do menu do selo; as abas que não pertencem a nenhum
  exame do perfil ficam ocultas, inclusive no Multimodal. Abrir uma gravação
  de outro exame continua funcionando. Chaves novas do `config.json`:
  `usage_profile` (padrão "Tudo": instalações existentes não mudam nada) e
  `usage_profiles` (só os personalizados). Teste: `testes/test_p4_perfis.py`.

- **Abertura rápida com tela de abertura (P9).** O lançador
  `EEG_Data_Collector.py` deixou de recompilar o `ROA.py` inteiro a cada
  abertura (6,7 s medidos no Windows): compila uma vez para um `.pyc` em
  cache (`.roa_cache/` ao lado do programa ou, sem permissão de escrita,
  `%LOCALAPPDATA%\ROA\cache`), invalidado sozinho quando o `ROA.py` ou a
  versão do Python mudam, e roda o `.pyc`. Na primeira abertura a compilação
  roda num processo à parte, para a animação não congelar. Enquanto carrega,
  uma tela leve mostra a logo do ROA entrando com fade e uma linha de sinal se
  desenhando, com o progresso em palavras nos 9 idiomas e fundo claro ou
  escuro conforme o tema salvo; ela some com um fade assim que a primeira
  janela aparece, sem atraso de propósito, e funciona até com um `ROA.py`
  antigo. `--sem-splash` (ou `ROA_SEM_SPLASH=1`) desliga a tela.
- **Atualizador também atualiza o lançador** quando o `version.json` trouxer
  as chaves novas `launcher_url` e `launcher_sha256` (opcionais: manifestos
  antigos seguem funcionando). Só grava se o `.py` do lançador existir ao lado
  do programa, depois de o `ROA.py` já estar gravado, com SHA-256 conferido e
  o arquivo compilando; se falhar, avisa e o programa segue com o lançador
  atual. Sem `update_config.json`, a verificação usa o manifesto do repositório
  oficial (`VERSION_URL_PADRAO`); o arquivo, quando existe, continua mandando.
- `ferramentas/mede_arranque.py` mede o tempo até a primeira tela; bateria de
  testes offscreen em `testes/` (`python testes/roda_todos.py`) e pipeline de
  tradução em `ferramentas/` (`coleta_faltantes.py` → `trad/<lote>/` →
  `aplica_trad.py`), com `testes/test_vazamento_idioma.py` garantindo que toda
  chave de `tr()` existe nos 8 idiomas.

- **Documentação (P5).** Textos-fonte das seções novas do Manual do Usuário
  em `docs/manual_1.10/pt/` (abertura rápida, perfis de uso, canais em uso,
  painéis em gavetas, atlas muscular, Replay) traduzidos para os 8 idiomas
  (`docs/manual_1.10/<idioma>/`, rótulos de interface iguais aos do programa)
  e seções do Manual Técnico em `docs/manual_1.10/tecnico/`. A ajuda interna
  (Ajuda → Assistente) ganhou 6 perguntas, 4 guias passo a passo (Replay,
  marcar movimentos, perfil de uso, eletrodos no desenho do corpo), 2 verbetes
  (Replay, SENIAM) e 6 seções na base de conhecimento, tudo nos 9 idiomas; as
  entradas que citam gavetas ou a edição da linha do tempo ficam fora do nível
  Simples. Toda classe e função nova do 1.10.0 tem docstring em português
  (`testes/test_p5_ajuda.py`).
### Corrigido
- **Só os canais em uso (P1).** Com 8 canais de EMG o mapa "Atividade
  muscular (canais × tempo)" listava CH1 a CH64, porque `_emg_update_advanced`
  percorria `range(MAX_CHANNELS)` e os canais 9 a 64 também estão marcados
  como EMG no config. Agora há um helper único (`canais_por_tipo` no módulo;
  `_canais_em_uso`, `_tipo_do_canal`, `_canais_em_uso_tipo` e
  `_refresh_listas_canais` na janela) usado em todos os pontos que montavam
  listas por tipo: combos do canal EMG (MDF/MNF, APDF, espectrograma), combos
  "Canal" do Atlas, ERP, slots do Layout Custom, linhas da tabela de
  Calibração, legenda do envelope EMG, laços `_update_emg_view`,
  `_emg_update_advanced`, `_emg_update_ergonomics`, `_emg_atlas_update_live` e
  o diálogo de co-contração. As listas repopulam (preservando a seleção)
  quando muda o número ou o tipo dos canais e ao aplicar a escolha da tela
  inicial; o ERP segue os canais da gravação carregada. Teste:
  `testes/test_p1_canais_em_uso.py` (5 exames × 8/16/32/64 canais × 2 níveis).
- **Nomes dos perfis prontos e título da aba Bio traduzidos.** "Cérebro (EEG)",
  "Músculos (EMG)", "Coração (ECG)", "Olhos (EOG)", "Tudo" e "Minha bancada"
  passavam por `tr()` através de uma variável, por isso a coleta de chaves não
  os via e eles saíam em português nos outros idiomas (tela inicial,
  assistente, Sistema). O título da aba "Músculos"/"Coração"/"Olhos" em modo
  único também não era traduzido. Agora estão nos 8 dicionários
  (`ferramentas/trad/p5_rotulos/`) e `chaves_extras.txt` registra as chaves
  dinâmicas para a coleta.

### Alterado
- **`bleak` e `ob_core` fora do caminho crítico da abertura (P9).** O import
  do `bleak` (Bluetooth) saiu do topo do arquivo (custava 0,3 a 1 s no
  Windows) e passou a acontecer só ao procurar aparelhos; o diagnóstico da
  ponte C++ `ob_core` roda 2 s depois de a janela aparecer, não antes da tela
  inicial.
- **Importações pesadas adiadas (P9).** `scipy.signal` e `scipy.fft` passam a
  ser importados na primeira vez que são usados (`_ModuloAdiado`), não na
  abertura: `import scipy.signal` sozinho custava 1,2 s (puxa scipy.stats,
  interpolate e optimize) e nada disso é preciso para a tela inicial. As
  funções chamadas são as mesmas; só o momento do import muda.
- **Medição do arranque** (Linux da nuvem, Python 3.11; no Windows do autor a
  compilação custava 6,7 s, então o ganho lá é bem maior). Tempo até a tela
  inicial desenhada, mediana de 3 aberturas:

  | Como abre | Antes (1.9.0) | Depois |
  |---|---|---|
  | lançador, aberturas seguintes (cache pronto) | 2,03 s | **0,90 s** |
  | lançador, primeira abertura (compila e grava o cache) | 2,03 s | 1,59 s |
  | `python ROA.py` direto (compila sempre) | 2,02 s | 1,13 s |
  | só `import ROA`, sem `.pyc` | 2,64 s | 1,35 s → 0,02 s de carga do `.pyc` |

- URL do repositório atualizada para `github.com/rodrigooa43-create/ROA` em
  `CODE_URL`, no catálogo de erros (E308, E402, E403, E404) nos 9 idiomas e em
  `CITATION.cff`; a URL antiga (`.../OpenBionica`) redireciona. `version.json`
  não foi tocado (é publicação).


## [1.9.0] — 2026-09-25

Responde à **crítica de usabilidade** de 17/09/2026: o programa era bom, mas
quem só aplica o exame se perdia entre dezenas de abas e ajustes de pesquisa.
A 1.9.0 abre no **modo simples** para todos. A tela inicial tem uma coluna
(exame, paciente, "Novo exame" e "Abrir uma gravação"), a porta do aparelho
é achada sozinha, o filtro do exame liga ao conectar, a barra de ação diz em
qual dos três passos você está (conectar, gravar, gerar o relatório) com um só
botão em destaque, o da próxima ação, e o relatório PDF fica a um clique ao
parar a gravação. Nada foi removido: o modo completo devolve a interface da
1.8.4 na hora, sem reiniciar. Na mesma versão o relatório PDF passou a
descrever o exame gravado (EMG, ECG e EoG têm figuras e números próprios), a
simulação passou a gerar cada tipo de sinal a 250 Hz sem perda, a Topografia
foi redesenhada (spline esférica, barra com unidade nas três vistas, ERD% com
sinal), a fonte deixou de depender de quem abre a janela e os 79 achados das
capturas do guia de imagens (`docs/ACHADOS_CAPTURAS_GUIA_IMAGENS.md`) foram
triados; os que procediam estão corrigidos abaixo. Guia de imagens, Manual do
Usuário e Manual Técnico foram refeitos com as telas novas.

### Adicionado
- **Tamanho da letra (100/125/150%)** em Sistema → Tema e Cores, para os dois
  níveis: `config.ui_font_scale` (chave nova, padrão 1.0) multiplica todo
  `font-size` das folhas de estilo (`build_stylesheet`, tela inicial e
  assistente), as pílulas e selos do cabeçalho e as fontes dos gráficos
  (`_apply_plot_fonts`); sobrevive à troca de tema porque a escala é lida
  dentro de `build_stylesheet`. Acima de 125% a barra de ação (Início,
  Desconectar, Iniciar Gravação, Marcar evento, Exibição) para em 125% para
  caber em 1366 px, e o eixo dos nomes de canal do Empilhado cresce junto.
  Pedido da validação de uso com leigos (G19).
- **Modo simples (exame)**: a interface passa a ter dois níveis, e o padrão é o
  simples para todos, inclusive para quem já usava o programa (um `config.json`
  antigo, sem a chave `ui_level`, abre no simples). Nasceu de uma crítica de
  usabilidade: quem só aplica o exame se perdia entre dezenas de sub-abas e
  ajustes de pesquisa. Nada foi removido; o que some no simples fica só
  escondido e volta no modo completo.
  - **Interruptor**: combo "Exibição" na barra de ação (Simples (exame) /
    Completo (pesquisa)), item "Mudar para Completo (pesquisa)" / "Voltar
    para Simples (exame)" no menu Ajuda e na paleta de comandos
    (Ctrl+Shift+P), botão "Mudar para Completo (pesquisa)" no rodapé da tela
    inicial e a página "Como você vai usar o ROA?" do assistente de primeiro
    uso ("Simples (exame)" vem marcado). Os dois níveis têm um nome só em
    todo lugar desde a validação com leigos (ver Corrigido). A troca vale na
    hora, sem reiniciar, e fica gravada em `config.ui_level`.
  - **O que some no simples**: as sub-abas de análise e de ajuste fino (ficam
    Voluntários, Conexão, Tempo Real, Offline e Configurações, mais a aba do
    sinal escolhido em EMG, ECG e EoG), os menus Ferramentas e Diagnóstico, a
    telemetria do cabeçalho (amostras, acelerômetro, qualidade, tempos), o
    Protocolo na barra de ação e, no Offline, os botões de exportação e de
    análise de pesquisa (EDF, importador, estatística, Área Maker, Bancada,
    ICA). Os combos Simples/Avançado das abas EMG, ECG e EoG acompanham o
    nível global.
  - **Tela inicial simples**: coluna única com "Exame:" (o tipo salvo, com
    "Trocar" para tipo e número de canais), "Paciente:" com "+ Novo", e dois
    cartões, "Novo exame" e "Abrir uma gravação", além de "Treino (sem
    aparelho)". A porta do aparelho é achada sozinha: com uma só
    porta a janela já abre conectando; com várias pergunta "Qual porta é o
    aparelho?"; sem nenhuma oferece tentar de novo ou simular.
  - **Atalhos de fluxo** (valem nos dois níveis): a dica da barra de ação
    passou a acompanhar o estado ("Conectando…", erro de conexão em vermelho
    com "Procurar de novo", aviso quando a conexão abre e nenhum dado chega em
    5 s, sessão gravada, gravação carregada); ao parar de gravar, o diálogo
    "Sessão gravada" oferece "→ Relatório PDF" e "Abrir pasta"; o Offline
    ganhou os botões "→ Relatório PDF" e "Salvar figura (PNG)", que gravam na
    pasta da sessão carregada; o emblema da modalidade no cabeçalho é clicável
    e troca o tipo de exame; o menu Ajuda abre o "Manual do usuário (PDF)"
    no idioma da interface (em português quando não há o do idioma).
  - **Filtro do exame ligado ao conectar**: no simples, se o notch e o
    passa-faixa estão ambos desligados, o programa liga o filtro do tipo de
    sinal (rede elétrica + passa-faixa) para o traçado aparecer limpo. A
    gravação sai filtrada e isso fica registrado: aviso na barra de ação, linha
    no log e `"filters_auto": true` no `summary.json`, ao lado de `filters`.
    Quem já tinha um filtro ligado não é afetado, e o modo completo não muda.
    A constante `SIMPLES_LIGA_FILTRO` desliga o comportamento com uma linha.
  - O relatório PDF da sessão traz no título o exame da gravação, lido do
    `summary.json` (em gravação antiga, o exame em uso; antes, "EEG" fixo),
    e o paciente/voluntário gravado no `summary.json`. Desde a validação com
    leigos (etapa c, em Corrigido) o relatório inteiro fala a língua da tela.
- **Estudo por Paciente: figuras para publicação** (`figuras_artigo/` na pasta
  de cada paciente). Nasceram de três perguntas reais de quem leu as figuras
  de um estudo de reabilitação: "antes e depois de quê?", "de qual sessão?" e
  "onde estava cada canal?". Cada figura responde a sua pergunta na própria
  imagem:
  - `estrutura_da_coleta.png`: repetições de cada exercício de avaliação por
    data e por momento, com o horário de cada bloco, e gravação ausente ou
    interrompida marcada como tal (antes, a falta de um exercício baixava o
    total da sessão sem aviso);
  - `antes_depois_rms.png` e `antes_depois_mdf.png`: uma coluna por sessão e
    uma linha por exercício, antes × depois por canal, sem juntar datas;
    ponto cheio só onde a contração se distingue do repouso;
  - `antes_depois_rms_barras.png` e `antes_depois_mdf_barras.png`: a mesma
    comparação no formato de barras das figuras de artigo, uma linha por
    sessão e uma coluna por músculo; barra listrada onde a contração não se
    distingue do repouso e "×" em exercício não gravado ou interrompido. O
    título usa o nome com que essas figuras aparecem nos relatórios
    ("Amplitude do sinal muscular por exercício", "Frequência mediana (MDF)
    por exercício"), para quem leu a versão antiga reconhecer a mesma figura;
  - `canais_e_musculos.png`: canal, músculo informado e quantas gravações
    tiveram contração distinguível;
  - `LEGENDAS_SUGERIDAS.txt`: legendas com os números tirados dos próprios
    registros (gravações ausentes, pontos confiáveis, processamento) e os
    limites que o texto do artigo precisa declarar.

  As figuras desta pasta saem em 300 dpi, a resolução que as revistas pedem.
- Campo **Músculo de cada canal** ("Blue Ch1=Bíceps braquial; …"): o arquivo
  do aparelho identifica o canal, não o músculo. O nome aparece nas legendas
  e na figura de evolução.
- Opção **Anonimizar (P01, P02…)**: o nome do paciente sai de pastas,
  planilhas, figuras, relatórios e nomes de arquivo.
- `ferramentas/varre_sem_tr.py`: varredura por AST de texto de tela sem `tr()`.
  Classifica cada literal pelo destino (interface, log, chave interna ou
  arquivo, sem destino), segue variáveis locais até o `setText` e sabe em que
  argumento está o texto (`addItem(texto, dado)`, `setLabel("left", texto)`,
  `getSaveFileName(pai, título, nome_padrão, filtro)`).
- `ferramentas/envolve_tr.py`: reescrita em massa com splice em bytes. Cada
  f-string convertida é conferida pedaço a pedaço contra o molde. Plural por
  expressão e comentário no meio da f-string são recusados para revisão manual.
- `coleta_faltantes.py` aceita `ROA_TRAD_LOTE` (como o `aplica_trad.py`) e recolhe
  as tabelas exibidas por `tr(variável)`. `aplica_trad.py` passou a conferir os
  campos `{0}`/`{1:.1f}` e o `%p`, e guarda uma cópia por lote
  (`ROA.py.antes_trad_<lote>`) em vez de sobrescrever a anterior.

### Alterado
- **Validação de uso com leigos (27/09/2026), etapa pacote: manuais, guia
  e pacote refeitos com as telas desta rodada** (ROA.py não alterado).
  - Manual do Usuário (9 idiomas, `Manual_ROA/texto_novo*.py` regerados com
    `gera_manual_usuario.py --todos`): a seção "Simples (exame) e Completo
    (pesquisa)" foi reescrita em linguagem simples com o glossário da rodada
    (paciente, exame, gravação, aparelho, treino): tela inicial com Início e
    Sair, a caixa "Novo exame" sem aparelho, "De quem é este exame?", os
    passos 1-2-3, "Gravação salva", o nome do relatório e "Abrir relatório",
    o relatório com "Como ler este relatório" (figura nova, 41), "Rever uma
    gravação", Evolução do paciente, tamanho da letra, as pílulas, a ajuda
    por nível e os quatro caminhos para o Completo. As figuras 37 a 41 foram
    refeitas em cada idioma com o sinal de treino e um paciente fictício
    (`correcoes/pacote_manual_fotos.py`); 0 glifos nulos nos 9 idiomas e no
    volume; o PDF em português copiado para `Manual_ROA/manual_usuario.pdf`.
    No manual em chinês o nome do nível ficou uniforme ("简单（检查）", como
    na tela; a fonte CJK do PDF desenha esses parênteses como os comuns).
  - Manual Técnico (9 idiomas, `ferramentas/gera_manuais_tecnicos.py`):
    "Dois níveis de interface" no capítulo de arquitetura, "Os testes
    acrescentados na 1.9.0" no capítulo de testes, o parágrafo dos menus com
    Arquivo, Ferramentas e Ajuda e a troca de nível, "Zerar fadiga" no lugar
    de "Reset fadiga"; figuras e anatomia das 23 telas refeitas
    (`Manual_Tecnico/capturas.py` e `anatomia.py` por idioma).
  - Guia de imagens (`docs/GUIA_IMAGENS_ROA_com_fotos.pdf`,
    `docs/GUIA_IMAGENS_ROA.pdf` e a cópia em `Develyn/`): fotos refeitas
    pelos scripts de `ferramentas/guia_imagens/guia_img/scripts`; os itens 0
    e 1 descrevem o relatório novo (`Relatorio_<exame>_<voluntário>_<data>.pdf`,
    "Como ler este relatório", nunca por cima); "Completo (pesquisa)",
    "Zerar fadiga", HEOG/VEOG, "Limiar (µV)" e "Claro (branco)" nos textos
    e nas legendas das fotos. As 89 fotos que o guia usa foram refeitas em
    28/09 (o script de captura de ECG envolve só os widgets visíveis no
    detalhe Simples da aba, que desde a etapa d esconde RMSSD/SDNN/pNN50, e
    procura o rótulo "MWA (integral) + limiar"); 0 glifos nulos e nenhum
    caminho de usuário no texto dos dois PDFs.
  - `FORMATO_DADOS.md` documenta `filters_auto`,
    `report_channels.eog_threshold` e os arquivos `Relatorio_*.pdf` e
    `Figura_*.png` da pasta da gravação; `COMECE AQUI.txt` cita "Treino
    (sem aparelho)" e os dois níveis.
- **O PDF da sessão Multimodal tem uma página por modalidade.** Com os tipos de
  canal gravados no summary.json, a página 1 é o relatório de EEG só dos canais
  de EEG e as seguintes são o de EMG, o de ECG e o de EoG, cada uma com as
  figuras, o resumo e o veredito de qualidade da sua modalidade. Cada página
  diz, na própria página, o que ela é e onde estão as outras ("Pagina 1 de 4:
  relatorio de EEG dos canais de EEG (CH1-CH8). As demais modalidades tem
  relatorio proprio: EMG (p. 2), ECG (p. 3), EoG (p. 4)."). Antes saía uma
  página de EEG com os 16 canais, EMG e ECG com bandas de EEG, e sem o aviso
  que esta entrada e o Manual do Usuário prometiam. Multimodal sem os tipos
  gravados continua no formato de EEG, agora com o aviso na página.
- **Figura de sinal do PDF legível com muitos canais.** Até 8 canais numa
  coluna; de 9 a 16 em duas; acima disso em três ou quatro, sempre na
  proporção da caixa da página. Com 16 canais numa coluna a figura ocupava 4 cm
  de largura e os rótulos não se liam; agora ocupa a largura toda (17 cm), com
  cerca de 1,2 cm por painel. O rótulo do canal fica deitado, à esquerda; com
  três ou quatro colunas ele vai para dentro do painel, no canto de cima, e a
  escala do eixo y sai (deitado, ele invadia a coluna da esquerda e o
  `tight_layout` desistia, deixando o espaçamento padrão).
- **Topografia: a cor esmaece longe dos eletrodos, nas três vistas.** A spline
  esférica continua; onde a cobertura dos eletrodos é baixa, a cor vai para o
  fundo da cabeça (até 60%). Nos temas escuros o fundo da cabeça fica perto da
  ponta baixa da viridis (no ROA Escuro, a 60 unidades RGB) e a área sem
  eletrodo se lia como potência baixa; quando o fundo fica a menos de 100
  unidades de alguma cor da escala, o véu vai para um cinza neutro a pelo
  menos 100 de todas (no ROA Escuro, em T7 sem eletrodo, (126,114,143) a 140
  da cor do valor baixo; era (42,35,76), a 43). A cobertura é uma soma de gaussianas de desvio
  0,45 vez o espaçamento da montagem (mediana da distância de cada eletrodo ao
  vizinho): entre dois vizinhos a cobertura soma e não há véu; nos buracos da
  montagem e fora do eletrodo mais externo, há. Com dado fixo: com 8 canais e
  foco em C3, o máximo local de 10% da escala em T7 (sem eletrodo) fica sob
  véu de 0,6; com 16 canais e foco em C3, o platô em x ≈ -0,16 também (0,6);
  com 8 canais e foco occipital, o platô entre O1 e O2 recebe 0,3 em y = -0,5
  e 0,12 em média na parte a mais de meio espaçamento dos eletrodos. A dica do
  combo "Mapa" (Topografia e Offline) diz que fora dos eletrodos o valor é
  interpolado, não medido. Quadro sem variação entre eletrodos fica sem véu:
  não há valor a atribuir, e o véu desenharia ilhas num mapa uniforme.
- **Qualidade de sinal pelo tipo do canal.** O semáforo do cabeçalho, os LEDs
  e o veredito do PDF usam limiares do tipo (`QUALIDADE_LIMIARES`): os de EEG
  são os de sempre (ruidoso acima de 150 µV RMS); EoG, ruidoso acima de
  1000 µV; EMG e ECG, acima de 1500 µV; 60 Hz dominante é ruidoso em qualquer
  tipo. No EMG a rede é medida como linha: a potência de 57-63 Hz acima do
  piso dos vizinhos (50-56 e 64-70 Hz), sobre a de 20-120 Hz. A fração de
  55-65 sobre 1-80 Hz, que vale para os outros tipos, passava de 40% sem rede
  nenhuma, porque o EMG tem potência larga nessa faixa: no simples, com o
  filtro do exame ligado, o EMG simulado mostrava "▲ 1 ruidoso(s)" de vez em
  quando (rede de 0,43 com RMS de 15 µV). Canal "off" fica fora da contagem,
  com o LED apagado (○).
- **Modo simples com acabamento novo: um só botão cheio por tela, e ele é a
  próxima ação.** Quem escolhe é o estado: desconectado, "Conectar"; conectado,
  "Iniciar Gravação"; gravando, "Parar Gravação" cheio em vermelho; sessão
  parada ou gravação carregada no Offline, "→ Relatório PDF"; no Offline sem
  gravação, "Carregar selecionada". Os outros botões ficam em contorno neutro
  legível, e a aba de grupo escolhida, o selo do exame e a seleção de tabela
  deixaram de ser blocos azuis cheios (a aba vira cartão com filete de 3 px; a
  seleção, tinta clara com texto escuro). A dica da barra virou a frase do passo
  ("Passo 1 de 3 · Conectar o aparelho", "Passo 2 de 3 · Gravar o exame",
  "Passo 3 de 3 · Gerar o relatório"), montada na mesma máquina de estado; o
  texto de antes continua na dica de ferramenta, e avisos e erros aparecem como
  sempre. Conexão e sinal viraram um par de pílulas do mesmo tamanho, com forma,
  cor e palavra (● CONECTADO em verde, ■ DESCONECTADO em vermelho, âmbar para
  atenção); o cabeçalho diz "Paciente: <nome>" em vez de um "nenhum" solto (com
  teto de largura e o nome inteiro na dica de ferramenta) e o selo do exame
  ganhou o ▾ de "trocar". Cronômetro em 20/16 pt, títulos e estado em poucos
  degraus (10, 11, 12, 14, 16, 20 pt; o corpo continua em 10 pt), cabeçalho e
  barra de ação em cartões com mais respiro, linhas de tabela mais altas. No
  Offline, título e instrução em linhas separadas; em Conexão, "Atualizar"
  voltou ao tamanho natural (ocupava um terço da largura); na caixa "Sessão
  gravada", "→ Relatório PDF" cheio e "Abrir pasta"/"Fechar" em contorno (o
  Enter continua em Fechar); na tela inicial, cartões com teto de altura, o
  bloco no terço de cima e "Novo exame" em destaque. As cores saem do tema pela
  regra de contraste WCAG que o ROA já usa na paleta dos canais (texto
  secundário a 7:1, borda de controle a 3:1, pílulas a 4,5:1), então os temas
  escuros e o de alto contraste herdam a regra. Tudo fica atrás do nível
  Simples: as regras vivem na folha do app presas à janela com
  `nivelUi="simples"` e a densidade (tela com menos de 900 px de altura) fica
  numa global de módulo, de modo que troca de tema, o `main()` e as folhas
  locais dos diálogos seguem o nível sem refazer nada. Trocar para o Avançado
  com a janela aberta devolve o visual da 1.8.4: repole só os tipos atingidos,
  e cada página na primeira vez que aparece (0,4 a 0,7 s por troca, contra 0,3
  a 0,5 s na 1.8.4 e ~10 s de refazer a folha inteira). Seis chaves novas de
  tradução nos 8 idiomas; em espanhol, italiano e chinês "Conectar o
  aparelho" e "Gravar o exame" usam o mesmo termo do resto da interface
  (aparato, apparecchio, 录制), não um sinônimo só desta tela.
- **Topografia redesenhada nas três vistas** (Visualizar → Topografia, e o
  mesmo mapa 2D do Offline, do Layout Custom e do ERS/ERD). **O campo mudou de
  interpolação:** a IDW 1/d² deu lugar à spline esférica (Perrin et al., 1989,
  m = 4, a mesma família do EEGLAB e do MNE). A IDW fazia de cada eletrodo um
  platô, e eletrodo isolado virava alvo de anéis concêntricos: um foco frontal
  único, na linha média, aparecia como dois (em Fp1 e em Fp2, com uma sela no
  meio), F7/F8 com 4,11 contra 4,00 ganhavam ilhas fechadas e C3/C4, halos. A
  spline passa pelo valor de cada eletrodo, é cortada na faixa medida (nenhuma
  cor mostra um valor que nenhum eletrodo mediu) e, entre o último anel de
  eletrodos e o contorno da cabeça, repete o valor da borda em vez de
  extrapolar. O campo também passou a ter o eletrodo onde ele é desenhado (0,92
  do raio; antes o pico do campo ficava em 1,00 R), o que muda o mapa perto da
  borda. Seguem as âncoras da viridis e o modo CSD/Laplaciano; a sub-aba se
  chama "2D (spline)". O acabamento também mudou: borda da cabeça lisa
  (máscara vetorial com antialiasing no lugar de `setClipPath`), tabela de cor
  no lugar dos 9.216 `setPixelColor` por quadro, cabeça, nariz e orelhas num
  contorno só. No 2D o valor fica dentro do disco num corpo só para o quadro
  inteiro, e só quando cabe na corda do disco; o nome vai acima, abaixo ou ao
  lado, onde não cobre outro disco nem outro nome, e o disco nunca passa de 42%
  da distância ao vizinho. Com 64 canais os valores (e os nomes que não cabem)
  ficam na dica de ferramenta de cada eletrodo: antes o nome era escrito por
  cima do valor do disco de cima (AF3 sobre Fp1, O1 sobre PO3) e os discos se
  tocavam. A dica traz nome, valor com unidade e, no Tempo Real, "módulo de
  expansão"; o anel verde que marcava a expansão saiu (sumia sobre o disco
  verde-azulado e não tinha legenda). O domo 3D é traçado por pixel sobre a
  projeção esférica, lê o MESMO campo do 2D, tem silhueta e aro suaves e não
  desenha a face interna do lado oposto. A sombra dele ficou só na faixa da
  borda (no máximo 15%): o Lambert anterior escurecia até 45% da cor, a região
  occipital era lida na barra até meia escala abaixo do dado, e o rodapé dizia
  "sombreado = relevo de potência", o que nunca foi verdade. O rodapé agora diz
  que a cor é o dado e a sombra da borda só dá volume; no quadro plano não há
  sombra. A Tomografia usa a paleta do 2D em 11 camadas (número ímpar: o meio
  da escala cai no meio de uma camada e o quadro plano sai na mesma cor do 2D),
  amplia o campo antes de posterizar e desenha as isolinhas como linhas
  contínuas. As três vistas têm barra de escala com os números das pontas e a
  unidade (µV²; o domo e a Tomografia não tinham barra nenhuma); em quadro baixo
  e largo (1366 × 768, Offline) a barra vai em pé ao lado da cabeça, e a cabeça
  fica com a altura toda. **Na Tomografia a barra só traz números na fatia do
  escalpo:** abaixo dele as camadas são o campo × e^(−1,6·d), nenhuma cor chega
  à ponta alta e quem lesse a cor pelos números do escalpo subestimaria o valor
  medido; a barra troca os números por "modelo ilustrativo: cores do escalpo ×
  0,53" (a 40%). O combo "Mapa" (Interpolado/CSD) vale só para o 2D: o domo e a
  Tomografia dizem POTÊNCIA no título e a dica do combo avisa. No modo CSD o
  disco mostra o próprio |CSD|, o número da cor e da barra (antes mostrava a
  potência bruta pintada na cor do |CSD|, e 4 de 16 discos ficavam fora da
  barra).
- **Quadro sem variação entre eletrodos não pinta mais a cabeça de amarelo.**
  Com todos os valores iguais, ou faixa abaixo de 1% do valor, as três vistas
  mostram uma cor só, a do meio da escala, e uma marca aponta o meio da barra.
  Iguais de fato, a barra diz "sem variação entre eletrodos"; abaixo de 1%, diz
  "variação < 1% entre eletrodos" e as pontas mostram o menor e o maior valor
  (com 100 e 100,9 as pontas diziam "100" e "100" e os discos, "100" e
  "101"). Antes o min-max caía na divisão pelo máximo e o mapa inteiro ia ao
  topo da escala, como se a cabeça toda estivesse no pico. Numa escala com o
  zero como âncora, um quadro todo zero fica na ponta baixa. Os avisos saem
  nos nove idiomas e cabem inteiros na barra mais estreita (340 px); em russo
  a primeira tradução passava 14 px do espaço livre e ficou a forma curta.
- **Custo da Topografia.** As vistas ocultas só guardam o dado (0,1 a 0,6 ms
  por quadro, contra 4 a 32 ms na 1.8.4) e o campo é calculado ao pintar, uma
  vez por quadro para as três vistas; a parte da spline que só depende da
  montagem fica em cache. Dado novo no tamanho da aba (845 × 554), medido nesta
  máquina em rodadas alternadas com a 1.8.4: 2D 5 a 7 ms (1.8.4: 26 a 35), domo
  15 a 17 ms (14 a 19) e Tomografia 14 a 17 ms com 8 e 16 canais (7 a 12); com
  64 canais, 15, 21 e 17 a 18 ms (76 a 79, 44 a 46 e 35 a 37). **A Tomografia
  com poucos canais ficou 1,3 a 2 vezes mais cara que na 1.8.4**, em troca das
  isolinhas contínuas; elas saem numa grade de 96 × 96 para conter o custo (a
  versão anterior deste bloco chegava a 25 a 48 ms, com picos de 60 a 84 ms ao
  vivo). A atualização continua a cada 0,5 s.
- Canais com rótulo antigo ou maiúsculo (FP1, T3, "EEG C3-A1") entram na
  topografia pela posição do eletrodo equivalente. Canal sem posição fica fora
  do mapa e da escala; canal sem valor (NaN, vazio) também sai da escala e o
  disco mostra "—", sem derrubar o desenho. O domo nasce um pouco menos inclinado (0,42 rad) para o occipital
  não ficar escondido atrás da borda.
- **Sub-abas fixas no modo simples.** A visibilidade por modo de exame e por
  nível era aplicada pela posição de cada sub-aba, e arrastar uma delas fazia
  a regra esconder a aba errada. Os mapas passaram a resolver a posição pela
  página (a ordem de criação continua sendo a referência): no modo completo as
  sub-abas continuam arrastáveis, como na 1.8.4, e só o modo simples as mantém
  fixas.
- **A pasta da sessão leva o nome do paciente** quando há voluntário ativo e o
  campo "Nome do sujeito" está no padrão: `V01_Maria_Silva_<data>_<hora>` em vez
  de `V01_voluntario_<data>_<hora>` (nos dois níveis). Com o campo preenchido ou
  com modelo próprio, nada muda. Por causa disso, a **exportação BIDS** passou a
  montar o `ses-` só com o carimbo de data e hora (`ses-20260918101200`) e não
  mais com o começo do nome da pasta, para o nome do paciente não ir parar num
  conjunto feito para circular pseudonimizado.
- **Assistente de primeiro uso**: as opções de layout perderam o sufixo com os
  códigos internos ("(ts1, fft, head, bands)") e o layout só é gravado quando a
  página aparece, isto é, no caminho "Pesquisa". A página "Como você vai usar o
  ROA?" acompanha na hora o idioma escolhido na página anterior.
- **Ao conectar o aparelho no modo simples** estando em Configurar, a janela vai
  para a tela do sinal da modalidade (antes só simulação e playback faziam
  isso). No modo completo continua onde estava, para quem conecta e segue
  ajustando filtros, hardware ou calibração.
- **No modo simples a janela abre na tela do sinal da modalidade** (Músculos,
  Coração, Olhos), não sempre no Tempo Real de EEG.
- O `summary.json` ganhou `"acquisition_mode"` (modalidade em que a sessão foi
  gravada). `"filters_auto"` continua verdadeiro nas reconexões da mesma janela
  e só volta a falso quando o operador mexe nos filtros.
- Parar a gravação acrescenta só a sessão nova à tabela do Offline. A pasta
  inteira só é varrida na abertura e em "Atualizar lista": varrer a cada parada
  travava a tela por segundos em acervos grandes, com a aquisição ainda ligada.
- A dica da barra de ação quebra linha e cede largura em janela estreita; de um
  erro de conexão ela mostra só a primeira linha (o texto inteiro vai na caixa
  de mensagem e no log).
- **Manual do Usuário com a seção "Modo simples e modo completo"** nos nove
  idiomas (pt, en, es, it, fr, de, ja, zh, ru): tela inicial do modo simples,
  janela com a barra de ação, sessão gravada e tela Offline (figuras novas
  37 a 40, capturadas em cada idioma), como trocar de modo e os limites
  conhecidos. A seção abre o bloco de novidades do capítulo 1 e entra no
  sumário. PDFs por idioma em `Manual_ROA/idiomas/` e volume único
  `Manual_ROA/Manual_ROA_9_idiomas.pdf` regenerados por
  `gera_manual_usuario.py --todos`. O `Manual_ROA/manual_usuario.pdf`, que o
  menu Ajuda → "Manual do usuário (PDF)" abre, passou a ser o manual novo em
  português; o anterior ficou como `manual_usuario_1.8.4_antigo.pdf`.
- **Documentação refeita para a 1.9.0.** Manual do Usuário (9 idiomas, 49 a
  56 páginas cada, e o volume único de 474 páginas) e Manual Técnico (9
  idiomas, 87 a 94 páginas) regenerados com as figuras novas, e o guia de
  imagens também. Na seção "Modo simples e modo completo" o texto acompanha
  o visual novo: o sinal de que dá para gravar é a frase "Passo 2 de 3 ·
  Gravar o exame" (antes "Pronto para gravar."); o cabeçalho é descrito com
  "Paciente:", o selo do exame com ▾ e as pílulas de conexão e de sinal; a
  barra de ação, com o único botão cheio e os passos 1-2-3 (a mensagem de
  sempre fica na dica de ferramenta). Saiu a nota de que a simulação mostra
  "perdendo amostras", que a 1.9.0 corrigiu, e o limite "o PDF traz bandas
  de EEG em EMG, ECG e EoG" virou o comportamento novo (Multimodal continua
  no formato de EEG, com aviso). O capítulo 8 ganhou "A Topografia na versão
  1.9.0": o texto antigo descreve a IDW e o domo com relevo, e o remendo
  diz o que mudou (spline, barra com unidade nas três vistas, sombra só na
  borda, Tomografia com números só no escalpo, quadro sem variação, ERD% com
  sinal). Os nomes de botão e de aba citados são os do dicionário de cada
  idioma. `sincroniza_pacote.py` passou a gravar a publicação na pasta da
  versão (`Atualizacao_GitHub_v<versão>`), não mais fixa em v1.8.4.

### Corrigido
- **Validação de uso com leigos (27/09/2026), etapa final: segunda rodada
  com as pessoas simuladas.** Depois das etapas a-d e acerto, as quatro
  pessoas operaram o programa de novo (simulador tela a tela) e sete
  achados persistiam ou apareceram; mais dezoito "incomoda" pequenos foram
  fechados. O Completo (pesquisa) mantém todos os recursos.
  - **Barra de ação (G05)**: o aviso do filtro ao conectar não esconde mais
    o passo: no Simples ele vai DEPOIS da frase, "Passo 2 de 3 · Gravar o
    exame · Filtro do exame ligado: tira o ruído da tomada." (aviso
    "anexo", `_dica_temporaria(anexa=True)`); quem clicava Iniciar Gravação
    antes de 5 s nunca via o passo 2. Ligar o aparelho ou o treino apaga a
    gravação aberta no Analisar do selo ("Gravação aberta: …") e da dica
    ("Passo 3 de 3" e "→ Relatório PDF" vazavam para o Treino depois de
    "Abrir uma gravação"); o aviso temporário anterior também é apagado.
    Só a gravação que JÁ estava aberta ao conectar deixa de contar: uma
    carregada depois, com o aparelho ligado, volta a dar "Passo 3 de 3"
    ou "Pronto · relatório gerado" como antes.
  - **Marcar evento**: a barra confirma "Evento 1 marcado aos 3 s.", o
    botão conta "⚑ Marcar evento (1)" (volta ao normal ao parar) e a linha
    do marcador tem 2 px; na aba Músculos nada mudava na tela.
  - **Caixas de "salvo" (G25)**: no Simples "Relatório salvo na pasta de
    Maria Teste, 27/09 às 19:26 (Relatorio_EEG_….pdf)." e "Figura salva na
    pasta de …" (`_frase_arquivo_salvo`) no lugar do caminho em 7 linhas; o
    caminho inteiro fica na dica de ferramenta da caixa e em Abrir pasta
    (o Completo mantém "Arquivo salvo: <caminho>"). "Treino salvo na pasta
    de gravações como treino_2026-09-27_19-31-05 (sem paciente), 27/09 às
    19:31. Você acha de novo em Início → Abrir uma gravação."; a gravação
    sem paciente com aparelho diz o nome da pasta do mesmo jeito. Depois
    de Salvar figura a barra diz "Figura salva: Figura_EEG_….png" com
    **Abrir figura** por 8 s (ficava "Pronto · relatório gerado", do PDF
    que a gravação já tinha).
  - **Consultor (G22)**: a conversa sai na fonte da interface (o
    QTextBrowser herdava a monoespaçada do QTextEdit); a FAQ "Onde ficam
    minhas gravações" tem resposta própria no Simples ("Ficam na pasta de
    cada paciente … Início → Abrir uma gravação, ou Ajuda → Pasta do
    programa / gravações"; a do Completo cita "Pasta de configuração /
    sessões", que só existe lá) via `a_simples` na HELP_FAQ e
    `help_answer(nivel)`; a FAQ "O que quer dizer Sinal OK" virou lista
    (uma cor por item); no Simples os links "Aprofundar" são só FAQ e guias
    (sem "SNR — Signal-to-Noise Ratio" nem "Por trás disso
    (metodologia)").
  - **Exame de músculos**: no Simples, com nenhum músculo marcado, Iniciar
    Gravação pergunta "Músculos não marcados" com Marcar músculos (vai à
    aba Músculos) / Gravar assim mesmo / Cancelar; o PDF só avisava no fim.
    No PDF, as ativações do TKEO são fundidas antes de contar
    (`emg_fundir_ativacoes`: buracos < 0,25 s juntam, < 0,1 s cai): 6
    surtos saíam como 12 contrações, e a figura mostrava 6 faixas; "Cada
    faixa laranja … é uma contração contada"; "Cansaço muscular: sim" só
    com 1 min de gravação e 10 contrações no canal (44 s sintéticos saíam
    "sim"); abaixo de 1 min, "gravação curta demais (menos de 1 minuto)".
    Eixos das barras em palavras no Simples ("Força média do sinal (RMS,
    em µV)", "Força máxima (µV)", rodapé "µV = milionésimo de volt").
  - **PDF de EEG e ECG**: ritmos com nome na língua da tela nos gráficos
    (`rotulo_banda`: Teta, Alfa, Gama; o texto dizia "alfa 37%" e o
    gráfico "Alpha"); no Simples, barras de percentual por ritmo no lugar
    do espectro em escala log (10⁻¹¹ a 10³) e do mapa canal × ritmo, que
    ficam no Completo. ECG do Simples com o traçado só do canal usado na
    análise ("canal usado: CH2" no título) em vez de 8 traçados iguais.
  - **Telas**: "Abrir uma gravação" no Simples mostra a pílula neutra "○
    Vendo gravação" (era "■ DESCONECTADO" vermelho) com a dica "Para gravar
    de novo, clique em ▶ Conectar."; o assistente de primeiro uso mostra
    "Recusar e sair" só na página do termo, discreto, com Avançar como
    padrão; a janela "Tipo de exame e número de canais" explica "Canal =
    cada eletrodo (uma linha de sinal na tela). 8 canais é o padrão do
    aparelho." e o combo não corta mais "8 canais"; Sistema › Sessão e
    Arquivos ganhou **Abrir pasta** e "Para uma cópia de segurança, copie
    esta pasta inteira (gravações e cadastro de pacientes)"; no Completo o
    campo "Nome do voluntário (sem cadastro)" fica desligado com voluntário
    ativo, com a nota "Só vale sem voluntário ativo." (G04); ⌂ Início na
    barra nos dois níveis; ao mudar para o Completo a barra avisa "Modo
    Completo (pesquisa): todos os recursos. Para voltar, use Exibição →
    Simples (exame)."; o último paciente usado fica em
    `config.last_volunteer_dir` e a tela inicial reabre com ele marcado
    "(último usado)" (escolher "(nenhum)" de propósito zera); os nomes de
    canal do Empilhado saem a 11 pt no Simples e a dica do gráfico diz onde
    fica cada eletrodo ("CH1 Fp1 — testa, lado esquerdo",
    `descricao_posicao_10_20`; G37); a figura salva do Offline alarga o
    eixo esquerdo durante a exportação para o rótulo em pé não cobrir "CH4
    músculo". No Completo a 150% em 1366 px o cabeçalho às vezes ficava
    com os LEDs e o separador (1383 px em 1346) porque o teste de corte
    lia a geometria antiga logo depois da troca de letra; o pedido do
    layout agora complementa o teste (`_update_header_responsive`).
  - Tradução: 55 frases novas nos 8 idiomas (lote `leigo_final`); 4 chaves
    órfãs apagadas.
- **Validação de uso com leigos (27/09/2026), etapa acerto: achados dos
  revisores de fluxo, PDF e textos.** Depois das etapas a-d, três revisores
  operaram o programa de novo (simulador tela a tela, relatórios sintéticos
  e reais, os 9 idiomas) e apontaram o que ficou. Nada saiu do Completo
  (pesquisa).
  - **Sair pela tela inicial deixava o programa rodando invisível**: "⌂
    Início" esconde a janela (`hide`) e o `close()` seguinte não emitia
    `lastWindowClosed`, então `app.exec()` nunca voltava (processo fantasma,
    log em uso, o próximo "abrir o ROA" virava um segundo processo).
    `_voltar_ao_inicio` chama `_encerrar_programa` (`app.exit(0)` no tique
    seguinte; `quit()` do Qt 6 não sai de laço aninhado).
  - **Tela inicial dizia "(nenhum — selecione ou cadastre)" com um paciente
    em uso**, e "(nenhum)" escolhido não soltava o paciente: o combo nasce
    no paciente em uso (`_populate_volunteers`, mesmo registro da janela) e
    a escolha "(nenhum)" feita no combo (`volunteer_escolhido` na escolha)
    deixa sem paciente em `apply_launcher_choice`; os caminhos sem combo
    (Abrir uma gravação, Configurações) não mexem no paciente.
  - **Analisar no Simples com 2-3 gravações mostrava UMA linha** e uma barra
    de rolagem minúscula: a tabela pede 4 linhas inteiras no Simples
    (`_offline_minimos`) e o repartidor cede o que falta ao traçado
    (`_offline_reparte`); ao abrir uma gravação por duplo clique a linha
    marcada é a DELA (`_offline_linha_da_aberta`; repovoar a lista marcava a
    mais recente por cima).
  - **Letra 125/150% em 1366 px**: as pílulas e selos do cabeçalho param em
    125% (`_pt_cab`, `ESCALA_CABECALHO_MAX`), como a barra de ação; se
    ainda não couber (idioma de palavra longa) o par de pílulas perde a
    reserva de pior caso e o selo do paciente e o badge encolhem
    (`_ajusta_cabecalho_simples`, com histerese); a página Sistema não ganha
    mais barra horizontal (quatro rótulos sem quebra de linha, um deles na
    página oculta "Caminhos e Auditoria", que conta no mínimo do
    `QStackedWidget`).
  - **"▲ perdendo amostras 5%" depois de trocar tema ou letra**: a perda era
    cumulativa desde a conexão e o repolimento da folha (que trava a
    interface por segundos) ficava acusado até desconectar; fora da
    gravação a conta recomeça na última troca (`_zera_referencia_perda`,
    `_perda_ref`). Gravando, continua a conta desde o REC.
  - **"voluntario_…" e "sessão" no Simples** ao gravar sem paciente com o
    aparelho: a pasta passa a `exame_<data>` (o Completo mantém
    `voluntario_`), o rodapé diz "Gravando o exame de Maria Teste" /
    "Gravando o exame sem paciente" e a coluna Gravação do Analisar mostra
    "(sem paciente)" para as pastas antigas `voluntario_…` (a pasta fica na
    dica). Nome da pasta de gravações antigas, `data.csv` e `summary.json`
    não mudam.
  - **Gravação que já tinha relatório gerava outro (`…_2.pdf`)**: ao
    carregar, `_relatorio_existente` acha o `Relatorio_*.pdf` (ou o
    `report.pdf` antigo) mais recente e a dica oferece "Abrir relatório";
    o botão de contorno "→ Relatório PDF" do Analisar continua para gerar de
    novo. Vale também no Completo depois de "Carregar selecionada".
  - **Título da janela em português no Completo** ("[CONECTADO]",
    "[GRAVANDO]", "[PLAYBACK]") em todos os idiomas: `_update_window_title`
    usa tr() nos dois níveis (chave nova "[PLAYBACK]  {0}").
  - **Histórico em Configurar → Pacientes** fora de tr() ("(4792 amostras,
    0 markers)") e com "sessão" no Simples: "({0} amostras, {1} eventos)",
    "N gravação(ões):" / "Nenhuma gravação ainda." no Simples.
  - **Relatório PDF — piscadas com dois critérios**: a tela contava 11 e o
    PDF 27 na mesma gravação. Com o filtro do exame (passa-altas) cada
    piscada vira um pico e um vale da mesma altura, e `eog_piscadas` contava
    o vale; agora o evento de polaridade oposta que começa até 150 ms depois
    do anterior é descartado (rebote do filtro). Além disso a sensibilidade
    da aba Olhos vai para o `summary.json` (`report_channels.eog_threshold`,
    chave nova) e o PDF conta com o MESMO critério da tela
    (`eog_piscadas_tela`, também usado pela aba Olhos); sem a chave
    (gravação antiga) vale o detector do módulo, e o PDF diz qual critério
    usou.
  - **ECG com ritmo implausível afirmado como fato** ("210 batimentos por
    minuto … febre", "Qualidade do sinal: boa"): no Simples o quadro traz
    uma frase só ("Não deu para medir os batimentos com segurança neste
    canal…"), sem bpm, faixa, SDNN nem causas; o aviso sai ANTES do quadro
    (`_pdf_topo`) e o cabeçalho diz "Qualidade do sinal: ruim no canal do
    coração". No Completo os números ficam, com o aviso no topo.
  - **Multimodal: "Músculo não informado em CH1-CH4"** com os músculos em
    CH9-CH12: `channel_muscles` é fatiado por seção como os tipos e a frase
    numera pelo canal global (`secao_idx`). Nome do músculo traduzido no PDF
    (`nome_canal_por_tipo` passa por tr(): "Biceps Brachii" no PDF em
    inglês) e inteiro no quadro leigo ("CH10 Tríceps Braquial", não
    "Braqui.").
  - **`data.csv` com a última linha incompleta** (programa fechado à força,
    queda de energia) levantava `ValueError` cru (E999) no → Relatório PDF e
    no Carregar: `_loadtxt_tolerante` lê o que dá, o PDF e o Analisar avisam
    "A gravação terminou de forma inesperada; foram lidos N segundos" e a
    leitura entrou no E118.
  - **Gravação marcada `sample_rate_ok = false`** (ou com mais de 2% de
    amostras perdidas) saía no PDF sem aviso: "O programa não conseguiu
    guardar todas as amostras desta gravação: os números abaixo podem estar
    errados; grave de novo" antes do quadro, em toda página (o Completo
    leva junto o aviso técnico gravado).
  - **Faixas de referência**: "faixa comum em adultos acordados, em repouso
    e sem ler: 8 a 21 por minuto; Bentivoglio et al., 1997" e "60 a 100;
    American Heart Association"; "Abaixo da faixa comum" lembra que ler ou
    olhar uma tela baixa a taxa.
  - **Gravação de olhos/coração sem `summary.json`** saía como "Relatório
    de EEG · Cérebro" com "delta 94%, comum no sono profundo": o exame é
    deduzido pelos nomes das colunas (`EOG_*`, `ECG_*`, `EMG_*`;
    `_pdf_modo_pelos_nomes`), o título diz "(tipo de exame deduzido pelos
    nomes dos canais)" e o nome do arquivo segue o exame deduzido.
  - **Figura do envelope de EMG ilegível** (rótulos de ~3 pt, espremida no
    fim da página): 1 polegada por canal, letra 8, e a parte de EMG ganha
    uma página para as figuras de baixo quando faltaria largura (abaixo de
    12 cm); a altura de cada figura é limitada à página.
  - **Sobras do glossário no Simples**: sub-aba "Gravações e Arquivos",
    menu Ajuda "Pasta do programa / gravações", dica "Inicia ou termina a
    gravação do exame.", diálogo "Escolha a gravação (arquivo data.csv)",
    dica leiga do "Evolução do paciente…", faixa "Sinal de treino: …" na
    aba Bio, aba "Bio (EMG/ECG/EOG)" no Multimodal e "Nenhum canal de
    olhos"; "Salvar figura (PNG)" sem gravação carregada usa a linha 0,
    como o Carregar (G24).
  - `_modo_treino` só considera a thread que está RODANDO: depois de
    desconectar, o modo antigo ficava colado e a pasta seguinte saía
    "treino_" no aparelho.
- **Validação de uso com leigos (27/09/2026), etapa d: telas de análise,
  ajuda e textos.** O Analisar do Simples parecia laboratório, a figura saía
  com a faixa azul e sem título, a Evolução misturava tipos de exame, a
  ajuda respondia com guias que mandavam a telas escondidas e sobrava jargão
  ("Porta COM", "VID", "Threshold", "Lime (verde-limao)", "placa base") nas
  telas de configuração. Nada saiu do Completo (pesquisa): o que mudou lá
  foi só acento, inglês cru e ".py".
  - **Analisar no Simples é "Rever uma gravação" (G12)**: somem o quadro
    FFT/Bandas/Estatísticas, o combo "FFT/Stats do canal", a linha da janela
    e da taxa, "Abrir CSV…" e a faixa azul de seleção (`_ajustar_offline_nivel`,
    aplicado na troca de nível); a tabela diz Paciente/Gravação/**Exame**
    (tipo lido do `summary.json`, `_scan_session_dir`) em vez de
    Voluntário/Sessão/Markers; o rótulo da gravação aberta vira frase,
    "Gravação de V01 Maria Teste, 27/09 às 09:07, 12 segundos"
    (`_offline_frase_gravacao`), e repovoar a lista não o apaga mais; duração
    e tamanho com vírgula ("12,4s"). No Completo volta tudo, inclusive o
    título "Modo Offline — Análise de Sessões Gravadas".
  - **Salvar figura (G15)**: `Figura_<exame>_<paciente>_<data_hora>.png` na
    pasta da gravação (nunca por cima: `_2`, `_3`; `_nome_arquivo_saida`
    compartilhado com o relatório), exportada sem a faixa de seleção, com
    título "V01 Maria Teste · EEG · Cérebro · 27/09/2026 09:07" e o eixo dos
    canais em µV (tudo restaurado depois); a caixa "Figura salva" tem **Abrir
    figura** (padrão), Abrir pasta e Fechar.
  - **Evolução do paciente (G21)**: cada métrica pertence a um tipo de exame
    (`METRICA_MODALIDADE`); só entram as gravações desse tipo (o Multimodal
    quando tem canais do tipo, e só esses canais) e a tela diz "N
    gravação(ões) de outro tipo de exame foram ignoradas"; métrica nova
    "Frequência cardíaca (bpm) — ECG" (Pan-Tompkins + RR); métrica
    pré-selecionada pelo exame em uso e paciente em uso já escolhido; no
    Simples "Paciente:", rótulos em palavras ("Ondas do cérebro (força do
    ritmo escolhido)", "Força do músculo", "Cansaço do músculo", "Batimentos
    do coração por minuto", "Piscadas por minuto"), "Ritmo:", campo de canais
    escondido, sem citar a Estatística guiada e com "não é laudo nem
    diagnóstico"; números por `num_loc`.
  - **Assistente de ajuda (G22)**: `help_answer(nivel, modalidade)`; no
    Simples ficam de fora os documentos que citam telas ocultas
    (`_HELP_TELAS_SO_COMPLETO`, marcados como `so_completo` no corpus) e os
    cartões de método, e o guia não é promovido por cima da resposta; FAQ
    leigas novas ("O que quer dizer Sinal OK (e as cores)", "Ligar o
    aparelho", "Gravar um exame", "Salvar relatório em PDF"); pergunta de
    definição ("o que é/o que quer dizer") não vira guia
    (`_help_quer_definicao`); pergunta que traz o título inteiro de uma FAQ
    ("onde ficam minhas gravações") vai para ela; o exame em uso só desempata
    de leve; atalhos e exemplos leigos no campo; o cartão de método não
    repete o título; os links do intro que levam a guias ocultos somem no
    Simples; o guia "Deixar o sinal limpo" e o manual explicam o selo como o
    código faz (canais ruins/ruidosos OU perda de amostras).
  - **Jargão (G34-G38)**: na janela "Tipo de exame e número de canais" as
    dicas dizem o que cada exame mede e o combo diz só "8 canais", "16
    canais" (sem "placa base"/"módulo"); Configurar > Conexão "Aparelho
    (porta USB):" e "Pasta das gravações:"; Pacientes com "Usar no exame",
    "Deixar sem paciente", "Excluir paciente…", coluna "Código", "Em uso:
    V01 — Maria Teste" e a contagem de gravações atualizada ao parar de
    gravar; barra "Aparelho conectado (COM3)"; Sistema: temas com rótulo
    traduzido e a chave de `THEMES` no `userData` (`rotulo_tema`; "Verde-limão",
    "Claro (branco)", "Sistema (padrão)"; `config.theme` e temas
    personalizados intactos), "Tema (cores da tela)", "(muda na hora e fica
    salvo)", "Alguns textos só mudam depois de fechar e abrir o programa",
    Sessão e Arquivos por nível (Gravações, "Prévia do nome da próxima
    gravação", "Pasta onde as gravações ficam", "→ Arquivo EDF (outros
    programas)", sem a frase BIDS onde não há o botão; no Completo "serão",
    "é", "junto ao programa" e "Nome do voluntário (sem cadastro):"); barra
    de cima "Filtro do exame ligado: tira o ruído da tomada e deixa só as
    frequências do exame"; eixos de todos os gráficos no idioma da tela
    (`pg.AxisItem.tickStrings` trocado na classe: "0,5" em pt/es/it/fr/de/ru);
    abas Músculos/Coração/Olhos no Simples com "Sensibilidade", "Zerar",
    "movimentos rápidos dos olhos", "% do tempo com o olhar parado", "Canal
    das piscadas (vertical)", "Onde estão os eletrodos (desenho do corpo)",
    "Sinal do coração (cada triângulo é um batimento)"; regressão ocular,
    RMSSD/SDNN/pNN50, colunas % MVC/Qualidade e histórico de montagens só no
    Completo, onde "Threshold"/"Reset" viraram "Limiar"/"Zerar" e
    HEoG/VEoG viraram HEOG/VEOG.
- **Validação de uso com leigos (27/09/2026), etapa c: relatórios PDF.** O
  relatório saía todo sem acento e em siglas ("Relatorio de Sessao - EEG",
  "Sujeito: voluntario", "Fs: 250.0 Hz", "APTO (8 OK, 0 ruidosos…)",
  "Banda dominante: Alpha (180 uV2)", "MDF=-0.32 +/- 0.09 Hz/s (nao
  conclusivo)"), com metade da página em branco e o link do GitHub no rodapé.
  `_generate_pdf_report` foi refeito (G07, G08, G09, G10, K3):
  - **Todo texto por `tr()`, com acento e no idioma da interface.** A
    Helvetica do reportlab cobre Latin-1 (pt/en/es/it/fr/de); em russo,
    chinês e japonês `pdf_fontes` registra uma TTF/TTC do Windows
    (segoeui.ttf; msyh.ttc; YuGothM.ttc, meiryo.ttc ou msgothic.ttc, com
    `subfontIndex`) e passa a mesma família ao matplotlib das figuras; sem
    nenhuma delas, cai na Helvetica trocando o que ela não imprime
    (`_EscritorPdf.seguro`). Conferido com fitz + fontTools: nenhum glifo
    nulo em ru, zh e ja. O texto sem espaços (chinês, japonês, caminho de
    arquivo) quebra por caractere na largura útil.
  - **Cabeçalho em palavras**: "Relatório de EEG · Cérebro" (os mesmos nomes
    de exame da tela), "Paciente: V01 Maria Teste" ou "Paciente: não
    informado" no Simples ("Voluntário:" no Completo; o valor de fábrica
    "voluntario" nunca aparece: `sujeito_digitado` em `resumo["subject"]` e
    em `config.subject`), "Data da gravação", "Duração: 23 segundos"
    (`duracao_em_palavras`), "Canais", "Eventos marcados"; a taxa de
    amostragem só no Completo. "Qualidade do sinal: boa / com ruído em N de
    M canais / ruim em N de M canais" (`_pdf_qualidade_palavras`) no lugar de
    "APTO"; o veredito técnico fica no bloco do fim, no Completo.
  - **Quadro "Como ler este relatório"** no topo, 2 a 4 frases por
    modalidade: EEG (o ritmo que mais apareceu, em palavras: "alfa (8 a 13
    Hz), comum em pessoa acordada e relaxada…", e a divisão do sinal entre os
    ritmos em %); EMG (quantas contrações, força média relativa à mais forte
    da própria gravação, "Cansaço muscular: sim / não / não dá para dizer"
    com o porquê, pela inclinação da MDF e seu erro-padrão); ECG ("Frequência
    cardíaca média: 70 batimentos por minuto (faixa comum em adultos em
    repouso: 60 a 100)", dentro/abaixo/acima, e a variabilidade (SDNN) só
    com o MESMO mínimo de RR da tela (`ECG_RR_MIN`), senão "Gravação curta
    demais para a variabilidade: faltam N intervalos"); EOG ("Piscadas: 9 na
    gravação, 18 por minuto (faixa comum: 8 a 21 por minuto)", conclusão em
    palavras, sacadas); Multimodal (uma parte por tipo de sinal e, se só
    houver EEG, "Nenhum canal de músculo, coração ou olhos foi gravado"). Em
    todo quadro, "Este relatório não é laudo nem diagnóstico.".
  - **"Detalhes técnicos" no fim**: Welch, PSD, potências por banda, MDF ±
    EP, TKEO, SENIAM, %CVM, SDNN/RMSSD/pNN50, SD1/SD2, PERCLOS, critério do
    canal, veredito técnico e canais desligados, completo no Completo; no
    Simples só o canal usado e o pedido de marcar o músculo dos canais sem
    nome (nada se perde no Completo). Números com `num_loc` (vírgula em
    pt/es/it/fr/de/ru), unidades µV e µV².
  - **Coerência com a tela**: o `summary.json` ganhou a chave nova
    `report_channels` (`{"ecg", "eog_v", "eog_h"}`, base 0), gravada ao
    iniciar e atualizada ao parar com os combos das abas Coração e Olhos
    (`_canais_escolhidos_na_tela`); o PDF de ECG usa esse canal ("canal
    escolhido na tela") e, sem ele, o critério antigo impresso com a verdade
    ("o único canal marcado como ECG", "entre os N marcados, o de ritmo mais
    regular (a tela não guardou a escolha)", "nenhum canal marcado…"); o de
    EOG usa os canais V/H da tela antes do nome e do sinal. As piscadas e a
    taxa por minuto da aba Olhos zeram ao INICIAR a gravação (`_eog_reset`
    em `_start_recording`; antes só ao conectar), então a tela e o PDF contam
    o mesmo trecho. O EMG desenha os eventos marcados ("Marcar evento") como
    linhas tracejadas nas figuras temporais (`_pdf_marcadores`, também no
    traçado dos 10 s das outras modalidades). No Simples o ECG traz
    "Batimentos por minuto ao longo da gravação" com a faixa 60 a 100 no
    lugar do tacograma RR e sem Poincaré (os dois seguem no Completo).
  - **Nomes de canal pelo tipo (G13)** no Tempo Real, no Offline e no PDF:
    `nome_canal_por_tipo`/`rotulos_canais_por_tipo` (a regra que só o PDF
    tinha) dão "CH2 Bíceps Braquial", "EMG CH3", "ECG CH6" (no Simples "CH3
    músculo", "CH6 coração", "CH7 olhos"); o Empilhado refaz os nomes ao
    trocar tipo ou músculo; o Offline lê `channel_types`/`channel_muscles`
    do `summary.json` da gravação e esconde a sub-aba "Bandas EEG" quando a
    gravação não é de EEG nem Multimodal (`_offline_mostra_bandas`). O
    cabeçalho do `data.csv` NÃO muda (registrado em `FORMATO_DADOS.md`).
  - **Página sem grandes vazios**: as figuras de baixo saem no tamanho real
    e, quando cabe, uma embaixo da outra na largura que sobra
    (`_EscritorPdf`, cursor de página com quebra automática e rodapé em toda
    página); títulos das figuras em palavras ("Ritmos do sinal", "Força de
    cada ritmo em cada canal", "Batimentos por minuto ao longo da gravação").
    Rodapé "Gerado pelo ROA v1.9.0 em <data>. Não é laudo nem diagnóstico.";
    a URL do código vai para os metadados do PDF (título, autor, assunto e
    palavras-chave) e, no Completo, também para o rodapé. Tarja "SINAL DE
    TREINO" (Simples) / "SINAL SINTÉTICO" (Completo) traduzida.
  - A pergunta do relatório sem `summary.json` diz "vai sair como
    \"Paciente: não informado\"" (Completo: "Voluntário") em vez de "O campo
    Sujeito"; a chave antiga e mais 4 do PDF antigo saíram dos 8 dicionários;
    153 frases novas traduzidas em en/es/it/fr/de/ja/zh/ru (lote `leigo_c`).
  - Gravações antigas (com `report.pdf`, sem `report_channels`) continuam
    abrindo; nenhuma chave do `summary.json` foi removida ou renomeada.
- **Validação de uso com leigos (27/09/2026), etapa b2: avisos e visual.**
  - **Aviso "Nenhum aparelho encontrado" com jargão e três botões iguais**
    (G33): dizia "Ligue a placa, conecte o cabo USB (ou o dongle)" e os três
    botões da tela inicial saíam azuis, idênticos. Agora (`_caixa_sem_aparelho`)
    a frase curta vem seguida de "O que fazer" em três passos (ligar o
    aparelho e ver a luz, encaixar o cabo USB ou o receptor sem fio, esperar
    5 segundos), "Tentar de novo" é o único botão cheio e o padrão, "Treino
    (sem aparelho)" e "Cancelar" ficam em contorno (repolidos com `#ghostBtn`)
    e Cancelar é a recusa do X e do Esc. Título "Novo exame".
  - **Multimodal com 8 canais gravava só EEG sem avisar** (G11): a divisão
    fixa 1-8 EEG / 9-12 EMG / 13-14 ECG / 15-16 EoG deixava os 8 canais da
    placa base todos em EEG. `layout_multimodal(n)` divide pelo número de
    canais em uso (8: 1-3 cérebro, 4-5 músculos, 6 coração, 7-8 olhos; 16 ou
    mais: a divisão de antes) e é usada por `apply_launcher_choice`; no
    diálogo "Trocar" da tela inicial, marcar Multimodal sobe o combo para 16
    sozinho e uma nota explica a divisão do número escolhido (8 continua
    possível). Na janela, faixa âmbar persistente no Simples
    (`_build_aviso_multimodal`) quando o exame é Multimodal e todos os canais
    em uso estão em EEG, com o botão "Marcar músculos, coração e olhos"; a
    mesma oferta aparece ao escolher Multimodal de novo pelo distintivo
    (`_oferecer_canais_do_exame("Hibrido")`, que grava direto pelo handler e
    sincroniza os combos em silêncio).
  - **Treino mostrava "● CONECTADO" em verde e três selos** (G16): no Simples
    a pílula de conexão vira "● TREINO — sem aparelho" em âmbar (dica: sinal
    de exemplo gerado pelo programa), a pílula de sinal diz "✓ Sinal de
    treino", o selo "MODO SIMULAÇÃO" some (fundido na pílula) e o rodapé diz
    "Treino (sem aparelho): o sinal é de exemplo, gerado pelo programa.". No
    Completo continua tudo como na 1.8.4 (CONECTADO, MODO SIMULAÇÃO, Sinal OK).
  - **Pílula "Sinal OK" igual à de conexão e sem explicação** (G17): no
    Simples ela tem forma própria (borda tracejada de 2 px, `_estilo_pilula(…,
    tracejada=True)`) e ícone ✓; o contraste medido do texto sobre a tinta é
    4,88:1 (ok), 4,59:1 (aviso) e 4,53:1 (erro), conferido no teste. As dicas
    passam a dizer a ação e os canais: "Sinal com ruído em CH2 (Fp2). Peça
    para a pessoa relaxar e ficar parada, confira se o eletrodo está bem
    encostado e afaste os cabos da tomada…", "Sinal ruim em CH5 (P7): eletrodo
    solto, sem contato ou saturado. Recoloque o eletrodo…", e no verde
    "Eletrodos com bom contato nos N canais em uso.".
  - **"● REC" pequeno e aviso de treino só no rodapé** (G19): no Simples o
    indicador de gravação é a pílula vermelha "● GRAVANDO", do tamanho das
    outras (`_pinta_rec`); no Completo continua "● REC". O aviso de treino
    saiu do rodapé para a pílula do cabeçalho (G16) e o tamanho da letra
    100/125/150% está em Adicionado.
  - **Assistente de boas-vindas: caixinha do termo quase invisível, termo sem
    resumo e em fonte monoespaçada** (G26): as caixas do assistente têm borda
    de 2 px na cor do texto e fundo branco (marcada, o azul do tema;
    `FirstRunWizard._qss_caixas`), um resumo de quatro frases em palavras
    comuns fica acima do termo ("não é um dispositivo médico, não faz
    diagnóstico e o relatório não é laudo…"), a dica "◀ Marque esta caixa
    para continuar" explica o Concluir apagado e some ao marcar, e o termo
    abre em fonte proporcional (a folha do app põe monoespaçada em todo
    `QTextEdit`).
  - Chaves órfãs apagadas dos 8 dicionários: a frase antiga do aviso sem
    aparelho, "Treinar sem o aparelho (simulação)" e as duas dicas curtas do
    semáforo; 27 frases novas traduzidas em en/es/it/fr/de/ja/zh/ru (lote
    `leigo_b2`).
- **Validação de uso com leigos (27/09/2026), etapa b1: fluxo do exame.**
  - **"Passo x de 3" seguia a aba, não o que a pessoa já fez** (G05): parar
    a gravação com o aparelho ligado deixava "Passo 2 de 3", gerar o PDF não
    mudava nada e, com a gravação carregada, clicar em Sistema voltava ao
    passo 1. A dica da barra (`_atualizar_dica_contextual`) segue a ordem
    gravando > relatório gerado > gravação recém-parada > gravação carregada
    > conectado, sem depender da aba: depois de Parar é "Passo 3 de 3 ·
    Gerar o relatório" mesmo conectado; depois do PDF, "Pronto · relatório
    gerado" com o botão "Abrir relatório"; o passo 2 volta ao clicar em
    Iniciar Gravação; em Analisar sem gravação carregada, "Escolha uma
    gravação na lista" em vez de "Conectar o aparelho".
  - **Relatório `report.pdf` sem botão para abrir e gravado por cima do
    anterior** (G06/K5): o arquivo chama-se
    `Relatorio_<exame>_<paciente>_<data da gravação>.pdf` (sem acento nem
    espaço; `_2`, `_3`… se já existir; `_nome_arquivo_relatorio`) e a caixa
    final tem "Abrir relatório" como botão padrão (abre o PDF no leitor do
    sistema) e "Abrir pasta" secundário (`_caixa_abrir_pasta(arquivo=)`). A
    demo de 30 s, a dica do botão do Offline, o texto do E118 e ERROS.md
    acompanham; um `report.pdf` antigo continua onde está.
  - **Gravar sem paciente** (G25): no Simples, com o aparelho real e nenhum
    paciente em uso, Iniciar Gravação pergunta "De quem é este exame?"
    (lista de pacientes, "+ Novo", "Gravar para este paciente", "Gravar sem
    paciente", Cancelar). O treino sem aparelho grava como `treino_<data>`
    em vez de `voluntario_<data>` (no Completo, `simulacao_`). A caixa ao
    parar chama-se "Gravação salva" no Simples e diz "Salva na pasta de
    Maria Teste, 27/09 às 10:15." (o caminho inteiro fica na dica de
    ferramenta e em "Abrir pasta"); no Completo continua "Sessão gravada"
    com o caminho.
  - **Exame trocado na tela inicial não ficava guardado** (G02): o diálogo
    "Trocar" grava `acquisition_mode` e o número de canais
    (`config.launcher_channels`, chave nova com padrão 8) ao clicar OK;
    antes só o botão "Completo" salvava e quem clicava Sair reabria em EEG.
  - **Sem Sair nem Início na tela do exame** (G18): menu "Arquivo" com
    "Voltar ao início (trocar paciente ou exame)" e "Sair" (Ctrl+Q). Voltar
    ao início para a gravação (com confirmação), desconecta, reabre a tela
    inicial e aplica a escolha nova na mesma janela; "Sair" lá fecha o
    programa. No Simples há também o botão "⌂ Início" no canto da barra de
    ação. O `QShortcut` Ctrl+Q antigo saiu (repetido com o item do menu, o
    atalho ficaria ambíguo e nenhum dos dois responderia).
  - **Sistema mostrava "voluntario" como nome da próxima gravação** (G04):
    a prévia usa o mesmo nome que a gravação recebe, com o prefixo VID
    (`_nome_pasta_proxima_gravacao`), e é recalculada ao trocar de paciente
    e ao conectar; no Simples o campo "Nome do sujeito/participante" fica
    oculto (o paciente vem do cadastro).
  - **Com uma gravação só, "Carregar selecionada" exigia escolher antes**
    (G24): a linha mais recente já vem marcada ao preencher a lista, o botão
    sem seleção usa a primeira e a caixa de lista vazia chama-se "Abrir
    gravação" (era "Offline").
  - **Analisar mostrava gravações de outro paciente e o topo não dizia de
    quem era a aberta** (G03): com paciente em uso a lista traz só as
    gravações dele (a varredura fica guardada em `_offline_sessoes_todas` e
    a troca de paciente só refiltra), com a caixa "Mostrar de todos os
    pacientes"; ao abrir uma gravação de outro paciente cadastrado, o selo
    do topo vira "Gravação aberta: V02 Pedro Teste" em cor de aviso e
    aparece o botão "Usar este paciente" (no Completo, "Gravação de:" e
    "Usar este voluntário"). `data.csv` e `summary.json` não mudaram.
  - Lote de tradução `leigo_b1`: 40 frases novas nos oito idiomas; três
    chaves órfãs apagadas (dica e demo com `report.pdf`, texto antigo do
    E118).
- **Validação de uso com leigos (27/09/2026), etapa a: base e textos gerais.**
  Quatro pessoas simuladas (fisioterapeuta, estudante, aposentado e
  recepcionista de clínica) operaram o programa real tela a tela; os achados
  confirmados estão em `docs/VALIDACAO_USO_LEIGO_ROA_1.9.0.pdf`. Nesta etapa:
  - **Botões padrão do Qt saíam em inglês** ("Cancel", "Ignore", "Yes", "No")
    no meio de mensagens em português, inclusive no cadastro de paciente da
    tela inicial (K2/G23). O `main()` passa a instalar o `QTranslator` do
    próprio Qt (`qtbase_pt_BR.qm` e o dos outros oito idiomas,
    `instala_tradutor_qt`) logo depois de criar a aplicação e de novo a cada
    troca de idioma. Quando o `.qm` não vem junto (o `.exe` sem a pasta
    `PySide6/translations`), uma reserva em Python traduz os botões padrão
    por `tr()`. `traduz_botoes()` cobre caixas montadas à mão e
    `pede_texto()` substitui os seis `QInputDialog.getText` (renomear
    eletrodo, cadastro da tela inicial, nome de protocolo e de receita), que
    não deixavam trocar o "Cancel".
  - **Janela principal abria em 1600x980 e passava da tela de notebook**
    (G20/K1): em 1366x768 com a barra de tarefas sobram ~690 px de altura,
    menos que o mínimo de 720. O tamanho agora sai da área útil da tela
    (`geometria_inicial`), o mínimo passa a 1100x640, em telas de até 1440
    px de largura a janela abre maximizada, e posição e tamanho ao fechar
    ficam em `config.window_geometry`/`window_maximized`, restaurados só se
    couberem na tela atual (`geometria_cabe`).
  - **Números ora com ponto, ora com vírgula na mesma tela** (G27): o helper
    `num_loc(x, casas, formato, sinal)` (`num_pt` é o mesmo) formata pelo
    `QLocale` do idioma da interface, sem separador de milhar. Já vale no
    resumo e na tabela da Evolução e nos rótulos da aba Olhos (PERCLOS,
    fixação, k/b).
  - **"ROA — Launcher" e "Edição Pesquisa" no modo simples** (K6/G31): a tela
    inicial se chama "ROA — Início"; no Simples o título da janela é
    "ROA v1.9.0" (com "[CONECTADO]", "[GRAVANDO]" ou "[TREINO — sem
    aparelho]") e a edição só aparece no Completo. O título acompanha a
    troca de nível. "EoG · Olhos" virou "EOG · Olhos" nos rótulos visíveis
    (as chaves internas continuam `EoG`).
  - **O modo tinha três nomes e o item do menu ficava com a marca trocada**
    (G29/G30): "Modo completo", "Avançado (pesquisa)" e "Detalhe desta aba"
    eram a mesma coisa, e no completo o menu mostrava "✓ Modo simples
    (exame)". Os níveis se chamam "Simples (exame)" e "Completo (pesquisa)"
    em todo lugar (menu Ajuda, seletor Exibição, tela inicial, assistente de
    primeiro uso, paleta de comandos); o item do menu deixou de ser marcável
    e diz para onde leva ("Mudar para Completo (pesquisa)" / "Voltar para
    Simples (exame)"). Os seletores "Detalhe desta aba" das abas Músculos,
    Coração e Olhos ficam ocultos no Simples.
  - **Sobre e Atalhos descreviam outro programa** (G39): no Simples o Sobre
    tem três frases comuns e o aviso "não é um dispositivo médico e não faz
    diagnóstico"; no Completo a lista técnica foi atualizada (biossinais
    EEG/EMG/ECG/EOG, 8 a 64 canais, BIDS, dois níveis). Os atalhos são
    filtrados pelo nível (no Simples ficam F1, Ctrl+R, Ctrl+Shift+C, Ctrl+Q
    e M).
  - **A mesma pessoa era voluntário, paciente e sujeito** (K3/G27): no Simples
    é "paciente" na tela inicial ("Ana Teste (código V01)", "Novo exame",
    "Treino (sem aparelho)"), no cadastro "+ Novo" ("Cadastrar novo
    paciente" / "Nome do paciente:"), na dica da pílula e em Configurar >
    Pacientes (cabeçalho, botões "Novo paciente" e "Excluir paciente",
    coluna "Gravações", histórico e confirmação de exclusão). No Completo
    continuam os termos de pesquisa. Nada mudou nos arquivos gravados, nas
    colunas do `data.csv` nem nas chaves do `summary.json`. As 44 frases
    novas foram traduzidas nos oito idiomas (lote `leigo_a`) e 11 chaves que
    ficaram órfãs saíram dos dicionários.
- **PDF de EoG sem o filtro do exame contava 2 piscadas (3,9/min) de ~10.**
  O detector media a piscada contra a mediana da gravação inteira, e os
  degraus do olhar vertical (±30 a ±130 µV) entravam na escala: o limiar
  subia a ~240 µV, a altura da própria piscada. Agora a linha de base é
  local (`eog_linha_base`: mediana de meia janela antes e de meia janela
  depois de cada ponto, escolhida pela mediana curta em volta dele), e o
  evento só conta se sobe a partir do nível de antes dele, volta ao nível
  de onde saiu (a sacada não volta) e fica perto da base também em relação
  à própria altura. Só a sobra do MESMO lado do evento conta como "não
  voltou": o vale que o passa-altas deixa depois da piscada fica do lado
  oposto e não a reprova, e um evento do lado oposto à polaridade das
  piscadas do canal, menor que metade da altura delas, é esse vale e não
  outra piscada. Em 24 simulações de 60 s o detector acha 407 de 409
  piscadas sem filtro, com 0 a mais (antes, 174 com 139 a mais), e 394 com
  o filtro do exame, com 15 a mais (antes, 327 com 173 a mais: o
  passa-altas faz de cada degrau uma cauda que passava do limiar). Piscadas
  duplas (a 2a 0,4 a 0,7 s depois da 1a) com o filtro do exame: 240 de 240
  em 12 casos (numa versão intermediária desta correção, 148); o olhar que
  vai a outra altura e volta em 0,6 a 2 s não vira mais piscada (numa versão
  intermediária, 16 a 19 de 19). Vale para o PDF e para taxa, duração e AVR
  (esta medida contra o nível do início de cada piscada), sem depender de o
  filtro estar ligado.
- **PERCLOS de 17 a 24% no PDF de EoG sem nenhuma piscada.** O PERCLOS
  procurava eventos de até 2 s com uma base de 8,8 s, e o olhar vertical
  que vai a outra altura e volta em 1,2 a 2 s contava como olho fechado: a
  linha do PDF dizia "Piscadas=0 taxa=0.0/min" e, ao lado,
  "PERCLOS=23.99%". Agora entram as piscadas normais de 150 ms ou mais e,
  dos fechamentos de 0,5 a 2 s, só os que têm a polaridade e a altura
  (0,6 a 1,6 vez) das piscadas normais do próprio sujeito; com menos de 3
  piscadas não há régua e o PERCLOS sai 0. Sem piscada, 0,00% com e sem
  filtro; com 10 piscadas e 5 fechamentos de 1 s em 60 s, 12,3% (o mesmo
  com o eletrodo invertido).
- **Aba Olhos ao vivo: olhar para cima e ficar contava como piscada e como
  olho fechado.** A mesma base do buffer inteiro: com o olhar 200 µV acima
  por 2,5 a 3 s, 44 "piscadas" de 8 e PERCLOS de 31%. A aba usa agora a
  linha de base local do relatório e só conta pico cujo trecho acima do
  limiar dura ao menos 50 ms (a borda de um degrau deixa um bico de poucas
  amostras): 8 de 8 e PERCLOS de 3%. No EoG simulado sem filtro já contava
  certo (12 de 12 em 40 s) e continua; com o filtro do exame passou de 15
  para 12 de 12.
- **Depois de desconectar, a Topografia, o índice de Foco e a envoltória de
  EMG continuavam recalculados a cada 500 ms sobre o buffer da última
  conexão** (e sobrescreviam qualquer valor posto nas vistas). O cálculo
  para ao desconectar e volta ao conectar; a última imagem fica na tela,
  esmaecida a 40% como o traçado.
- **"Amostras: N" sumia do cabeçalho do avançado durante a gravação em
  EMG, EoG e Multimodal** (em EEG e ECG ficava). Era o cabeçalho responsivo
  escondendo a contagem por falta de espaço: as reservas de largura eram as
  do pior caso absoluto ("Amostras: 99.999.999" e o Δt com "drops: 99999",
  ~170 px a mais). Amostras e Δt passam a reservar a ordem de grandeza atual
  e crescem sozinhos quando o número ganha um dígito (um re-layout por
  dígito, não a cada quadro); ao desconectar voltam à reserva inicial. No
  corte, o Δt sai antes de Amostras, como abaixo de 1500 px. Gravando, com
  5 e 6 dígitos, a contagem fica à vista e sem corte a 1600, 1536 e 1366 px
  nas cinco modalidades.
- **Offline: a coluna "Voluntário" mostrava "—" numa sessão gravada com o
  sujeito digitado e sem voluntário cadastrado.** Mostra o sujeito do
  summary.json, com "(não cadastrado)" quando o nome não está no cadastro, e
  a dica diz que nenhum voluntário cadastrado estava ativo na gravação.
- **Topografia, custo do domo com 64 canais**: 30 ms por quadro de dado novo
  (mediana de 20 rodadas, teto do teste 35 ms), e o teste falhou uma vez com
  a máquina ocupada (38,9 ms). O lugar dos nomes dos eletrodos (busca O(n²)
  em Python) só depende da posição dos discos e agora fica guardado; a
  imagem do domo interpola o campo só nos pixels que aparecem, com índices e
  pesos guardados por ângulo, em float32 (a imagem difere da anterior em no
  máximo 1 nível de cor). Domo de 64 canais: 17,8 ms (antes 30,0); de 8 e
  16: 11,2 e 12,0 ms (antes 17,7 e 19,2); tomografia de 64: 18,2 ms (antes
  22,6). O teto do teste não mudou.
- **EoG e Multimodal simulados acusavam "▲ 1 ruidoso(s)" no modo completo,
  sem filtro.** A simulação estava certa: o canal horizontal de EoG fica com
  o olhar desviado a ±120 ou ±260 µV entre as sacadas (RMS de 174 a 252 µV
  em 38 de 56 janelas de 2 s), e o EMG do Multimodal contrai a 150-176 µV RMS.
  O critério é que lia os dois com o limiar de EEG (150 µV). Agora o limiar é
  o do tipo do canal (ver Alterado); no Multimodal o semáforo chegava a
  "▲ 3 ruidoso(s)".
- **No PDF de EoG os canais "off" entravam no traçado e na contagem de
  qualidade** ("7 OK, 1 ruidosos … de 8 canais", com o canal horizontal como o
  ruidoso). Agora o PDF mostra só os canais em uso ("Canais: 2 de 8"), diz na
  página quais ficaram de fora ("CH3-CH8") e conta "2 OK, 0 ruidosos, 0 ruins
  de 2 canais". Vale para toda modalidade. Com todos os canais "off" o
  relatório mostra todos (não há outros), diz isso na página e dá o veredito
  "SEM CANAIS ATIVOS"; antes a página dizia "fora do relatorio: CH1-CH8" e
  mostrava os oito, com "APTO (0 OK, 0 ruidosos, 0 ruins de 0 canais)".
- **Painel "Piscadas por minuto" do PDF de EoG sem sentido em gravação
  curta.** Numa gravação de 30 s saía uma barra só num eixo de -0,4 a 0,4,
  rotulado "Janela de 60 s". Agora o eixo é o tempo da gravação: janelas de
  60 s quando há ao menos duas, senão de 10 s, cada uma convertida para
  piscadas por minuto, com a faixa normal (8 a 21/min) sombreada; janela final
  com menos da metade da duração fica de fora.
- **PDF de EMG, ECG, EoG e Multimodal rotulava os canais com nomes 10-20 de
  EEG** (Fp1…O2 do mapeamento padrão; no Multimodal, o EMG saía como F3/F4).
  O nome 10-20 só rotula canal de EEG. Canal de EMG sai com o músculo
  escolhido na aba Músculos, que o summary.json passou a gravar
  (`hardware.channel_muscles`), por exemplo "CH1 Bíceps Braquial". O canal
  vem na frente porque o rótulo é cortado na figura (22 caracteres) e no
  resumo (24), e só o nome do músculo perde o fim ("CH1 Extensor Radial
  Lon."); com o canal no fim o corte o levava embora ("Gastrocnêmio Medial
  (C", "Extensor R"), e numa coleta bilateral os dois bíceps saíam como duas
  linhas "Bíceps Bra" iguais. Sem
  músculo, e nos canais de ECG e EoG, sai o tipo e o número ("EMG CH2",
  "ECG CH6"). Nome dado pelo usuário (ex.: "EOG_V") fica como está.
- **PDF gerado depois (Offline, sessão antiga) dizia "Sujeito: (nao
  informado - arquivo sem summary.json)" com o summary.json na pasta.** O
  relatório só lia o voluntário cadastrado; o sujeito digitado, que o
  summary.json também guarda (`subject`), só aparecia no PDF da sessão que
  acabara de ser gravada. A linha do cabeçalho do PDF passou a quebrar na
  largura da página, e as linhas do resumo também (com os rótulos novos a
  linha da base do TKEO passava da margem direita).
- **No modo completo, depois de desconectar, o cabeçalho continuava com
  "Amostras: 4.270", os LEDs de canal verdes e o Δt da última conexão.** O
  buffer antigo continua na memória e o timer dos gráficos reescrevia os
  números a cada quadro. Agora Amostras, g, LEDs e Δt voltam ao estado de
  antes de conectar, como o semáforo já fazia, e voltam a contar na próxima
  conexão.
- **A pílula "Paciente: nenhum" ignorava o sujeito digitado para a gravação.**
  Sem voluntário cadastrado ativo, a pílula (simples) e o selo (completo)
  mostram o nome do campo "Nome do sujeito" e a dica diz que é o sujeito
  digitado; sem nenhum dos dois, continua "nenhum". Digitar o nome atualiza
  a pílula na hora. O sujeito de fábrica do config.json ("voluntario"), que
  ninguém digitou, conta como ausente: instalação nova abre com "nenhum"
  traduzido, não com "Patient: voluntario". Ele continua dando nome à pasta
  e indo no summary.json, como antes.
- **Offline no simples numa tela de ~844 pt de altura (1536x864 a 125%): a
  barra de sub-abas de baixo saía cortada e a divisória não se mexia.** Os
  três mínimos (tabela, traçado de 220 px e análises de 150 px) passavam da
  altura do splitter; o QSplitter espremia o quadro do traçado abaixo do
  mínimo dele e a FFT ficava com 103 px. Agora os mínimos saem da altura que
  sobra (também quando o bloco de cima cresce ao carregar uma sessão): as
  análises têm a barra inteira e ao menos 100 px de gráfico, o traçado cede
  de 220 até 160 px para a FFT chegar a ~150 px (abaixo de 160 só se nem a
  barra inteira couber), nenhum painel fica abaixo do mínimo e traçado e
  análises não colapsam ao arrastar. A janela conta como baixa até 880 px
  (antes 800), o que esconde o título e a instrução. No simples, a 844 pt:
  FFT de 153 px e traçado de 209 px (antes 103 e 221, com o quadro 17 px
  abaixo do mínimo); a 790: 147 e 161; a 768: 125 e 161. A divisória sobe e
  desce.
- **Aba Músculos com placa de 8 canais: abaixo de CH8 sobravam os rótulos
  CH9 a CH64 sem linha.** O rótulo CHn do cartão não entrava na lista do que
  some além de `num_channels`.
- **A linha da sessão sumia da lista do Offline a 1366x768**, nos dois níveis.
  A tabela pedia só 45 px (o cabeçalho sozinho tem ~30) e o quadro do traçado
  guardava o mínimo de construção, 220+2+30 px, mesmo depois de a tela baixa
  baixar o traçado para 160: o ganho nunca chegava ao resto. Agora a tabela
  pede cabeçalho + uma linha inteira e o quadro acompanha o mínimo do traçado;
  a 1366x768 a linha aparece (30 px de área útil, antes 8) e a FFT fica com
  área de gráfico.
- **A simulação gravava com bem menos de 250 amostras por segundo.** Com EMG de
  8 canais e a aba Tempo Real aberta, o `data.csv` de 20 s saía com 1.151
  linhas (51 Hz) no modo completo e a 209 Hz no simples, com o cabeçalho em
  "Sinal OK"; no Multimodal de 16 canais, 148 Hz e `sample_rate_ok` falso. O
  sinal simulado novo, maior que a escala padrão de 100 µV, deixava o desenho
  das curvas caro, o gerador ficava sem vez e o marcapasso reancorava
  descartando amostras que nunca chegavam a ser geradas — e a dica de "tela
  atrasada" ainda garantia que nenhuma amostra tinha sido perdida. Agora o
  simulador recupera até 5 s de atraso entregando num bloco só o que já venceu,
  cada amostra com o carimbo do seu prazo; ao conectar em simulação a escala se
  ajusta sozinha também no modo completo; as curvas do Empilhado recortam o que
  está fora da vista, como as do Individual; o que a reancoragem ainda pular
  entra na contagem de perdas, com dica própria de simulação; e a dica de tela
  atrasada só afirma arquivo completo quando a taxa efetiva bate com a nominal.
  Medido nos três casos, inclusive com a escala forçada em 100 µV: 250 Hz, sem
  perda.
- **O contador de perdas da placa contava bytes, não pacotes.** Um byte fora de
  sincronia virava cerca de 32 "perdas"; a resposta de texto da Daisy ao
  comando "C" chegava depois da limpeza do buffer e acendia "drops" vermelho em
  toda conexão; e um 0xA0 no meio do dado podia forjar um salto de até 255
  amostras no `dropped_samples` do `summary.json`. Agora o leitor ressincroniza
  sem contar byte, só aceita o realinhamento com dois pacotes válidos seguidos
  (byte de parada 0xC0–0xC6 conferido), conta pelo salto do número de amostra,
  divide por dois na Daisy (dois pacotes por amostra) e descarta a resposta da
  placa antes de iniciar. Em fluxo sintético: 20 bytes de texto no meio dão 0
  perdas (antes 20) e um pacote truncado dá 1 (antes 17).
- **A taxa de piscadas saía subestimada por 60 s depois do Reset da aba
  Olhos.** A janela da taxa passou a vir do total de amostras, que o Reset não
  zera. Com 17 piscadas/min reais a tela mostrava 4 aos 12 s, 7 aos 25 s e 13
  aos 45 s, e o histórico começava deslocado no eixo do tempo. O Reset (e a
  troca de canal) agora guarda a amostra de referência; aos 25 s a taxa já sai
  na faixa certa.
- **O filtro automático do modo simples cortava EMG e ECG no Multimodal.** O
  tipo majoritário era contado nas 64 posições, que o launcher completa com
  "EEG": ligava 0,5–70 Hz na cadeia de filtros, que é global, e o `data.csv`
  gravava o EMG sem a banda de 70–125 Hz e o ECG sem 70–100 Hz. Agora conta só
  os canais em uso e, com tipos misturados, liga apenas o filtro da rede
  elétrica; o passa-faixa fica a critério do operador.
- **O relatório de ECG podia analisar o canal errado.** Ele ficava com o canal
  em que o detector achava mais batimentos, e o detector normaliza o sinal: com
  um ECG de 70 bpm, um canal de ruído e um desligado no mesmo arquivo, o PDF
  publicava FC 177,5 bpm, SDNN 148,6 ms e pNN50 76%, todos do ruído. Agora usa
  o canal marcado como ECG na gravação; sem marcação, só aceita canal de ritmo
  plausível (RR mediano entre 300 e 2000 ms e variação abaixo de 35%) e fica
  com o mais regular. O resumo diz qual critério escolheu o canal, e sem
  nenhum candidato o relatório sai pelo caminho "nenhum batimento detectado".
- **O relatório de EoG adivinhava qual canal era o vertical.** Sem "vert/horiz"
  nos nomes, tomava o 1º como vertical e o 2º como horizontal — o inverso do
  próprio simulador —, e numa gravação com 17 piscadas imprimia "Piscadas=0"
  ao lado da faixa normal de 8 a 21 por minuto. Agora o que o nome não decide é
  decidido pelo sinal (vertical é o canal com mais piscadas, horizontal o com
  mais sacadas), o resumo diz isso, e sem piscada a linha da faixa normal dá
  lugar a "taxa não interpretável".
- **A barra "%CVM" do relatório de EMG dividia a gravação por ela mesma.** O
  pico do envelope era dividido pela maior média móvel do mesmo envelope, o que
  dá cerca de 125% para qualquer amplitude (de 5 a 900 µV) e afirmava uma
  normalização por contração máxima que não existia. A barra passa a mostrar o
  pico do envelope em µV, e o resumo diz que %CVM exige uma contração
  voluntária máxima medida em ensaio próprio.
- **O detector de ativação de EMG zerava numa gravação que já começa
  contraindo.** O limiar era calibrado nos primeiros 0,5 s do arquivo; se ali
  já havia contração, o PDF dizia "ativacoes=0" e não sombreava nada. Quando o
  começo está acima da mediana do registro, a linha de base passa para o trecho
  mais quieto do arquivo e o resumo registra isso. As 10 contrações do teste
  voltam a ser achadas com 0, 0,2 e 0,4 s de repouso inicial.
- **A inclinação da MDF saía sem incerteza.** Sem fadiga nenhuma a estimativa
  oscila ±0,09 a ±0,15 Hz/s, e metade das gravações imprimia um número
  negativo que a legenda chamava de fadiga. O relatório agora mostra o
  erro-padrão ("-0,04 +/- 0,09 Hz/s") e escreve "não conclusivo" enquanto a
  inclinação não passa de dois erros-padrão.
- **O PDF de uma sessão simulada era igual ao de um exame real**, com nome de
  voluntário e veredito "APTO", embora o `summary.json` já soubesse que o sinal
  era sintético. Agora o PDF traz no topo uma tarja vermelha ("SINAL SINTETICO
  — gerado pelo próprio programa, nenhum eletrodo envolvido") e o rótulo da
  sessão carregada no Offline começa por "SINAL SINTÉTICO" (ou "REPRODUÇÃO"
  para playback).
- **Os avisos do relatório ficavam só na caixa de mensagem.** A caixa some com
  um clique e o PDF, que é o que circula, não dizia nada — o caso mais grave
  era a sessão sem modalidade declarada, que saía com título e figuras de EEG.
  Os avisos agora são impressos no próprio PDF, abaixo do resumo, e o título
  ganha "(modalidade não declarada)".
- **O curso temporal ERD%(t) mostrava −18,6% fixo sem evento nenhum**, inclusive
  antes do aviso. A densidade média na banda dependia da largura que a máscara
  cobria: 6,0 Hz na janela de 0,5 s contra 4,9 Hz no repouso. Agora a
  referência é fatiada em janelas do mesmo comprimento das de análise e o Welch
  usa nfft fixo de 256, de modo que os dois lados pegam os mesmos bins. Em 6
  sinais sintéticos sem efeito, a média do curso passou de −22,8% para −1,5%;
  com ERD injetado de −50%, sai −50%. `compute_band_power` ganhou o mesmo nfft
  (em ruído branco, janela de 0,5 s contra 3 s: de +24,9% para −0,8%).
- **O mosaico ERSP podia mostrar faixas de ±4,7 dB sem evento.** Com só um
  pre_rest de 3 s como referência cabiam 11 janelas, e o ruído dessa estimativa
  aparecia como faixa horizontal quase do tamanho da escala. Agora a
  referência junta as janelas de todos os trechos de repouso do arquivo (264
  no teste; desvio das médias por frequência de 1,29 para 0,19 dB), e o
  diálogo avisa quando sobram menos de 40 janelas.
- **A tabela de classificadores pintava de verde acurácia compatível com o
  acaso.** O verde começava em 65% fixo, mas o teto de acaso é 68,4% com 20
  tentativas e 76% com 10. Agora verde é acima de max(65%, teto) e amarelo a
  partir do teto; uma linha diz que o teste de permutação vale só para o CSP.
- **A ajuda lia as barras de ERD% ao contrário.** Dizia "barra alta = o ritmo
  caiu = ativação", mas a barra alta (verde) é ERS; a dessincronização é a
  barra para baixo, em vermelho. Corrigido nos nove idiomas.
- **O cartão "SNR SSVEP" oscilava ordens de grandeza sem estímulo.** Média no
  alvo contra mediana no ruído, sobre um único periodograma de 2 s: sem SSVEP
  nenhum a mediana era 1,15 e passava de 4,6 em 5% dos quadros. Agora são
  mediana dos dois lados sobre Welch de ~4 s (três segmentos de 2 s), com uma
  casa decimal: sem estímulo, mediana 0,95 e p95 2,6.
- **Os controles "Isolar mu" do ERS/ERD ficavam debaixo dos botões de
  classificação**, na mesma célula do grid: os dois campos da faixa, "Detectar
  mu individual" e a caixa do Laplaciano não podiam ser clicados em largura
  nenhuma. A linha de classificação foi para uma linha própria.
- **A segunda fila de botões do Offline saía cortada dos dois lados**
  ("statística guiada.", "cada (ligar blocos"). A caixa "Mostrar rótulos dos
  marcadores" foi para a linha de baixo do traçado e só aparece no modo
  completo; o rótulo de estado foi para a primeira fila, sem o caminho da pasta
  (que ficou na dica de ferramenta). A 1366 px os oito botões cabem inteiros.
- **Os avisos de "nenhum canal EMG/ECG/EoG" mandavam a uma aba escondida no
  modo simples** ("marque os canais em Filtros e Canais"). No simples o texto
  agora aponta o distintivo da modalidade, e escolher ali um exame de EMG, ECG
  ou EoG sem nenhum canal daquele tipo oferece marcar os canais na hora.
- **O painel "Log da Sessão" saía em português em qualquer idioma, sem dizer
  por quê**, e no modo simples ocupava a aba Conexão quase inteira. O log
  continua em português de propósito (é o `session.log.txt` que vai para o
  suporte); a dica do painel agora diz isso no idioma da janela e o painel só
  aparece no modo completo. A linha "Modo de aquisição aplicado" deixou de sair
  duas vezes na abertura.
- **O ajuste de tela baixa do Offline olhava o monitor, não a janela.** Num
  monitor de 1080 com a janela em 768 px nada mudava, e trocar de monitor não
  reavaliava. Agora decide pela altura da janela, com histerese, a cada
  redimensionamento.
- **A Topografia ao vivo passava 34 px da tela a 1366x768** e escondia O1, O2 e
  a barra de cor com os rótulos novos "baixo · / alto ·". O mapa agora fica
  numa área de rolagem, como o do Offline.
- **O diálogo "Grupos de tamanhos diferentes" ficava em português em todos os
  idiomas**: era o único `tr(f"…")` do arquivo, e a chave já saía formatada. Os
  números agora são formatados depois do `tr()`, e o `varre_sem_tr.py` passou a
  acusar `tr()` com f-string.
- **No rodapé do Tempo Real as marcas do eixo do acelerômetro saíam umas sobre
  as outras** (com o Z em 1 g havia três marcas em ~35 px) e a legenda X/Y/Z
  saía cortada ou sumia. As marcas agora são de 1 em 1 g e a legenda foi para o
  título do painel.
- **As curvas do histórico do Focus atravessavam a legenda.** A legenda saiu da
  área de dados e foi para o título do gráfico.
- **Dois combos "Exibição:" iguais na mesma tela.** O da aba agora se chama
  "Detalhe desta aba:" e as dicas dizem qual vale para o programa inteiro e
  qual muda só aquela aba.
- **A barra de sub-abas de um grupo ainda não aberto guardava o arranjo do modo
  anterior.** Trocar EEG → EMG → EEG antes de abrir Analisar deixava a aba
  "Análises" invisível, sob "Offline". A barra agora refaz o arranjo a cada
  troca de modo.
- **Relatório PDF da sessão agora descreve o exame que foi gravado.** Para EMG,
  ECG e EoG o PDF trazia o conteúdo de EEG — série temporal, espectro com as
  faixas delta a gama e o mapa canal × banda —, de modo que quem gravava
  músculo recebia um mapa de bandas de EEG sem sentido físico e quem gravava
  coração recebia o "espectro médio" de um QRS. Só o título e o campo Sujeito
  mudavam. Agora cada modalidade tem as suas figuras e o seu resumo em números:
  EMG sai com o sinal e as ativações detectadas por TKEO sombreadas, o envelope
  linear da SENIAM por canal e barras de RMS e de pico do envelope em µV, mais RMS, pico
  do envelope, número de ativações e inclinação da MDF por canal; ECG sai com o
  traçado e os picos R marcados, o tacograma RR e o gráfico de Poincaré, mais
  FC média, RR médio, SDNN, RMSSD e pNN50; EoG sai com as piscadas marcadas, o
  canal horizontal com as sacadas e as piscadas por minuto, mais taxa por
  minuto, PERCLOS, total de sacadas e amplitude mediana. Sessão sem
  modalidade declarada continua no formato de EEG, agora com um aviso dizendo
  isso; a Multimodal sai com uma página por modalidade (ver a entrada
  seguinte). Quando nada é detectado (gravação ruim, eletrodo solto) a figura sai
  escrita "nenhum batimento detectado" em vez de o PDF morrer com o erro E118.
- **O título da figura do PDF dizia "Sinal EEG" mesmo quando o cabeçalho da
  página já dizia ECG.** Agora a figura leva a modalidade da própria sessão.
- **O "espectro médio" do PDF era, na verdade, dos últimos 4 segundos da
  gravação.** Uma FFT de 4 s sobre o fim do registro — numa sessão de 17 min,
  0,4% dela, justamente quando o eletrodo já está sendo retirado — aparecia sob
  o rótulo "Espectro médio (FFT) — todos os canais". Agora é uma PSD de Welch
  sobre a **gravação inteira**, com o eixo em µV²/Hz. Os números do gráfico
  mudam em relação às versões anteriores.
- **As faixas das bandas no espectro do PDF saíam todas na mesma cor**, um
  retângulo azul único de 0,5 a 50 Hz que não separava banda nenhuma. Agora
  cada faixa usa a cor da sua banda (a mesma das barras na tela) e leva o nome
  escrito acima.
- **O PDF carimbava no campo Sujeito o nome que estivesse na configuração
  atual.** Numa pasta sem `summary.json` — que é o caso de todo arquivo aberto
  por "Abrir CSV…", "Abrir EDF/BDF…", "iCelera Nano…" e "Importar arquivos…" —
  o relatório de um exame de outra pessoa saía com o nome do sujeito
  configurado na máquina. Agora, fora da sessão que está sendo gravada naquele
  momento, o campo sai como "(nao informado - arquivo sem summary.json)" mais a
  linha "Origem:" com o arquivo de verdade, e o programa avisa antes de gerar.
- **A exportação para FIF gravava em silêncio a taxa medida pelos carimbos de
  tempo.** Quando faltavam amostras, justapor as sobreviventes encolhe o eixo
  do tempo: numa perda de 20% concentrada num trecho, um sinal de 10,0 Hz era
  lido no MNE como 8,0 Hz, e toda frequência saía deslocada na mesma proporção.
  Agora, quando o desvio passa de 0,5%, cada amostra volta ao índice que o
  carimbo dela manda, vãos de até 5 amostras são interpolados, vãos maiores
  viram anotações `BAD_lacuna` (que o MNE já respeita), os marcadores
  acompanham a amostra a que pertencem e o arquivo fica na taxa nominal. O
  programa diz quantas amostras faltaram e quanto tempo foi marcado como
  lacuna. Sem a coluna de tempo para reconstruir, ao menos pergunta antes de
  gravar em vez de exportar calado.
- **O script `analyze_mne.py` parava no meio em toda sessão com marcador.** Com
  o MNE 1.7 ou mais novo, `power_tf.plot()` devolve uma lista, e o
  `fig.savefig()` seguinte quebrava com `AttributeError`: não saía nem o
  `tf_channel0.png` nem o `report_mne.html`. Agora o script usa
  `epochs.compute_tfr` quando existe (com o `tfr_morlet` antigo como
  alternativa), aceita a lista, fixa o backend Agg para funcionar em máquina
  sem tela e protege o bloco de tempo-frequência, de modo que uma falha ali não
  impede mais o relatório HTML.
- **A ICA do script `analyze_mne.py` destruía o sinal em montagens de até 15
  canais.** A referência média (CAR) consome um posto, mas a ICA pedia
  `min(15, n_canais)` componentes; com 8 canais a matriz de mistura saía
  singular e o `ica.apply` devolvia ruído numérico — a potência alfa caía de
  7,1e-11 para 7,4e-43 V²/Hz, e a tabela de bandas, as épocas e o "Sinal limpo"
  do relatório eram todos lixo. Agora são `n_canais - 1` componentes.
- **A tabela de potência do script MNE dizia µV²/Hz e imprimia V²/Hz**, um
  fator de 10¹² em todas as bandas. Agora a conversão é feita e o rótulo
  confere.
- **O FIF exportado não levava as posições dos eletrodos.** Sem elas o MNE
  avisava duas vezes que não conseguia desenhar as topografias dos componentes
  da ICA, e o `report_mne.html` saía só com o traçado. Agora a montagem
  `standard_1020` é gravada dentro do arquivo (só em sessões de EEG), o que
  também serve a quem abrir o FIF no Brainstorm, no FieldTrip ou no EEGLAB.
- **Na Evolução do paciente, sessões do mesmo dia ficavam com rótulos iguais no
  eixo.** A data era cortada em 10 caracteres e a hora ia junto: três sessões
  de um mesmo dia viravam três vezes "2026-09-19". Agora o eixo mostra dd/mm e,
  quando todas caem no mesmo dia, dd/mm HH:MM; a coluna Data da tabela abre na
  largura do conteúdo, em vez dos 100 px que cortavam o carimbo.
- **A aba Offline mostrava três nomes diferentes ao mesmo tempo.** Ao abrir um
  arquivo que não se chama `data.csv`, a tabela continuava com outra sessão
  marcada, o rótulo de status trazia o nome da pasta e o que estava carregado
  era um terceiro arquivo. Como o botão de relatório grava `report.pdf` na
  pasta, duas gravações na mesma pasta sobrescreviam o mesmo relatório sem
  aviso. Agora o rótulo é o nome do arquivo aberto, o caminho inteiro fica na
  dica de ferramenta e a seleção da tabela é limpa quando a carga não veio dela.
- **Os rótulos dos marcadores cobriam o traçado no Offline.** Numa gravação com
  200 marcadores havia um a cada 6 px e cada rótulo, de cerca de 40 px, cobria
  outros seis, escritos por cima do canal de índice 1 (o C3 da montagem BCI).
  Agora o rótulo só sai quando cabe, acima do traçado e alternando entre duas
  alturas; o texto de cada marcador continua acessível na dica de ferramenta da
  linha, e uma caixa "Mostrar rótulos dos marcadores" desliga todos de uma vez.
- **Em tela de 1366x768 as análises do Offline abriam com 27 px úteis.** Os
  mínimos dos três painéis somavam a altura disponível inteira, de modo que
  arrastar a divisória não adiantava nada. Com a janela baixa (menos de 800 px
  de altura) o parágrafo de instrução do topo agora se recolhe e o mínimo do
  traçado cai de 220 para 160 px; as análises abrem com 108 px e a divisória
  volta a funcionar.

- **Simulação passa a gerar cada canal conforme o tipo marcado** (EEG, EMG,
  ECG, EoG e "desligado"). Antes todo canal recebia as mesmas três senoides de
  10, 20 e 6 Hz, mudando só a fase, e o resultado enganava quem treinava sem o
  aparelho: a Topografia usava 4% da escala de cor (e a Tomografia e a CSD,
  derivadas dela, ficavam ainda mais achatadas), a aba Músculos não via
  contração nenhuma (0% das amostras acima do limiar de 50 µV, MDF presa em
  10,00 Hz, "Fadiga: --"), a aba Coração lia as cristas das senoides como picos
  R e anunciava 196 bpm com HRV de aparência clínica, a aba Olhos não via
  piscada nem sacada, o joystick de EMG não saía do centro e a conectividade
  dava a mesma coerência (0,69) em todos os pares. Agora o EEG tem alfa forte
  no occipital e teta no frontal conforme a posição do eletrodo, com
  dessincronização alternando de hemisfério; o EMG tem ciclos de contração de
  4 s com atraso próprio por canal e queda de frequência mediana ao longo do
  tempo; o ECG sai de um complexo PQRST a 70 bpm; o EoG tem piscadas e sacadas;
  o canal marcado "desligado" recebe só ruído; e o acelerômetro alterna repouso
  e movimento. Marcar um canal como EMG durante a simulação passa a valer na
  hora, sem reconectar. Para não deixar dúvida, a aba Bio avisa que o sinal é
  gerado pelo programa.
- **"Perdendo amostras N%" deixou de aparecer com o arquivo íntegro.** O
  cabeçalho media a perda pelo intervalo entre chegadas: como a cadência dispara
  em rajada depois de um atraso do sistema, 60 s de simulação num computador
  ocioso acusavam "■ perdendo amostras 34%" enquanto o `data.csv` saía completo,
  a 248,4 Hz e com o espectro no lugar certo — e a dica ainda dizia, falsamente,
  que o eixo de tempo ficava comprimido. A perda passa a ser contada na fonte,
  pelo número de amostra que a placa manda, e o aviso amarelo de tela que não
  acompanha virou um estado separado ("tela atrasada"), que nem aparece no modo
  simples. O filtro em tempo real também ficou cerca de oito vezes mais barato
  por amostra (os canais são filtrados de uma vez), que era a causa das rajadas.
- **Rótulos do cabeçalho cortados em uso.** Ao trocar de "Sinal OK" para o aviso
  de qualidade, o resumo crescia sem que a barra fosse refeita e o texto saía
  cortado; no modo completo o emblema da modalidade, o selo "MODO SIMULAÇÃO" e o
  resumo apareciam cortados em metade das verificações, mesmo sobrando espaço.
  O cabeçalho agora refaz o arranjo e esconde a telemetria menos crítica só
  quando algum rótulo está de fato cortado. O indicador de tempos deixou de
  mostrar a deriva da cadência no meio do texto (ela foi para a dica de
  ferramenta), o que encurtou a largura reservada e baixou a largura mínima da
  janela.
- **Barra de ação não cresce mais em tela estreita.** Com a frase longa de erro
  de conexão e o botão "Procurar de novo" ao lado, a dica quebrava em cinco
  linhas, a barra ia de 48 para 93 px de altura e o combo "Exibição" perdia
  53 px e saía cortado a 1100 px. A dica agora ocupa no máximo duas linhas, com
  reticências quando não cabe e o texto inteiro na dica de ferramenta, e o
  combo deixou de ceder largura.
- **Contagem de canais EMG e listas de canais não inventam mais canais.**
  O rótulo contava os 64 canais possíveis: numa placa de 8, escolher "exame de
  músculos" na tela inicial fazia a aba dizer "64 canais EMG ativos", e os
  combos de joystick, de ECG e de EoG ofereciam CH1 a CH64 — canal inexistente
  dava traçado zerado sem aviso. Agora tudo é limitado aos canais que a placa
  tem, acompanha a troca de placa e, quando nenhum dos canais em uso está
  marcado como EMG, o rótulo diz onde marcá-los.
- **Fonte dos números volta a alinhar em coluna.** As famílias Inter e
  JetBrains Mono eram pedidas sem alternativa fora da folha de estilo: em
  computador sem elas instaladas a interface inteira caía em Tahoma, inclusive
  a tabela de estatísticas, os valores do mapa de cabeça e os eixos do PDF, que
  precisam de fonte de largura fixa. O programa passa a escolher, ao abrir, a
  primeira família disponível de cada pilha.
- **Marcador de evento agora cai em cima do traçado.** A linha tracejada do
  "Marcar evento" era colocada no tempo contado desde a conexão, enquanto o
  traçado mostra só os últimos segundos: aos 14 s de sessão a linha ia para
  x = 14 s num gráfico que termina em 10 s, ou seja, fora da tela. Na vista
  empilhada era pior: a linha nascia colada na borda direita e ficava parada
  ali enquanto o sinal andava, e os rótulos dos doze últimos marcadores se
  empilhavam todos na mesma altura do canto. Agora a linha nasce no instante
  certo, anda junto com o traçado e sai sozinha pela esquerda quando o evento
  deixa a janela, com os rótulos vizinhos alternando de altura. De quebra, o
  marcador deixou de criar uma linha em cada um dos 64 gráficos possíveis
  (eram 1.920 objetos depois de 30 marcadores) e passa a desenhar só nos
  canais em uso.
- **O controle "Janela:" do Tempo Real passa a valer nas duas vistas.** Ele só
  afetava a vista empilhada; na vista por canal o traçado mostrava sempre os
  10 s inteiros do buffer e mexer no número não mudava nada na tela que o
  pesquisador estava olhando. Atenção: por isso a vista por canal passa a
  abrir com 5 s (o valor do controle) em vez de 10 s. O controle ganhou dica de
  ferramenta.
- **Snapshots automáticos deixaram de mentir.** A pasta `snapshots/` não era
  criada: quando ela não existia, nenhuma imagem era gravada e o log anunciava
  "Snapshot #N salvo em snapshots/" assim mesmo. Agora a pasta é criada, cada
  imagem é conferida e o log diz quantas saíram ("Snapshot #N (motivo): 7/7
  imagens em snapshots/"), com uma segunda linha em vermelho nomeando o que a
  gravação recusou. Painel que não está montado na tela sai da conta em vez de
  virar erro. Além disso, as imagens de FFT, bandas e estatísticas saíam com o
  tamanho de construção (264×197 px, com duas das oito linhas de canal
  visíveis) enquanto a aba Análises não tivesse sido aberta uma vez — e no modo
  simples ela fica escondida, então saíam cortadas a sessão inteira. A aba é
  pré-aquecida ao abrir o programa, sem piscar na tela.
- **Topografia deixou de sair de uma cor só.** As cores eram calculadas
  dividindo cada eletrodo pelo maior valor do quadro: com variação pequena
  entre eletrodos (o caso comum, e sempre o da simulação) todos caíam no topo
  da escala, o mapa saía amarelo por inteiro e a Tomografia mostrava um disco
  liso, sem uma única linha isopotencial. A escala passa a ir do menor ao maior
  valor medido, e as pontas da barra de legenda trazem os dois números, para
  não dar a impressão de contraste onde há pouca variação. A topografia de
  ERD% continua ancorada no zero, onde o zero quer dizer "sem
  dessincronização".
- **Nome do eletrodo legível em qualquer cor do mapa.** Ele era escrito sempre
  em preto sobre o disco colorido: na faixa escura da escala o contraste caía a
  1,4:1 (o mínimo aceitável é 4,5:1) e o rótulo praticamente sumia, no mapa 2D
  e no domo 3D. O nome e a borda do disco passam a sair em preto ou branco
  conforme o fundo, e o valor numérico, que fica fora do disco, ganhou uma
  tarja atrás.
- **O domo 3D passa a girar de verdade.** Arrastar na horizontal mudava o
  desenho mas não a profundidade: os mesmos quatro eletrodos (P7, P8, O1, O2 na
  montagem de 8 canais) ficavam escondidos em qualquer ângulo e a nuca nunca
  vinha para a frente. A ordem das rotações foi corrigida e a inclinação
  inicial baixou de 54° para 34°, o que já mostra os oito eletrodos de cara. A
  legenda de baixo agora explica o que cada direção do arrasto faz.
- **A Tomografia mostra os eletrodos.** A vista desenhava o campo posterizado,
  os contornos e os anéis de referência, mas nenhum eletrodo — o operador não
  tinha como saber onde estavam os canais na fatia. Eles aparecem com nome e
  com o tom da camada em que estão, e somem quando o controle de profundidade
  os deixa fora da fatia.
- **Mapa de cabeça não fica mais cortado nos painéis.** O widget exigia 420×420
  px: num painel do Layout Custom, que dá 265 px de altura, 155 px ficavam de
  fora e sumiam a parte de baixo da cabeça (O1/O2) e a barra de cores inteira.
  O mínimo caiu para 260×240, onde o desenho inteiro cabe; a aba Topografia
  continua com o tamanho generoso de antes.
- **Legenda do Histórico não cobre mais o traçado.** As 64 curvas possíveis
  eram registradas na legenda e as desligadas continuavam listadas com o ícone
  de olho riscado: a legenda ficava com 1.362 px de altura num gráfico de
  389 px e transbordava por cima e por baixo. Agora ela lista só os canais em
  uso e em quatro colunas.
- **Fadiga do EMG parava de inventar pontos com a tela parada.** A cadência dos
  cálculos de MDF/MNF, do atlas e do espectrograma vinha de um resto de
  divisão do contador de amostras: com a aquisição encerrada o contador
  congela e, se parasse num múltiplo, cada atualização de tela recalculava o
  mesmo espectro e empilhava o mesmo valor no histórico. Em 41 s de tela parada
  os 600 pontos do histórico viravam todos iguais, empurrando a contração real
  para fora e deixando a reta de tendência plana. A cadência passa a exigir
  sinal novo.
- **Gráficos de Focus e do joystick de EMG cobrem o tempo que anunciam.** Os
  títulos prometiam "últimos ~60 s" e "últimos ~30 s", mas o histórico era
  podado por número de pontos supondo uma cadência que não existe: na prática o
  Focus mostrava de 12 a 16 s e o joystick de 36 a 40 s, e a janela mudava
  conforme a carga do computador. A poda passa a ser pelo relógio.
- **Piscadas e sacadas deixaram de ser contadas mais de uma vez.** A aba Olhos
  marcava cada evento pelo relógio do computador, supondo que a última amostra
  do traçado tinha acabado de chegar. Como a tela é redesenhada numa cadência
  própria, o atraso entre as duas coisas variava de 10 a 400 ms, e em 27% dos
  quadros a mesma piscada mudava de instante o bastante para ser recontada:
  numa medida com 11 piscadas reais a tela mostrava 22, com "45 piscadas/min"
  onde havia 24, e as sacadas iam de 15 para 43. Os triângulos também caíam na
  subida ou na descida da piscada em vez do pico, e os losangos das sacadas
  antigas se empilhavam na borda direita do gráfico, sobre trechos sem
  movimento nenhum. Tudo passa a ser marcado pelo número da amostra, que não
  depende do relógio. Dois efeitos a notar: a taxa exibida agora é por minuto
  de sinal recebido (está dito na dica de ferramenta) e, com a aquisição
  parada, ela congela no último valor em vez de cair sozinha; e o aviso de
  microssono, que ficava aceso para sempre depois do primeiro disparo, volta a
  apagar depois de 2 s.
- **Contadores da aba Olhos zeram ao conectar de novo.** Piscadas, sacadas,
  PERCLOS e o histórico de taxa continuavam somando os da sessão anterior.
- **Alvo do olhar não escapa mais do círculo.** O ponto e o rastro eram presos
  a um quadrado, não ao disco desenhado: num olhar na diagonal eles ficavam até
  41% para fora da borda. Agora o olhar extremo encosta na borda e a direção,
  que é o que se lê, fica preservada.
- **Eixos do coração e da taxa de piscadas em "kms" e "mmin".** Com intervalo
  RR acima de 1000 ms, o gráfico de Poincaré escrevia "RR(n) (kms)" num eixo e
  "RR(n+1) (ms)" no outro — unidades diferentes num gráfico cujo sentido
  inteiro é comparar os dois eixos na mesma escala. O mesmo acontecia com o
  tacograma, com o histograma de RR e, numa sessão de 30 s, com o eixo de tempo
  da taxa de piscadas ("mmin", com marcas em 200, 400 e 600).
- **Título do Atlas Muscular aparecia como "Atlas Muscular _Posicionamento".**
  O "&" do texto era lido pelo Qt como marca de atalho de teclado: ele sumia e
  o espaço seguinte saía sublinhado, nos nove idiomas.
- **Coluna "Qualidade média" cortada no histórico de montagens.** As colunas
  nasciam com 100 px fixos e o cabeçalho pedia 123 px ("ualidade médi"). Agora
  cada uma pega a largura do seu conteúdo e a primeira absorve a sobra.
- **Aba Músculos e "Filtros e Canais" não rolam mais para o lado.** As duas
  grades eram montadas para 64 canais, em oito blocos lado a lado, e os blocos
  vazios continuavam ocupando espaço mesmo numa placa de 8: a grade de
  mapeamento muscular pedia 4067 px de largura e a aba ficava com 2529 px de
  rolagem horizontal. Os blocos sem canal em uso agora somem (a mesma grade
  pede 769 px com 8 canais) e voltam ao escolher 16, 32 ou 64. De quebra, os
  blocos do terceiro em diante, que nunca tiveram cabeçalho, ganharam o seu.
- **Coluna "Eletrodo" da aba Músculos anunciava eletrodos de couro cabeludo.**
  Numa coleta de EMG ela mostrava Fp1, Fp2, C3... que não existem no protocolo,
  e o eletrodo que o operador acabou de posicionar no Atlas não aparecia em
  lugar nenhum da linha do canal. A coluna passa a se chamar
  "Eletrodo / músculo" e, nos canais marcados como EMG, mostra o eletrodo do
  Atlas e o músculo escolhido, atualizando na hora em que qualquer um dos dois
  muda. Os cabeçalhos "Tipo" e "Eletrodo" também ficavam em português nos
  outros oito idiomas.
- **Legenda de qualidade do Atlas tinha duas caixas da mesma cor.** "média" e
  "boa" saíam ambas em mostarda e o laranja, que é a cor do anel quando o
  contato está ruim, não aparecia na legenda. As quatro caixas passam a mostrar
  as quatro faixas reais. Na imagem exportada, o subtítulo também saía metade
  fora da tarja de fundo.
- **Linha de referência achatava o gráfico de fadiga muscular.** A linha
  tracejada do início da sessão ficava parada em 0 Hz até haver medida, e o
  eixo se esticava para acomodá-la: com o MDF entre 77 e 83 Hz, a escala ia de
  -4 a 87 Hz e a variação, que é o assunto do painel, virava uma reta. A linha
  só aparece depois de calibrada e não puxa mais a escala.
- **Filtro recomendado para EMG dizia "20 Hz - Nyquist" e entregava 120 Hz.**
  O preset pedia 124 Hz, acima do máximo que o controle aceita, e era cortado
  em silêncio — no modo simples ele é aplicado sozinho ao conectar. O preset
  passa a ser 20-120 Hz e o rótulo diz o número real (a diferença de sinal é
  de 0,4% da energia na banda).
- **Mapa de co-contração calibrado por sessão gravada saía em outra escala.**
  A calibração pedia o envelope por "rms" em minúsculas, que não casava com
  nenhum dos métodos e caía no de retificação simples: a nuvem nascia cerca de
  20% abaixo da escala do ponto medido ao vivo, e a janela era fixa em 150 ms
  em vez da configurada. Mapas salvos antes continuam com a escala antiga.
- **Painel de músculos falhava nos primeiros instantes da aquisição.** Enquanto
  chegavam menos amostras do que a janela do envelope (menos de 100 ms, ou
  menos de 300 ms se a janela estiver aumentada), o envelope saía mais longo
  que o próprio traçado e o desenho era recusado com "X and Y arrays must be
  the same shape" no log; o resto do quadro — barras, LEDs, contagem de
  ativações — ficava sem atualizar até o buffer encher.
- **Aba Focus/SSVEP abria num canal que não existe.** Com a placa de 8 canais o
  seletor listava os 64 canais possíveis e vinha marcado no CH20 (Oz), que
  nunca recebe amostra: os quatro cartões ficavam em "0.00", o espectro em
  zero e nada na tela dizia por quê. O seletor passa a listar só os canais
  ativos e a começar no melhor eletrodo disponível para foco e SSVEP (Oz, O1,
  O2, POz, Pz, Cz ou Fz — com 8 canais, O1). Ao mudar o número de canais na aba
  Conexão, a escolha do operador é preservada; se o canal escolhido deixar de
  existir, o programa cai num desses eletrodos em vez de cair em Fp1.
- **Baseline de foco aceitava calibração zerada.** Com o canal mudo (ou com o
  eletrodo solto), os 5 s de calibração terminavam com baseline 0,00 e o
  programa registrava "Baseline definido" no log, mas os cartões continuavam
  mostrando valor absoluto e o Estado dizia "(sem baseline)" para sempre, sem
  explicação. Agora a baseline nula é recusada, o cartão Estado diz "Baseline
  falhou" e uma única caixa explica o motivo — canal sem sinal (nomeando o
  canal) ou métricas nulas com sinal presente.
- **Cartão do SSVEP mostrava quase zero mesmo com o alvo em silêncio.** O SNR
  dividia o pico pela MÉDIA da vizinhança de ruído; como a vizinhança de um
  alvo de 12 Hz inclui 10 Hz, o pico de alfa levantava o piso e o número
  desabava três ordens de grandeza (0,0008 onde a medida honesta é ~0,5). A
  vizinhança passa a ser resumida pela mediana, e quando ela tem menos de três
  raias o cartão mostra "--" em vez de um número inventado. O cartão foi
  renomeado para "SNR SSVEP", que é o que ele mede. Baselines de foco colhidas
  antes desta versão não se comparam com as de agora: recalibre.
- **Gráfico de foco misturava duas unidades no mesmo eixo.** Ao definir a
  baseline, os pontos anteriores à calibração continuavam no gráfico, mas
  passavam a ser divididos por ela — valores medidos antes de existir a
  referência apareciam como múltiplos dela. O histórico passa a ser zerado no
  momento da calibração, e o rótulo do eixo diz qual unidade está na tela
  ("Métrica (bruta)" ou "Métrica (× baseline)").
- **Barra de feedback do BCI escondia o próprio texto.** "← Esquerda | Direita
  →" era escrito dentro da barra, na cor do texto do aplicativo sobre o azul do
  preenchimento (1,9:1 de contraste): a partir de valor −9 o lado esquerdo
  sumia por completo. Os dois rótulos saíram para fora da barra, o trilho ganhou
  uma marca no centro (valor 0 enchia metade da barra sem querer dizer nada) e
  a decisão corrente aparece escrita abaixo ("Esquerda 62%", "Direita 30%" ou
  "Indeciso").
- **Dois cliques seguidos em "Calibrar" gravavam quase o mesmo trial.** A
  captura pegava sempre os últimos N segundos do buffer, sem cronômetro: dois
  cliques com 0,27 s de intervalo produziam trials com 91% das amostras em
  comum. Trials assim caem em folds diferentes da validação cruzada e devolvem
  uma acurácia que mede memorização. Agora o programa recusa gravar enquanto
  não tiver chegado sinal novo suficiente, dizendo quantos segundos faltam (ou
  que não há aquisição ligada).
- **"Acurácia (validação cruzada)" quase invisível no tema padrão.** O rótulo
  usava um verde fixo da paleta de modalidades, com 1,2:1 de contraste sobre o
  branco; passou a usar a cor de texto do tema. Os cartões Calmness e SNR SSVEP
  da aba Focus tinham o mesmo problema e acompanham.
- **ERP anunciava "Pico+ @ 0 ms".** A busca do pico começava na própria amostra
  do marcador, que é justamente a de significado mais frouxo depois da correção
  de linha de base; passa a começar na amostra seguinte, como a documentação da
  função já dizia. A legenda do gráfico, que mostrava o texto fixo "Média (N
  épocas)", passa a trazer o N real das épocas calculadas.
- **Topografia do ERS/ERD escondia 4 dos 15 eletrodos.** FP1, FP2, T3 e T4 não
  batiam com a tabela de posições do sistema 10-20 (que usa Fp1, Fp2, T7, T8) e
  sumiam do mapa e da interpolação, embora o título dissesse "(15ch)" — e eram
  justamente os eletrodos de controle que a validação "focal ou global" usa. Os
  nomes passam a ser normalizados e vêm do arquivo carregado, não de uma lista
  fixa. O mapa também deixou de marcar canais como "módulo de expansão" (isso
  só faz sentido no Tempo Real) e o anel que destaca a área esperada ficou mais
  fino e tracejado, longe do número.
- **ERD% mudava conforme a taxa de amostragem lida do arquivo.** O curso
  temporal comparava potência somada de janelas de 0,5 s com a de um repouso de
  3 s; como o número de raias espectrais difere entre as duas, o mesmo arquivo
  lido com a taxa nominal ou com a taxa medida pelo leitor dava ERD% com até 37
  pontos percentuais de diferença, e ruído estacionário sem tarefa nenhuma
  aparecia como −18% ou +26%. A comparação passa a ser feita em densidade
  espectral média, que não depende do número de raias. A medida usada em todo o
  resto do programa não mudou.
- **ERD% por canal inflava com repouso curto.** A média das razões por
  tentativa é dominada pelas tentativas de baseline fraca: com 3 s de repouso,
  ruído estacionário sem efeito de tarefa marcava +25% e um ERD real de −50% de
  potência era lido como −38%. Passou a ser a razão entre as potências médias
  (o método clássico de Pfurtscheller e Lopes da Silva, 1999): o mesmo ruído dá
  ~0% e o ERD de −50% é lido como −50%. As escalas das barras e da topografia
  mudam de valor; comparações com resultados anteriores precisam ser refeitas.
- **Curso temporal da validação do ERD começava deslocado.** A curva nascia uns
  3 dB abaixo de zero antes mesmo do aviso, porque a janela deslizante e o
  trecho de repouso eram medidos com resoluções diferentes. Cada curva passa a
  ser referenciada pelo próprio trecho anterior ao aviso, e o rótulo do eixo diz
  isso. O formato da curva e o veredito focal/global não mudam.
- **Mosaico tempo×frequência (ERSP) mostrava faixas de até 6 dB sem evento
  nenhum.** O repouso era estimado numa janela de 512 amostras e a análise em
  janelas de 62: a razão entre as duas versões do mesmo espectro virava ganho
  nas laterais e perda no centro, e em sinal estacionário o mapa chegava a
  encostar no limite da escala. O repouso passa a ser estimado com janelas do
  mesmo tamanho das de análise. Os valores em dB do mosaico mudam.
- **Classificador de band-power rendia muito abaixo do CSP nos mesmos dados.**
  A regularização do LDA era um valor absoluto que não regulava nada com
  atributos de variância próxima de 1: com 15 canais (30 atributos) e ~32
  tentativas de treino, o band-power ficava em 61% contra 97% do CSP. Passou a
  ser um encolhimento proporcional aos próprios dados, e o band-power vai a
  ~89%. CSP e Riemanniano não se movem, e em sinal sem informação nenhuma os
  três continuam no nível de acaso.
- **Botão "Fechar" saía em inglês nos nove idiomas**, inclusive em português,
  nos diálogos de validação do ERD, do exemplo de validação em lote, do núcleo
  de aquisição C++ e dos termos de uso — o Qt não tem tradutor carregado neste
  programa e o rótulo vinha do padrão dele.
- **"p = 0,012 (significativo)" ficava em português nos outros oito idiomas**,
  ao lado de um "NÃO significativo" que era traduzido: só a palavra afirmativa
  estava fora da tradução.
- **Estudo por Paciente: os nomes dos músculos se cobriam no eixo das figuras
  antes × depois.** O rótulo saía com o nome inteiro numa linha só, e com
  quatro canais de nomes reais os rótulos vizinhos chegavam a se sobrepor em
  37 px — quem lia a figura não sabia qual ponto era de qual músculo. O nome
  passa a ser dobrado em várias linhas, o painel cresce com o número de canais
  e o corpo da letra encolhe a partir de sete canais. Medido com os mesmos
  nomes: as folgas passaram de −37, −30 e −42 px para +21, +17 e +27 px.
- **O aviso "gravação incompleta" era escrito em cima do ponto mais alto** do
  mesmo painel, a 2 px de folga (e sobreposto no painel de uma das datas).
  Agora o painel reserva uma faixa no topo e o aviso fica a 17 px do ponto mais
  alto.
- **Na figura de barras antes × depois, o "×" de exercício não gravado era
  desenhado FORA do painel**, em cima do rótulo "0" do eixo Y, porque nada
  fixava os limites do eixo X e a marca não entra no cálculo automático. Pior:
  a linha que tem os nomes dos exercícios ganhava limites diferentes das de
  cima, de modo que o mesmo exercício caía em posições diferentes de uma linha
  para a outra (23,9% da largura contra 3,9%). Agora todos os painéis usam os
  mesmos limites e o "×" nasce logo acima do eixo, dentro do painel.
- **O aviso da linha da rede elétrica saía escrito por cima das barras** no
  panorama, vermelho sobre índigo e ilegível: ele era posicionado em
  coordenadas de dado e começava dentro da primeira barra. Agora é ancorado à
  direita do painel, com tarja branca atrás, e o topo de todas as barras
  continua visível.
- **A legenda do painel de qualidade do panorama chegava a cobrir uma barra
  empilhada**, porque era deixada no "melhor lugar" que o desenhista escolhesse.
  Passou para cima do painel, como já era no mapa de qualidade.
- **A nota de rodapé da figura de canais e músculos nascia à esquerda da
  tabela**, e o recorte automático da imagem deixava 13% de margem branca de um
  lado contra 1,4% do outro. A nota passou a ser ancorada na tabela e a figura
  saiu de 2066 para 1827 px de largura, com as duas margens em 1,5%.
- **Uma gravação interrompida no meio da contração era contada como boa.** Se a
  fase de ação tinha menos de meio segundo — o mesmo piso que o cálculo das
  métricas já usava para descartar o bloco — o registro saía sem métrica
  nenhuma, mas o veredito de qualidade continuava "utilizável", porque ele não
  olhava a duração. A árvore na tela, o panorama, a planilha de qualidade e a
  tabela de canais contavam esse canal como aproveitável enquanto as figuras
  antes × depois o marcavam com "×". Agora o canal de gravação interrompida sai
  como "não utilizável" (com os números medidos preservados) e o denominador da
  tabela de canais passa a contar só as gravações que renderam métrica de ação.
- **Na legenda sugerida, "processado no ROA" e o processamento colavam numa
  frase só** ("processado no ROA notch da rede e harmônicos"). Entrou um
  dois-pontos. A legenda também passou a citar as **gravações incompletas** —
  as que existem, aparecem como "×" nas figuras, e não eram mencionadas em
  lugar nenhum; antes só as ausentes eram listadas.
- **A legenda do gráfico de evolução cobria pontos de dado** quando havia mais
  sessões no eixo (medido: 1 ponto coberto com 5 sessões, 2 com 8). Ela passou
  para fora do painel, à direita.
- **No gráfico de bruto × limpo, o ponto de veredito raro sumia por baixo do
  vizinho.** Tudo era desenhado num traço só, na ordem dos registros: com
  pontos aglomerados, 4 de 30 ficavam escondidos sob um ponto de outra cor
  desenhado depois. Agora há um desenho por veredito, o mais raro por cima e
  com borda branca fina.
- **Com a anonimização ligada, a árvore na tela continuava mostrando o nome
  real do paciente e o nome de arquivo original**, enquanto as pastas, as
  planilhas, as figuras e o PDF já saíam como P01. A tela passa a receber os
  mesmos códigos do disco.
- **Os 47 textos novos desta rodada apareciam em português numa janela em
  inglês, espanhol, italiano, francês, alemão, japonês, chinês ou russo.** Eram
  chaves criadas pelas próprias correções — a legenda da escala de cor do mapa
  de cabeça, a dica de arrastar para girar e inclinar, "Mostrar rótulos dos
  marcadores" e a sua explicação, "Métrica (bruta)" e "Métrica (× baseline)",
  as duas recusas de baseline zerada, o aviso de trial sobreposto, o aviso de
  sinal simulado, o de nenhum canal EMG entre os canais em uso, a dica da taxa
  medida e do relógio, o aviso de tela atrasada, os dois avisos de amostra
  perdida na exportação FIF e as mensagens do relatório sem `summary.json`.
  Agora todas têm tradução nos oito idiomas, com os campos de formato
  (`{0}`, `{1:.1f}`) conferidos um a um: um campo perdido na tradução vira
  erro na frente do usuário no idioma que ninguém testa.
- **"Baseline falhou", o estado do painel de Foco, nunca chegava ao
  dicionário.** Ele sai por `tr(variável)`, e a coleta de faltantes só enxerga
  literais dentro de `tr()`: a chave nunca entrava na lista a traduzir e ficava
  em português em todos os idiomas, ao lado de FOCADO, RELAXADO e NORMAL, que
  já estavam declarados à mão. Declarada em `ferramentas/coleta_faltantes.py`,
  junto dos outros estados.
- **Quem abria a janela sem passar pelo `main()` ficava com a fonte que o Qt
  escolhesse.** A troca de Inter e JetBrains Mono pela primeira família
  instalada de cada pilha (Segoe UI, Cascadia Code e as seguintes) só
  acontecia dentro do `main()`; testes, capturas e quem embute o ROA criavam a
  janela direto, e os ~40 pontos que pedem `QFont(FONT_UI)` ou
  `QFont(FONT_DATA)` caíam no substituto do Qt. No modo offscreen ele escolheu
  Agency FB, condensada, e deformou os rótulos de dezenas de figuras do manual
  e do guia: "CH1 Fp1", os números dos eixos do Tempo Real e as tabelas. A
  escolha virou uma função que roda uma vez por processo e é chamada pelo
  `main()`, pela janela principal e pelo launcher antes de qualquer fonte ser
  criada, e que põe essa fonte em 10 pt como fonte da aplicação quando ela
  ainda não a tem (Segoe UI, onde Inter não está instalada).
- **As figuras do guia de imagens e dos manuais mostravam a topografia antiga
  e a fonte condensada.** Foram refeitas, com o mesmo nome e o mesmo tamanho em
  pixels: as 82 fotos do guia (e o `docs/GUIA_IMAGENS_ROA_com_fotos.pdf`), as
  quatro de topografia do Manual do Usuário nos 9 idiomas (`figuras_idiomas/`,
  `figuras/` e as que o manual de fato embute, `antigo/figuras/fig_NNN.png`),
  as do modo simples (37 a 40, 9 idiomas) no visual novo e as abas Topografia,
  Layout Custom e ERS/ERD do Manual Técnico. A captura do guia passou a preparar
  a aplicação como o `main()` (Fusion, fontes, densidade, tema e paleta) e a
  abrir no nível Avançado: com o Simples como padrão, as abas fotografadas
  sumiam. `Manual_Tecnico/capturas.py` ganhou o mesmo nível e `CAPTURAS_SO`
  para refazer só algumas abas. Legendas e textos dos itens de topografia
  acompanham as fotos (spline, barra com unidade, domo sem relevo, 11 camadas,
  ERD% com sinal, FP1/FP2/T3/T4 no mapa); os números citados nas legendas são
  os das capturas novas.
- **Topografia do ERS/ERD com o sinal do ERD%.** O mapa recebia |ERD%|: T3
  (ERS de +13) e T4 (ERD de −13,5) saíam com a mesma cor e o mesmo número, e
  FP2 (ERS de +12,8) parecia dessincronização, enquanto o gráfico de barras ao
  lado mostrava os sinais certos. Agora a escala é divergente e centrada no
  zero (azul = ERD, como no mapa ERSP do próprio ROA; vermelho = ERS), o disco
  mostra o valor com sinal (+13,0, −13,5) e a barra vai de "ERD · −29,7 %" a
  "ERS · +29,7 %", com o 0 no meio. O título deixou de dizer "POTÊNCIA ·
  |ERD%|" (não é potência) e passou a "ERD% · MU". O mapa usa os nomes do
  arquivo, como as barras: antes o mapa dizia T7/T8 e as barras, T3/T4.
- A troca Simples ↔ Avançado deixou de mandar `StyleChange` sintético à
  janela, às abas, às tabelas e às barras de rolagem: só combo, botão e
  cabeçalho de tabela guardam o `sizeHint` do outro nível e precisam dele.
- **Diálogo não modal aberto durante a troca de nível** (por exemplo o mapa de
  co-contração) ficava com o visual do nível anterior: o repolimento não descia
  em outras janelas. Os diálogos visíveis da janela são repolidos junto.
- **Cabeçalho do modo completo a 1366 px.** Saíam "Research Open Analysi",
  "DESCONECTA", "-0.00" sobre os pontos de qualidade e "±0" colado ao logotipo
  (igual à 1.8.4). Abaixo de ~1500 px o subtítulo, o g do acelerômetro e o Δt
  ficam ocultos (o Δt médio e o jitter
  continuam no registro de auditoria da sessão), o estado da
  conexão nunca é cortado, e o cabeçalho é reavaliado ao voltar do modo
  simples (antes só ao redimensionar a janela).
- **Logotipos no tema escuro.** O "RÔA" azul saturado sobre o fundo quase preto
  deixava "research open analysis" ilegível na tela inicial: no tema escuro o
  logotipo sai na cor de acento do tema. O logotipo BionicaLab aparecia numa
  caixa branca no cabeçalho escuro porque o recorte do fundo usava uma chamada
  do PyQt5 (`bits().setsize`) que não existe no PySide6 e caía sempre no
  `except`; o recorte funciona e, no escuro, o logotipo também vai para a cor
  de acento. A troca de tema ao vivo refaz o do cabeçalho.
- **Topografia a 1366 × 768** (Visualizar → Topografia): o quadro era mais alto
  que a área visível e a barra com os números só aparecia rolando. As três
  vistas pedem 300 px de altura (antes 420) e, em quadro baixo, a barra vai ao
  lado da cabeça. O rótulo "Profundidade da camada" da Tomografia ganhou margem
  e o valor (o desenho repetia o mesmo texto logo acima dele).
- **Offline em tela baixa.** A FFT da seleção ficava com 50 a 70 px de gráfico,
  o rótulo do eixo cortado ("Amplitude (") e 15/10/5 encostados: as análises
  pedem 150 px, o eixo Y tem metade das marcas e, abaixo de 800 px de janela,
  o rótulo vira só "µV". Ao abrir a sub-aba Topografia com uma gravação
  carregada, a divisória dá a ela até 360 px: o traçado cede até 100 px e, se
  ainda faltar (1366 × 768), a tabela de sessões sai de cena enquanto a
  Topografia está aberta (os botões ficam); tudo volta ao sair da sub-aba. A
  1600 × 1000 a Topografia ganha 360 px com a tabela à vista; a 1366 × 768,
  ~270 px, com a cabeça e a barra inteiras. Antes só se via o título
  "POTÊNCIA · ALPHA".
- **Modo simples:** no passo 3 havia dois "→ Relatório PDF" na tela (o cheio da
  barra e o de contorno do Offline); o do Offline some enquanto o da barra
  aparece. O selo "MODO SIMULAÇÃO" vai em contorno âmbar (cheio, disputava com o
  único botão cheio da tela); o rodapé âmbar continua avisando.
- **Depois de desconectar**, o último traçado ficava na tela com a cor cheia ao
  lado de "DESCONECTADO" e parecia sinal chegando. Fica a 30% até a próxima
  conexão (nos dois níveis).
- **Sumário impresso dos manuais em japonês e chinês saía em quadradinhos**
  (três páginas inteiras): a entrada ia para o sumário como texto puro e era
  desenhada em DejaVu. `Manual_Tecnico/base.py` passa a entrada por
  `_confere()`. Os dois manuais foram regenerados na 1.9.0 com a correção;
  os sumários em japonês e chinês saem legíveis e sem glifo nulo.
- Manual do Usuário: o triângulo do botão "▶ Protocolo" (nove idiomas) e a
  seta de "Python↔C++" (zh) tinham virado caractere nulo na extração do PDF
  antigo e saíam como quadradinho; `gera_manual_usuario.py` os repõe.
- **Escolher "Multimodal" na tela inicial não era aplicado.** A lista de tipos
  de sinal do Multimodal tinha 16 itens e era percorrida até o número máximo de
  canais; o erro de índice era engolido e a janela abria no modo anterior, sem
  voluntário ativo e sem navegar. A lista agora é completada como a do padrão.
- **Voluntário escolhido na tela inicial ou na paleta de comandos não ficava
  ativo.** O código chamava `VolunteerRegistry.set_active`, que nunca existiu;
  o `AttributeError` era engolido e a sessão saía sem voluntário. Agora usa
  `select_volunteer`, atualiza a tabela e o indicador do cabeçalho, e a falha,
  se houver, vai para o log.
- **"+ Novo" da tela inicial não cadastrava ninguém**: só mostrava um aviso
  mandando cadastrar depois, dentro da janela. Agora pede o nome, cria o
  voluntário, deixa-o selecionado e avisa quando já existe um paciente com o
  mesmo nome.
- **Reabrir uma gravação ou uma sessão recente pela tela inicial forçava o modo
  EEG**, mesmo que a gravação fosse de EMG, ECG ou EoG. O modo salvo é mantido.
- **A tela inicial sempre abria com EEG marcado** e ignorava o tipo de exame
  usado da última vez (`config.acquisition_mode`). Agora restaura o tipo salvo.
- **Fechar o programa durante uma gravação encerrava sem perguntar.** Agora
  pede confirmação ("A gravação ainda está em andamento. Parar e fechar o
  programa?", padrão Não) e, se confirmado, para a gravação antes de sair.
- **Offline: o traçado da sessão ficava esmagado** (68 px de altura em
  1366x768 e em 1600x1000) e "Salvar figura (PNG)" gravava uma tira ilegível.
  A Topografia offline pede 420x420 de mínimo e, como página direta das
  análises, empurrava o bloco inferior para ~498 px, mesmo com a aba oculta no
  modo simples. A página agora fica numa área de rolagem (a classe da cabeça e
  a Topografia ao vivo não mudaram), o traçado tem mínimo de 220 px e a
  divisão vertical passou a tabela 20%, traçado 50%, análises 30%. Medido nos
  dois níveis, com e sem sessão: 221 px em 1366x768 e 322 px em 1600x1000.
- **"Salvar figura (PNG)" não depende mais do tamanho da janela**: a figura é
  redesenhada pelo exportador do pyqtgraph com 2400 px de largura em 16:9
  (2400x1350). Se o exportador falhar, vale a cópia da tela de antes e o motivo
  vai para o log.
- **"■ perdendo amostras N%" continuava no cabeçalho depois de DESCONECTADO.**
  O buffer e os contadores da conexão encerrada seguem na memória e o semáforo
  continuava a avaliá-los. Ao desconectar ele volta a "Sinal: —" (mesmo texto,
  estilo e dica de antes de conectar) e só volta a avaliar na conexão seguinte.
  O cálculo da perda não mudou.
- **O caminho da pasta quebrava logo depois de "C:"** nas caixas "Sessão
  gravada", "Salvar figura (PNG)" e "PDF gerado". O texto exibido leva um
  espaço de largura zero depois de cada separador e quebra nas pastas; o
  caminho usado para abrir a pasta é o original.
- 39 textos do modo simples traduzidos nos oito idiomas (arquivados em
  `ferramentas/trad/aplicadas_naolancado_modo_simples/`). "Multimodal", rótulo
  do emblema de modalidade, nunca tinha entrado nos dicionários.
- **Ctrl+P (captura de tela da aba) não gravava nada nas abas Bio do modo
  Multimodal.** O nome da aba vira nome de arquivo, e a barra de
  "Bio (EMG/ECG/EoG)" levava o Qt a gravar numa subpasta inexistente;
  o `save` devolvia False sem aviso. Caracteres proibidos em nome de
  arquivo agora viram sublinhado, e a falha de gravação aparece na barra
  de status e no log.
- **Frequência mediana (MDF) presa à grade do Welch.** O motor pegava o
  primeiro ponto do espectro acima da metade da potência: com janela de 256
  amostras a 1 kHz, a MDF só assumia múltiplos de 3,9 Hz, e uma diferença de
  um degrau parecia queda de fadiga. Agora é interpolada entre os dois pontos
  que cercam a metade da potência. Vale para a Área Maker, o Estudo por
  Paciente e tudo que usa `run_recipe`.
- LEIA-ME e legendas do Estudo por Paciente saíam com uma linha em branco
  entre cada linha no Bloco de Notas (CR duplicado ao gravar em modo texto).
- **Texto de tela em português em qualquer idioma porque o código nunca
  chamava `tr()`.** Uma varredura da AST do ROA.py achou 603 literais e
  f-strings indo direto para a tela: caixas de mensagem (QMessageBox), títulos e
  filtros de QFileDialog e QInputDialog, `setText`/`setToolTip`, itens de combo,
  legendas e eixos de gráfico, cabeçalhos de tabela, tooltips dos LEDs e dos
  comandos rápidos, o texto do Offline, ERS/ERD, BCI, Estatística guiada e
  intra-sessão, Importador, Tela inicial, Sobre e núcleo C++. Todos passam por
  `tr()`. As f-strings viraram `tr("… {0} … {1:.1f}").format(…)`, com campos
  numerados para a tradução poder trocar a ordem das palavras.
- Tabelas exibidas cruas agora traduzem no ponto de exibição, com a chave em
  português intacta: título e tipo dos 79 erros no Diagnóstico de erros (a
  busca também aceita o texto traduzido), nome, ajuda e portas dos blocos da
  Bancada e seus exemplos prontos, métricas da Evolução e da Estatística
  intra-sessão, presets de layout do assistente, status do ritmo do ECG, estados
  de foco, de alerta do EoG e de fadiga do EMG, e a edição do app no título da
  janela.
- **Protocolos de fábrica** aparecem traduzidos no combo, na descrição, na
  tabela de fases, na linha do tempo e no rótulo da fase em execução. O combo
  guarda o nome no dado do item: `config.protocol_active` e os marcadores
  gravados continuam com o nome em português. O sufixo " #n" da repetição fica
  fora da chave (`rotulo_fase_tela`).
- Plurais montados por expressão (`fase{'s' if n != 1 else ''}`, `arquivo{'s'…}`,
  `ruidoso{'s'…}`), HTML colado com `+` e a postura do acelerômetro
  ("Inclinado " + "frente") foram reescritos como frases inteiras. O veredito
  do classificador BCI ("ACIMA"/"DENTRO" solto no meio da frase) virou duas
  frases.
- **`tr()` não achava a tradução de texto com espaço ou quebra de linha nas
  pontas** (`tr(" Em média, {0} é maior.")`): a coleta guarda a chave sem as
  pontas. `I18N.tr` agora traduz o miolo e devolve as pontas. Afetava 15 chaves.
- O título da janela era posto antes de o idioma do config valer e ficava em
  português até a primeira troca de estado.
- "(rastreabilidade da coleta)" ficava em português dentro das oito traduções
  do registro de auditoria. O botão "Assinar (markers)" do LSL e o "Cancelar
  assinatura" estavam traduzidos como assinar documento em it, fr, de, ja, zh e
  ru (Firma, Signer, Signieren, 署名, 签名, Подписать); agora é assinar o stream.
- 627 textos novos traduzidos nos oito idiomas (dois lotes, arquivados em
  `ferramentas/trad/aplicadas_naolancado_interface/`).
- Inglês: "colour"/"colours" em quatro textos (topografia, domo e o teto de
  acurácia do BCI) passaram a "color"/"colors", a grafia do resto da
  interface (103 ocorrências); os lotes arquivados em `ferramentas/trad/`
  também, para que reaplicar um lote não traga a grafia de volta.
- A paleta de comandos oferecia a aba "Bio (EMG/ECG/EoG)" em modo único,
  em que a barra de abas mostra "Músculos", "Coração" ou "Olhos": quem
  digitava o nome visto na tela não achava a aba. A paleta passou a usar o
  nome que a barra mostra. Achado pelo `test_modo_simples.py`.
- **Figuras, guia e manuais refeitos com o ROA fechado (etapa pacote).** As
  fotos tinham sido tiradas antes do fechamento: o rodapé dizia "ROA v1.8.4"
  e parte das telas era anterior à etapa código (pílula do paciente, Músculos
  com CH9 a CH17 sem linha, Topografia sem esmaecimento). Refeitas pelos
  mesmos scripts: as 82 entradas do guia (89 fotos), as figuras 37 a 40 do
  Manual do Usuário e as quatro de topografia (`figuras_idiomas/`, `figuras/`
  e `antigo/figuras/`) nos nove idiomas, e as 30 figuras do Manual Técnico
  nos nove idiomas. `Manual_Tecnico/capturas.py` passou a conectar em
  simulação antes de fotografar (a Topografia saía no caso plano, "sem
  variação entre eletrodos"), fotografa no modo Multimodal as quatro abas que
  o modo EEG esconde (Bio, Layout Custom, EMG Joystick, Rede e Eventos; antes
  saíam sem a aba na barra e o Layout Custom sem dado) e troca, só no texto
  exibido, a pasta temporária por um caminho neutro. As legendas do guia com
  números lidos na tela foram atualizadas (15 legendas em 8 arquivos) e as
  topografias citam o esmaecimento.
- `docs/GUIA_IMAGENS_ROA.pdf` (sem fotos) não tinha gerador e estava
  desatualizado. `gera_guia.py <saida.pdf> --sem-fotos` gera o mesmo texto sem
  as fotos, e `finaliza_guia.py` grava as duas versões.
- Manual do Usuário (nove idiomas): a sessão Multimodal é descrita com uma
  página por modalidade (e o formato de EEG com aviso só quando a gravação não
  guardou o tipo de cada canal); a caixa do PDF é citada pelo nome atual
  ("Relatório de EEG gerado", com o nome do exame; o texto dizia "PDF
  gerado"); o remendo da Topografia 1.9.0 ganhou o parágrafo do esmaecimento
  longe dos eletrodos. Manual Técnico (nove idiomas): a nota da Topografia cita
  o esmaecimento. PDFs regenerados: Usuário com 49 a 56 páginas e o volume de
  476, Técnico com 87 a 94; `Manual_ROA/manual_usuario.pdf` é a cópia do pt.
- **Pacote:** "Termos e Licenças/Como citar este software.cff" estava em 1.1.0
  porque o `sincroniza_pacote.py` não copiava o `CITATION.cff`; agora copia,
  junto com o `ROTEIRO_AUDITORIA.md` ("Documentação/Roteiro de auditoria
  técnica.md"). O roteiro tinha dois caminhos com o nome de usuário do
  Windows (C:\Users\<nome>\...), trocados por caminhos relativos na fonte. O
  `sincroniza_pacote.py` procura caminhos de usuário em todo texto que copia,
  antes de mexer no pacote, e de novo no pacote inteiro (fora do `_internal`)
  e no texto dos PDFs antes do zip; achando um, para sem gerar o zip.

### Testes
- Validação de uso com leigos, etapa pacote (ROA.py não alterado): os 17
  arquivos de `testes/` em sequência, cada um num processo, mais
  `smoke_nivel.py` nos 10 casos e `verif_fluxo.py` nos dois níveis. Todos
  PASS: ajuda_idiomas 101/101, ajuda_metodos 31/31, ajuda_ranking 26/26,
  estudo_artigo 18/18, fluxo_gravacao 83/83, metodos_2026 81/81,
  metodos_modalidades 49/49, modo_simples 166/166, relatorio_pdf 160/160,
  simulacao_tipos 29/29, topografia 129/129, traducao_erros_faq 54/54,
  traducao_listas 69/69, traducao_metodos 51/51, uso_leigo 647/648 na bateria
  (o processo `config_d simples` caiu por carga, 0xC0000005, e passou 26/26
  sozinho), vazamento_idioma 30/30, taxa_gravada 31/31; smoke 10/10;
  verif_fluxo 33/33 e 30/30.
- `testes/test_uso_leigo.py`, etapa final (caso `final`, nos dois níveis):
  aviso do filtro anexo ao passo 2 e o passo 2 depois dele, selo e dica
  limpos ao ligar o treino, contador e barra do "Marcar evento" (e a
  largura da linha, o events.csv), caixas do relatório e da figura por
  nível, barra "Figura salva" com Abrir figura e o eixo restaurado, frase
  do treino salvo, pílula "Vendo gravação", consultor (fonte, FAQ por
  nível, lista do Sinal OK, links), pergunta dos músculos (Cancelar /
  Marcar músculos / Gravar assim mesmo / com músculo não pergunta), popup
  de canais, assistente, Sistema (Abrir pasta, campo do voluntário,
  cópia de segurança), ⌂ Início, aviso do Completo, último paciente no
  config e na tela inicial, `descricao_posicao_10_20`, fonte e dica dos
  nomes de canal, `emg_fundir_ativacoes`, `rotulo_banda`, gravação
  carregada depois de ligar o treino (conta no passo). No caso `pdf_c` a
  verificação da faixa de piscadas procurava a frase antiga ("faixa
  comum: 8 a 21 por minuto", trocada na etapa acerto) e só passava quando
  os 4 s de treino não tinham piscada; agora procura a frase atual.
  `testes/test_relatorio_pdf.py`, `parte_final`: 6 surtos = 6 contrações
  e 6 faixas na figura, "curta demais" abaixo de 1 min e não acima, eixos
  por nível, ritmos em português (barras no Simples, espectro e mapa no
  Completo, "Alpha=" no bloco técnico), ECG do Simples com 1 canal e do
  Completo com 3.
- `testes/test_uso_leigo.py`, etapa acerto (casos `acerto` e `acerto_cab`,
  nos dois níveis, mais 85 verificações em 4 processos): Sair pela tela
  inicial termina o laço do Qt, paciente em uso na tela inicial e "(nenhum)"
  que solta, pasta `exame_`/prévia sem "voluntario", rodapé "Gravando o
  exame de…", histórico por tr(), "(sem paciente)" na lista, tabela com 4
  linhas e a linha aberta marcada, relatório existente reconhecido, perda
  zerada após tema/letra, sobras do glossário, aba Bio, título do diálogo,
  Salvar figura pela linha 0, título da janela em inglês; e, em tela de
  1366x768 (`_tela_1366`), cabeçalho que cabe a 125/150%, pílula parada em
  125%, Sistema sem barra horizontal e o modo apertado do cabeçalho.
  `testes/test_relatorio_pdf.py`, `parte_acerto2` (26 verificações): ECG
  implausível nos dois níveis (frase única, aviso antes do quadro,
  qualidade), músculos do Multimodal (CH11), músculo traduzido em inglês,
  `data.csv` truncado (leitura, PDF, E118), `sample_rate_ok=false`, EOG sem
  `summary.json`, faixa com fonte, envelope de 1 pol/canal, piscadas do
  gerador com o filtro do exame (`eog_piscadas` = geradas ±1;
  `eog_piscadas_tela` = critério da tela reescrito à parte; PDF com a
  sensibilidade gravada). Expectativas antigas ajustadas: "Excluir
  paciente…", rodapé com a gravação aberta (G03), pílula em 125%, faixas com
  fonte, parte de ECG do Multimodal achada pelo título; a conferência do
  cabeçalho apertado (600 px forçados) não processa eventos entre a chamada
  e a leitura, porque o tique de qualidade reaplica a largura real da
  janela e, com a máquina carregada, desfazia o estado forçado só na
  bateria. Bateria dos 16 arquivos depois da etapa: todos PASS com a máquina
  ociosa (na bateria em sequência, um processo do `analisar_d` caiu por
  carga, 0xC0000005, e passou 26/26 sozinho).
- `testes/test_uso_leigo.py`, etapa d (casos `analisar_d`, `ajuda_d`,
  `launcher_d` e `config_d`, nos dois níveis onde cabe, mais 132
  verificações em 7 processos): cabeçalho e coluna Exame/Markers, quadro de
  análises, combo, faixa e "Abrir CSV…" por nível, frase da gravação e a
  virada ao trocar de nível; nome, pasta, caixa e `_2` da figura, título e
  restauração do gráfico; métrica pré-selecionada, paciente em uso, ECG,
  rótulos leigos, gravações ignoradas contadas e a banda EEG só com EEG,
  vírgula e Estatística guiada por nível; `help_answer` por nível (FAQ do
  Sinal OK, definição não promovida, guias ocultos fora, título inteiro na
  pergunta), atalhos, exemplos e respostas do diálogo; dicas e combo da
  janela "Tipo de exame"; Conexão, Pacientes (botões, coluna, "Em uso",
  contagem ao parar), barra, temas (rótulo × chave, troca pelo rótulo),
  Sistema, `tickStrings` em pt/en, abas Bio por nível e a virada.
- `testes/test_relatorio_pdf.py`, etapa c da validação com leigos
  (`parte_leigo_c`, mais 67 verificações; as antigas ajustadas aos textos com
  acento e vírgula decimal): duração em palavras, qualidade em palavras,
  rótulos por tipo nos dois níveis, cabeçalho Simples/Completo (Paciente/
  Voluntário, "não informado", sem Fs nem APTO, quadro "Como ler", rodapé,
  URL só nos metadados no Simples, taxa com vírgula, inglês com ponto),
  EMG (contrações, força relativa, cansaço, sem MDF/TKEO/SENIAM no Simples,
  "CH2 músculo", marcador virando linha nas figuras, MDF ± no Completo), ECG
  (faixa 60 a 100, canal da tela, "gravação curta demais" com o limiar
  `ECG_RR_MIN["sdnn"]`, SDNN em 90 s, critério com a verdade), EOG (faixa 8 a
  21, conclusão, canais da tela, PERCLOS só no Completo, canais off no fim),
  Multimodal só EEG e canal da tela traduzido para a seção, e ru/zh/ja sem
  glifo faltando (fontTools) nem "Glyph missing" do matplotlib.
- `testes/test_uso_leigo.py`, etapa c (caso `pdf_c` nos dois níveis, mais 42
  verificações): combos V/H → `_canais_escolhidos_na_tela`, piscadas zeradas
  ao iniciar a gravação, `report_channels` no `summary.json` (com as chaves
  de sempre), PDF gerado da gravação com os canais da tela, tarja, cabeçalho
  e faixa 8 a 21, Offline com "CH1 olhos"/"EOG CH1" e "Bandas EEG" escondida
  (e de volta numa gravação de EEG), `data.csv` intacto, Empilhado com
  músculo/tipo e refeito ao trocar o tipo, pergunta sem `summary.json` por
  nível.
- `testes/test_uso_leigo.py`, etapa b2 (mais 82 verificações em 4
  processos): caixa "Nenhum aparelho encontrado" (título, passos, papéis e
  botão padrão, Cancelar/Treino em `_porta_automatica`), `layout_multimodal`
  8/16, diálogo "Trocar" subindo para 16 e a nota nos dois números, faixa
  âmbar só no Simples e a oferta que divide os 8 canais, pílulas do treino
  nos dois níveis (texto, cor de aviso, selo fundido, "✓ Sinal de treino",
  rodapé, título), contraste medido das três pílulas, borda tracejada da
  pílula de sinal, dicas com canal e ação (ruído e ruim, com
  `classifica_qualidade_canal` substituída), "● GRAVANDO"/"● REC", combo de
  tamanho da letra (config, config.json, folha a 15 pt, ticks a 14 pt,
  pílula a 21 pt, sobrevivendo à troca de tema e voltando a 100%) e o
  assistente (resumo, dica que some, caixinha de 2 px com contraste medido,
  fonte proporcional do termo).
- `testes/test_uso_leigo.py`, etapa b1 (mais 112 verificações em 5
  processos): treino sem aparelho nos dois níveis (menu Arquivo e Ctrl+Q,
  botão ⌂ Início só no Simples, "Escolha uma gravação na lista" e caixa
  "Abrir gravação" com a lista vazia, pasta `treino_`/`simulacao_` e prévia
  igual, "Passo 3 de 3" ao parar mesmo conectado e em qualquer aba,
  `Relatorio_EEG_<data>.pdf` com "Abrir relatório" e `_2.pdf` na segunda
  vez, "Pronto · relatório gerado", passo 2 de volta na nova gravação,
  linha mais recente já marcada e Carregar sem seleção, Voltar ao início com
  confirmação e Sair); pacientes (prévia com VID recalculada, campo do
  sujeito oculto no Simples, lista do Analisar só do paciente em uso e a
  caixa "Mostrar de todos", "Gravação aberta: V02 …" com "Usar este
  paciente", diálogo "De quem é este exame?" com os quatro botões e o
  "+ Novo", a pergunta só no Simples com aparelho real); tela inicial
  ("Trocar" grava exame e canais no config e a tela reaberta mostra a
  escolha). `test_fluxo_gravacao.py` acompanha o fluxo novo (caixa
  "Gravação salva" no Simples, nome do PDF, "Abrir relatório", segundo
  relatório em `_2.pdf`).
- `testes/test_uso_leigo.py` (novo, 84 verificações em 5 processos, um por
  caso): `num_loc` em pt/en/de/ja; `geometria_inicial` e `geometria_cabe`
  para 1366x728 e 1920x1040; tradutor do Qt com `.qm` e a reserva sem `.qm`
  (QMessageBox em pt e es), `traduz_botoes` e `pede_texto`; janela principal
  nos dois níveis (título, item do menu Ajuda, combos Exibição e "Detalhe
  desta aba", aba Pacientes/Voluntários, dica da pílula, Sobre e Atalhos por
  nível, a troca de nível levando tudo junto e voltando, geometria salva
  restaurada só se couber e gravada ao fechar); tela inicial nos dois níveis
  ("ROA — Início", nome do paciente com o código, cartões e botões, título e
  campo do "+ Novo"). `test_modo_simples.py` acompanha os nomes novos
  (Pacientes, itens do menu, dica da pílula) e `apoio_janela.py` instala a
  tradução do Qt como o `main()`.
- `test_metodos_2026.py` (81 verificações; eram 74): olhar vertical que vai e
  volta em 1,2 a 2 s sem piscada dá PERCLOS ~0 e nenhuma piscada; olhar que
  vai e volta em 0,6 a 1 s não vira piscada; 5 fechamentos de 1 s entre
  piscadas normais dão PERCLOS de 9 a 15%, igual com o eletrodo invertido;
  piscadas duplas a 0,4 s acham 20 de 20, sem filtro e com o filtro do
  exame (notch 60 Hz + passa-faixa 0,1 a 30 Hz causal). Com o ROA.py de
  antes desta correção, 4 desses casos falham.
- `test_relatorio_pdf.py` (52 verificações): PDF de EoG simulado sem nenhuma
  piscada e sem filtro sai com "Piscadas=0" e PERCLOS abaixo de 0,5% (antes,
  23,99%).
- `verif_fluxo.py` lê a dica inteira pela dica de ferramenta (no simples a tela
  mostra a frase do passo) e confere também a frase de cada passo, o botão
  cheio (Iniciar Gravação, Parar em vermelho, → Relatório PDF) e o "→ Relatório
  PDF" do botão da dica com gravação carregada; no avançado, que nenhum botão
  ganhou papel e que o botão da dica continua oculto no Offline, como na 1.8.4.
- `teste_topografia.py` (111 verificações, só dados sintéticos): quadro plano
  e faixa de 0,8% dão cor única no meio da escala e o aviso nas três vistas
  (faixa de 2% não); 0, 1 e 64 canais, NaN, None, lista curta, FP1/T3 da
  montagem BCI, F10/T10/P10 sem posição e painéis de 120 × 90 a 1534 × 240
  desenham sem exceção; valor escrito no disco igual ao dado, cor do disco
  igual ao min-max e ao mapa no centro do eletrodo; no CSD o disco mostra o
  |CSD| dentro da barra; custo de dado novo abaixo de 35 ms com 8, 16 e 64
  canais; caches com limite; campo dentro da faixa medida; domo lendo o mesmo
  array do 2D e sem face interna; Tomografia recortada no raio da fatia.
- `teste_acertar.py` (66 verificações, só dados sintéticos e janela offscreen):
  foco frontal único (um só máximo local, linha média sem sela) com 8 e 16
  canais; spline passando pelo eletrodo, dentro da faixa medida e sem
  extrapolar fora do anel; 64 canais em três tamanhos sem nome sobre disco ou
  sobre outro nome e sem discos encostados; dica do eletrodo; cor igual nas três
  vistas no quadro plano; avisos "sem variação" e "variação < 1%"; sombra do
  domo acima de 0,85 e ausente no plano; barra da Tomografia sem números abaixo
  do escalpo; ERD% com sinal, cores diferentes para ERS e ERD e barra
  simétrica; cabeçalho do completo sem corte a 1366 (também depois de ir e
  voltar do simples); diálogo aberto acompanhando a troca de nível; StyleChange
  só em botão, combo e cabeçalho de tabela; traçado esmaecido ao desconectar;
  selo em contorno e um só "→ Relatório PDF" no simples; FFT do Offline com 150
  px; logotipo BionicaLab sem caixa branca.
- Lote de tradução `blocoA2` (8 chaves × 8 idiomas, arquivado em
  `ferramentas/trad/aplicadas_blocoA2/`); cinco chaves que ficaram órfãs (a
  aba "2D (IDW)", a dica antiga do combo "Mapa", os dois rodapés do domo com
  "relevo de potência" e o rótulo solto da profundidade) saíram dos oito
  dicionários.
- Lote de tradução `pend2` (22 chaves × 8 idiomas, arquivado em
  `ferramentas/trad/aplicadas_naolancado_pend2/`), com a conferência do
  `aplica_trad.py`; as duas chaves que ficaram órfãs (a frase antiga das barras
  de ERD% e o rótulo do Offline com o caminho) saíram dos oito dicionários.
- `test_vazamento_idioma.py` ganhou duas verificações: o painel de log explica,
  traduzido, que fica em português e é do modo completo; e nenhum `tr()`
  recebe f-string. `varre_sem_tr.py` passou a contar `tr()` com f-string.
- Lote de tradução `pendências` (47 chaves × 8 idiomas): além da conferência do
  `aplica_trad.py` (marcadores `%d`, campos `{}` e tags HTML idênticos ao
  português), um teste próprio formata cada molde com valores de exemplo em
  cada idioma — um campo perdido na tradução quebra ali, não na tela —, recusa
  chave longa copiada do português, confere que nenhuma chave existe num
  idioma e falta no espelho inglês, e que a coleta sai zerada. Contra o ROA
  anterior ao lote: 19/38; depois: 38/38.
- `test_vazamento_idioma.py` (27 verificações): o config de teste cai no modo
  simples, então a tela inicial passou a ser varrida duas vezes, simples e
  completa (`ui_level="avancado"`), para o launcher de três painéis não ficar
  sem cobertura.
- `test_estudo_artigo.py` (17 verificações, só dados sintéticos): mapa
  canal → músculo, MDF fora da grade e estável entre repetições, as quatro
  figuras e as legendas geradas com gravação ausente e interrompida, e
  anonimização sem sobra do nome em pastas, arquivos e planilhas.
- `test_vazamento_idioma.py` (26 verificações, antes 8): além das chaves do
  dicionário, acusa qualquer texto visível com cara de português (ç, ã, é… ou
  palavras que só o português usa) em japonês, e em processos à parte em chinês
  e russo. Lê também tooltips, itens de tabela, árvore e lista, QTextEdit, menus
  e textos de gráfico pyqtgraph, e abre onze diálogos (Bancada, Assistente,
  Diagnóstico de erros, Estatística guiada e intra-sessão, Evolução,
  Importador, Primeiro uso, Mapa de co-contração, Paleta, Tela inicial). Passa
  o `varre_sem_tr.py` no código (nenhum literal de tela sem `tr()`), confere que
  o protocolo escolhido grava a chave em português e que texto com pontas
  traduz. Com `ROA_VAZ_DUMP=prefixo` grava a lista inteira de vazamentos.
  A versão nova achou ~270 textos que a antiga deixava passar. Suíte: 477/477.
- Verificação final da 1.9.0, offscreen, com sinal simulado e nenhuma pasta
  de dado real aberta: `py_compile` ok; os 10 testes de `testes/` passam
  (101, 31, 26, 18, 70, 49, 54, 69, 51 e 30 verificações); a fumaça dos dois
  níveis nas cinco modalidades sai igual à da etapa anterior; o fluxo
  completo passa em 32/32 no simples e 29/29 no completo. Trinta segundos de
  gravação simulada em EEG, EMG, ECG, EoG e Multimodal, nos dois níveis: 0
  amostra perdida, 7.571 a 7.694 linhas no data.csv, taxa de 250,0 Hz no
  arquivo e no summary.json (`sample_rate_ok` verdadeiro). Na simulação o
  carimbo de tempo é o do marcapasso, então esses 250,0 Hz não medem um
  aparelho; pelo relógio de parede deram 250,7 a 253,0 amostras por segundo.

- Acabamento, etapa código (`scratchpad\acabamento\teste_codigo.py`, um
  processo por bloco, offscreen, sinal simulado ou sintético, config e
  sessões em pasta temporária): 69/69 depois; contra o ROA.py de antes da
  etapa, 15 ok e 34 falhas, com os oito defeitos reproduzidos (PDF Multimodal
  de 1 página e sem aviso, figura de 16 canais com proporção 0,56, EoG com
  "7 OK, 1 ruidosos" e eixo de piscadas de -0,44 a 0,44, "Amostras: 1.011" e
  LEDs verdes depois de desconectar, "▲ 1/2/3 ruidoso(s)" em EoG e
  Multimodal, "Paciente: nenhum" com o sujeito digitado, quadro do Offline em
  235 px com mínimo de 252 e FFT de 103 px a 844 pt, CH9…CH64 visíveis com 8
  canais). A conferência da topografia com dado fixo foi refeita antes e
  depois (`confere_topo_veu.py`). Lote de tradução `acab` (4 chaves × 8
  idiomas, arquivado em `ferramentas/trad/aplicadas_naolancado_acab/`).
  Depois da etapa: os 10 testes de `testes/` passam (101, 31, 26, 18, 70, 49,
  54, 69, 51 e 30 verificações), a fumaça dos dois níveis nas cinco
  modalidades sai sem erro, o fluxo passa em 32/32 no simples e 29/29 no
  completo e `varre_sem_tr.py` acha 0 destino de tela sem `tr()`. O
  `teste_pend_ui.py` da etapa pendências falhava em uma verificação que exigia
  traçado do Offline de exatamente 160 px a 1366x768 no completo: com 160 os
  três mínimos passavam da altura e o quadro era espremido; agora o traçado
  fica com 154 px e nenhum painel abaixo do mínimo (o teste foi atualizado na
  etapa testes para 140-160 px e passa). O diff `ROA.py.acab_codigo` →
  ROA.py inclui também a paleta de comandos da etapa testes (ver Corrigido). O domo com 64 canais
  ficou mais rápido com o véu em cache (24,7 ms por dado novo; era 30,2).

- Acabamento, etapa testes. Seis testes de comportamento do usuário foram
  para `testes/` e viajam no pacote (`Documentação/testes`), no formato dos
  outros (um assunto por arquivo, dados sintéticos ou simulação em pasta
  temporária, "RESULTADO: n/m PASS" no fim):
  - `test_modo_simples.py` (143): abas, controles, menus e paleta de cada
    nível nas cinco modalidades, um processo por caso; a troca pelo menu
    Ajuda e a gravação da escolha no config.json;
  - `test_fluxo_gravacao.py` (61): tela inicial, conectar, gravar e parar
    pela barra, caixa "Sessão gravada", relatório sem diálogo de arquivo,
    Offline e Salvar figura, nos dois níveis;
  - `test_topografia.py` (120): quadro plano, 0/1/64 canais e nomes sem
    posição sem exceção, custo por quadro, valor e cor do disco, caches e o
    véu longe dos eletrodos;
  - `test_relatorio_pdf.py` (43): relatório de EEG, EMG, ECG, EoG e
    Multimodal (uma página por modalidade), canais "off" fora, rótulos por
    tipo e músculo; lê o PDF com PyMuPDF, pypdf ou um leitor mínimo próprio,
    porque o programa não depende dessas bibliotecas;
  - `test_simulacao_tipos.py` (21): cada tipo de canal simulado medido com a
    régua do exame, e a simulação chegando à janela;
  - `test_taxa_gravada.py` (31): data.csv e summary.json com a taxa e a
    duração do que foi gravado, e o contrário (arquivo a 125 Hz sai com
    `sample_rate_ok` falso e o aviso).
  Com `apoio_janela.py` e `apoio_casos.py`, que montam a janela como o
  `main()` (tela offscreen de 1920x1080, config em pasta temporária, caixas
  respondidas sozinhas). Contra o ROA.py de antes da etapa código,
  `test_relatorio_pdf` dá 23/36 e `test_topografia` acusa a falta do véu.
- Os testes da rodada de pendências que não acompanhavam mudanças
  intencionais da 1.9.0 passaram a conferir o comportamento, não o texto do
  código: p1 (a janela criada sem o `main()` resolve FONT_UI/FONT_DATA para
  famílias instaladas), p2 (Tomografia sem `_grid`: 11 camadas no campo e na
  imagem; os 8 eletrodos desenhados, centro na cor da camada e anel de
  contraste, e omitidos fora da fatia a 100% de profundidade; mínimo da aba
  Topografia 360x300, igual ao do domo), p4 (FP1/T3 no lugar de Fp1/T7 com o
  nome do arquivo, os 15 no desenho), p5 e `teste_pend_ui.py` (mínimo do
  traçado do Offline entre 140 e 160 px em tela baixa, sem espremer) e p7
  (a chave aposentada do rodapé do domo fica listada com o motivo e a que a
  substituiu é conferida nos 8 idiomas). Os achados 9 e 11 do p2, que a
  verificação final deixou sem conferir, estão cobertos e passam.
- Bateria final da etapa, um processo por vez, offscreen: `py_compile` ok; os
  16 testes de `testes/` passam (101, 31, 26, 18, 61, 70, 49, 143, 43, 21,
  31, 120, 54, 69, 51 e 30 verificações); os 7 de `bloco_a`, os 7 de
  pendências e o `teste_codigo.py` (69/69) passam; `varre_sem_tr.py` acha 0
  destino de tela sem `tr()`.

- Acabamento, etapa acerto (revisão da etapa código): os sete achados foram
  reproduzidos antes de corrigir ("Patient: voluntario" com config novo em
  inglês; PDF de EMG com "Gastrocnêm" e dois "Bíceps Bra"; véu do tema
  escuro a 43 da cor do valor baixo; EMG simulado com o filtro do exame em
  "▲ 1 ruidoso(s)", rede de 0,43; "APTO ... de 0 canais" com todos os canais
  "off"; "Tight layout not applied" com 61 canais; "colour" no inglês).
  Testes novos ou ampliados: `test_modo_simples.py` (161; pílula com config
  novo em en, ru e pt), `test_relatorio_pdf.py` (49; canal preservado no corte,
  coleta bilateral, todos "off", 24 canais sem aviso do `tight_layout`),
  `test_topografia.py` (128; véu nos temas escuro e claro, nas três vistas) e
  `test_simulacao_tipos.py` (25; EMG com o filtro do exame e controle com
  rede de 60 Hz). Contra o ROA.py de antes da etapa, a pílula dá 3/6 em en e
  em ru, o PDF 42/44, a simulação 24/25 e a topografia acusa a falta da cor
  do véu. Bateria, um processo por vez, offscreen: `py_compile` ok; os 16
  testes de `testes/` passam (101, 31, 26, 18, 61, 70, 49, 161, 49, 25, 31,
  128, 54, 69, 51 e 30); os 7 de `bloco_a`, os 7 de pendências e o
  `teste_codigo.py` (69/69) passam; `varre_sem_tr.py` acha 0 destino de
  tela sem `tr()`.

- Acabamento, etapa pacote (ROA.py não alterado): cada PNG refeito foi aberto
  e conferido (rodapé "ROA v1.9.0", telas novas, CJK e cirílico certos); os
  PDFs dos manuais, conferidos com fitz, têm "1.9.0", nenhum rodapé 1.8.4,
  os textos novos nos nove idiomas e 0 glifo nulo (inclusive ja, zh e ru); a
  trava de caminho de usuário do `sincroniza_pacote.py` foi testada com casos
  positivos (barra invertida, barra, JSON escapado) e negativos (Public,
  <usuario>, arquivo binário); o ROA.zip foi conferido só por `zipfile`
  (APP_VERSION 1.9.0, SHA do ROA.py igual ao de desenvolvimento,
  version.json, este CHANGELOG, manuais de hoje, .cff em 1.9.0, `sessions/` e
  `logs/` vazias, nenhum CSV/EDF/FIF de sessão, nenhuma pasta V##_*, nenhum
  caminho C:\Users\<nome>).

- Acabamento, etapa verificação (ROA.py não alterado, SHA-256
  `80e88e80…f438`): `py_compile` ok; os 16 testes de `testes/` passam (101,
  31, 26, 18, 61, 70, 49, 161, 49, 25, 31, 128, 54, 69, 51 e 30); os 7 de
  `bloco_a`, os 7 de pendências e o `teste_codigo.py` (69/69) passam, com
  uma ressalva: na bateria o `teste_topografia.py` acusou "domo 64ch: dado
  novo 38,9 ms" (limite 35 ms), numa rodada em que todos os tempos saíram
  25 a 40% acima dos da etapa acerto; rodado sozinho três vezes, deu 29,6,
  28,4 e 27,7 ms e 111/111. `varre_sem_tr.py` acha 0 destino de tela sem
  `tr()`. Fumaça dos dois níveis nas cinco modalidades com rc=0 e stderr
  vazio; fluxo do simples 32/32 e do completo 29/29. Trinta segundos de
  simulação por modalidade nos dois níveis: o data.csv tem exatamente as
  amostras chegadas durante a gravação (7.599 a 7.727 linhas), taxa de
  250,0 Hz pela coluna de tempo, 0 amostra perdida e `sample_rate_ok`
  verdadeiro nos dez; o PDF de cada um foi gerado e a página 1 conferida (o
  Multimodal com quatro páginas, uma por modalidade). Topografia
  fotografada com dado fixo: as três vistas com a mesma escala (136 a
  385 µV²) e o mesmo foco occipital. ROA.zip conferido só por `zipfile`:
  0 falha.

- Últimos acertos, etapa código: cada item foi reproduzido antes de corrigir,
  com os testes novos rodados contra o ROA.py de antes da etapa (cópia
  `ROA.py.ult_codigo`): piscadas sobre degraus do olhar 0 de 20 e o PDF de EoG
  sem filtro 4 de 9 (`test_metodos_2026.py`, `test_relatorio_pdf.py`); aba
  Olhos com o olhar para cima 44 de 8 e PERCLOS de 31%
  (`test_simulacao_tipos.py`); Topografia, Foco e envoltória recalculados
  depois de desconectar, sem esmaecer, e a coluna Voluntário em "—" nos dois
  níveis (`test_fluxo_gravacao.py`); "Amostras" escondida gravando a 1536 px
  em EEG e a 1536-1600 px em EMG e Multimodal (`test_modo_simples.py`). O
  `test_topografia.py` confere que o dado novo não refaz o lugar dos nomes e
  que um ângulo novo refaz. Custo da Topografia medido em 20 rodadas de
  mediana de 15, antes e depois (ver Corrigido). Lote de tradução `ult` (2
  textos novos nos 8 idiomas, `ferramentas/trad/aplicadas_naolancado_ult/`).
  Bateria, um processo por vez, offscreen: `py_compile` ok; os 16 testes de
  `testes/` passam (101, 31, 26, 18, 75, 74, 49, 166, 51, 29, 31, 129, 54, 69,
  51 e 30, o `test_vazamento_idioma.py` por último); `teste_codigo.py` 69/69;
  `smoke_nivel.py` com rc=0 e stderr vazio nos 10 casos (no avançado, 2 de 54
  controles "ui" ocultos, antes 3: a telemetria do cabeçalho passou a caber);
  `verif_fluxo.py` 32/32 no simples e 29/29 no avançado; `varre_sem_tr.py`
  acha 0 destino de tela sem `tr()`.

- Últimos acertos, etapa pacote: os dois manuais não foram regerados, porque
  nenhuma correção desta rodada muda o que eles descrevem (o Manual do Usuário
  e o Técnico não falam da coluna Voluntário do Offline, do que a Topografia
  faz ao desconectar nem do nome das colunas do data.csv, cujo formato não
  mudou; as fichas de Piscadas e PERCLOS saem do catálogo do ROA.py, cujo
  texto não mudou, e continuam certas: a piscada é a deflexão que volta à
  linha de base, e o PERCLOS conta só eventos acima de 150 ms). O ROA.zip e a
  pasta de publicação foram regerados com o ROA.py e este CHANGELOG. Bateria
  final, um processo por vez, offscreen, com o ROA.py inalterado (mesmo
  SHA-256 antes e depois): `py_compile` ok e os 16 testes de `testes/` passam,
  992 verificações (101, 31, 26, 18, 75, 81, 49, 166, 52, 29, 31, 129, 54, 69,
  51 e 30, o `test_vazamento_idioma.py` por último), stderr vazio em todos;
  Topografia de 64 canais a 19,3 ms (2D), 18,2 ms (domo) e 18,6 ms
  (tomografia) por quadro de dado novo (teto 35 ms).

### Conhecido
- No nível Completo (pesquisa), o bloco "Detalhes técnicos" do relatório de
  EEG escreve os nomes das bandas em inglês ("Banda dominante: Alpha",
  "Delta=… Theta=… Alpha=… Beta=… Gamma=…", "Mu só nos canais
  sensório-motores") num PDF em português; as figuras e o quadro "Como ler
  este relatório" já saem em português. Visto na foto do item 0 do guia de
  imagens ao fechar o pacote; o ROA.py não foi alterado nesta etapa (fica
  para a próxima correção: usar `rotulo_banda` também nesse bloco).
- Trocar o **tamanho da letra** com a janela aberta refaz a folha de estilo
  do aplicativo inteiro, como a troca de tema (~10 s numa janela com todas
  as abas montadas); a escolha fica salva e na próxima abertura já vale
  desde o início. Acima de 125% a barra de ação e o cabeçalho (pílulas e
  selos) param em 125% (ver Adicionado e a etapa acerto em Corrigido); no
  Completo, com a telemetria do cabeçalho visível, a 150% em 1366 px o
  cabeçalho responsivo esconde amostras, g e Δt como já fazia abaixo de
  1500 px. A perda de amostras que essa troca causa fora da gravação deixa
  de ficar acusada na pílula de sinal (a conta recomeça na troca).
- As fontes das faixas de referência do relatório (Bentivoglio et al.,
  1997, para as piscadas por minuto; American Heart Association, para a
  frequência cardíaca em repouso) foram escolhidas nesta etapa e precisam da
  confirmação do autor antes de publicar.
- Gravação de olhos feita ANTES desta etapa não tem
  `report_channels.eog_threshold`: o PDF conta as piscadas com o detector do
  módulo (`eog_piscadas`, limiar adaptativo) e pode diferir do número que a
  aba Olhos mostrou ao vivo; o próprio PDF diz qual critério usou. Nas
  gravações novas a tela e o PDF usam o mesmo critério.
- A parte de EMG do relatório (e o PDF de EMG) passou a ter 2 páginas: as
  figuras do envelope e das barras vão para a página seguinte na largura
  útil em vez de ficarem espremidas no fim da primeira.
- **Sem script de build do `.exe` no projeto**: o `instalador.iss` citado em
  `COMO_PUBLICAR.md` não está na pasta. Os `qtbase_*.qm` dos botões padrão
  entram no pacote pelo hook de PySide6 do PyInstaller 6 (vão para
  `_internal/PySide6/translations`, onde `instala_tradutor_qt` procura); se
  um dia o pacote sair sem eles, a reserva em Python traduz só os botões
  padrão (OK, Cancelar, Sim, Não, Ignorar, Fechar, Salvar, Descartar...).
  Ao escrever o script, conferir que essa pasta vai junto.
- **Trocar de tema com a janela aberta ficou ~13% mais lento** (10,4 a 11,1 s
  contra 9,4 a 9,9 s, medido no offscreen com a janela recém-aberta): as regras
  do modo simples (5,6 mil de 12,3 mil caracteres da folha do app) ficam
  sempre na folha, presas a `nivelUi="simples"`, para a troca de nível custar
  0,4 a 0,7 s em vez de ~10 s. Ver KNOWN_ISSUES (MS-TEMA-QSS).
- Com 64 canais a Topografia 2D não escreve os valores nos discos e parte dos
  nomes fica só na dica de ferramenta (a 699 × 330 aparecem 50 de 61).
- Japonês e o ⚑ em russo e japonês saem em quadradinhos na captura offscreen
  (o motor FreeType do offscreen não carrega a fonte). O leiaute foi conferido;
  o texto precisa ser conferido numa sessão Windows real antes de publicar. As
  figuras dos manuais em japonês, chinês e russo saem da plataforma real, com a
  janela invisível, e a captura do guia troca o ⚑ para Segoe UI Symbol.
- Ficam em português de propósito: log e mensagens de exceção interna, o
  Estudo por Paciente exportado (CSV/PDF), metadados gravados (summary.json,
  sidecar BIDS, EDF) e os rótulos de fase gravados nos marcadores. O relatório
  PDF da sessão (`_generate_pdf_report`) sai no idioma da interface desde a
  etapa c da validação com leigos; a fonte Unicode de ru/zh/ja vem do
  Windows (`C:\Windows\Fonts`): noutro sistema sem essas fontes o PDF cai na
  Helvetica com o texto que ela consegue imprimir.
- Rótulo de fase ou nome de protocolo criado pelo usuário não tem tradução
  e aparece como foi escrito.
- Os valores `maximo`, `soma` e `valor` do bloco Normalizar e a variável `saida`
  do bloco de código continuam em português em todos os idiomas, porque são o
  que o usuário digita. As traduções trazem o sentido entre parênteses.
- A legenda do gráfico de envelope da aba Músculos ainda lista CH5 a CH17
  (ocultos) com placa de 8 canais; o painel de canais ao lado já mostra só
  CH1 a CH8.
- Documentos do pacote que o `sincroniza_pacote.py` não copia e que diferem
  da fonte: "Códigos de erro (E0XX).md" (o pacote traz a versão de 11/08,
  com o nome antigo no título), "Aviso — software de pesquisa.txt",
  "Licenças das bibliotecas usadas.md" e "Termo de uso.md/.txt". Precisam de
  uma decisão sobre qual versão vale antes de entrar na cópia automática.
  O `FORMATO_DADOS.md` já vai ("Formato dos arquivos de dados.md"). O
  ROA.exe e o `_internal/EEG_Data_Collector.py` (1.3.2) continuam de 11/08.
- Sessão gravada antes do acabamento não tem `hardware.channel_muscles`: no
  PDF os canais de EMG dela saem como "EMG CHn", não pelo músculo.
- Em modo único a aba Bio só troca de nome ("Músculos", "Coração", "Olhos")
  em português. Nos outros idiomas ela continua com o nome geral traduzido
  ("Bio (EMG/ECG/EoG)"), porque a troca compara o texto em português e os
  três nomes curtos não estão nos dicionários. Não vaza português, mas o
  recurso não funciona fora do português.
- O nome de cada coluna de canal do data.csv é o **rótulo do mapeamento**,
  não o tipo do sinal: com o mapeamento padrão, EMG, ECG, EoG e Multimodal
  gravam `Fp1_uV … O2_uV` (e `F7_uV … P4_uV` nos canais 9-16). Fica assim
  de propósito, porque é o formato que os scripts de análise já leem. O
  tipo real de cada canal está no summary.json, em
  `hardware.channel_types`, e o músculo de cada canal de EMG em
  `hardware.channel_muscles` (ver FORMATO_DADOS.md). O PDF já rotula pelo
  tipo ("EMG CH1", "ECG CH6").
- Piscada que coincide com uma sacada vertical (a sacada começa durante a
  piscada) pode não ser contada ou sair contada deslocada: nas 24
  simulações de 60 s, as 2 não achadas sem filtro e as 15 não achadas com o
  filtro do exame têm todas uma sacada a menos de 0,5 s. É o caso ambíguo
  também para quem lê o traçado.
- Num canal só, o olhar vertical que vai a outra altura e volta em até
  ~0,5 s tem o desenho de uma piscada e é contado como piscada (19 de 19
  com 0,4 s). Rajadas de EMG (mastigação, 80 µV por 300 ms) também passam:
  17 "piscadas" em 60 s sem filtro e 21 com filtro (antes desta correção,
  15 e 18).
- O PERCLOS só conta fechamento longo (0,5 a 2 s) quando há ao menos 3
  piscadas normais na gravação para servir de régua: quem só fecha os olhos
  longamente, sem piscar, sai com PERCLOS 0. A aba Olhos ao vivo continua
  com o PERCLOS próprio dela (fração do buffer acima do limiar), que não é o
  mesmo número do PDF.

## [1.8.4] — 2026-09-12

### Adicionado
- **Manual Técnico em nove idiomas** (pt, en, es, it, fr, de, ja, zh, ru). O
  gerador ganhou um mecanismo de idioma (`MANUAL_LANG`, `texto_<lang>.py`,
  `INLINE` + `T()`), capturas e anatomia da janela refeitas por idioma, e o
  mesmo código emite os nove PDFs. Vão em `Documentação/Manual Técnico (xx).pdf`.
- **Manual do Usuário atualizado** nos nove idiomas: bloco de novidades
  1.8.0-1.8.4 no capítulo 1, Área Maker por modalidade (cap. 11), assistente
  com busca por método (cap. 17) e três capítulos novos — Estudo por Paciente,
  catálogo de métodos por modalidade (tabelas geradas do próprio catálogo) e
  Referências. O gerador original de 2025 tinha se perdido; o conteúdo foi
  recuperado do PDF publicado (`Manual_ROA/extrai_manual_antigo.py`) e
  reconstruído em `gera_manual_usuario.py`.

### Corrigido
- **Diálogos de erro (E001-E079) e FAQ do assistente saíam em português em
  qualquer idioma.** `error_info()` e o corpus da FAQ passam por `tr()`;
  263 textos traduzidos nos oito idiomas (pares título/mensagem dos 79 erros
  e as 37 perguntas da FAQ). A resposta sobre idiomas dizia "seis opções";
  são nove.
- Títulos dos capítulos de modalidade do Manual Técnico ficavam em português
  nas outras línguas (formatados antes da tradução).
- **Catálogo de erros em português com frases quebradas.** Ao gerar o
  catálogo, os valores variáveis viraram palavras genéricas e deixaram 14
  mensagens erradas ("nenhum dado chegou em algunss", "recebidos de a porta",
  "assumindo Hz", "(- Hz)", "O recurso o recurso"). Reescritas, com as
  traduções acompanhando.
- O diálogo de erro tinha "Erro" e "Detalhe técnico" fixos em português;
  passam por `tr()`.
- O assistente só abria a lista de guias com a palavra "guias"; agora aceita
  o pedido nos nove idiomas (guides, guías, Anleitungen, ガイド, 指南,
  руководства…), como os manuais traduzidos instruem.
- O nome da Área Maker tinha duas ou três traduções no mesmo idioma (em
  chinês a FAQ usava o nome da Bancada). Padronizado pelo texto do botão em
  interface, FAQ e os dois manuais.
- **Fórmulas e unidades dos 101 métodos, nomes e ações dos músculos do
  atlas, modelos prontos e métricas de receita, e tipos de fase do protocolo
  apareciam em português em qualquer idioma** — no cartão do método do
  assistente, no combo da Área Maker, na paleta de comandos (Ctrl+Shift+P),
  no rótulo de ação do músculo e nas
  fichas do Manual Técnico. 238 textos traduzidos nos oito idiomas (fórmulas
  com a matemática intacta e decimal no padrão de cada língua), e `tr()` nos
  pontos de exibição. A fórmula traduzida fica fora do índice da busca, que
  permanece como antes.
- Manual Técnico traduzido: a janela montada para ler a paleta de comandos
  devolvia a interface ao português, e tudo o que vinha depois dela (formatos,
  apêndices, catálogo de erros) saía em português nos oito idiomas.
- Manual do Usuário em japonês e chinês: rodapé com marcação crua e
  parágrafos justificados com buracos. Figuras dos manuais em cores
  indexadas: o volume de nove idiomas deixa de ter 83 MB.
- **A busca do assistente (F1) não respondia a perguntas em russo, japonês ou
  chinês.** `_help_norm` terminava em `[^a-z0-9 ]+` → espaço, o que apagava
  todo cirílico e todo ideograma: "как подключить устройство" virava só espaços
  e "フィルタの設定" virava " ". Como tokens, TF-IDF e casamento aproximado
  partem dessa normalização, o corpus já traduzido nunca era alcançado. A
  remoção de marcas combinantes ainda trocava ガ por カ e й por и. Agora a
  normalização mantém letras de qualquer escrita (`\w`, sem sublinhado), tira
  acento só de letra latina, converte largura cheia (ＥＭＧ, ？) e dobra ё → е.
  O texto latino sai idêntico ao de antes: nas 1860 perguntas comparadas
  (pt, en, es, de, fr), o top-3 da busca não mudou.
- **Japonês e chinês, que não separam palavras, são indexados por bigramas
  de caractere** (陷波滤波 → 陷波, 波滤, 滤波), o padrão de busca CJK sem
  dicionário. Siglas latinas coladas no texto (RMS, ERD, EMG) continuam
  tokens inteiros. O russo ganhou corte de flexão próprio
  (подключить/подключение → подключ), e a stoplist ganhou palavras de ru, zh
  e ja. As do japonês saíram da frequência medida no corpus (ください/です
  estavam em mais da metade dos documentos).
- Ajustes da busca para CJK: o desempate pelo título conta sequências de
  bigramas como palavras (サンプルエントロピー perdia para a MSE), o pedido de
  definição reconhece что такое/とは/是什么, e a guarda de assunto de fora
  exige que o 1º documento cubra metade dos caracteres da pergunta
  ("チョコレートケーキの作り方" achava a "COMポート" pelo pedaço "ート").
- O nome do método no idioma ativo conta como citação de método na cascata
  do diálogo (antes só o rótulo em português contava), e as pistas de
  modalidade aceitam ЭМГ/肌电/筋電 e afins.
- O código de erro não era reconhecido colado em texto CJK ("E001是什么错误"):
  `\b` não vê fronteira entre dígito e ideograma. A fronteira passou a ser só
  ASCII (`_HELP_CODIGO_ERRO`).
- O pedido do índice de guias passa pela mesma normalização
  (`_help_pede_guias`) e aceita pontuação e largura cheia ("ガイド？").

### Testes
- `test_traducao_erros_faq.py` (54 verificações): português do catálogo sem
  restos da geração, mensagens de erro e respostas da FAQ traduzidas nos oito
  idiomas, diálogo sem texto fixo e pedido de guias em cada língua.
- `test_traducao_listas.py` (69 verificações): fórmulas e unidades com
  palavras, músculos, ações articulares, modelos e métricas de receita e fases
  do protocolo traduzidos nos oito idiomas; cartão do método e paleta passando
  por `tr()`; símbolos das fórmulas preservados na tradução.
- `test_ajuda_idiomas_nao_latinos.py` (101 verificações): normalização das
  escritas e igualdade com a antiga no texto latino dos seis idiomas latinos,
  bigramas e siglas, radical russo, corpus no idioma ativo, os 101 métodos
  achados pelo nome traduzido em ru/ja/zh, perguntas reais ("фильтр notch",
  "ノッチフィルタ", "陷波滤波", "HRVとは"…), cascata, assunto de fora e
  pedido de guias. `test_ajuda_ranking.py` (26/26) e `test_ajuda_metodos.py`
  (31/31) seguem passando.

### Conhecido
- As palavras-chave curadas de cada FAQ (`k`) existem só em português, então
  uma pergunta longa em outro idioma tem menos termos para casar. Exemplo:
  "как проверить импеданс электродов перед записью" não traz a FAQ de
  impedância entre as três primeiras.

## [1.8.3] — 2026-09-12

### Adicionado
- **42 métodos de uso corrente na literatura de 2021-2026**, com foco em EMG
  (13), depois EEG (13), ECG (11) e EoG (5). Cada um com fórmula, unidade,
  roteiro, referência de origem e — novidade — `refs_extra`: a evidência
  recente (revisão, replicação, toolbox) de que o método é de uso corrente,
  que a aba Referências e agradecimentos passa a creditar também. 46
  referências novas, todas conferidas no Crossref (dois DOIs que eu tinha de
  memória estavam errados e foram trocados antes de entrar).
  - EMG: latência de ativação (Hodges & Bui), inclinação da MDF (Merletti),
    coerência intermuscular beta (Farmer; revisão 2023), pausas musculares e
    tempo em repouso (Veiersted; replicação 2024), APDF P10/P50/P90 (Jonsson),
    entropia fuzzy (Chen), taxa de subida RER (Aagaard), inclinação do RMS
    para a JASA (Luttmann), correlação cruzada de envelopes e atraso
    (Nelson-Wong).
  - EEG: PLV, PLI, wPLI, ciPLV, dPLI, ImCoh, AEC ortogonalizada (conectividade
    robusta à condução de volume), entropia multiescala, índice de
    engajamento β/(α+θ), taxa de surtos beta (Shin), Higuchi e SampEn para
    EEG, e o crédito ao Gratton pela regressão ocular que o ROA já fazia.
  - ECG: FC média, índice de estresse de Baevsky, capacidade de desaceleração
    (Bauer; população geral 2024), fragmentação da FC (PIP), SampEn e MSE dos
    RR, % de ectópicos, kSQI e pSQI de qualidade, CSI e CVI de Toichi.
  - EoG: duração das piscadas, AVR de Johns, fixações por I-DT (duração e
    taxa), movimentos oculares lentos (SEM).
- Motor de receitas aceita métricas de PAR novas (coerência, correlação,
  conectividade) e o campo `cvm` (µV) para normalizar em %CVM.
- Medida do intervalo QT pelo método da tangente: o QTc estava no catálogo
  sem ramo no motor.

### Corrigido
- **Métrica catalogada sem implementação devolvia o desvio padrão em
  silêncio.** "% da CVM" e "QT corrigido" estavam na Área Maker e o motor
  devolvia std(sinal) com o rótulo errado na tabela. O fallback agora avisa,
  a Área Maker mostra o aviso, e as duas métricas ganharam ramo.
- **Ranqueamento da ajuda com 101 métodos.** Cartões irmãos se citam no
  roteiro ("compare com a inclinação da MPR") e a busca por nome errava o
  cartão. Três regras: o título pesa mais que o corpo (por palavra, a partir
  de duas); a expansão por sinônimo vale metade e não se aplica quando a
  pergunta nomeia um método; e a pista de modalidade não penaliza um cartão
  cujo título casa com três ou mais palavras. 101/101 nomes de método voltam
  no próprio cartão (tolerância: o par MPR).
- TDPSD (Khushaba 2014) foi implementado e RETIRADO antes de entrar: com a
  normalização λ do artigo, os descritores ficam ~0 para qualquer sinal — é
  um vetor para classificador, não um escalar. Fica registrado para não ser
  proposto de novo.

### Testes
- `test_metodos_2026.py`: 70 checagens de resposta conhecida (onset a 392 ms
  de um evento a 400 ms, DC = 15 ms exato num padrão determinístico, PIP de
  67,8% em RR aleatório, QT ≈ 390 ms de uma onda T gaussiana…). Bugs que o
  teste pegou antes do enxerto: onset com limiar do envelope suavizado
  (falso positivo em repouso), wPLI por bins diluído numa fonte estreita, SEM
  na posição em vez de na velocidade, AVR inflada por derivar ruído cru.
- 207 textos novos traduzidos nos oito idiomas (1 664 linhas). Suíte total:
  235 checagens.

## [1.8.2] — 2026-09-10

### Adicionado
- **Manual Técnico do ROA**, com todas as funcionalidades, adotado junto ao
  Manual do Usuário. 75 páginas, 27 figuras e 24 tabelas: as 23 telas uma a
  uma com a captura da janela real, ficha completa dos 59 métodos (fórmula,
  unidade, aplicação, roteiro e referência), Área Maker, protocolo, arquivos
  gerados, menus, atalhos, os 40 comandos da paleta, formatos de entrada e
  saída, e apêndices com as 35 referências em ABNT, os 79 erros catalogados,
  o glossário e os atlas. Vai no pacote como `Manual Técnico.pdf`, ao lado de
  `Manual do Usuário.pdf`.
- O manual é **gerado a partir do próprio software**: `Manual_Tecnico/` traz
  o harness de capturas, o extrator da anatomia das abas e o gerador do PDF.
  As tabelas de referência saem de `CATALOGO_METODOS`, `REFS_METODOS`,
  `ERROR_CATALOG`, `HELP_*` e `RECIPE_*`, então não têm como divergir do
  código.
- O PDF sai com sumário paginado e 105 marcadores de navegação.

### Corrigido
- **O assistente respondia outra pergunta.** "MPR fadiga EMG" recebia uma
  explicação sobre número de trials em imagética motora, e "como medir fadiga
  muscular por EMG" recebia uma aula de remoção de artefato por ICA. A busca
  estava certa nos dois casos — o cartão correto era o primeiro resultado.
  Quem errava era a cascata do diálogo: o consultor metodológico pontuava por
  contagem de palavras e vencia com palavra de duplo sentido ("fadiga" está
  no texto sobre trials; "EMG" e "muscular", no texto sobre artefato de EEG).
  Agora um acerto direto da busca só perde para o consultor quando ele pontua
  alto e a pergunta não é de outra modalidade.
- **Queixa de problema volta guia, não ficha de método.** "o sinal está cheio
  de ruído, o que faço?" caía num cartão de SSC, com o guia "Deixar o sinal
  limpo antes de gravar" em segundo lugar. A promoção do guia só vale quando
  a pergunta não cita nenhum método pelo nome — promover sempre fazia "SDNN
  ECG" cair no guia de HRV em vez da ficha do SDNN.

### Testes
- `testes/test_ajuda_ranking.py` (26 checagens): fixa a fonte de resposta
  esperada para 20 perguntas e confere que digitar o nome de qualquer um dos
  59 métodos devolve o cartão daquele método. Suíte agora com 165 checagens.

## [1.8.1] — 2026-09-10

### Adicionado
- **Os 59 métodos, seus guias e a aba Referências passam a falar os nove
  idiomas.** 315 textos novos traduzidos para inglês, espanhol, italiano,
  francês, alemão, japonês, chinês e russo — 2 520 entradas. Inclui rótulo,
  aplicação e passo a passo de cada método, além da interface da aba
  Referências e dos cartões do assistente.
- `ferramentas/coleta_faltantes.py` varre o ROA por AST e lista o que ainda
  não tem tradução; `ferramentas/aplica_trad.py` confere marcadores `%d`,
  tags HTML e traduções esquecidas ANTES de gravar, e recusa a gravação
  inteira se achar um problema.
- Guia ilustrado da MPR em PDF, na área de trabalho, com as telas reais e as
  figuras que explicam o deslocamento da banda média no Brasil.

### Corrigido
- **A Área Maker mostrava português com a interface em outro idioma.** O combo
  de métricas montava os itens com o rótulo cru do catálogo, sem passar por
  `tr()`. O mesmo acontecia na lista de métodos da aba Referências.
- **Nove rótulos do formulário da Área Maker nunca haviam sido traduzidos** —
  "Nome da receita:", "Recorte", "Pré-filtro", "Baseline p/ ERD%" e outros
  saíam em português em todos os idiomas, desde antes desta versão. O valor
  padrão do campo de nome também.
- O guia da MPR trazia `s⁻¹`, que a fonte do PDF não possui e desenhava como
  caixa; e a legenda de uma figura afirmava o contrário do que o gráfico
  mostrava.

### Corrigido — auditoria de idioma na janela inteira
Uma varredura dos 10 108 textos da janela com a interface em japonês achou
oito vazamentos ANTERIORES a este trabalho, todos corrigidos:
- Combo de modo de aquisição ("Hardware (porta COM real)", "Simulação",
  "Playback") e os tipos de painel do Layout Custom saíam em português.
- **`tr()` chamado em nível de módulo congela o português.** Três entradas de
  `PROTOCOL_PHASE_TYPES` traduziam no import, quando o idioma ainda é `pt`, e
  o texto nunca mais mudava. A tradução passou para o momento da exibição.
- Combos de músculo, de tipo de canal e de tipo de fase exibiam o texto que
  ERA TAMBÉM a chave gravada no config. Agora exibem `tr(chave)` e guardam a
  chave em `userData` — a interface fala japonês e o arquivo de configuração
  continua em português, que é o que o código indexa.

### Testes
- `testes/test_traducao_metodos.py` (51 verificações). A parte decisiva lê o
  texto do PRÓPRIO WIDGET, e não o dicionário: foi exatamente essa lacuna que
  deixou o vazamento da Área Maker passar na primeira rodada.
- `testes/test_vazamento_idioma.py` (8 verificações) abre o app em japonês,
  percorre as 22 sub-abas e varre todo widget atrás de português sobrevivente.
  Inclui a checagem de que os combos de chave separada continuam gravando a
  chave, e não a tradução — senão o config vira lixo ao trocar de idioma.

## [1.8.0] — 2026-09-10

### Adicionado — separação por modalidade
- **Catálogo de métodos** como fonte única de verdade: cada método declara a
  que modalidade pertence, sua referência, fórmula, aplicação e guia de uso.
  A mesma tabela alimenta o filtro da Área Maker, os guias do assistente e a
  aba Referências — impossível o programa calcular algo que não esteja
  creditado, e impossível creditar o que ele não calcula.
- **Área Maker com seletor de Modalidade.** Antes, quem analisava EMG via
  "ERD% de imagética motora" na lista de métricas e um seletor de bandas em
  "Alpha". Agora cada modalidade mostra só o que é seu: 26 métodos em EMG,
  17 em EEG, 9 em ECG, 6 em EoG.

### Adicionado — métodos de EMG
- **MPR média/baixa e alta/baixa** sobre distribuição tempo-frequência de
  Cohen classe B [Karthick & Ramakrishnan 2016; Barkat & Boashash 2001], com
  a inclinação da regressão como índice de fadiga. A banda média é deslocada
  automaticamente para fora da rede local: em 50 Hz reproduz o 55-95 Hz do
  artigo, em 60 Hz usa 65-95 Hz, seguindo a mesma justificativa dos autores.
- Conjunto clássico de tempo: SSC, WAMP, MYOP, detector logarítmico, DASDV,
  AAC e inclinação do MAV [Hudgins 1993; Phinyomark 2012].
- Entropia amostral [Richman & Moorman 2000] e dimensão fractal de Higuchi
  [Higuchi 1988].
- **Sinergias musculares por NMF** [Lee & Seung 1999; Torres-Oviedo & Ting
  2007], com curva de VAF e critério de 90%.
- **Normalização por CVM** [SENIAM; Merletti & Parker 2004] — a única forma
  de comparar amplitude entre pessoas e entre dias.

### Adicionado — métodos de EEG
- **Separação periódico / aperiódico** [Donoghue et al. 2020]: expoente e
  deslocamento do 1/f, e potência da banda ACIMA do fundo aperiódico.
- Parâmetros de Hjorth [Hjorth 1970], entropia de permutação [Bandt & Pompe
  2002], complexidade de Lempel-Ziv [Lempel & Ziv 1976], DFA [Peng et al.
  1994], acoplamento fase-amplitude de Tort [Tort et al. 2010], assimetria
  alfa frontal [Davidson 2004] e frequência de borda espectral.

### Adicionado — métodos de ECG e EoG
- Detecção de QRS de Pan-Tompkins [Pan & Tompkins 1985]; SDNN, RMSSD e pNN50
  [Task Force 1996]; Poincaré SD1/SD2 [Brennan et al. 2001]; QTc de Bazett e
  de Fridericia; respiração derivada do ECG [Moody et al. 1985] e arritmia
  sinusal respiratória.
- Detecção de sacadas por limiar robusto [Engbert & Kliegl 2003], sequência
  principal [Bahill et al. 1975], piscadas, taxa de piscadas, PERCLOS
  [Wierwille & Ellsworth 1994] e estabilidade da fixação (BCEA).

### Adicionado — aba Referências e assistente
- **Sistema → Referências**: 33 referências sustentando 59 métodos, em ABNT,
  com DOI clicável, filtro por modalidade, busca que varre também o texto de
  aplicação, e botão para copiar a lista pronta para um trabalho. Inclui
  bibliotecas de terceiros com licença, normas seguidas e agradecimentos.
- **Assistente de ajuda com um guia por método** (59 cartões gerados do
  catálogo): o que mede, passo a passo, avisos, fórmula, onde fica no
  programa e a referência com DOI.
- Ranqueamento da busca melhorado: bônus de título proporcional à raridade
  do termo (nome próprio de método agora vence palavra comum) e desempate
  por modalidade citada na pergunta.

### Corrigido
- **ERD levantava NameError sempre que era pedido pela receita.** A linha da
  linha de base usava uma variável `chan` que não existe naquele escopo —
  ou seja, a métrica central de imagética motora estava quebrada no motor de
  receitas.
- A busca da aba Referências não varria o texto de aplicação: procurar
  "fadiga" não achava a MPR nem o Dimitrov.
- A árvore do Estudo por Paciente cortava o nome do arquivo.

### Testes
- `testes/` passa a viver ao lado do código: a suíte anterior morava em pasta
  temporária e foi apagada pelo sistema.
- `test_metodos_modalidades.py` (30 verificações) e `test_ajuda_metodos.py`
  (31). O DSP de cada modalidade foi validado contra sinais de resposta
  conhecida antes de entrar: EMG 31/31, EEG 23/23, ECG e EoG 28/28.

## [1.7.1] — 2026-08-22

### Adicionado
- **Estudo por Paciente** (Analisar → Estudo por Paciente): analisa uma pasta
  inteira de gravações e organiza a saída por paciente e, dentro de cada
  paciente, por data. Nasceu de um pedido concreto — resultados que chegavam
  reunidos num bloco só e precisavam ser acompanhados pessoa a pessoa ao longo
  do tempo.
  - Leitor de CSV clínico com cabeçalho em comentário e coluna de fase
    (formato do Symbios/MyoSym e, de modo geral, qualquer exportação com
    coluna de estado). Paciente, data, hora, exercício e grupo saem do
    cabeçalho, do nome do arquivo ou da pasta, nessa ordem de preferência.
  - Limpeza com o notch do próprio ROA na frequência de rede detectada no
    sinal, mais os harmônicos, antes de qualquer medida.
  - Métricas pelo motor de receitas (`run_recipe`): RMS, MAV, pico a pico,
    iEMG, comprimento de onda, cruzamentos por zero, MDF, MNF, Dimitrov
    FInsm5 e tempo ativo por TKEO — escolhidas na própria aba.
  - Agregação **bloco a bloco**: cada repetição e cada repouso entram
    separados e o valor da sessão é a mediana entre eles. Concatenar os
    trechos criaria degraus artificiais no espectro e falsearia MDF e MNF.
  - **Veredito de qualidade por canal** (utilizável / marginal / não
    utilizável) a partir da razão ação/repouso, da fração do envelope forte
    dentro da ação e da potência na rede elétrica. O veredito acompanha cada
    número nas planilhas e nos relatórios, para que ninguém compare ruído de
    rede entre datas achando que compara ativação muscular.
  - Saída: uma pasta por paciente, uma subpasta por data, planilhas de
    resultados, de qualidade, de antes/depois e de evolução (uma coluna por
    data), mais relatório em PDF de cada data e do paciente inteiro, com
    figuras de sinal, envelope, mapa de qualidade e linha do tempo.
  - Planilhas com BOM, ponto e vírgula e vírgula decimal — o Excel em
    português abre com dois cliques —, sempre com Paciente e Data nas
    primeiras colunas, mesmo dentro da pasta do paciente.
  - Recusa gravar a saída dentro da pasta de origem: a varredura passaria a
    ler os próprios resultados.
- Aba disponível em todas as modalidades (EEG, EMG, ECG, EoG e Multimodal) e
  na paleta de comandos, nos nove idiomas do aplicativo.

### Corrigido
- A paleta de comandos não listava BCI Trainer (MI); passou a listar.

### Testes
- `test_estudo.py`: 54 verificações com dados sintéticos de dois sujeitos, um
  com surto muscular real e outro só com 60 Hz. O primeiro sai 32/32 canais
  utilizáveis (razão 19x), o segundo 0/32 — que é a discriminação que o
  veredito precisa ter.

## [1.7.0] — 2026-08-11

### Adicionado — a Bancada

A Área Maker ganhou um **editor de grafo**: em vez de preencher um formulário
(métrica + banda + canais), você **liga blocos por fios** e monta a análise
que o seu laboratório precisa.

- **14 blocos** em 6 categorias: fonte, tratamento de sinal (canais, recorte,
  passa-faixa, notch, envelope), medida (potência de banda, RMS,
  co-contração), combinação (razão entre tabelas, normalização, resumo
  estatístico), **código autoral** e resultado.
- **Portas tipadas.** Só encaixa o que faz sentido — e quando o programa
  recusa uma ligação, ele **diz o motivo**: "tipos diferentes: Sinal não
  encaixa em Tabela", "isso fecharia um ciclo", "essa entrada já está
  ocupada". Um editor que recusa em silêncio é pior que não ter editor.
- **Bloco de código em Python**: quando o que você precisa não existe pronto,
  escreva. O bloco recebe `entrada`, tem `np` e `scipy.signal` à mão e
  devolve `saida`. Vira parte do grafo como qualquer outro bloco.
- **4 exemplos prontos** que já rodam — alfa por canal, razão teta/beta,
  co-contração de pares e um com bloco autoral (fator de crista, para achar
  canal com artefato). Vale mais que documentação: abra, veja os fios e mexa.
- A bancada inteira salva em **.json** e reabre, com posições e ligações.
- Execução em **ordem topológica**, com detecção de ciclo. Bloco com ponta
  solta é **pulado com aviso**, não derruba o grafo — em bancada meio montada
  isso é normal.

**Sobre segurança:** o bloco de código roda **dentro do programa**, com os
seus arquivos ao alcance. Não é caixa-forte, e o programa diz isso na tela.
Por isso, ao **abrir uma bancada de outra pessoa** que contenha código, o ROA
**pergunta antes** de permitir a execução — e, se você recusar, o grafo roda
com aquele bloco bloqueado.

**Sobre licença:** a ideia de editor de grafo com portas tipadas é comum a
várias ferramentas da área (OpenViBE, Simulink, Node-RED). Esta implementação
foi **escrita do zero**, de propósito: o OpenViBE é AGPL-3 e o ROA é MIT —
aproveitar a arquitetura é livre, copiar código tornaria o ROA inteiro AGPL.

### Adicionado — isolar o ritmo mu
A pergunta era "dá para isolar os dados dentro das ondas mu?". Por frequência,
**não dá**: mu e alfa ocupam a mesma faixa de 8–13 Hz e nenhum passa-faixa
separa os dois. O que separa é onde aparecem, como reagem e em que frequência
exata — e a aba **ERS/ERD** passou a tratar os três.

- **Faixa em Hz editável** ao lado do seletor de banda. Mexer nela passa o
  seletor para *Personalizada*, para o rótulo nunca anunciar uma faixa
  enquanto a conta usa outra — e o sumário do resultado agora imprime a faixa
  efetivamente usada.
- **Detectar mu individual**: procura o pico desta pessoa nos trechos de
  repouso, sobre os canais sensório-motores, e centra a faixa nele. O pico é
  individual como a IAF; com uma janela fixa em 8–13, quem tem o pico em
  11,5 Hz perde metade da energia e o ERD sai subestimado. A busca **desconta
  a inclinação 1/f** do espectro — sem isso o "pico" cai sempre na borda de
  baixo da faixa.
  O limiar de "existe pico?" foi **medido, não estimado**: em 40 registros de
  30 s de ruído 1/f puro a saliência do maior pico ficou entre 1,2 e 2,03; com
  um mu realista (ruído de banda estreita, não senoide) o mínimo foi 8,1 já
  com 3 µV. O limiar ficou em 4,0. O primeiro palpite, 1,25, dava "pico
  encontrado" para ruído puro. Sem pico destacado o programa **mantém a faixa
  como estava** e diz que não achou.
- **Laplaciano (C3/Cz/C4)**: subtrai de cada canal central a média dos
  vizinhos, pela geometria 10-20. É filtro de *espaço*, não de frequência —
  aperta o mu no córtex sensório-motor e derruba o alfa posterior, que chega
  espalhado. Medido em sinal sintético: um componente de 10 Hz comum a todos os
  canais cai de 289 para 10 µV², enquanto o componente local de 11 Hz sobrevive.
- **Origem do ERD**: depois de calcular, o programa compara a queda nos canais
  centrais com a dos posteriores e diz se aquilo tem cara de **mu**, de **alfa
  posterior** (o caso do voluntário que fechou os olhos), de **misto**, ou se
  simplesmente **não houve reação**. Sem canal de uma das regiões, declara
  *indeterminado* em vez de comparar o que não foi medido. Essa verificação é a
  única resposta honesta para "é mu mesmo?".

Na sessão de imagética motora que acompanha o projeto, o veredito é "sem
reação": a mediana do ERD é **+41%** — ou seja, ERS, não ERD. O programa agora
diz isso em vez de rotular o resultado como mu.

### Adicionado — o assistente passou a guiar, não a apontar
O pedido veio de uma frustração real: *"fiz uma pergunta simples no bloco de
ajuda e ele não soube me guiar"*. Medindo o assistente com 16 perguntas escritas
como uma pessoa escreve, **8 devolviam resposta errada ou nada**: "meu eeg nao
conecta" caía num verbete sobre número de canais, "o que significa ERD?" caía no
catálogo de códigos de erro, "quero medir co-contração" caía na sequência de
tempo do protocolo, e "como ligo blocos na bancada?" não devolvia nada.

- **16 guias de solução.** Cada um tem *o que você terá no fim*, **passos
  numerados** com o caminho literal da interface, *o que costuma dar errado* e
  *se acontecer isso →* a saída. Cobrem primeira coleta sem hardware, placa que
  não conecta, limpar o sinal, gravar e conferir a sessão, exportar, figura de
  publicação, potência de banda, ERD/ERS, treinar BCI, antes × depois, atlas
  muscular, co-contração, HRV, Bancada, protocolo e atualizar sem perder dados.
- **Glossário de 36 siglas** (ERD, ERS, HRV, RMSSD, SDNN, DFA, HTI, TINN, ApEn,
  SampEn, CSP, LDA, MVC, MDF, MNF, PSD, CAR, BIDS, EDF, FIF, LSL, SSVEP, ERP…),
  cada verbete com o nome por extenso, o que é e **onde ver aquilo no programa**.
  *"O que é X?"* e *"como faço X?"* passaram a ser perguntas distintas: a
  primeira responde com a definição, a segunda com o procedimento.
- **A busca casa flexão de verbo.** Era o defeito de fundo: o índice comparava
  palavras inteiras, então "exporto" não encontrava "exportar" e "conecta" não
  encontrava "conectar".
- **Pergunta fora do assunto não recebe mais palpite.** "Qual a receita de
  brigadeiro?" casava com *Receitas de análise* — a palavra existe no índice. Se
  só uma palavra de uma pergunta de várias é conhecida, o encontro é
  coincidência e o assistente diz que não sabe.
- **Quando não sabe, mostra o que existe.** A resposta antiga pedia para
  reformular com outra palavra-chave, o que devolve o problema para quem já não
  sabia o que perguntar; agora entrega o índice dos 16 guias, clicáveis.
- **Pergunta de procedimento não é mais interceptada pela metodologia.** "O
  sinal está cheio de ruído, o que faço?" recebia uma aula sobre remoção de
  artefato por ICA *depois* da coleta. Guia e consultor agora são avaliados
  juntos: o guia responde **como**, e o **por quê** fica a um clique.

Medição final: **16/16** perguntas caem no guia certo em primeiro lugar, **6/6**
definições caem no glossário.

### Adicionado — Manual do Usuário completo, num só PDF, nos nove idiomas
`Manual_ROA/Manual_ROA_9_idiomas.pdf`: capa, índice de idiomas e os **nove
manuais completos em sequência**, cada um com o seu sumário e com as capturas
de tela feitas com o programa rodando **naquele idioma**.

- **19 capítulos, 43 mil caracteres, 42 figuras.** O corpo vem do
  `manual_usuario.tex` revisado pelo autor, convertido por um extrator que
  verifica o que perdeu: **96% de cobertura de palavras** contra o PDF
  publicado, e as 4% ausentes são capa, sumário e rodapé.
- **Seis capítulos novos** para o que entrou depois da v1.3.1 e não estava
  documentado: Bancada, mapa de co-contração, ECG/HRV, assistente com guias e
  glossário, integridade da gravação e idioma/tema/cores.
- **Todas as 42 figuras refeitas na v1.7.0.** A auditoria das capturas anteriores
  encontrou **13 figuras vazias ou na tela errada**: a calibração sem nenhuma
  impedância medida, o treinador de BCI dizendo "clique em Calibrar", a
  estatística guiada com "0 sessões", o ECG com "-- bpm" e sem traçado, o EoG
  com zero piscadas, a co-contração sem as retas de referência, o protocolo
  mostrando a tela de streaming UDP/LSL (aba errada, e as duas figuras
  idênticas entre si) e o núcleo C++ mostrando a aba de Configurações em vez do
  diálogo. Todas agora mostram o programa com dado real, calculado pelo código
  de produção.
- Cada idioma reconstrói o programa do zero para capturar: os rótulos são
  resolvidos na construção dos widgets, e trocar a língua depois deixaria
  metade da tela na anterior. O idioma vai gravado no `AppConfig` **antes** de
  a janela nascer — sem isso a janela reimpõe o português.

### Adicionado — Termo de Uso em inglês americano
`TERMS_OF_USE_EN.md`. Fora do português o programa passa a exibir esta versão
no aceite do primeiro uso: pedir aceite de um contrato que a pessoa não lê é
aceite de fachada.

- A tradução passou por **revisão adversarial seção a seção** — um revisor
  independente, instruído a *achar erro*, procurando obrigação que sumiu ou
  enfraqueceu, inversão de sentido, perda de ênfase em cláusula limitativa e
  falso amigo jurídico. Ele **alterou 3 das 16 seções**, entre elas a da LGPD
  e as Disposições Gerais.
- Regras que a tradução tinha de respeitar e respeitou (verificado no arquivo
  final): **LGPD não virou GDPR nem HIPAA** (0 ocorrências das duas), a lei é
  citada com número — *Law No. 13,709/2018* —, e "controlador"/"operador" foram
  para *controller*/*processor* com a referência ao artigo, preservando a
  distinção que o original faz entre o "Operador do Software" (quem opera o
  programa) e o "operador" da lei.
- Tem **cláusula de idioma prevalecente**: em caso de divergência, vale a
  versão em português. O arquivo em português continua no pacote.

### Corrigido — o resto da mistura de línguas
Fotografar a interface em nove idiomas expôs o que a varredura por código não
pegava, porque nenhum destes textos era argumento direto de um widget:

- **53 rótulos de eixo de gráfico** (`Tempo (s)`, `Amplitude`, `Potência`,
  `Frequência`…) iam direto para o `setLabel` do pyqtgraph e ficavam em
  português em qualquer idioma. Na captura em alemão, tudo estava traduzido
  menos o texto embaixo do traçado.
- **Textos de estado do cabeçalho e do rodapé**: "Pronto para gravar.",
  "● Sinal OK", "ATENÇÃO: modo SIMULAÇÃO ativo — sinais não são reais" e
  "Conectado em modo PLAYBACK".
- **A moldura do assistente**: "Você", "Consultor", "Aprofundar:" e os seis
  botões de atalho de tema. Os rótulos dos botões ficavam dentro do *iterável*
  de um `for` — o mesmo esconderijo que já havia deixado outras listas de fora.
- **Botões do editor de protocolo** ("+ Linha de base", "+ Ação muscular",
  "+ Repouso", "+ Aviso") e os combos de separador e de unidade de tempo do
  importador, pelo mesmo motivo.
- **Os rótulos que o atlas muscular desenha sozinho.** "Vista Frontal
  (anterior)", os nomes das regiões do corpo (Rosto, Pescoço, Peito, Abdômen,
  Coxa, Trapézio, Glúteo, Panturrilha…), a contagem de eletrodos e a legenda de
  qualidade são escritos no `paintEvent` com QPainter — não são argumento de
  widget nenhum. Foi a página do manual em japonês que denunciou: legenda em
  japonês, desenho do corpo em português. Junto com eles, mais três textos
  desenhados ("Arraste p/ girar", "Sequência vazia", "Mapeie músculos por
  canal").
- **Emblema do cabeçalho cortado nos idiomas de palavra longa.** "MODO
  SIMULAÇÃO" vira "SIMULATIONSMODUS" em alemão e "РЕЖИМ СИМУЛЯЦИИ" em russo;
  sem largura mínima, o Qt encolhia o rótulo e o aviso mais importante da tela
  aparecia truncado. A largura mínima passou a vir da métrica da fonte.

O dicionário foi de 839 para **1302 chaves por idioma**, com zero string de
interface sem tradução nos oito idiomas.

### Corrigido
- **O zoom do atlas muscular ampliava o texto junto com o corpo.** O
  `paintEvent` aplicava a transformação de zoom ao desenho inteiro, então no
  enquadramento do braço (2,6×) o rótulo de um eletrodo ficava quase três vezes
  mais largo, atravessava a figura e saía cortado na borda; o cabeçalho da
  vista e a legenda de qualidade cresciam do mesmo jeito, e a silhueta ampliada
  ainda passava por cima do título. Agora só a **geometria do corpo** escala:
  marcador, número, rótulo, títulos e legenda mantêm tamanho de leitura e são
  posicionados convertendo a coordenada anatômica para pixel. Junto vieram três
  correções que o zoom tornou visíveis:
  - eletrodo **fora do quadro** não é mais desenhado (antes o rótulo dele era
    empurrado para a borda, sugerindo um eletrodo que não estava ali);
  - dois rótulos próximos **se desviam** em vez de escrever um sobre o outro;
  - o cabeçalho e a legenda passaram a ser desenhados por último, sobre um
    fundo translúcido, para a silhueta ampliada não os cobrir.
- **O expoente da sequência principal do EoG era exibido mesmo sem base para
  estimá-lo.** O ajuste `V ≈ k·A^b` é a inclinação de uma reta em log-log; se
  todas as sacadas registradas têm amplitude parecida, não há alavanca para
  estimar inclinação nenhuma. O `polyfit` devolvia um número, avisava "poorly
  conditioned" — milhares de vezes no log de uma sessão — e o rótulo mostrava
  esse número como se fosse medida. Agora exige 8 sacadas e uma faixa mínima
  de amplitudes; abaixo disso mostra o que falta, como o painel de HRV.
- **O botão "Avançar" do assistente de primeiro uso voltava ao português.** Ele
  nascia traduzido, mas o texto é reescrito a cada troca de página e essa
  reescrita não passava pelo `tr()`. Numa captura do assistente em inglês,
  "Decline and exit" e "Back" apareciam traduzidos e "Avançar" não.
- **`paintEvent` do atlas podia morrer com `KeyError`.** A leitura do canal do
  eletrodo era `e["channel"]`; um dicionário sem esse campo derrubava o
  desenho — e falha dentro de `paintEvent` não vira erro visível, vira um
  widget que simplesmente para de se redesenhar.
- **A tecla F1 nunca existiu.** Três textos de ajuda diziam "Pressione F1" e a
  tabela de atalhos ainda a anunciava como "Sobre o aplicativo" — mas nenhum
  `QShortcut` a registrava: quem apertava não recebia nada. F1 passou a abrir o
  assistente, que é o que a ajuda promete. A tabela também omitia
  <kbd>Ctrl+Shift+P</kbd>, <kbd>Ctrl+P</kbd> e <kbd>F11</kbd>, que existiam e
  não tinham outro lugar onde ser descobertos; agora ela é montada a partir dos
  atalhos realmente registrados, e um teste compara as duas listas.
- **Nome antigo vazando em texto ao usuário.** A saudação do assistente ainda se
  apresentava como "Consultor OpenBionica", e a base de conhecimento dizia "No
  OpenBionica: Analisar → …". Corrigidas 13 ocorrências no programa e 70 nos
  documentos. O nome do **repositório** e o do **arquivo legado**
  (`OpenBionica.py`) continuam intactos de propósito — o atualizador automático
  busca por eles, e o CHANGELOG registra história, não estado atual.
- **O painel avançado de HRV nunca executou.** LF/HF, HTI/TINN, Poincaré, DFA e
  ApEn/SampEn eram calculados sobre os intervalos que cabem na janela de
  análise de 10 s — cerca de 11 batimentos a 75 bpm. Os portões herdados disso
  eram aritmeticamente inalcançáveis: o `>= 32` do bloco não-linear exigiria
  198 bpm e o `>= 20` do espectral exigiria 126 bpm, enquanto o aviso
  `< 120 RR` nunca podia ser falso, porque em 10 s cabem no máximo 32 RR.
  Numa sessão de 5 minutos simulada com HRV conhecida, **cinco dos seis blocos
  não escreveram uma única vez**, e o SDNN exibido saía 41% abaixo do real.
  Agora os picos R entram numa série da **sessão inteira** (em tempo absoluto,
  com deduplicação entre janelas sobrepostas) e cada índice tem seu próprio
  mínimo de RR — abaixo dele o painel mostra quanto ainda falta em vez de um
  número sem significado. Ao fim dos mesmos 5 minutos: LF/HF 2,64, HTI 8,1,
  TINN 148 ms, SD1 12,7 / SD2 38,5, DFA α1 1,12 / α2 0,74, ApEn 0,874,
  SampEn 1,627 — e SDNN de 28,7 ms contra 28,7 ms reais.
- **O pico R era localizado no envelope, não na onda R.** O detector devolvia o
  máximo da média móvel de energia, que marca a *região* do QRS. O viés é quase
  constante e some na diferença, mas o jitter de ±19 ms entrava em quadratura e
  inflava o **RMSSD** — o índice vagal de referência — de 18 ms reais para
  52 ms. O pico passou a ser refinado no sinal filtrado (±60 ms, por valor
  absoluto, para tolerar derivação com R negativa), e batimentos na cauda da
  janela só entram na série depois de sair da zona de transitório do filtro.
  RMSSD medido: **18,0 ms contra 18,0 ms reais**; jitter de 0,6 ms.
- **DFA com escalas pareadas erradas.** A regressão log-log usava
  `scales[:len(F)]`, o que só estaria certo se as escalas descartadas fossem
  sempre as últimas — uma escala pulada no começo deslocava todo o pareamento
  e enviesava o expoente α. Um `F(n)` igual a zero (série constante) também
  fazia `log10(0)` contaminar a regressão e devolver NaN sem aviso.
- **Custo dos índices não-lineares.** Acumular a série tornaria ApEn/SampEn
  (O(N²) em Python) um travamento da interface: 0,37 s com 200 RR, 6,91 s com
  800. Ficaram com teto de amostras e recálculo a cada 10 s — refresh medido em
  10,2 ms, dentro do orçamento de 50 ms do timer de 20 Hz.
- **Taxa de piscadas com erro de ordens de grandeza**, que travava o indicador
  de Estado de Alerta em FADIGA permanentemente. Eram quatro defeitos
  encadeados: a deduplicação comparava instantes no eixo do buffer circular,
  a lista de piscadas crescia sem limite, o denominador da taxa era o vão
  entre marcadores em vez dos 60 s prometidos, e a ausência total de piscadas
  não era tratada.

### Verificado e NÃO confirmado
Dois achados da crítica externa **não se reproduzem** no código atual —
verificados rodando o código de produção, não por leitura:

- **"O espectrograma satura inteiro (níveis fixos em [−80, 0] dB)"**: hoje ele
  usa auto-escala por percentil p2–p98 recalculada a cada quadro (medido:
  −17,2 a +16,4 dB, com 96,7% da imagem dentro da faixa) e **tem barra de
  cor**. Os níveis fixos não existem mais.
- **"O treinador de BCI exibe acurácia de treino — 100% em ruído branco"**: o
  rótulo diz *"Acurácia (5-fold CV)"*, traz o nível de acaso e emite veredito.
  Alimentado com **ruído branco puro em 30 sementes**, exibe média de **51%**
  (chegando a 100% em 1 semente, coerente com α=0,05). A covariância do CSP
  **já é normalizada pelo traço**. O modo de falha descrito existiria se o
  rótulo mostrasse treino — e ele não mostra.

## [1.5.1] — 2026-08-10

Ataca a **perda de amostras** apontada na crítica da v1.4.0. A causa medida
não foi a que o relatório supunha.

### O que a medição mostrou

A crítica atribuía a perda ao desenho dos gráficos ("`_on_sample` roda na
thread da interface a 250 Hz"). Reproduzi o experimento com a janela visível
e laço de eventos real, descartando a rodada de aquecimento e alternando a
ordem dos cenários. Resultado:

| | antes | depois |
|---|---|---|
| Sem gráfico na tela | 236,6 Hz (perda 5,4 %) | **250,6 Hz** |
| Com Tempo Real desenhando | 236,3 Hz (perda 5,5 %) | **250,6 Hz** |
| Primeiros 10 s de uso | 109,5 Hz (perda 56 %) | **250,1 Hz** |

**A aba aberta não fazia diferença** (0,1 % entre os dois cenários). E o
consumidor — filtrar, gravar no buffer, escrever a linha do CSV, UDP e LSL —
custa **44 µs por amostra, 1,1 % do orçamento de 4000 µs** a 250 Hz. Não era
ele o gargalo.

### Corrigido

- **A cadência de aquisição não se sustentava.** O laço do simulador, medido
  **sem consumidor nenhum**, já rodava a 242,9 Hz: `time.sleep` nunca acorda
  antes do prazo e quase sempre acorda depois, e dormindo um período por volta
  o atraso **acumula**. Entrou a classe `_Marcapasso`, que mira **prazo
  absoluto** (`início + n·dt`) em vez de dormir um período por vez, de modo
  que um atraso pontual é absorvido na volta seguinte. Vale para Simulação e
  Playback. Medido: 250,00 Hz, desvio −0,00 %.
- **Uma travada longa virava rajada.** Se o sistema operacional segurasse o
  processo (janela arrastada, disco ocupado), o laço tentava recuperar todo o
  atraso de uma vez e despejava dezenas de amostras com carimbos amontoados.
  Agora, atraso acima de 0,25 s **reancora no presente** — perder a cadência
  por um instante é melhor que falsificar a linha do tempo.
- **A penalidade dos primeiros 10 s desapareceu** junto, pelo mesmo motivo: o
  atraso do início não é mais arrastado para o resto da sessão.
- **Carimbo do CSV com resolução de microssegundo** (era 0,1 ms). Duas
  amostras muito próximas arredondavam para o mesmo texto e reapareciam como
  timestamp duplicado — o defeito que cegava a medição de taxa.

### Nota honesta sobre hardware real

Estas medições são do Modo Simulação, que é onde a crítica também mediu. Com
placa real quem produz é a porta serial, não este laço, então o marcapasso não
se aplica a ela — o que vale ali é a folga do consumidor (1,1 %), que é
grande. Não tenho como reproduzir o cenário com hardware aqui.

## [1.5.0] — 2026-08-10

Primeira leva de correções da **crítica técnica externa da v1.4.0** (106
achados, 62 graves). Esta versão ataca o eixo do relatório: **o número na tela
não correspondia ao que aconteceu no eletrodo**.

### Corrigido — integridade do dado

- **Relógio monotônico, carimbado na origem.** Cada amostra passa a levar o
  instante em que foi produzida (`time.perf_counter`, na thread de
  aquisição). Antes o tempo era lido na thread da interface com
  `time.time()`: amostras que chegavam em rajada dividiam a mesma leitura
  (**66 % dos intervalos davam exatamente zero**) e um ajuste de relógio no
  meio da coleta reescrevia o eixo do tempo do experimento.
- **A mesma sessão dava três durações diferentes** — 66 s na tela, 148 s no
  CSV e 692 s no `summary.json`. Três causas, todas corrigidas:
  - o `t=0` era o **Conectar**, não o **REC** (por isso 692 s);
  - o leitor offline media a taxa pela **mediana** das diferenças entre
    timestamps; com 66 % de zeros a mediana era 0, a medição falhava em
    silêncio e ele caía no valor nominal (por isso 66 s). Agora a taxa vem do
    **vão total ÷ nº de intervalos**, que é imune a repetições;
  - a duração agora é a **do dado** (primeira à última amostra), com a mesma
    fórmula nos dois lados — as três fontes concordam por construção, não por
    coincidência.
- **Taxa efetiva declarada e conferida.** O `summary.json` ganhou
  `sample_rate_ok` e um campo `aviso` que dispara quando a taxa efetiva se
  afasta mais de 5 % da nominal. Antes ele gravava `23,876 Hz` para um EEG
  sem que nada sinalizasse o absurdo.
- **Marcadores apontavam para fora do arquivo.** O índice gravado no
  `events.csv` era o total de amostras desde a *conexão*: um evento na linha
  718 saía registrado como 17.087. Qualquer script que alinhasse eventos por
  índice errava em silêncio. Agora o índice é a linha do `data.csv`.
- **"● Sinal OK" verde com o contador de perdas em 90 mil.** A integridade da
  aquisição passou a ter **precedência** sobre a qualidade do eletrodo: a
  partir de 2 % de perda o indicador vira alerta e explica o efeito (eixo de
  tempo comprimido, frequências deslocadas).

### Corrigido — honestidade do arquivo e posicionamento

- **Sessão do Modo Simulação era assinada como hardware real.** O
  `summary.json` trazia o bloco completo do amplificador (ADS1299, 24 bits,
  4,5 V) e um SHA-256 atestando um arquivo que nunca tocou um eletrodo. Agora
  há `data_source` (`synthetic`/`replay`/`hardware`), `is_real_signal`, e o
  bloco do amplificador **só aparece quando havia amplificador**.
- **A atualização aceitava código sem verificação.** A conferência de hash era
  *fail-open*: manifesto sem o campo `sha256` fazia o `.py` baixado ser
  gravado e executado na abertura seguinte, sem checagem alguma. Agora é
  **fail-closed** — sem impressão digital, recusa.
- **"Edição Clínica" → "Edição Pesquisa".** O rótulo descrevia *destinação de
  uso*, que é o critério de enquadramento como dispositivo médico, e
  contradizia o próprio Termo (que declara não ser dispositivo médico).
  Removidas também as **17 menções à FDA 21 CFR Part 11**, norma que o
  software citava sem implementar.

## [1.4.0] — 2026-08-10

### Adicionado
- **Mapa de co-contração** (aba EMG → *Mapa de co-contração…*): mede a
  **intenção de movimento** a partir de um par agonista/antagonista.
  Grava-se um movimento de cada vez; cada nuvem vira uma reta por regressão
  pela origem (m_f e m_e), e a **bissetriz angular** entre elas (m₀) separa
  flexão de extensão. O ponto ao vivo mostra de que lado está a intenção e
  com que intensidade (W, de −1 a +1). O mapa é exportável em `.json` para
  alimentar um controlador de prótese, e dá para calibrar de uma sessão já
  gravada usando os marcadores de fase.
  Método de **Fonseca et al., IEEE/EMBS NER 2025** — o valor W segue a eq. (1)
  do artigo. Ao lado dele, o índice clássico de co-contração
  (Falconer & Winter) responde a outra pergunta: quanto os dois músculos
  estão ativos ao mesmo tempo, isto é, se a articulação está enrijecida.
- **Zoom no atlas muscular**: roda do mouse (ancorada no cursor), arraste com
  o botão direito para deslocar, e enquadramentos prontos por região —
  cabeça e pescoço, ombro e braço, **antebraço e mão**, tronco, quadril e
  coxa, perna e pé. No corpo inteiro, a mão ocupava poucos pixels e
  posicionar eletrodo ali era sorte.
- **4 temas novos**, entre eles o **ROA (azul clínico)**, agora o **padrão**:
  o azul do logotipo sobre branco. Também *ROA Escuro* (sala com pouca luz),
  *Alto Contraste* (projeção/baixa visão) e *Sepia* (leitura longa).

### Alterado
- **Tela inicial**: a **logo ROA** substitui o símbolo genérico, e os quatro
  cards ganharam **ícones desenhados que dizem o que fazem** — um traçado de
  biossinal com ponto de gravação, um espectro em barras, uma cabeça
  emitindo ondas e uma senoide sintética em moldura tracejada. Antes eram
  formas geométricas (▶ ■ ◆ ◯) sem relação com o conteúdo.

### Corrigido
- **O ícone do programa aparecia genérico na barra de tarefas.** No Windows a
  barra não usa o ícone da janela: ela agrupa por *AppUserModelID*, e sem um
  id próprio o programa herda o ícone do processo host. Agora o ROA declara o
  seu, e o ícone também é definido no nível da aplicação.
- **Mais português misturado no idioma escolhido.** A varredura anterior só
  olhava o argumento direto do widget, então não via texto que entra por
  variável de laço — o padrão
  `for nome, lo, hi in (("Largo 1-50", 1, 50), …): QPushButton(nome)`.
  Era justamente o caso dos presets de filtro e de canal, dos cabeçalhos
  *Ativo / Canal / Tipo / Filtro recomendado / Threshold EMG* e de outros 46
  textos. **Cobertura agora: 790 termos em 8 idiomas, zero sem tradução.**
- **Zoom do atlas: âncora no cursor.** Ao ampliar, `(1 − zoom)` é negativo, e
  um `max()` de proteção contra divisão por zero destruía o sinal — o ponto
  sob o cursor fugia a cada giro da roda.

## [1.3.2] — 2026-08-10

Conclusão da troca de marca: agora o **arquivo** também se chama ROA.

### Alterado
- **`OpenBionica.py` passou a se chamar `ROA.py`.** O nome antigo vinha de
  antes da marca ser ROA e era a última peça fora do lugar.
- `APP_NAME_ASCII` (usado em metadados EDF/BIDS, que não aceitam acento)
  passou de `OpenBionica` para `ROA`.

### Corrigido
- **O atualizador passou a gravar no arquivo de onde o código foi
  carregado** (`__file__`), em vez de num nome fixo. É isso que mantém
  funcionando quem instalou quando o arquivo se chamava `OpenBionica.py`:
  o lançador daquelas máquinas fica no disco e nunca é atualizado a
  quente, então aponta para o nome antigo para sempre. Com o nome fixo,
  a atualização criaria um segundo arquivo e a máquina continuaria
  abrindo o velho, sem erro visível.
- O lançador de compatibilidade (`EEG_Data_Collector.py`) procura o
  código em cascata — `ROA.py`, depois `OpenBionica.py` — e, se não
  achar nenhum, explica o que faltou em vez de estourar um erro de
  Python. Ele também declara `APP_VERSION`, que o executável lê.

### Adicionado
- Guia **"Guardando seus dados ao atualizar"** (PDF + texto, na pasta do
  programa): para quem já usa, mostra onde ficam gravações, voluntários e
  configurações, e como não perdê-las ao trocar de pasta. Existe porque
  as gravações ficam **dentro** da pasta do programa — substituir a pasta
  leva os dados junto.
- Aviso equivalente no `COMECE AQUI.txt`, que é o primeiro arquivo que a
  pessoa abre.

### Nota sobre o repositório
O repositório continua se chamando `OpenBionica`. O endereço que cada
instalação consulta está gravado no computador do usuário e contém o nome
do repositório; renomeá-lo dependeria do redirecionamento do GitHub, que
deixa de existir se alguém registrar o nome antigo. Detalhes em
`LEIA_ANTES.txt` do pacote de publicação.

## [1.3.1] — 2026-08-10

Segunda rodada da revisão, guiada por novos retornos de uso (nome da marca,
mistura de idiomas, cabeçalho tremendo, comparação exigindo 2 arquivos).

### Alterado
- **Marca:** o subtítulo correto é **Research Open Analysis** (não
  "Algorithms") — corrigido no app, logos (`roa_logo.png`, `roa_icone.png`,
  `roa.ico`) e manual.
- **Estatística guiada:** agora aceita **1 arquivo por grupo**. Quando
  qualquer um dos grupos tem um arquivo só, **os dois** passam a ser
  fatiados em janelas de até 10 s e cada janela vira uma amostra — os dois
  lados precisam da mesma unidade amostral, senão estaríamos comparando
  "média de sessão" contra "média de janela". A janela é a mesma nos dois
  grupos (limitada pela gravação mais curta) e a **duração real é
  informada** no resultado. O resumo distingue 1×1 (não generaliza para o
  paciente) de 1×N (janelas da mesma gravação não são independentes, então
  o p é otimista) e a opção "pareadas" é ignorada nesse modo.
- **Mapeamento de Canais:** mostra apenas os canais **em uso** (acompanha o
  seletor 8/16/32/64ch); a caixa "Mostrar todos os 64 canais" revela o
  restante como opcional.
- **Pasta e pacote renomeados para `ROA`**; a cópia do aplicativo que ficava
  em `_internal/` (uma versão 1.1.0 inteira, de 883 KB, com a marca antiga,
  usada como semente caso o `.py` da raiz sumisse) foi substituída pela
  mesma casca de compatibilidade da raiz — antes, apagar um arquivo fazia o
  programa "voltar no tempo" em silêncio.
- Menções remanescentes de "OpenBiônica" na documentação, nos metadados de
  citação e no núcleo C++ passaram a dizer ROA. **Os nomes de arquivo e do
  repositório continuam `OpenBionica`** de propósito: é por eles que o
  atualizador automático encontra a nova versão.

### Adicionado
- **3 idiomas novos:** Alemão (Deutsch), Japonês (日本語) e Russo (Русский) —
  9 idiomas no total, com dicionário completo em todos.
- **Ícone do aplicativo** trocado para a marca ROA — inclusive o ícone
  embutido no `ROA.exe` (trocado no recurso do executável, sem refazer o
  build) e no atalho da Área de Trabalho.
- Docstrings nas últimas 5 funções que faltavam — **100 % de cobertura**
  (775 defs documentadas).
- `EEG_Data_Collector.py` (a casca de compatibilidade) passou a declarar
  `APP_VERSION`: o launcher do executável lê a versão local por esse nome e
  sem ela reportava `0.0.0`, o que faria toda consulta parecer "atualização
  disponível" caso a verificação automática fosse ligada.

### Corrigido
- **O idioma escolhido não era salvo** para italiano, francês, chinês,
  alemão, japonês e russo: a config só aceitava `pt`/`en`/`es` na leitura,
  então a escolha era gravada e **descartada ao reabrir** — o programa
  voltava inteiro ao português e parecia que a tradução "não pegava".
  Era a causa principal da queixa de idioma.
- **Mistura de línguas ao trocar idioma:** a re-tradução ao vivo só sabia
  reverter textos exibidos em inglês/espanhol; com a tela em
  italiano/francês/chinês, parte da interface ficava no idioma antigo.
  Agora o mapa reverso cobre todos os idiomas, dá prioridade ao idioma
  anterior (desfaz colisões de sinônimos, ex.: francês *Paramètres* servia
  a "Configurações" e a "Parâmetros"), guarda a chave em português dentro
  do próprio widget — de modo que as trocas seguintes são exatas — e a
  varredura também re-traduz sub-abas genéricas e cabeçalhos de tabelas.
- **546 textos de interface passaram a respeitar o idioma.** Ficavam sempre
  em português, entre eles: a **barra de menus inteira** (Ferramentas e
  Ajuda), os botões da **barra de ação** (Conectar / Iniciar Gravação /
  Marcar evento / Protocolo) **e os textos que eles assumem ao serem
  clicados**, o **assistente de primeira execução**, a aba
  **Configurações**, a aba **Offline**, os botões de **exportação**
  (EDF/FIF/PDF/BIDS), a aba **Rede e Eventos**, a página **Protocolo
  (tempos)**, 17 títulos de janela e a barra de status.
- **Eletrodos repetidos no mapeamento de fábrica:** os canais 62-64 vinham
  como F8/T8/P8, que já ocupavam os canais 10/14/6. Em 64 canais o CSV saía
  com colunas duplicadas (`F8_uV` duas vezes). Passaram a ser F10/T10/P10.
- **Estatística guiada, teste pareado:** com grupos de tamanhos diferentes
  o excedente era descartado em silêncio e os pares formados por posição na
  lista — o que emparelha voluntários errados. Agora o programa avisa e
  oferece rodar como não pareado.
- **Estatística guiada, seleção de arquivos:** se o único arquivo escolhido
  falhasse ao abrir (ex.: .edf corrompido), a seleção anterior do grupo era
  apagada. Agora ela é preservada.
- **Importar perfil de protocolo:** trocava o mapeamento de canais sem
  atualizar a tela, e a primeira edição seguinte desfazia o perfil recém
  importado.
- Correções de tradução apontadas em auditoria: `Amostras: 0` estava em
  inglês no dicionário alemão; *Layout Custom* e *Dead zone* não haviam
  sido traduzidos para o italiano; o gráfico de Poincaré ficara sem
  tradução em chinês e japonês; e o estado FOCADO colidia com o modo Focus
  em chinês.
- **Cabeçalho "tremendo"** durante aquisição/simulação: os contadores
  (amostras, acelerômetro, Δt) ganharam largura mínima de pior caso e
  padding estável — os números mudam sem empurrar o layout.
- Traduções que faltavam nos idiomas já existentes (85 chaves em EN/ES e
  103 em IT/FR/ZH) foram completadas — abas, tabelas e mensagens que
  ficavam em português.

## [1.3.0] — 2026-08-09

Revisão geral guiada por feedback de uso real (telas apertadas, idioma,
"antes e depois" do paciente).

### Alterado
- **Nova marca: ROA — Research Open Analysis.** O produto deixa de se chamar
  OpenBiônica: cabeçalho ("◢ ROA" + subtítulo), títulos de janela, launcher,
  Sobre, relatórios e rodapés usam a marca nova, e o ícone passou a ser o
  símbolo ROA (anel com capelo, `roa.ico`; o cérebro antigo fica de fallback).
  **Nomes de arquivo NÃO mudaram**: `OpenBionica.py` continua sendo o código
  (o atualizador dos usuários procura por esse nome no GitHub) e o repositório
  segue `rodrigooa43-create/OpenBionica`. O executável do pacote foi renomeado
  para `ROA.exe` (o atalho usa o caminho real, então continua funcionando).

### Adicionado
- **Evolução do paciente** (Analisar → Offline): curva de uma métrica por
  sessão — potência de banda EEG, RMS ou frequência mediana de EMG, picos de
  EoG — com data de cada coleta, reta de tendência e variação percentual entre
  a primeira e a última. O "antes e depois" ao longo dos dias.
- **Cores individuais por banda** nos gráficos de barras (Delta…Gamma), com
  seletor em Sistema → Configurações → Tema e Cores e padrão já colorido
  (antes era tudo verde).
- **Badge de canais clicável**: o "8ch" do cabeçalho vira menu — defina ali
  quantos canais está usando (8–64), com atalho para o tipo de cada canal.
- **Três idiomas novos**: italiano, francês e chinês (simplificado) — 215
  chaves de interface traduzidas em cada um.
- **Área Maker**: métricas novas — razão entre bandas (ex.: teta/beta), pico
  alfa individual (IAF, que rejeita registro sem alfa resolvível) e entropia
  espectral.
- **Consultor**: dicionário de sinônimos ("salvar"→exportar, "ondas"→bandas,
  "melhorou"→evolução…) e nove respostas novas (exportação, bandas, ritmo
  sensório-motor, evolução, cores, canais, idiomas, protocolo, importação).

### Corrigido
- **ERS/ERD reformulada**: controles de 5 para 3 linhas, botões com altura
  mínima (o texto saía cortado em janelas baixas), divisor vertical ajustável
  entre os gráficos e o mapa ERSP, e rolagem quando a janela não comporta tudo.
- **54 títulos de grupo sem tradução** ("Carregamento e parâmetros", "Atalho
  na Área de Trabalho"…) envolvidos em tr() e traduzidos nos 5 idiomas.
- **Importador**: reconhece cabeçalhos comentados com `%` (OpenBCI GUI) e
  `//`, além do `#`.

### Adicionado (ciclo anterior, 04/08)
- **Sequência de tempo do protocolo** (Sistema → Configurações → Protocolo (tempos)):
  editor onde se monta a coleta em fases — linha de base, ação muscular, repouso,
  aviso — com duração de cada uma, número de repetições e prévia em linha do tempo
  colorida. Durante a gravação, o executor percorre a sequência, mostra a fase atual
  com contagem regressiva na barra de ação, emite bipe na troca e **grava um marcador
  por fase** no `events.csv`, que é o que torna a segmentação por condição automática.
  Protocolos podem ser duplicados, exportados e importados em `.json`. Acompanham
  cinco modelos prontos, dois deles transcritos de um protocolo real de reabilitação
  de membro superior com sEMG (calibração MVC de 35 s e exercícios de 55 s, com
  slots de 5 s).
- **Documentação do código**: 447 funções e classes que estavam sem docstring foram
  documentadas em português, elevando a cobertura de 41 % para **100 %** (756 de 756).
  As docstrings explicam o papel de cada trecho e registram armadilhas concretas
  (unidades, efeitos colaterais, o motivo de constantes) em vez de repetir a assinatura.
- **Manual do usuário v1.2.1**: novas seções sobre modos de sinal, sequência de tempo
  do protocolo e importação de qualquer formato; seção do atlas muscular atualizada
  para o mapa de calor que segue o eletrodo. Cinco figuras novas geradas do programa
  em execução. O `manual_usuario.pdf` passou a acompanhar o pacote.

### Corrigido (ciclo anterior, 04/08)
- **Timers pesados não rodam mais em aba oculta**: a coerência da aba Conectividade
  (O(n²) em pares de canais — 2016 pares a cada 2 s com 64 canais) e o recálculo dos
  painéis do Layout Personalizado (5×/s) continuavam sendo executados mesmo com a aba
  fechada e mesmo nos modos EMG/ECG/EoG, onde essas abas nem existem. A guarda compara
  o **índice** da sub-aba, não o rótulo — comparar texto deixaria a proteção sempre
  ativa fora do português, já que os rótulos são traduzidos.
- **Listagem de sessões**: sessões importadas em subpasta (`importados_edf/<nome>/`)
  não apareciam na tabela, e a duração era calculada com a taxa de amostragem padrão
  em vez da taxa real do arquivo. A contagem de canais em formatos não nativos também
  estava errada; quando a taxa não pode ser determinada, isso passa a ser sinalizado.

## [1.2.1] — 2026-07-15

Foco em **HRV do ECG** e **oculometria do EoG** de nível de pesquisa — gráficos
que seguem a sequência do tempo, no mesmo espírito das melhorias do EMG/EEG.

### Alterado
- **Renomeação para OpenBiônica**: o executável passou a chamar-se **`OpenBionica.exe`**
  e o código-fonte principal, **`OpenBionica.py`**. Para não exigir recompilação do
  executável já distribuído (cujo lançador interno inicia pelo nome antigo), o arquivo
  **`EEG_Data_Collector.py` foi mantido como um lançador mínimo** que apenas invoca o
  `OpenBionica.py`. O hot-update passou a baixar/substituir o `OpenBionica.py`
  (`version.json` → `py_url`/SHA-256 atualizados). Nenhum dado do usuário é afetado.

### Adicionado
- **ECG — HRV espectral visual (bandas VLF/LF/HF)**: a razão LF/HF deixou de ser só
  um número — agora há o **espectro HRV (PSD)** da série RR interpolada a 4 Hz, com as
  **bandas VLF (0,0033–0,04 Hz), LF (0,04–0,15 Hz) e HF (0,15–0,40 Hz) sombreadas** e a
  área sob a curva preenchida. Reporta **potência por banda em ms²**, **potência total**
  e **unidades normalizadas** (LFnu/HFnu). Referência: Task Force (1996).
- **ECG — HRV geométrica (histograma RR + índice triangular)**: **histograma dos
  intervalos RR** (bins de 1/128 s ≈ 7,8 ms) com o **triângulo interpolado** desenhado
  por cima; reporta o **índice triangular (HTI = N/altura do modo)** e o **TINN** (largura
  da base, ms) — descritores robustos a batimentos ectópicos.
- **EoG — sequência principal das sacadas (main sequence)**: gráfico de **amplitude ×
  velocidade de pico** por sacada, com **ajuste da lei de potência V ≈ k·A^b** sobreposto
  (Bahill 1975; Engbert-Kliegl). Desvios sistemáticos da curva indicam fadiga oculomotor.
- **EoG — taxa de piscadas ao longo do tempo (sonolência)**: curva da **taxa de piscadas
  (janela deslizante de 60 s) × tempo de sessão**, com a **faixa de vigília normal
  (8–18/min) sombreada** e leitura de **PERCLOS** (% do tempo com olhos fechados) e da
  **tendência** (subindo/estável/caindo). Padrão-ouro de sonolência (Wierwille 1994).

### Correções
- **EoG — contagem de sacadas**: a deduplicação passou a usar **tempo absoluto (relógio)**
  em vez de tempo relativo ao buffer. O refratório anterior "travava" no fim do buffer e
  passava a **descartar sacadas novas** em sessões contínuas; agora cada sacada física é
  contada uma única vez (também alimenta corretamente a sequência principal).

## [1.2.0] — 2026-07-10

Foco em **visualizações anatômicas** e correções visuais finas.

### Adicionado
- **EMG — gráficos temporais fiéis + Área Maker**: a aba EMG ganhou (1) um
  **espectrograma EMG** (frequência × tempo) do canal selecionado, com a **curva MDF
  sobreposta** — mostra a mediana espectral **descendo com a fadiga** ao vivo; e (2) um
  **mapa de atividade muscular** (canais × tempo) colorido por %\,MVC. A **Área Maker**
  ganhou métricas de EMG — **MAV, iEMG, comprimento de onda, cruzamentos por zero, MDF,
  MNF, Dimitrov FInsm5 e %\,do tempo ativo (TKEO)** — mais **5 modelos prontos** de EMG
  (fadiga MDF/Dimitrov, ativação RMS/MAV, duty cycle), com recorte + filtro 20–450 Hz.
- **EMG — ergonomia e ativação no tempo**: (1) **marcadores de onset/offset (TKEO)**
  sombreados sobre o envelope — as janelas de contração ficam visíveis na linha do tempo;
  (2) **APDF** (Amplitude Probability Distribution Function) com P10 (carga estática),
  P50 (mediana) e P90 (pico) — indicador ergonômico de carga muscular; (3) **comparação
  de fadiga entre músculos** (MDF em % vs início por canal) — mostra qual músculo fadiga
  mais rápido.
- **Exemplo "estilo PT-51" na Área Maker**: reproduz, **sem deep learning**
  (`numpy`/`scipy`), o núcleo de um classificador de imaginação motora com
  **embedding Riemanniano** (covariância → tangente log-Euclidiano) +
  **classificação por protótipos (MDM)** + **curva few-shot** — o análogo clássico
  do Prototypical Network. Roda sobre as sessões BCI carregadas (cada arquivo = um
  sujeito), reportando **MDM within-subject**, **MDM LOSO cross-subject** e a curva
  de acurácia × K-shot. Serve de linha de base e didática para modelos de ML.
- **Análise BCI de nível de pesquisa (aba ERS/ERD)**: além do ERD/ERS por canal e do
  curso temporal, três novos recursos sobre o CSV BCI carregado — (1) **Classificadores
  clássicos** (Band-power+LDA, **CSP+LDA**, **Riemanniano+LDA**) com **validação cruzada
  5-fold**, nível de acaso e **teste de permutação** (linha de base a superar com ML);
  também no modo **Repouso × MI** (separa imaginação de repouso — melhor quando as
  duas classes de MI são parecidas, ex.: pé plantar × dorsi);
  (2) **Mapa Tempo×Frequência (ERSP)** embutido no painel, dos canais C3/Cz/C4,
  alinhado ao início da MI, **por classe** (com mapa de diferença entre as classes);
  (3) **Índice de lateralidade C3/C4** (padrão contralateral clássico da MI de mãos).
  Tudo em `numpy`/`scipy` puros.
- **Atlas Muscular Interativo (EMG)**: silhueta do corpo em vistas **Frontal** e
  **Posterior** (braços, pernas, pescoço, rosto, peito, costas, glúteo, panturrilha…),
  com **mapa de calor por %MVC** dos músculos trabalhados. Permite **posicionar
  eletrodos clicando na imagem**, numerados (1, 2, 3…) e **renomeáveis**, arrastáveis
  (duplo-clique renomeia, Delete remove). Cada eletrodo mostra um **anel de qualidade/
  acurácia** do contato (SNR do envelope + contaminação de rede 50/60 Hz), o %MVC ao
  vivo e liga-se a um canal. Inclui **tabela de eletrodos**, **histórico de montagens**
  (data, voluntário, nº de eletrodos, qualidade média) e **exportação da imagem em alta
  resolução (PNG 2×)**.
- **Topografia EEG 3D (domo)**: mapa topográfico **pseudo-3D** do escalpo com
  sombreamento (relevo de potência) e **rotação pelo mouse** — sem dependências extras.
- **Topografia estilo Tomografia**: cortes **isopotenciais** posterizados com linhas de
  contorno e **controle de profundidade** que "fatia" camadas internas (modelo de
  condução de volume).
- **EOG — olho anatômico**: além do diagrama XY, um **olho que pisca** ao detectar a
  piscada e cuja **pupila acompanha o olhar**.

### Correções (visuais)
- **Fundo das tabelas** agora **acompanha o tema/cor** selecionada em todos os casos
  (paleta reaplicada por tabela + `build_stylesheet` tolerante a temas antigos).
- **Caixas de texto/cortes**: seletor de cor e campo hex (Cores), botões rápidos de
  escala, campos de filtro, largura dos eixos e colunas de tabela **alargados** para não
  cortar o conteúdo.
- Rótulos do mapa muscular **nunca cortam** nas bordas (recorte reservado de cabeçalho/
  legenda).

### Interno
- Tudo em **QPainter/numpy puro** — as novas visualizações funcionam no `.exe` sem
  `pip install`.

## [1.1.0] — 2026-07-05

Revisão geral (Ondas 1 e 2): leitura de EDF, artefatos, consultor e análise visual.

### Correções de UX + modalidades (rev. jul/2026)
- **Executável renomeado** para `OpenBiônica.exe`.
- **Aba Offline**: botões em **duas linhas** (rótulos não cortam mais); o gráfico
  abre **limpo** (grade separando canais, texto‑guia, região oculta até carregar, e
  cada canal limitado a ±0,45 — sem virar "bloco").
- **ERS/ERD**: ao escolher a classe, a topografia **destaca a área esperada** (córtex
  contralateral: mão E→C4, mão D→C3; pé→Cz).
- Removido o botão **"vs LORETA / MNE"** da Topografia.
- **EMG (reforço, estilo EMGworks/Noraxon)**: **linha de tendência de fadiga**
  (regressão do MDF, Hz/min + R²), **índice de Dimitrov FInsm5** (relativo ao início)
  e **onset/offset por TKEO** (Teager‑Kaiser).
- **ECG (estilo Kubios)**: **correção de ectópicos** (Lipponen‑Tarvainen) a montante do
  HRV e **elipse SD1/SD2** ajustada no gráfico de Poincaré.
- **EOG**: **regressão ocular Gratton‑Coles** (limpa o EEG: `EEG − β·VEoG`) com
  relatório de redução de variância.

### Adicionado
- **Multi-placa (agnóstico de placa)**: reconhece e **mapeia canais pelo NOME do
  eletrodo** (padrão 10-20, case-insensitive, nomenclatura antiga T3/T4/T5/T6 e
  montagens referenciadas tipo `C3-A1`), independentemente da ordem. Classifica
  canais especiais (gatilho/estímulo, referência A1/A2, EOG/ECG/EMG, anotação).
  Testado com exames do **iCelera/BioWave** (20/20 eletrodos mapeados).
- **Topografia da montagem do arquivo** (aba Offline): head plot (interpolado e
  **CSD/Laplaciano**) por banda usando os eletrodos **do próprio arquivo** carregado
  — localização correta para qualquer placa, não só a montagem ao vivo.
- **Eventos automáticos na importação**: extrai marcadores das **anotações EDF+**
  (TALs) e das **bordas do canal de gatilho** (ex.: 'Foto estimulo' do iCelera).
- **Importar exame iCelera Nano** (aba Offline): EDF + opcional `*_markers.csv` do
  protocolo, **sincronizado** por relógio ou por 2 anotações-âncora; reusa o leitor
  próprio (sem pyedflib). Canais mapeados por nome, eventos do protocolo no sinal.
- **Abrir EDF/BDF com reparo automático**: leitor tolerante (numpy) que lê arquivos
  recusados por EDFbrowser/pyedflib por caractere não-ASCII no cabeçalho; converte
  para CSV nativo respeitando a taxa real, com **nomes de eletrodo canônicos** e
  descartando canais não-EEG. Também no cadastro de voluntário.
- **Remoção de artefatos por ICA sem instalar nada**: FastICA em numpy puro
  (detecta piscadas por Fp1/Fp2), salva `data_clean.csv` — dispensa MNE/pip.
- **Consultor metodológico** (F1): entende a intenção e responde de forma focada e
  **com referências** (base `GUIA_METODOLOGICO.md`, embutida no código); balões de
  conversa e perguntas de aprofundamento; escalonamento honesto quando não sabe.
- **Topografia CSD / Laplaciano de superfície** (realça fontes locais, reduz
  condução de volume) + comparativo honesto com LORETA/sLORETA/MNE/EEGLAB.
- **Área Maker**: métricas **ERD% vs baseline** e **potência relativa (%)**,
  **modelos prontos** (estilo OpenVIBE), campo de baseline e rótulo de unidade.
- **Estatística guiada** mais clara: multi-sujeito explícito, amostra mínima por
  grupo (verde ≥5 / âmbar ≥2 / vermelho <2) e aceita EDF.
- **Menu de clique-direito** na tabela de voluntários (novo/selecionar/importar/deletar).
- Bases de conhecimento (`GUIA_METODOLOGICO.md`, `BASE_CONHECIMENTO.md`) **embutidas
  no `.py`** como fallback — a atualização a quente (que troca só o `.py`) fica
  autossuficiente.
- **Integridade de dados / Regras de Ouro** (auditoria roteiro‑revisão): `summary.json`
  agora grava **proveniência** (seed, versões de numpy/scipy/PySide6, hash dos
  parâmetros de DSP), **receita de DSP com fase causal declarada** (G‑01/G‑02/G‑06),
  **metadados obrigatórios de hardware** (ADC ADS1299, taxa nominal, referência,
  tipos de canal — G‑04), **taxa efetiva medida vs nominal + amostras perdidas**
  (G‑03/G‑07) e nota de **privacidade** (biossinal = dado sensível LGPD art.11).
- **Topografia com colormap perceptual (viridis)** — seguro para daltonismo,
  no lugar do HSV (VIZ‑09).
- **Aviso de segurança elétrica** do hardware no Termo de Uso (IEC 60601‑1;
  OpenBCI não certificado; usar em bateria/isolado — GOV‑06).
- Governança: `GOVERNANCE.md`, `SECURITY.md`, `CITATION.cff` (GOV‑10).
- **DSP/análise avançados** (fecha itens ausentes do roteiro): notch de **harmônicos** + **auto 50/60 Hz** (DSP‑03), **reamostragem anti‑aliasing** (DSP‑04), **PSD multitaper** (EEG‑04), **correção aperiódica 1/f** FOOOF‑lite (EEG‑05), **onset/offset EMG por TKEO** (EMG‑03), **correção de ectópicos** RR (ECG‑02), **HRV por Lomb‑Scargle** (ECG‑03), **regressão ocular Gratton‑Coles** (EOG‑03) e **decimação preservadora de pico (LTTB)** no traçado (VIZ‑02).
- **Núcleo de aquisição em C++ (`ob_core/`)** — ponte **Python↔C++** (ctypes, ABI‑C
  estilo BrainFlow) que **desacopla o data‑path do Python**: **ring buffer
  lock‑free**, thread de aquisição própria, clock monotônico e contador de perdas
  (ARQ‑01/02/03, G‑03/G‑07). **Agnóstico de placa** (a placa é um *Device*
  plugável — não depende da Cyton) e **testável sem hardware** (device sintético);
  com **fallback em Python** quando a DLL não está compilada. Menu *Ferramentas →
  Núcleo de aquisição C++ (status/teste)*.

### Corrigido
- **E999 ao abrir** sem sessões (atributo de tema inexistente na lista de recentes).
- **Fundo dos gráficos** não acompanhava a troca de tema.
- Taxa de amostragem incorreta ao converter EDF (precisão da coluna de tempo).

## [1.0.0] — 2026-06-28

Primeira versão pública open source (projeto **OpenBionica**).

### Adicionado
- **Tema "Claro Clínico"** (agora padrão), aplicado também às barras de menu/status.
- **Indicador de qualidade sempre visível**: por canal com **símbolo+cor**
  (● OK · ▲ ruidoso · ■ ruim — acessível a daltônicos) e **semáforo agregado**
  no cabeçalho.
- **Header responsivo** (esconde telemetria menos crítica; a marca nunca corta).
- **Proveniência** (versão do app + repositório) em `summary.json`, log, relatório
  PDF e exports EDF/FIF/BIDS.
- **Veredito de QC** no relatório PDF (APTO / DUVIDOSO / DESCARTAR).
- **Estatística guiada** (comparar grupos de sessões): escolhe o teste sozinho
  (Shapiro → t/Welch/Wilcoxon/Mann-Whitney/ANOVA/Kruskal), efeito (Cohen d),
  correção de Holm, tabela e conclusão em linguagem simples, export HTML/CSV.
- **Comparar condições da sessão** (intra-sessão, genérico/multimodal): compara
  as condições que existirem (banda EEG, RMS ou ERD% vs repouso), escolhe o teste.
- Documentos: `DISCLAIMER_USO_PESQUISA.txt`, `FORMATO_DADOS.md`, `CHANGELOG.md`,
  `KNOWN_ISSUES.md` (registro de bugs + controle de melhorias).
- **Logging estruturado** de aplicação (níveis + rotação) em
  `Documents/EEG_Coletor/logs/app.log`.
- **Handler global de exceções** (`sys.excepthook` + `faulthandler`): em vez de
  fechar em silêncio, loga o traceback e mostra um diálogo amigável com detalhes.
- **Sistema de erros codificados ("Erro E0XX")**: catálogo de **79 códigos**
  (`ERROR_CATALOG`) com mensagem amigável (o que houve + o que fazer); função
  `notify_error()` (loga + sinaliza); handler global vira **Erro E999**; exports
  EDF/FIF/BIDS/PDF e o update já sinalizam com código. Menu **Ajuda → Diagnóstico
  de erros (simular)** para consultar/testar cada notificação. Doc `ERROS.md`.
- **Assistente de ajuda OFFLINE** (menu Ajuda → Assistente de ajuda, **F1**): chat
  que responde dúvidas e problemas buscando localmente em FAQ + catálogo de erros
  (digite "E115" ou "como faço impedância?"). **Nada sai da máquina** — sem IA na
  nuvem, sem internet. Agora **orgânico**: indexa o **manual** + a FAQ + o catálogo
  de erros por **TF-IDF** (`BASE_CONHECIMENTO.md` gerado do manual), respondendo
  além da FAQ curada, sem curadoria por pergunta.
- **Área Maker — Receitas de análise** (Analisar → Offline): monta um **pipeline**
  composável — **recorte temporal → pré-filtro (passa-banda) → métrica** (banda,
  RMS, pico-a-pico, desvio) por canais — roda em 1+ sessões (tabela Canal ×
  Sessões) e **salva/carrega/compartilha como `.json`** + exporta CSV.
  Reprodutibilidade; reusa `SignalProcessor`. Offline.
- **Desempenho/UX:** plots em tempo real com *downsampling*+*clip-to-view*
  (menos CPU com 16 canais, sem perda visual); HRV **LF/HF** avisa "⚠ janela
  curta" quando há menos de ~2 min de batimentos (validade estatística).
- **Menu Ferramentas:** **Perfil de protocolo** (exporta/importa montagem +
  tipos de sinal + EMG + impedância como `.json` reutilizável entre máquinas),
  atalho para a **Área Maker** e **Abrir pasta de logs**.
- **Assistente de primeiro uso** (idioma → layout → **aceite do Termo de Uso**);
  bloqueia o uso até o aceite e registra versão/data localmente.
- **Termo de Consentimento e Uso** (`TERMO_DE_USO.md`/`.txt`): open source, sem
  fins lucrativos, **offline, sem coleta de dados**; isenção de garantia,
  limitação de responsabilidade e responsabilidade do operador (LGPD).
- Menu **Ajuda**: "Verificar atualizações..." (manual) e "Termo de uso e
  privacidade...".
- **Instalador Inno Setup** (`instalador.iss`) com o termo como página de licença
  obrigatória + atalhos/desinstalador.

### Modificado
- **GUI migrada de PyQt6 (GPLv3) para PySide6 (LGPLv3):** permite distribuir o
  binário sem impor copyleft ao aplicativo (mantém o código sob MIT). pyqtgraph
  fixado ao mesmo binding via `PYQTGRAPH_QT_LIB`.
- **Offline por padrão (privacidade):** `auto_check=false` no launcher — nenhuma
  conexão automática; a atualização passa a ser **manual** (menu Ajuda).
- Autoria/edição: **"Bionica Lab / UFES" → "OpenBionica"** (sem vínculo
  institucional); `LICENSE` (MIT) e `APP_AUTHORS` atualizados.
- Logo da UFES no cabeçalho usa as **cores originais** (antes invertia no claro).
- Cabeçalho mais compacto; título não corta mais.

### Corrigido
> Auditoria com verificação adversarial — IDs em [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
- **NumPy 2.4**: `np.trapz` → `np.trapezoid` com fallback (quebrava análises).
- **Alias C2↔FCz** ao carregar EEG de outros sistemas.
- (EEG-001) `datetime.datetime.now()` → `datetime.now()` — quebrava import de exame.
- (EEG-002) atalho **"M"** não rouba mais a digitação de campos de texto (marker espúrio).
- (EEG-003) `layout_slots_cfg` corrompido não derruba mais o app no startup.
- (EEG-004) `config.json` salvo de forma **atômica** (`.tmp`+`os.replace`+`.bak`).
- (EEG-005) **playback** do CSV nativo ignora a coluna `marker` (não quebra mais).
- (EEG-006) teste pareado decide normalidade pelas **diferenças** (estatística correta).
- (EEG-007) falha de filtro não grava mais cru rotulado como filtrado em silêncio.
- (EEG-008) export **EDF** não vaza handle nem deixa arquivo parcial travado.
- (EEG-009) loader abre CSV com header mais largo que as linhas sem quebrar.
- (EEG-021) análise offline não quebra ao carregar sessão com mais canais que a tabela.
- (EEG-022) `import re` ausente (NameError latente na exportação BIDS e na
  sanitização de nomes) — adicionado ao topo.
- (EEG-023) `compute_fft`: escala da janela de Hanning corrigida
  (`2/sum(window)` em vez de `2/n`) — amplitude em µV estava ~2× subestimada.
- (EEG-024) **ECG Pan-Tompkins**: passa-banda 5–15 Hz agora é aplicado **dentro**
  do detector (antes era "assumido"; o filtro global é banda-EEG) → BPM/HRV mais
  confiáveis.
- (EEG-025) HRV Poincaré **SD2**: radicando negativo clampado (evita `NaN`).
- (EEG-028 parcial) **EoG**: direção agora é calculada **relativa à baseline**
  (mediana do buffer) — a deriva lenta não trava mais a direção; lista de blinks
  limitada (memória/taxa não fossilizam em sessão longa).

### Segurança
- Validação **SHA-256** do pacote de atualização (mantida) — rejeita download
  corrompido/alterado.

## [0.9.0] — 2026-05-14

### Adicionado
- LSL output (Lab Streaming Layer) com 2 outlets (EEG + Markers)
- Exportação EDF/EDF+ (pyedflib)
- Exportação FIF (MNE-Python)
- Relatório PDF automático (matplotlib + reportlab)
- LEDs de qualidade por canal no header (saturação/ruído/rede)
- Sample timing audit (Δt + jitter + drops detectados)
- SHA-256 + nonce por sessão (prova de integridade)
- Audit log estruturado (events.jsonl)
- Aba ERP averager (médias por marcador)
- Aba Conectividade (matriz de coerência)
- Modo Demo 30s (protocolo automático + PDF)
- Atalho `.lnk` na Área de Trabalho com ícone Bionica Lab
- README.md + LICENSE + requirements.txt + .gitignore
- Relatório técnico completo (`docs/REPORT.txt`)

### Mudado
- Aba Calibração compacta — 16 canais visíveis sem rolagem
- Aba Hardware compacta — 16 canais visíveis sem rolagem
- Configurações reorganizadas em sub-abas
- Pasta de salvamento default agora é `sessions/` junto ao .py (portável)
- Fontes: Inter (UI) + JetBrains Mono (dados)
- Corrigido flash de tema no startup (carrega config antes do stylesheet)
- Removidas todas as menções a "Daisy" (substituído por "módulo de expansão")
- Termos sem acento corrigidos (Conexão, Calibração, etc.)

### Corrigido
- Bug do scroll Y em modo 16 canais (eixos com largura fixa, scroll wrapper)
- Tabelas com fundo branco no tema escuro (table_bg/table_alt customizáveis)
- Encoding cp1252 ao gerar shortcut no PowerShell

## [0.8.0] — 2026-05-13

### Adicionado
- Suporte ao módulo de expansão (16 canais, auto-detecção)
- Editor de tema personalizado com 13 cores ajustáveis
- 4 temas pré-definidos (Lime, Claro, Escuro Puro, Sistema)
- Mapeamento 10-20 completo (60+ eletrodos: Fz, Cz, Pz, FCz, CPz, ...)
- Limites de impedância personalizáveis (kΩ)
- Layout customizável (4 painéis em QSplitter redimensionáveis)
- Snapshots automáticos durante gravação

## [0.7.0] — 2026-05-12

### Adicionado
- Aba Topografia (Head plot + Focus + EMG)
- Aba Espectrograma
- Aba Filtros & Canais (notch + bandpass + presets + toggle)
- Aba Hardware (grid por canal: gain/SRB/bias)
- Aba Rede & Eventos (UDP streaming + markers)
- Modo Playback (replay de CSV)
- Modo Simulação (sinal sintético)
