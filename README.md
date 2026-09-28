# ROA (Research Open Analysis)

Software livre, gratuito e **100% offline** para coleta, visualização e análise de
biossinais em tempo real: EEG (cérebro), EMG (músculos), ECG (coração) e EOG (olhos).
Serve tanto para aplicar um exame numa clínica quanto para pesquisa.

> **Não é dispositivo médico.** É software de pesquisa e ensino. Não use para
> diagnóstico ou decisão clínica. Leia `DISCLAIMER.txt` e `TERMO_DE_USO.md`.

## Dois modos de uso

- **Simples (exame)**: é o padrão. Tela inicial com duas escolhas, um botão em destaque
  por vez e a barra "Passo 1 de 3 → 2 de 3 → 3 de 3" (conectar, gravar, gerar o
  relatório). O relatório em PDF começa com um quadro "Como ler este relatório", em
  linguagem comum.
- **Completo (pesquisa)**: todas as análises (FFT, bandas, topografia, ERD/ERS, ICA,
  conectividade, estatística guiada, exportação EDF/FIF, LSL etc.). Dá para trocar de
  modo a qualquer momento, sem reiniciar.

Sem o aparelho? Use **Treino (sem aparelho)** na tela inicial: o programa mostra um sinal
de exemplo e todas as telas funcionam.

## Como rodar a partir do código

Requer Python 3.10 ou mais novo (testado com 3.12).

```bash
pip install -r requirements.txt
python ROA.py
```

O pacote pronto para uso (executável para Windows, manuais do usuário em nove idiomas,
manual técnico, documentação e termos) é distribuído pelo autor à parte deste repositório.

## Aparelhos e arquivos

- Placas compatíveis com o protocolo OpenBCI (Cyton, com ou sem módulos de expansão),
  pela porta USB. O programa encontra a porta sozinho.
- Importa gravações em EDF/BDF e CSV de outros sistemas.
- As gravações ficam na pasta `sessions/` ao lado do programa e as configurações em
  `Documentos/EEG_Coletor`. Nada é enviado para a internet.

## Arquivos deste repositório

| Arquivo | O que é |
|---|---|
| `ROA.py` | o programa (arquivo único) |
| `OpenBionica.py` | cópia idêntica de `ROA.py`, com o nome antigo, para quem atualiza a partir de versões anteriores |
| `EEG_Data_Collector.py` | lançador de compatibilidade usado pelo executável; não edite |
| `version.json` | versão publicada e SHA-256 do `ROA.py`; é o que o menu **Ajuda › Verificar atualizações** lê (só quando você pede) |
| `CHANGELOG.md` | histórico de versões, com a seção "Conhecido" (limitações atuais) |
| `LICENSE` | licença MIT |
| `TERMO_DE_USO.md`, `TERMS_OF_USE_EN.md` | termo de uso (português e inglês) |
| `THIRD-PARTY-LICENSES.md` | licenças das bibliotecas usadas |
| `DISCLAIMER.txt` | aviso: software de pesquisa, não é dispositivo médico |
| `CITATION.cff` | como citar |
| `SECURITY.md`, `GOVERNANCE.md` | política de segurança e governança do projeto |

## Uso com pessoas

Coletas com participantes humanos exigem aprovação de Comitê de Ética em Pesquisa (CEP)
e Termo de Consentimento Livre e Esclarecido (TCLE). Trate os dados conforme a LGPD:
o programa usa códigos de paciente (V01, V02...) nas pastas, e os dados ficam só na sua
máquina.

## Licença e citação

MIT. Se usar em pesquisa, cite conforme `CITATION.cff`.
