# Replay (1.10.0)

> Manual Técnico → novo capítulo "Replay de gravações".

Tudo no ROA.py, em blocos antes de `class _VirtualJoystickWidget`:

- **Tocador**: `TocadorReplay` (relógio real `QElapsedTimer × velocidade`,
  sinais `tempoMudou(float)`/`tocando(bool)`), `ReplayDialog(cena, dur,
  titulo, simples, aviso)` — a cena é qualquer widget com `set_tempo(t)` e,
  opcionalmente, `cursorMovido(float)`, `salvar()`, `tem_alteracoes()`.
- **Movimento (P6)**: `MOVIMENTOS_ORDEM/TITULOS/CORES`, `MUSCULOS_ESPERADOS`,
  `movimento_do_rotulo` (palavras-chave dos marcadores), `ModeloMovimentos`
  (2–4 faixas, `movimentos_em(t)`, desfazer/refazer, `salvar/carregar` de
  `movimentos.json`, `de_dict` tolerante), `trechos_de_marcadores`,
  `trechos_de_contracoes` (usa `emg_onset_tkeo` + `emg_fundir_ativacoes`),
  `modelo_inicial`, `intensidade_no_instante`, `aviso_incompatibilidade`,
  `LinhaDoTempoMovimentosWidget`, `ListaTrechosWidget`; figura:
  `FiguraMovimentoWidget` (`set_pose/set_ativacao/set_objeto`),
  `pose_do_movimento`, `pose_mesclada` (soma de deltas com limites; postura de
  teste cede a gesto de braço), `TAREFAS`, `pose_da_tarefa`.
- **Coração e olhos (P7)**: `detectar_batidas_gravacao` (`ecg_pan_tompkins`,
  `ecg_rr`, `correct_ectopic_rr` 30 % → adiantada/pausa), `aplicar_correcoes`,
  `salvar/carregar_batidas` (`batidas.json`), `detectar_eventos_olhos`
  (`eog_piscadas_tela`/`eog_piscadas`, `eog_sacadas`), `inverter_direcoes`,
  `olhar_no_instante`, `salvar/carregar_olhos` (`olhos.json`), widgets
  `CoracaoReplayWidget`, `FaixaBatidasWidget`, `ListaBatidasWidget`,
  `OlhosReplayWidget`, `LinhaDoTempoOlhosWidget`.
- **Cenas e abertura (P8)**: `CenaReplayEMG/ECG/EOG`, `_TracadoReplay`
  (pg.PlotWidget com cursor), `replay_exame_da_gravacao(modo, tipos)`,
  `abrir_replay(...)`; na janela `_offline_atualiza_replay` (habilita o botão
  pelo exame da gravação) e `_offline_abrir_replay`; botão
  `offline_replay_btn` na fileira 2 da aba Offline, em `_offline_botoes`.
  Canais: `report_channels` do `summary.json` (ecg, eog_h, eog_v,
  eog_threshold) com fallback pelo tipo.

Arquivos ao lado do `data.csv` (todos JSON utf-8, `"versao": 1`, aditivos:
não mudam `summary.json`): `movimentos.json` (faixas/trechos + `objetos`),
`batidas.json` (batidas corrigidas + histórico `correcoes`), `olhos.json`
(eventos + `inverter_h/v`). Testes: `test_p6_*`, `test_p7_replay`,
`test_p8_replay`.
