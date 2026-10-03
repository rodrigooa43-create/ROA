# P2 — Painéis em "gavetas" no Completo: notas de integração

Protótipo em `scratchpad/prototipos/p2_gavetas.py` (bloco entre os comentários
`# === INÍCIO DO BLOCO PARA O ROA.py ===` e `# === FIM DO BLOCO ===`, únicos no
arquivo). Imagens nesta pasta: `gavetas_claro.png`, `gavetas_escuro.png`,
`gavetas_recolhidas.png`, `menu_paineis.png`, `menu_gaveta.png`,
`gavetas_simples.png`. Teste: `testes/test_p2_gavetas_prototipo.py` (18 testes,
importa o protótipo pelo caminho absoluto; quando o bloco entrar no ROA.py,
trocar para `from _roa import ROA` e `ROA.PilhaGavetas` etc.).

As linhas do ROA.py citadas abaixo são as de hoje (o arquivo está sendo
editado por outro agente; os nomes de função/variável são a referência).

---

## 1. API pública (resumo)

| Peça | Para quê |
|---|---|
| `CatalogoPaineis()` | registro + estado atual + ordem + splits; `registrar(id, titulo, aba, exames, visivel, recolhido, altura)`, `ids_da_aba(aba)`, `ids_do_exame(exame)`, `estado_padrao(id)`, `estado_atual(id)`, `definir_estado(id, **campos)`, `definir_ordem(aba, ids)`, `definir_split(aba, nome, tamanhos)`, `restaurar_padrao(aba=None)`, `estado_da_aba(aba)`, `aplicar_estado_da_aba(aba, d)`, `para_config()`, `de_config(d)`; para o P4: `recomendados_para(exames)`, `estado_para_perfil(exames)`. |
| `PainelGaveta(id, conteudo, titulo=None, simples=False, aba_visivel=None, altura_padrao=None, fechavel=True)` | o invólucro de um QGroupBox (ou qualquer QWidget). `set_recolhido(b)`, `alternar_recolhido()`, `set_visivel_painel(b)`, `fechar()`, `set_altura(int|None)`, `tamanho_padrao()`, `set_titulo(t)`, `set_simples(b)`, `set_aba_visivel(fn)`, `esta_ativo()`, `estado()`; sinais `estadoMudou(id)`, `moverPedido(id, delta)`. `setVisible()` está sobrescrito: no Completo um `show()` de fora não reabre painel fechado. |
| `PilhaGavetas(aba, catalogo=None, dono=None, simples=False, aba_visivel=None, espacamento=6)` | `adicionar_painel(id, conteudo, titulo, exames, visivel, recolhido, altura, fechavel, stretch)`, `adicionar_gaveta(g, stretch)`, `adicionar_linha([...], nome, tamanhos, stretch)` (lado a lado em QSplitter), `botao_paineis()`, `gaveta(id)`, `gavetas()`, `ordem()`, `mover(id, ±1)`, `recolher_todos()`, `expandir_todos()`, `restaurar_padrao()`, `estado()`, `aplicar_estado(d)`, `salvar_agora()`, `set_simples(b)`, `set_aba_visivel(fn)`; sinal `estadoMudou(dict)` com debounce de 500 ms. Com `dono=janela`, registra cada gaveta em `janela._gavetas[id]`. |
| `gaveta_ativa(janela, id)` | para os laços de atualização; `True` se não houver gaveta com esse id (nunca bloqueia por engano). |
| `qss_gavetas(c)` | folha das gavetas; anexar em `build_stylesheet`. |

Formato de `config.paineis` (chave nova do config.json):

```json
"paineis": {
  "emg": {"ordem": ["emg.config_envelope", "emg.atlas", "..."],
          "paineis": {"emg.atlas": {"visivel": true, "recolhido": false, "altura": null}},
          "splits": {"tracado+tacograma": [720, 600]}},
  "ecg": {"...": "..."}
}
```

---

## 2. Como colar no ROA.py (passos gerais)

1. **Bloco**: logo depois de `_qss_simples` (fim das funções de estilo) e antes de
   `class EEGCollectorWindow`. Só usa `QtCore/QtGui/QtWidgets`, `tr` e `COLORS`
   (lidos em tempo de execução, nunca em nível de módulo).
