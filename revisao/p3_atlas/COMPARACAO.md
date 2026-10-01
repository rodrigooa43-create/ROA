# P3 — Atlas muscular: comparação das propostas de estilo

Três estilos de pintura sobre a MESMA geometria anatômica (spline Catmull-Rom
centrípeta convertida em Bézier cúbica, 8 cabeças de altura, ombros ≈ 2
cabeças, caixa do corpo 4 × 8 unidades de cabeça), todos em QPainter puro,
sem imagens. Módulo: `scratchpad/prototipos/p3_atlas_propostas.py`.
Imagens: `proposta_<A|B|C>_<frente|costas|lado>_<claro|escuro>.png` (300 × 470),
`*_mini.png` (90 × 140), `*_claro_grande.png` (600 × 900) e as folhas de
contato `propostas_folha_claro.png` / `propostas_folha_escuro.png`.

| | A — linha clínica | B — silhueta com volumes | C — anatômico delineado |
|---|---|---|---|
| Traço | contorno fino, preenchimento plano, sombra radial só nas junções (axila, virilha, queixo, tornozelo) | gradientes radiais discretos por grupo muscular + sombra interna da borda, contorno leve | contorno + linhas internas dos grupos (peitoral, deltoide, bíceps, reto abdominal, oblíquos, quadríceps, tibial, tríceps, latíssimo, eretores, isquiotibiais, gastrocnêmio) |
| Estética (claro) | limpa, "ficha clínica"; um pouco chapada no corpo inteiro | a mais "acabada": sensação de volume sem parecer render 3D | ilustração de atlas; as linhas dão ritmo e orientam o olho |
| Estética (escuro) | o corpo quase some contra o fundo (resolvido só clareando o preenchimento) | a melhor: os realces fazem o corpo se destacar do fundo sem contorno forte | boa; linhas em 50 % de mistura com o texto ficam legíveis sem gritar |
| Fidelidade anatômica | igual (mesma geometria) | igual; os volumes sugerem onde os ventres estão | a maior: as linhas marcam onde o ventre muscular (ponto SENIAM) fica, o que ajuda a colar o eletrodo no lugar certo |
| Miniatura 90 × 140 | corpo + pontos legíveis; sombras somem (ok) | corpo + pontos legíveis; os volumes ainda se percebem | corpo + pontos legíveis; as linhas viram ruído fino, quase invisíveis (ok) |
| Pintura DIRETA 300 × 470 (média de 50) | **4,2 ms** | 7,7 ms | 7,2 ms |
| Pintura DIRETA 600 × 900 (média de 50) | **9,9 ms** | 21,7 ms | 17,8 ms |
| Com CAMADA cacheada 300 × 470 | 2,5 ms | 2,3 ms | 2,5 ms |
| Com CAMADA cacheada 600 × 900 | 3,9 ms | 3,8 ms | 4,1 ms |

Tempos medidos offscreen (raster) nesta máquina, quadro completo: fundo,
corpo, 6 manchas de calor, 6 eletrodos com anel, título e rodapé.

## O que o tempo revelou

O perfil por componente (600 × 900) mostrou onde o custo está: traço largo
translúcido RECORTADO pelo corpo (sombra interna) = 6,4 ms; 15 gradientes
radiais de volume = 4,5 ms; contorno = 1,7 ms; 6 manchas de calor = 2,5 ms;
preenchimento = 0,6 ms; linhas internas = 0,07 ms; texto = 0,1 ms.

Conclusão: as linhas internas (C) são praticamente de graça; o que pesa são
sombra interna e volumes (B). Como o corpo é ESTÁTICO entre dois quadros (só
calor e eletrodos mudam, ~2×/s), o corpo passou a ser pintado uma vez numa
camada QPixmap transparente (cache por vista, tamanho, cores do tema e
transformação de zoom, no espaço da tela — nítida sob zoom) e cada quadro
custa um `drawPixmap`. Com isso os três estilos ficam em ~2,5 ms a 300 × 470
e ~4 ms a 600 × 900, e a escolha pode ser puramente estética e funcional.
A pintura direta continua sendo usada só na exportação (`render_highres`),
onde a nitidez na escala pedida importa mais que o tempo.

## Escolha: C com os volumes de B (atenuados)

- **C** é a que melhor serve a função: as linhas dos grupos musculares em
  traço leve dizem onde está o ventre do músculo, exatamente a informação
  de que o operador precisa para colar o eletrodo no ponto SENIAM. A
  numeração e o calor continuam legíveis por cima (as linhas têm ~95–130 de
  alfa).
- **B** vence no tema escuro e na sensação de "desenho acabado"; seus volumes
  foram incorporados ao final com alfa menor (95 escuro / 150 claro contra
  130/180 da proposta pura), para dar corpo sem competir com o calor.
- **A** fica como referência de custo mínimo; perde em legibilidade no tema
  escuro e em orientação anatômica.

O final (`p3_atlas_final.py`, `CorpoHumanoDesenho.volumes = True`) mede
2,9–3,6 ms a 300 × 470 e 4,6–5,2 ms a 600 × 900 pela rota do paintEvent
(camada cacheada), ~10–12 ms na pintura direta de exportação.

## Iterações feitas depois de olhar as imagens

1. Cabeça um pouco maior e orelhas no contorno; punho mais fino (0,22 UC) e
   dedos indicados por três traços; polegar lateral (posição anatômica).
2. Pés mais largos com dedos; quadril e tórax lateral mais largos; joelhos e
   cintura com curvas, nada de tubos.
3. Costas: o "losango" do trapézio virou um V suave + borda medial e espinha
   das escápulas; pregas glúteas e poplíteas; olécrano.
4. Perfil: tronco mais fundo (peito −0,54 UC, dorso +0,50), curva lombar,
   glúteo a +0,58 UC, nariz discreto, orelha e queixo; braço com contorno
   próprio por cima do tronco.
5. Rosto: linhas (cabelo, sobrancelhas, olhos, nariz, boca, queixo) só
   aparecem quando a cabeça tem ≥ 45 px de altura — invisíveis no corpo
   inteiro de 300 × 470, nítidas na área "Rosto".
6. Tema escuro: preenchimento do corpo a 10 % de mistura com a cor do texto
   (antes 5 %) para o corpo não sumir no fundo.
7. Bug corrigido no final: as linhas internas sumiam nas áreas ampliadas
   porque o pincel da pele preenchia cada linha aberta como polígono —
   `NoBrush` antes de desenhá-las.
8. Rótulos: nome curto do músculo (`ATLAS_NOMES_CURTOS`), "%MVC" → "%", Q só
   em janela ≥ 400 px, nome padrão "E<n>" omitido (o número já está no
   disco), caixa para FORA do corpo com troca de lado quando não cabe,
   linha-guia até o marcador e marcadores pintados por cima dos rótulos.

## Escala de cor do calor

Térmica: azul (52,118,222) → ciano (54,176,196) → âmbar (240,182,52) →
laranja (236,110,36) → vermelho (214,36,44). Testada nos dois temas
(`final_calor_niveis.png`): a viridis usada no mapa EEG começa num roxo
quase preto que some no tema escuro e termina num amarelo que some no claro;
a térmica tem contraste em todas as âncoras sobre `surface_alt` claro e
escuro, e lê-se como "frio → quente" sem legenda. A mancha cresce de 0,6 a
1,5 vezes o raio base (7,5 % da altura do corpo) e o alfa do centro sobe de
70 a 230 com a intensidade; a borda é sempre transparente e a mancha é
recortada pelo contorno do corpo (`setClipPath`).
