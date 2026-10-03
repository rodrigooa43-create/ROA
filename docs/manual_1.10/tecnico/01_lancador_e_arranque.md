# Lançador, cache de bytecode e arranque (1.10.0)

> Manual Técnico → Capítulo "Arquitetura" → nova seção depois de "Arquivo único ROA.py".

**Problema medido (1.9.0).** `EEG_Data_Collector.py` chamava
`runpy.run_path("ROA.py")`, que compila o fonte de ~80 mil linhas a cada
abertura (6,7 s no Windows do autor); o import do `scipy.signal` custava mais
1 a 2 s e nada disso era necessário para a tela inicial.

**Solução (lançador).**
1. *Cache de bytecode*: o lançador compila o `ROA.py` uma vez para
   `<pasta do programa>/.roa_cache/ROA.py.<cache_tag>.pyc` (ou
   `%LOCALAPPDATA%\ROA\cache` se a pasta não for gravável; último recurso, a
   pasta temporária). O arquivo tem um cabeçalho próprio: número mágico do
   bytecode da versão do Python + `mtime_ns` + tamanho do fonte. Qualquer
   diferença invalida o cache. A compilação da primeira vez roda num
   subprocesso (`--compilar-cache`) para a tela de abertura não congelar; se
   o subprocesso falhar, compila em memória.
2. *Execução*: o code object roda num módulo `__main__` novo com
   `__file__` = caminho do `ROA.py` (o atualizador grava em `__file__`;
   `SCRIPT_DIR` deriva dele), `sys.argv[0]` e `sys.path[0]` como `runpy`.
3. *Tela de abertura* (`SplashROA`): janela sem moldura, pintada à mão (sem
   widgets filhos, imune ao stylesheet que o ROA aplica depois), com a logo
   (`roa_logo.png` se existir; senão a marca escrita), fade de 900 ms, linha
   de sinal se desenhando em 1,4 s, progresso em palavras nos 9 idiomas
   (lidos de `config.json` sem importar o ROA) e fundo claro/escuro conforme o
   tema salvo. Fecha com fade de 260 ms quando qualquer outra janela de pelo
   menos 200×120 fica visível (polling a 60 Hz), ou após 90 s. O ROA.py pode
   escrever o progresso por `sys.modules["roa_splash"].progresso(texto)`;
   um ROA.py antigo funciona sem saber disso.
4. *Pré-import em thread*: numpy, PySide6.QtWidgets, pyqtgraph,
   serial.tools.list_ports e scipy.fft são importados numa thread enquanto a
   animação roda; falhas são ignoradas (o import real dentro do ROA.py mostra
   o erro).

**Solução (ROA.py).** `scipy.signal` e `scipy.fft` viraram proxies
preguiçosos (`_ModuloAdiado`): o módulo real é importado na primeira leitura
de atributo (hoje em `FilterChain.__init__`, ao construir a janela). `bleak`
deixou de ser importado no topo (`HAS_BLEAK = _module_available("bleak")`;
import real em `_BluetoothScanThread.run`). O diagnóstico do núcleo C++
`ob_core` roda 2 s depois de a janela aparecer (`_diagnostico_ob_core`).

**Medição.** `ferramentas/mede_arranque.py [N] [--sem-cache]` abre o programa
N vezes com `ROA_MEDIR_ARRANQUE=<time.time()>`; o `main()` imprime
`ROA_ARRANQUE_PRONTO <s>` quando a primeira tela está desenhada. Resultados no
`CHANGELOG.md`.

**Compatibilidade.** O `.exe` antigo (lançador 1.9.0 embutido) continua
abrindo o ROA.py novo, sem cache nem splash. O manifesto `version.json`
aceita as chaves opcionais `launcher_url` e `launcher_sha256`; com elas,
`_atualizar_lancador` grava o `EEG_Data_Collector.py` ao lado do programa
(só se o `.py` existir, depois do ROA.py, com SHA-256 conferido e `compile()`
OK). Sem `update_config.json`, `_check_updates_manual` usa `VERSION_URL_PADRAO`.