2. **`build_stylesheet`** (≈ linha 33042): o `return` vira
   `return _escala_fontes_qss(qss + _qss_simples(c) + qss_gavetas(c)) + _qss_barra_escala()`
   — dentro de `_escala_fontes_qss` porque a folha das gavetas tem `font-size: Npt`
   (acompanha "Tamanho da letra"). O cabeçalho mede a própria altura pela fonte
   (`_ajustar_metrica`, 22–30 px), então escala junto.
3. **`AppConfig`**: `self.paineis = {}` no `__init__`; em `load()`:
   `pa = d.get("paineis"); if isinstance(pa, dict): self.paineis = pa`; em `save()`
   acrescentar `"paineis": self.paineis` ao dict serializado.
4. **`EEGCollectorWindow.__init__`**, antes de `_build_ui`:
   `self._catalogo_paineis = CatalogoPaineis(); self._pilhas = {}; self._gavetas = {}`.
5. **Fábrica** (método novo):
   ```python
   def _nova_pilha(self, aba, aba_visivel=None):
       """Pilha de gavetas de uma aba, ligada ao catálogo e ao config."""
       p = PilhaGavetas(aba, catalogo=self._catalogo_paineis, dono=self,
                        simples=self._nivel_simples(), aba_visivel=aba_visivel)
       p.estadoMudou.connect(lambda d, a=aba: self._salvar_paineis(a, d))
       self._pilhas[aba] = p
       return p

   def _salvar_paineis(self, aba, estado):
       """Grava o arranjo de uma aba (debounce já feito pela pilha)."""
       self.config.paineis[aba] = estado
       self.config.save()
   ```
6. **Restaurar ao abrir** (fim de `_build_ui`, depois de todas as abas):
   `self._catalogo_paineis.de_config(self.config.paineis)` e, para cada pilha,
   `p.aplicar_estado(self.config.paineis.get(p.aba(), {}))` (não emite sinal).
7. **Nível**: em `_apply_detail_level` (≈ 45321), quando `chave == "ui"`, ANTES do
   laço `for w in self._detail_widgets[...]: w.setVisible(avancado)`:
   `for p in self._pilhas.values(): p.set_simples(not avancado)`.
   Motivo: `set_simples(True)` reabre o que estava fechado pelo usuário e o laço
   em seguida esconde o que é avançado; `set_simples(False)` volta a esconder os
   fechados e o `setVisible(True)` do laço não os reabre (override).
8. **`_register_advanced`**: registrar a **gaveta** (`pilha.gaveta(id)`), não o
   QGroupBox — senão, no Simples, sobraria uma gaveta vazia (sem cabeçalho,
   mas com o espaçamento do layout).
9. **Títulos que mudam por nível** (`_aplicar_nomes_bio`, ≈ 45468):
   `self._emg_atlas_grp.setTitle(...)` → `self._gavetas["emg.atlas"].set_titulo(...)`
   e `self._eog_alert_group.setTitle(...)` → `self._gavetas["eog.alerta"].set_titulo(...)`.
   No Completo o QGroupBox fica SEM título (quem mostra é o cabeçalho); `set_titulo`
   mantém os dois em sincronia e restaura o título no Simples.
10. **Botão "Painéis"**: cada aba já tem a linha `_make_detail_toggle(...)`; guardar o
    layout e pendurar o botão no fim:
    `row = self._make_detail_toggle("emg", ...); row.addWidget(pilha.botao_paineis()); outer.addLayout(row)`.
    Em abas sem essa linha (Análises, Filtros, Rede), uma `QHBoxLayout` com
    `addStretch()` + botão no topo.
11. **`closeEvent`** (≈ 62894), antes do `config.save()` final:
    `for p in self._pilhas.values(): p.salvar_agora()` — garante o último arraste
    mesmo dentro dos 500 ms do debounce.
12. **Idiomas**: 13 chaves novas de `tr()` (ver §7). `"Fechar"` já existe.
13. **QSS do Simples**: `QMainWindow[nivelUi="simples"] QGroupBox` tem especificidade
    maior que `QGroupBox[emGaveta="true"]`, mas no Simples a gaveta já põe
    `emGaveta="false"` e devolve o título, então as regras do Simples valem
    inalteradas. `QGroupBox` já está em `_TIPOS_REPOLIR`.

---

## 3. Músculos — `_build_emg_tab` (≈ 53693), aba `"emg"`

`aba_visivel = lambda: self._aba_esta_visivel("view", 3) and self.bio_tabs.currentIndex() == 0`.
Tudo que hoje vai em `outer.addWidget(grupo)` passa a `pilha.adicionar_painel(...)`;
`info_row` e a linha do seletor de nível ficam ACIMA da pilha, fora dela.

