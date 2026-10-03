# Atlas muscular em código (1.10.0)

> Manual Técnico → Capítulo "Widgets desenhados" → substitui a seção do MuscleAtlasWidget.

`AtlasCorpoWidget` (bloco antes de `class MuscleAtlasWidget`, que fica no
arquivo sem ser instanciado) tem a mesma API pública do widget antigo mais
`set_area/get_area/areas_disponiveis`, `set_numeracao`, `set_miniatura`.
Geometria em `CorpoHumanoDesenho`: pontos-guia em unidades de cabeça,
spline Catmull-Rom centrípeta → Bézier cúbica; vistas `front`/`back`/`side`
(`ATLAS_VISTAS`), 14 áreas (`ATLAS_AREAS`, recortes normalizados do corpo
inteiro; `para_area/de_area`), `ELETRODOS_SENIAM` (ponto do ventre por
músculo, lado D/E por espelho; 19 chaves antigas + rosto + extras), calor por
`pintar_calor` (gradiente radial, escala térmica própria, recortado pelo
corpo). O corpo é pintado numa camada QPixmap cacheada por (vista, tamanho,
cores, zoom): ~3 ms por quadro em 300×470.

Integração: `self.emg_atlas = AtlasCorpoWidget()` em `_build_emg_atlas_group`;
combo de vista com userData `view:front|back|side` e `area:<id>`;
`converter_montagem_antiga(eletrodos, ATLAS_MUSCLE_XY)` roda em
`set_electrodes` para itens sem `atlas == 2`; `AppConfig.load` aceita `view`
em `("front","back","side")` e preserva `atlas`. Chaves dinâmicas (áreas,
músculos, nomes curtos) em `ferramentas/chaves_extras.txt`. Teste:
`testes/test_p3_atlas.py`.
