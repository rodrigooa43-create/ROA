# Replay: ver a gravação como uma animação

> Manual do Usuário → Capítulo "Rever uma gravação" → nova seção "Replay" (depois de "Relatório PDF").

Ao abrir uma gravação de **músculos**, **coração** ou **olhos**, o botão
**▶ Replay** fica disponível (ele fica desligado para gravações de cérebro).
Abre uma janela com um tocador comum aos três exames: **▶ Tocar / ⏸ Pausar**,
**⏮ Início**, a linha do tempo arrastável e o relógio "0:05 / 0:30". No
Completo há também a velocidade (0,25× a 4×) e *Repetir*.

> A animação **simula** o que foi gravado: não é o vídeo da pessoa, e não é
> laudo nem diagnóstico. O selo no alto da janela repete isso.

## Músculos

Uma figura articulada vista de lado (tronco, ombro, cotovelo, antebraço,
punho, mão com dedos) refaz o **movimento marcado** na linha do tempo, e cada
músculo acende com a intensidade medida naquele instante. Supinação e
pronação são inconfundíveis: a palma clara virada para cima ou o dorso virado
para baixo, com o texto "palma para cima/baixo".

A linha do tempo (2 a 4 faixas) nasce dos **marcadores e fases** da gravação
("Flexão", "Extensão", "Repouso"…); sem marcador, as **contrações detectadas**
viram trechos "a definir". Faixas no mesmo instante se **somam** (por exemplo,
fechar a mão enquanto o cotovelo flexiona). Movimentos disponíveis: flexão e
extensão do cotovelo, supinação, pronação, flexão e extensão do punho, abrir e
fechar a mão, pinça, flexão e extensão do ombro, repouso.

No **Simples** você vê o tocador, a figura e a lista de trechos. No
**Completo** a linha do tempo é editável: arraste um bloco para movê-lo,
puxe a borda para esticar, clique com o botão direito para *Trocar o
movimento*, *Dividir aqui*, *Apagar*, *Adicionar/Remover faixa*; Ctrl+Z
desfaz. *Tarefa pronta* insere, a partir do cursor, uma sequência com o objeto
preso à mão: **levantar o halter**, **abrir/fechar a porta com a chave**,
**pegar o copo na mesa e levar à boca**. Quando os músculos ativos não
combinam com o movimento escolhido (por exemplo, tríceps ativo num trecho de
flexão), um aviso aparece. *Salvar* grava `movimentos.json` ao lado da
gravação; o programa pergunta se há marcações não salvas ao fechar.

## Coração

Um coração desenhado **bate no ritmo gravado**, ao lado do traçado com o
cursor e dos batimentos por minuto. A faixa embaixo mostra **todas** as
batidas: a regular é um traço fino; a **batida adiantada** é um triângulo
laranja; a **pausa maior** é um retângulo vazado vermelho (cor e forma, para
quem não distingue cores). A lista em palavras ("0:13 batida adiantada",
"0:25 pausa maior (1,7 s)") é clicável e leva o tocador até lá. As batidas são
as mesmas do relatório PDF. No Completo, o botão direito na faixa permite
**corrigir** (remover batida, adicionar batida aqui, marcar como regular /
adiantada / pausa maior); *Salvar* grava `batidas.json`.

## Olhos

Dois olhos desenhados **piscam nas piscadas e olham** para onde os sinais
mandam. *Inverter horizontal* e *Inverter vertical* trocam os lados, para o
caso de os eletrodos terem sido colocados ao contrário. A linha do tempo diz
em palavras o que aconteceu ("0:03 piscou", "0:05 olhou para a direita") e os
contadores somam piscadas e movimentos para os lados e para cima/baixo. No
Completo, o botão direito na lista remove um evento ou troca a direção;
*Salvar* grava `olhos.json`.