| Ordem | QGroupBox (variável) | id | exames | padrão sugerido | `gaveta_ativa()` em `_update_emg_view` (≈ 55150) |
|---|---|---|---|---|---|
| 1 | `ctrl_group` "Configuração do Envelope EMG" (avançado) | `emg.config_envelope` | EMG | visível, expandido | nenhum (só entradas) |
| 2 | `self._emg_atlas_grp` (de `_build_emg_atlas_group`) | `emg.atlas` | EMG | visível, expandido (visível também no Simples) | bloco "Atlas muscular" (`st - _emg_atlas_last_st >= SAMPLE_RATE//2`): acrescentar `and gaveta_ativa(self, "emg.atlas")` antes de `_emg_atlas_update_live` |
| 3 | `split` (cards `cards_scroll` + `emg_plot`) — hoje sem groupbox, `stretch=2` | `emg.canais` | EMG | visível, **`fechavel=False`**, `stretch=2`, título `tr("Canais EMG — envelope e ativações")` | não gatear: é o núcleo (barras/LED/contagem alimentam o resto) |
| 4 | `analysis_group` "Mapeamento Muscular e Análise Avançada (MVC, Fadiga, Co-contração)" (avançado) | `emg.mvc_fadiga` | EMG | visível, expandido | só os `setText` de `emg_fatigue_lbl`, `emg_cocontraction_lbl`, `emg_movement_lbl`, `emg_mvc_pct_lbls[ch]`; NÃO gatear `peak_envelope`/MVC (acumuladores) |
| 5 | `mnfdf_group` "Frequência Mediana (MDF) e Média (MNF)…" (avançado) | `emg.mnf_mdf` | EMG | visível, expandido | bloco "Plot MNF/MDF temporal" (`if hasattr(self, "emg_mdf_curve")` → `and gaveta_ativa(self, "emg.mnf_mdf")`), inclui a regressão/Dimitrov |
| 6 | `_g_adv` = `_build_emg_advanced_group()` "Análise Tempo×Frequência…" | `emg.tempo_freq` | EMG | **recolhido** (rfft + 2 imagens a 4 Hz) | `_emg_update_advanced(...)` só se `gaveta_ativa(self, "emg.tempo_freq")` |
| 7 | `_g_erg` = `_build_emg_ergonomics_group()` "Ergonomia (APDF)…" | `emg.ergonomia` | EMG | **recolhido** | `_emg_update_ergonomics(...)` só se `gaveta_ativa(self, "emg.ergonomia")` |

Portão compartilhado: a FFT de fadiga por canal (`fazer_fadiga`) alimenta
`_emg_median_freq_history` usado por 4, 5 e 7. Sugestão:
`fazer_fadiga = fazer_fadiga and (gaveta_ativa(self,"emg.mnf_mdf") or gaveta_ativa(self,"emg.mvc_fadiga") or gaveta_ativa(self,"emg.ergonomia"))`.
Efeito colateral aceitável: com os três fechados a série de MDF tem um buraco
(o eixo é índice de janela, não tempo; a regressão continua válida ao reabrir).
Alternativa sem o item 3 como gaveta: duas pilhas (acima e abaixo do `split`);
perde-se "mover" entre as metades.

Registro: `self._register_advanced("emg", pilha.gaveta("emg.config_envelope"), pilha.gaveta("emg.mvc_fadiga"), pilha.gaveta("emg.mnf_mdf"), pilha.gaveta("emg.tempo_freq"), pilha.gaveta("emg.ergonomia"))`.

---

## 4. Coração — `_build_ecg_tab` (≈ 55466), aba `"ecg"`

`aba_visivel = ... bio_tabs.currentIndex() == 1`. A linha `ctrl` (combo de canal,
coração, BPM, LED, `ecg_hrv_lbl`, reset) NÃO é painel: fica acima da pilha.

