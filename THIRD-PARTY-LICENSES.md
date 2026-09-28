# Licenças de Terceiros — ROA (OpenBionica)

O código do **ROA** é licenciado sob **MIT** (ver [LICENSE](LICENSE)).
Este projeto, porém, **depende de bibliotecas de terceiros**, cada uma sujeita à
**sua própria licença**. Os direitos sobre esses componentes pertencem aos
respectivos autores. Esta página atende à cláusula 10 do
[TERMO_DE_USO.md](TERMO_DE_USO.md).

> Gere uma lista exata da sua instalação com:
> `pip install pip-licenses && pip-licenses --format=markdown --with-urls`

---

## Interface gráfica (PySide6 / Qt) — LGPL v3

A interface usa **PySide6** (Qt for Python, da The Qt Company), licenciado sob
**LGPL v3** (também disponível sob comercial). O **Qt** subjacente é
**LGPL v3 / comercial**.

**Implicação prática (favorável):**
- A **LGPL v3** **não** impõe copyleft ao código do aplicativo. O código do
  ROA permanece sob **MIT**, e **distribuir um binário** que
  empacota PySide6/Qt é permitido, desde que cumpridas as condições da LGPL:
  - incluir o **texto da licença LGPL/Qt** e o aviso de uso do Qt;
  - permitir a **substituição das bibliotecas Qt** pelo usuário (no
    PyInstaller `--onedir`, as DLLs do Qt ficam acessíveis na pasta, o que
    satisfaz o requisito de relinking/substituição);
  - disponibilizar o **código-fonte do aplicativo** (já público neste repo).
- Mesmo assim, o `.exe` **não** é versionado no Git (é grande e binário) — é
  distribuído como *release asset*, acompanhado do fonte.

> Histórico: versões iniciais usaram **PyQt6** (GPL v3). O projeto **migrou para
> PySide6 (LGPL v3)** justamente para permitir a distribuição do binário sem
> impor GPL ao aplicativo.

---

## Bibliotecas e licenças

| Biblioteca | Licença | Site |
|------------|---------|------|
| **PySide6** (Qt for Python) | **LGPL v3** ou comercial | https://doc.qt.io/qtforpython/ |
| **Qt 6** (via PySide6) | **LGPL v3** ou comercial | https://www.qt.io/licensing |
| pyqtgraph | MIT | https://www.pyqtgraph.org/ |
| NumPy | BSD-3-Clause | https://numpy.org/ |
| SciPy | BSD-3-Clause | https://scipy.org/ |
| pyserial | BSD-3-Clause | https://github.com/pyserial/pyserial |
| pylsl / liblsl | MIT | https://github.com/labstreaminglayer/liblsl-Python |
| pyedflib | BSD-2-Clause | https://github.com/holgern/pyedflib |
| MNE-Python | BSD-3-Clause | https://mne.tools/ |
| matplotlib | Matplotlib License (estilo BSD/PSF) | https://matplotlib.org/stable/users/project/license.html |
| ReportLab | BSD-3-Clause (ReportLab) | https://www.reportlab.com/ |
| scikit-learn | BSD-3-Clause | https://scikit-learn.org/ |

As bibliotecas opcionais (pylsl, pyedflib, MNE, matplotlib, reportlab,
scikit-learn) só são exigidas para recursos específicos; o aplicativo degrada
graciosamente quando ausentes.

> Os textos completos das licenças de cada componente acompanham os respectivos
> pacotes (ex.: nas pastas `*.dist-info/` do ambiente Python). Para componentes
> sob LGPL/GPL, inclua o texto integral da licença ao redistribuir binários.
