# Canais em uso (1.10.0)

> Manual Técnico → Capítulo "Modelo de canais" → nova seção.

`self.num_channels` é o número de canais em uso e
`self.config.channel_signal_types` (sempre com `MAX_CHANNELS` itens, valores
"EEG"/"EMG"/"ECG"/"EoG"/"off") o tipo de cada um. Helpers únicos:

- módulo: `canais_por_tipo(tipos, n_em_uso, tipo)` (pura; `tipo=None` = todos);
- janela: `_canais_em_uso()`, `_tipo_do_canal(ch)`, `_canais_em_uso_tipo(tipo)`,
  `_rotulo_canal_combo(ch)`, `_repopular_combo_canais(combo, canais, tipo_vazio)`
  (userData = índice do canal, preserva a seleção pelo canal; vazio → um item
  `_msg_sem_canal(tipo)` com data -1) e `_refresh_listas_canais()`.

`_refresh_listas_canais()` é chamado por `_set_num_channels`,
`_on_channel_signal_type_changed` e `apply_launcher_choice`, e repopula: combos
EMG (MDF/MNF, APDF, espectrograma), combos "Canal" do Atlas, ERP (só sem
gravação carregada), `ch_combo` dos slots do Layout, linhas da `imp_table`
(`_refresh_imp_table_rows`), legenda do `emg_plot` (`_sincroniza_legenda_emg`)
e o `CoContractionMapDialog` aberto. Os laços `_update_emg_view`,
`_emg_update_advanced`, `_emg_update_ergonomics` e `_emg_atlas_update_live`
percorrem só `_canais_em_uso_tipo("EMG")`. No modo offline o ERP usa
`d["ch_names"]` da gravação (`_erp_popula_canais_da_gravacao`).

Teste: `testes/test_p1_canais_em_uso.py` (5 exames × 8/16/32/64 × 2 níveis).