| Ordem | QGroupBox (variável) | id | exames | padrão sugerido | `gaveta_ativa()` em `_update_ecg_view` (≈ 56014) |
|---|---|---|---|---|---|
| 1 | `left` (`ecg_raw_plot` + MWA) e `right` (tacograma + Poincaré) — hoje `split`, `stretch=2`, `right` avançado | linha `adicionar_linha([("ecg.tracado", left, tr("Traçado ECG e detecção de picos R")), ("ecg.tacograma", right, tr("Tacograma e Poincaré"))], nome="tracado+tacograma", tamanhos=[720, 600], stretch=2)`; `ecg.tracado` com `fechavel=False` | ECG | ambos visíveis | `ecg_tacho_curve.setData` e `ecg_poincare_scatter.setData` só se `gaveta_ativa(self, "ecg.tacograma")`; o traçado/Pan-Tompkins NUNCA é gateado (gera a série RR) |
| 2 | `zone_group` "Zonas de Treino (Karvonen) + Detecção de Arritmia + Recuperação" | `ecg.zonas` | ECG | visível, expandido | barato — gatear só os `setText` (`ecg_zone_lbl`, `ecg_arrhythmia_lbl`, `ecg_peak_bpm_lbl`, `ecg_recovery_lbl`); manter o rastreio de pico/recuperação |
| 3 | `nlhrv_group` "HRV não-linear (Kubios-style) — DFA, Entropia, Poincaré" | `ecg.hrv_nao_linear` | ECG | **recolhido** | bloco "HRV NÃO-LINEAR" inteiro (SD1/SD2, DFA, entropia) sob `if gaveta_ativa(self, "ecg.hrv_nao_linear"):` |
| 4 | `spec_group` "HRV Espectral (Welch/FFT) + Geométrica…" | `ecg.hrv_espectral` | ECG | **recolhido** | bloco "HRV GEOMÉTRICA" (histograma + HTI/TINN) só se ativo; o bloco "LF/HF" (Welch) alimenta `ecg_lfhf_lbl` (que mora em `zone_group`) E `ecg_psd_curve/ecg_psd_lbl`: rodar se `gaveta_ativa("ecg.zonas") or gaveta_ativa("ecg.hrv_espectral")` e dentro dele só desenhar a PSD se o espectral estiver ativo |

Registro: `self._register_advanced("ecg", pilha.gaveta("ecg.tacograma"), pilha.gaveta("ecg.zonas"), pilha.gaveta("ecg.hrv_nao_linear"), pilha.gaveta("ecg.hrv_espectral"))`
(hoje é `right, zone_group, nlhrv_group, spec_group`, ≈ 55877). O `_lbl_mwa`/`ecg_mwa_plot`
continuam registrados individualmente (ficam dentro de `ecg.tracado`).
Se a linha 1 parecer invasiva demais numa primeira leva, deixar o `split` como está
(fora da pilha, acima) e gatear só 2–4; perde-se a divisão persistida.

---

## 5. Olhos — `_build_eog_tab` (≈ 56484), aba `"eog"`

`aba_visivel = ... bio_tabs.currentIndex() == 2`. `ctrl` e `cards` (direção,
piscadas, taxa, olho, gaze) ficam acima da pilha.

| Ordem | Widget (variável) | id | exames | padrão sugerido | `gaveta_ativa()` em `_update_eog_view` (≈ 56942) |
|---|---|---|---|---|---|
| 1 | `self.eog_plot` (hoje sem groupbox, `stretch=2`) | `eog.tracado`, `fechavel=False`, `stretch=2`, título `tr("Traçado H/V — piscadas e sacadas")` | EoG | visível | não gatear (detecção de piscadas/sacadas alimenta tudo) — opcional: se não quiser mais um texto novo, deixar fora da pilha |
| 2 | `alert_group` = `self._eog_alert_group` "Estado de Alerta (sonolência) + Sacadas + Fixação" (visível no Simples) | `eog.alerta` | EoG | visível, expandido | heurística de FIXAÇÃO (diff sobre o buffer inteiro) e os `setText` de `eog_alert_state_lbl`, `eog_saccade_count_lbl`, `eog_fixation_pct_lbl`, `eog_blink_dur_lbl`, `eog_microsleep_lbl`; NÃO gatear a detecção |
| 3 | `oc_group` "Oculometria — sequência principal das sacadas + taxa de piscadas" (avançado) | `eog.oculometria` | EoG | **recolhido** (só rende depois de minutos de sacadas) | sequência principal (`eog_mainseq_scatter.setData` + `np.polyfit`) e `eog_blinkrate_curve.setData` + tendência + PERCLOS; manter a amostragem de `_eog_blinkrate_hist` a cada 1,5 s (é a série) |

