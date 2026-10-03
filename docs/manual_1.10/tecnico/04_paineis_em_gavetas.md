# Painéis em gavetas (1.10.0)

> Manual Técnico → Capítulo "Interface" → nova seção.

Classes (bloco antes de `class EEGCollectorWindow`): `CatalogoPaineis`
(registro estático em `_registrar_paineis_padrao`, instância global
`CATALOGO_PAINEIS`; `itens()` devolve `{id, titulo, aba, exames, padrao}`;
`para_config()/de_config()`; `estado_para_perfil(exames)` para o P4),
`PainelGaveta(QFrame)` (embrulha o QGroupBox: cabeçalho ▾/título/⋯/×, alça de
altura, `setVisible` sobrescrito para `_apply_detail_level` não reabrir
painel fechado; `esta_ativo()` = visível ∧ não recolhido ∧ aba visível),
`PilhaGavetas` (empilha gavetas, linhas lado a lado em QSplitter, botão
Painéis, `estadoMudou(dict)` com debounce de 500 ms), `gaveta_ativa(janela,
id)` e `qss_gavetas(c)` (anexado por busca tardia em `build_stylesheet`,
porque a folha é calculada também na importação).

Janela: `_nova_pilha(aba, aba_visivel)`, `_salvar_paineis(aba, estado)`
(grava `config.paineis[aba]`), restauro no fim de `_build_ui`
(`de_config` + perfil de uso para abas sem arranjo salvo), `set_simples` em
`_apply_detail_level("ui")`, gavetas registradas em `_register_advanced`,
`set_titulo` em `_aplicar_nomes_bio`, pendências gravadas no `closeEvent`.
Abas: emg (`emg.config_envelope`, `emg.atlas`, `emg.canais` núcleo,
`emg.mvc_fadiga`, `emg.mnf_mdf`, `emg.tempo_freq`, `emg.ergonomia`), ecg
(`ecg.tracado` núcleo + `ecg.tacograma` lado a lado, `ecg.zonas`,
`ecg.hrv_nao_linear`, `ecg.hrv_espectral`), eog (`eog.tracado` núcleo,
`eog.alerta`, `eog.oculometria`), analises (`ana.fft` + `ana.bandas`,
`ana.estatisticas`), filtros (6), rede (4). Portões `gaveta_ativa()` em
`_update_emg_view` (chamadas de `_emg_update_advanced`/`_emg_update_ergonomics`,
FFT de fadiga), `_update_ecg_view`, `_update_eog_view`, `_update_analysis`.
Config: chave nova `paineis` (`{aba: {"ordem", "paineis": {id: {visivel,
recolhido, altura}}, "splits"}}`). Teste: `testes/test_p2_gavetas.py`.
