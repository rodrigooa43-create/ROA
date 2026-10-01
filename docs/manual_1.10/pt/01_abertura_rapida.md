# Abrir o programa (tela de abertura)

> Manual do Usuário → Capítulo "Instalação e primeira execução" → depois de "Abrir o programa".

Ao abrir o ROA aparece uma pequena tela com a logo e uma linha de sinal se
desenhando. Embaixo dela, em palavras, o programa diz o que está fazendo
("Carregando as bibliotecas…", "Montando a tela inicial…"). Essa tela some
sozinha assim que a tela inicial estiver pronta; nada precisa ser clicado.

**Primeira abertura depois de instalar ou atualizar.** O programa é preparado
uma vez (a tela diz "Preparando o programa pela primeira vez…") e guarda o
resultado na pasta `.roa_cache`, ao lado do programa. Das vezes seguintes a
abertura é bem mais rápida. Se a pasta do programa não permitir gravação (por
exemplo, em `Arquivos de Programas`), o cache vai para a pasta do usuário
(`%LOCALAPPDATA%\ROA\cache`). Apagar essa pasta não causa problema: ela é
refeita na abertura seguinte.

**Se a tela de abertura atrapalhar** (por exemplo, numa automação ou num
computador com problema de vídeo), abra o programa com a opção `--sem-splash`
ou defina a variável de ambiente `ROA_SEM_SPLASH=1`.

**Atualizações.** Em *Ajuda → Verificar atualizações* o programa continua
baixando só o próprio código, nunca enviando dados seus. A partir desta versão
ele também pode atualizar o lançador (`EEG_Data_Collector.py`) quando a
atualização trouxer uma versão nova dele; se não conseguir, avisa e o
programa segue funcionando com o lançador atual.