`_aplicar_nomes_bio`: `self._eog_alert_group.setTitle(...)` → `self._gavetas["eog.alerta"].set_titulo(...)`.
Registro: `self._register_advanced("eog", pilha.gaveta("eog.oculometria"))`.

---

## 6. Outras abas do Completo ("2 ou mais painéis onde for limpo")

| Aba | Painéis hoje | Recomendo? | Ids / observações |
|---|---|---|---|
| **Análises** (`_build_analysis_tab`) | `fft_group` + `band_group` lado a lado (`graph_row`, stretch 2) e `stats_group` embaixo (stretch 1) | **SIM, primeira leva** — o caso canônico de "linha" | `adicionar_linha([("ana.fft", fft_group), ("ana.bandas", band_group)], nome="fft+bandas", stretch=2)` e `adicionar_painel("ana.estatisticas", stats_group, stretch=1)`; exames EEG. `_update_analysis` (≈ 59041, 500 ms): FFT só se `gaveta_ativa("ana.fft")`, barras só se `"ana.bandas"`, laço da tabela só se `"ana.estatisticas"`; se nenhum ativo, `return` no início. Sem scroll externo: os stretches mantêm o preenchimento de hoje. |
| **Filtros e Canais** (`_build_filters_tab`) | 6 empilhados: `reref_group`, `notch_group`, `bp_group`, `ch_group`, `bad_group`, `mode_group` | **SIM** | `filtros.reref`, `filtros.notch`, `filtros.bandpass`, `filtros.canais` (o grande; a alça não encolhe formulário, mas "recolher" vale ouro aqui), `filtros.canais_ruins`, `filtros.modo_exame` com `fechavel=False` (o seletor de modo tem de continuar à mão). Exames: todos. Sem gates (formulários). `layout.addStretch()` já existe. |
| **Rede e Eventos** (`_build_network_tab`) | 4 empilhados: `udp_group`, `lsl_group`, `lslr_group`, `mk_group` | **SIM** | `rede.udp`, `rede.lsl`, `rede.lsl_receber`, `rede.marcadores`. Só aparece no Híbrido. Sem gates. |
| **Sistema › Configurações › Tema e Cores** | 7 empilhados: `atalho_group`, `theme_group`, `letra_group`, `lang_group`, `bandsel_group` (avançado), `bandcolor_group`, `custom_group` | **SIM, segunda leva** | `sistema.atalho`, `sistema.tema`, `sistema.letra`, `sistema.idioma`, `sistema.bandas_em_uso`, `sistema.cores_bandas`, `sistema.editor_tema` (**recolhido**: editor grande e raro). Cuidado: `_aplicar_nomes_sistema` renomeia títulos → `set_titulo`. Também vale em **Sessão e Arquivos** (`_sess_group`, `_savedir_group`, `export_group`) e **Caminhos e Auditoria** (2). |
| **Conexão** (`_build_connection_tab`) | `conn_group`, `bt_group`, `exp_group`, `log_group` (3 avançados) | **SIM, com cuidado (segunda leva)** | `conexao.parametros` (`fechavel=False`), `conexao.bluetooth`, `conexao.expansao`, `conexao.log` (a alça é o ganho: log alto/baixo). Há um `QScrollArea` interno e `_ajustar_grid_conexao()` refaz o grid por nível — testar o relayout antes. |
| **Estudo por Paciente** (`_build_patient_study_tab`) | `caixa_pastas`, `caixa_proc`, `caixa_met`, `caixa_saida` | **NÃO** | É um fluxo em etapas (Pastas → Processamento → Métricas → Saída); mover/fechar etapas confunde e a pilha não tem "sem mover". Se quiser só recolher, precisaria de uma opção `movivel=False` (não implementada). |
| **Topografia** | `head_group`, `focus_group`, `emg_group` dentro de `QSplitter` aninhados | **NÃO agora** | Os splitters já controlam tamanho; uma gaveta dentro deles brigaria com a alça. Candidata a uma variante "gaveta em splitter vertical" depois. |
| **ERS/ERD** | 5 groupboxes em 3 splitters aninhados | **NÃO agora** | Mesmo motivo; análise offline, baixa frequência de uso. |
| **BCI Trainer** (2), **EMG Joystick** (2 + splitter depois) | formulários pequenos | **NÃO** | Pouco ganho; no Joystick o splitter vem depois dos grupos — não é "limpo". |
| Hardware (1), Protocolo (4 — editor em sequência), Mapeamento (1), Espectrograma/Tempo Real/Histórico/Calibração/ERP/Conectividade (0), Offline (splitters), Layout Custom (persistência própria) | — | fora de escopo | — |

