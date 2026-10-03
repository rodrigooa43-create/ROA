# Perfis de uso (1.10.0)

> Manual Técnico → Capítulo "Configuração" → nova seção depois de "Nível da interface".

**Modelo.** Constantes de módulo `PERFIL_TUDO = "Tudo"`,
`PERFIL_PERSONALIZADO = "Minha bancada"`, `EXAMES_PERFIL = ("EEG", "EMG",
"ECG", "EoG")`, `PERFIS_PRONTOS = {nome: exames}` (nomes em português, chaves
de `tr()`), `ROTULO_EXAME_PERFIL`. Funções puras: `perfis_disponiveis(config)`
→ `{nome: {"exames", "paineis", "pronto"}}`; `perfil_valido(config)` (cai em
"Tudo"); `exames_do_perfil(config, nome=None)` (acrescenta "Hibrido" com 2 ou
mais exames); `perfil_para_exames(exames)`; `rotulo_perfil(nome)`.

**Config.** Chaves novas: `usage_profile` (str, padrão "Tudo") e
`usage_profiles` (`{nome: {"exames": [...], "paineis": {id: bool}}}`, só os
personalizados). Config antigo sem as chaves → "Tudo" (nada muda). Lixo é
descartado na carga.

**Tela inicial.** `LauncherScreen._tipos_de_exame()` filtra
`_tipos_de_exame_todos()` pelo perfil; `_exame_atual()` cai no primeiro exame
do perfil (não mais em EEG fixo). Seletor `perfil_combo` (`_monta_combo_perfil`)
nos dois níveis; `_on_perfil_trocado` grava e chama `_aplica_perfil_na_tela`
(esconde radios fora do perfil no Completo; corrige `acquisition_mode` se saiu
do perfil).

**Assistente.** Páginas novas no `QStackedWidget`: índice 2
`_build_page_trabalho` (quatro cartões marcáveis; `_exames_marcados()`), índice
3 `_build_page_graficos` (só no caminho Pesquisa; lê `CATALOGO_PAINEIS.itens()`
via `globals().get`, recomendados = `padrao.visivel`); layout passa a 4 e termo
a 5. `_PAGS_SO_PESQUISA = (3, 4)` governa `_go_next`/`_go_back`.
`_aplicar_perfil_escolhido()` em `accept()` decide o nome do perfil e grava o
personalizado quando há 2–3 exames ou gráficos desmarcados.

**Janela.** `_apply_signal_mode_visibility` intersecta as regras do modo com a
união de `MODE_TAB_VISIBILITY` dos exames do perfil (mais `_ABAS_SO_MULTIMODAL`
no Multimodal); perfis com os 4 exames não cortam nada. `_aplicar_perfil_no_combo_modo`
desabilita itens do combo "Modo do exame"; `_menu_trocar_modalidade` não lista
exames fora do perfil. `_perfil_definir(nome)` → `_aplicar_perfil()` (muda o
modo se o atual saiu do perfil). CRUD em `_build_perfil_group` (Sistema → Tema
e Cores): `_perfil_novo`, `_perfil_duplicar`, `_perfil_renomear`,
`_perfil_excluir`, `_perfil_exames_mudaram`.

**Testes.** `testes/test_p4_perfis.py` (funções puras, config ida-e-volta,
tela inicial nos dois níveis, assistente, janela e CRUD).