---

## 7. Chaves novas de `tr()` (para o `test_vazamento_idioma` não quebrar)

Acrescentar nos dicionários `_en`, `_es`, `_it`, `_fr`, `_zh`, `_de`, `_ja`, `_ru`
da classe `I18N`. `"Fechar"` já existe. Se os títulos sugeridos nos §3–5 forem
adotados (`Canais EMG — envelope e ativações`, `Traçado ECG e detecção de picos R`,
`Tacograma e Poincaré`, `Traçado H/V — piscadas e sacadas`), traduzi-los também.

| pt (chave) | en | es | it | fr | zh | de | ja | ru |
|---|---|---|---|---|---|---|---|---|
| Painéis | Panels | Paneles | Pannelli | Panneaux | 面板 | Bereiche | パネル | Панели |
| Mostrar, ocultar e arrumar os painéis desta aba | Show, hide and arrange this tab's panels | Mostrar, ocultar y ordenar los paneles de esta pestaña | Mostra, nascondi e sistema i pannelli di questa scheda | Afficher, masquer et ranger les panneaux de cet onglet | 显示、隐藏和整理此标签页的面板 | Bereiche dieses Reiters anzeigen, ausblenden und anordnen | このタブのパネルを表示・非表示・整理 | Показать, скрыть и упорядочить панели этой вкладки |
| Recolher todos | Collapse all | Contraer todos | Comprimi tutti | Tout replier | 全部折叠 | Alle einklappen | すべて折りたたむ | Свернуть все |
| Expandir todos | Expand all | Expandir todos | Espandi tutti | Tout déplier | 全部展开 | Alle ausklappen | すべて展開 | Развернуть все |
| Restaurar o padrão | Restore default | Restaurar el predeterminado | Ripristina predefinito | Rétablir la disposition par défaut | 恢复默认 | Standard wiederherstellen | 既定に戻す | Восстановить по умолчанию |
| Recolher | Collapse | Contraer | Comprimi | Replier | 折叠 | Einklappen | 折りたたむ | Свернуть |
| Expandir | Expand | Expandir | Espandi | Déplier | 展开 | Ausklappen | 展開 | Развернуть |
| Opções do painel | Panel options | Opciones del panel | Opzioni del pannello | Options du panneau | 面板选项 | Bereichsoptionen | パネルのオプション | Параметры панели |
| Fechar painel (reabra pelo botão Painéis) | Close panel (reopen from the Panels button) | Cerrar panel (vuelva a abrirlo con el botón Paneles) | Chiudi pannello (riaprilo dal pulsante Pannelli) | Fermer le panneau (rouvrir via le bouton Panneaux) | 关闭面板（可通过"面板"按钮重新打开） | Bereich schließen (über die Schaltfläche Bereiche wieder öffnen) | パネルを閉じる（「パネル」ボタンで再表示） | Закрыть панель (открыть снова кнопкой «Панели») |
| Arraste para mudar a altura · duplo clique: tamanho padrão | Drag to change the height · double-click: default size | Arrastre para cambiar la altura · doble clic: tamaño predeterminado | Trascina per cambiare l'altezza · doppio clic: dimensione predefinita | Glisser pour changer la hauteur · double-clic : taille par défaut | 拖动调整高度 · 双击：默认大小 | Ziehen ändert die Höhe · Doppelklick: Standardgröße | ドラッグで高さを変更 · ダブルクリック：既定サイズ | Перетащите, чтобы изменить высоту · двойной щелчок: размер по умолчанию |
| Mover para cima | Move up | Subir | Sposta in alto | Monter | 上移 | Nach oben | 上へ移動 | Переместить вверх |
| Mover para baixo | Move down | Bajar | Sposta in basso | Descendre | 下移 | Nach unten | 下へ移動 | Переместить вниз |
| Tamanho padrão | Default size | Tamaño predeterminado | Dimensione predefinita | Taille par défaut | 默认大小 | Standardgröße | 既定サイズ | Размер по умолчанию |

---

## 8. Decisões tomadas no protótipo (e por quê)

- **Fechar = esconder.** `set_visivel_painel(False)` só chama `setVisible(False)`;
  widgets, curvas e históricos continuam vivos. O "não gasta processamento" vem dos
  gates `gaveta_ativa()` nos laços, não de destruir nada.
- **`esta_ativo()`** = aberto ∧ não recolhido ∧ `aba_visivel()` ∧ (com a janela na
  tela) `isVisible()`. O último termo cobre de graça "aba não corrente" (QStackedWidget
  esconde as páginas) e "escondido pelo Simples/_register_advanced".
- **Cromo só no Completo.** Com `simples=True` cabeçalho, menu e alça nem são criados
  (`_garantir_cromo` cria na primeira troca para o Completo). No Simples o estado da
  gaveta (fechado/recolhido/altura) é ignorado: quem manda é `_apply_detail_level`.
- **Gaveta "transparente" para o layout.** Quando `altura is None` a gaveta tem a
  política de tamanho do QGroupBox de hoje (inclusive herdando a expansividade do
  conteúdo). Recolhida vira `Fixed`; com altura fixa o corpo é `setFixedHeight`.
  Uma gaveta com `stretch>0` perde o stretch enquanto estiver recolhida/fixa
  (`_stretch_efetivo`), e a pilha tem um espaçador final de stretch 0 que só
  absorve espaço quando nada mais pode crescer.
- **Linha lado a lado** = `QSplitter` horizontal de células (`_CelulaLinha`): a
  gaveta recolhida fica colada no alto da célula em vez de esticar até a altura da
  vizinha; fechada, some e a vizinha ocupa a largura toda; o `splitterMoved` grava
  em `splits[nome]`.
- **Mover** move o item (gaveta ou linha inteira); `ordem` no config é a lista
  achatada de ids e, ao aplicar, os itens são ordenados pela posição do primeiro id.
- **Mínimo da alça** = `minimumSizeHint` do conteúdo: formulário não encolhe abaixo
  do que precisa (para sumir, recolhe-se). Duplo clique = `tamanho_padrao()`.
- **Títulos**: o QGroupBox escreve `&` como `&&`; a gaveta guarda o título canônico
  (com `&`), mostra-o no QLabel e escapa de novo só no QAction do menu.
- **`setVisible` sobrescrito** na gaveta para um `show()` de fora não reabrir painel
  fechado no Completo (é o que `_apply_detail_level` faz ao trocar de nível).

---

## 9. Dúvidas de design em aberto

1. **Esticar ou não.** A gaveta "natural" herda a expansividade do conteúdo, como o
   QGroupBox hoje — num tab sem scroll e com espaço sobrando, a moldura cresce com
   vazio dentro (ver `gavetas_recolhidas.png`, painel HRV). Alternativa: política
   `Maximum` (fica no `sizeHint`, o vazio vai para o fim da aba). Qual o autor prefere?
2. **Painéis-núcleo não fecháveis** (`fechavel=False`: canais EMG, traçado ECG/EOG,
   modo do exame, parâmetros de conexão) — manter a trava ou deixar fechar tudo?
3. **Mover dentro de uma linha**: o menu move a linha inteira; não há "trocar de
   lado". Precisa?
4. **Alça em formulários** só aumenta (mínimo = tamanho natural). Esconder a alça
   quando o conteúdo não encolhe?
5. **Estado por aba, global**: não varia por modo de exame nem por voluntário. O P4
   grava perfis via `estado_para_perfil(exames)` (não recomendados nascem fechados) —
   confirmar se é esse o comportamento esperado do perfil.
6. **Gravação**: cada arranjo chama `config.save()` (arquivo inteiro, fsync + .bak)
   após 500 ms parado. Alternativa: gravar só ao trocar de aba/fechar.
7. **Buracos nas séries** quando um painel que alimenta histórico (MDF, taxa de
   piscadas) fica fechado: aceitamos (eixo em índice) ou mantemos esses acumuladores
   sempre ligados e gateamos só o desenho? (As notas acima sugerem o segundo para
   ECG/EOG e o primeiro para a FFT de fadiga EMG, que é a parte cara.)
8. **Combo local "Detalhe desta aba" = Simples com global Completo**: o cromo
   permanece (o nível que decide é o global). Coerente?
9. **Glifos em texto** (▾ ▸ ⋯ ×): dependem da fonte do sistema ter os símbolos
   (DejaVu/Segoe UI/Inter têm). Precisa de fallback em ASCII (`v > ... x`)?
10. **Abas Topografia/ERS-ERD** (groupboxes dentro de splitters): ficam para uma
    variante "gaveta em QSplitter vertical", se o autor quiser.
