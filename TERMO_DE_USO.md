<!-- ANTES DE PUBLICAR, revise: (1) o nome do Autor/responsavel (Secao 2) — para validade juridica plena, use seu nome civil completo no lugar de 'ROA'; (2) confirme o e-mail de contato. Modelo: recomenda-se revisao por advogado. -->

# TERMO DE CONSENTIMENTO E USO DO SOFTWARE

**ROA** — Projeto ROA
Versão deste termo: 1.0 — Ano: 2026

> Leia este termo com atenção antes de instalar ou usar o software. Ao prosseguir com a instalação ou o uso, você declara que leu, entendeu e concorda integralmente com todas as condições abaixo. Caso não concorde, não instale e não utilize o software.

---

## 1. Definições

Para os fins deste Termo, aplicam-se as seguintes definições:

1.1. **"Software"**: o programa de computador **ROA**, desenvolvido no âmbito do projeto **ROA**, incluindo seu código-fonte e suas versões oficiais distribuídas pelo Autor.

1.2. **"Autor"**: a pessoa identificada na Seção 2 como responsável pelo desenvolvimento e pela distribuição oficial do Software.

1.3. **"Você", "Usuário" ou "Operador do Software"**: a pessoa física ou jurídica que instala, executa ou utiliza o Software. O termo "Operador do Software" é empregado no sentido leigo de "quem opera o programa" e **não** se confunde com a figura do "operador" da Lei Geral de Proteção de Dados Pessoais (ver Seção 6).

1.4. **"Participante"**: qualquer terceiro (voluntário, aluno, paciente, sujeito de pesquisa etc.) de quem o Usuário venha a coletar, registrar ou processar biossinais ou outros dados por meio do Software.

1.5. **"Dados Coletados"**: os biossinais, gravações, medidas, metadados de sessão e demais dados que o Usuário capturar, gerar ou processar por meio do Software, especialmente os relativos a Participantes.

1.6. **"Licença"**: a licença de código aberto sob a qual o Software é distribuído, identificada na Seção 4.

---

## 2. Identificação

2.1. O **ROA** é um programa de computador **open source** (código aberto) e **SEM FINS LUCRATIVOS**, desenvolvido no âmbito do projeto **ROA**.

2.2. Autor / Responsável: **ROA (projeto pessoal e independente)**.

2.3. Contato: **rodrigooa43@gmail.com**.

2.4. Repositório oficial do código-fonte: **https://github.com/rodrigooa43-create/OpenBionica**.

2.5. Titularidade dos direitos autorais: **© 2026 ROA**, ressalvada a Licença de que trata a Seção 4.

2.6. O Software é distribuído gratuitamente, sem qualquer cobrança, mensalidade ou licença paga.

2.7. **Projeto pessoal e independente.** O Software é um projeto **pessoal e independente** do Autor, que age em nome próprio. O Software **não representa, não vincula e não exprime posição** de qualquer instituição, universidade, empresa, órgão público ou entidade, e nenhuma relação institucional deve ser presumida a partir do seu uso.

---

## 3. O que o Software é e o que faz

3.1. O Software é uma ferramenta para **coleta, visualização e análise de biossinais** — tais como EEG (eletroencefalografia), EMG (eletromiografia), ECG (eletrocardiografia), EoG (eletrooculografia) e dados de acelerômetro — destinada a **pesquisa e educação**.

3.2. **Finalidade.** O Software se destina exclusivamente a fins de **pesquisa científica e ensino/aprendizado**. Não é um produto comercial nem clínico.

3.3. **DECLARAÇÃO IMPORTANTE — NÃO É DISPOSITIVO MÉDICO.**
O Software **NÃO é um dispositivo médico**, **NÃO foi certificado** por qualquer autoridade sanitária e **NÃO deve ser usado para diagnóstico, tratamento, monitoramento clínico ou qualquer decisão de saúde**. Os sinais, medidas, gráficos e análises produzidos têm caráter exploratório/educativo e **não substituem** avaliação, parecer ou conduta de profissional de saúde habilitado. **Nunca tome decisões clínicas com base nos resultados do Software.**

3.4. **Não constitui aconselhamento.** O Software e qualquer resultado, sinal, medida, gráfico ou análise por ele produzidos **não constituem aconselhamento médico, clínico, diagnóstico, terapêutico, psicológico, jurídico, científico-conclusivo nem regulatório**, e seu uso **não cria** qualquer relação médico-paciente nem profissional-cliente entre o Autor e o Usuário ou os Participantes.

3.5. **Segurança elétrica (hardware).** O Software é apenas *software* e **não fornece isolamento elétrico**. A **segurança elétrica é responsabilidade do amplificador/placa de aquisição** (isolamento, corrente de fuga, parte aplicada), conforme normas como a **IEC 60601-1** e a colateral **-2-26** (EEG). Placas de pesquisa como a **OpenBCI Cyton NÃO são certificadas** como equipamento médico: opere-as **alimentadas por bateria e isoladas da rede elétrica**, **nunca** conecte o participante a um sistema ligado à tomada (notebook no carregador, USB aterrado) sem isolamento adequado, e siga as instruções do fabricante do hardware. O Usuário é o único responsável por validar a segurança do conjunto antes de qualquer coleta com pessoas.

---

## 4. Natureza Open Source e Gratuita

4.1. O Software é distribuído sob a licença **MIT** (disponível em **https://github.com/rodrigooa43-create/OpenBionica/blob/main/LICENSE**).

4.2. Nos termos dessa Licença, você tem o direito de **usar, estudar, modificar e redistribuir** o Software e seu código-fonte, observadas as condições da Licença aplicável.

4.3. Em caso de divergência entre este Termo e a Licença **MIT** quanto aos direitos de uso do código, **prevalece a Licença MIT**. Este Termo a complementa com informações de privacidade, isenções e responsabilidades de uso.

4.4. **Sem transferência adicional de direitos.** Nada neste Termo ou na Licença transfere ao Usuário patentes, marcas ou quaisquer direitos não expressamente concedidos pela Licença **MIT**.

---

## 5. Privacidade

5.1. **Processamento local.** O Software processa os biossinais e demais Dados Coletados **exclusivamente de forma LOCAL**, na máquina onde é executado (por exemplo, na pasta `sessions/` e em `Documentos/EEG_Coletor`). Esses dados permanecem sob o controle exclusivo do Usuário.

5.2. **Sem tratamento remoto dos Dados Coletados.** O Software **NÃO realiza tratamento remoto, processamento em nuvem, envio, transmissão, telemetria, rastreamento, compartilhamento ou exfiltração** dos Dados Coletados. Nenhum Dado Coletado por você é, em qualquer hipótese, enviado ao Autor ou a terceiros pelo Software.

5.3. **Ausência de telemetria nesta versão.** Na presente versão do Software, **não há telemetria nem rastreamento adicionados pelo Autor**. Caso versões futuras passem a oferecer qualquer funcionalidade de rede adicional, isso será informado de forma destacada e permanecerá sob controle do Usuário. Bibliotecas e componentes de terceiros possuem suas próprias políticas (ver Seção 9).

5.4. **Autor sem acesso aos dados.** O Autor **NÃO tem acesso** a nenhum Dado Coletado por você por meio do Software. O Autor **não opera servidores** que recebam tais dados e, portanto, não os recebe, não os armazena e não consegue vê-los.

5.5. **Funcionalidade de rede — verificação manual e opcional de atualização.** A única funcionalidade de rede intencional do Software é uma verificação **MANUAL e OPCIONAL** de atualização. Em sua configuração padrão, o Software **não inicia intencionalmente nenhuma conexão de rede para envio de dados**. Quando — e somente quando — você aciona manualmente essa verificação:
- o Software apenas **BAIXA código** do repositório/infraestrutura oficial de hospedagem (https://github.com/rodrigooa43-create/OpenBionica);
- o Software **não transmite os Dados Coletados** nem informações de conteúdo pessoal;
- como em qualquer acesso à internet, a conexão poderá expor **metadados técnicos** (por exemplo, endereço IP, *user-agent* e data/hora) ao provedor de hospedagem do repositório (por exemplo, o GitHub), conforme a **política de privacidade desse terceiro**;
- essa verificação pode ser **desativada** e, por padrão, o Software funciona **offline**, sem iniciar conexões para envio de dados.

5.6. **Distinção essencial.** Há diferença entre (i) os **Dados Coletados** — que **nunca** são enviados pelo Software — e (ii) os **metadados técnicos de conexão** (como o endereço IP), inevitavelmente expostos ao provedor de hospedagem em qualquer download manual de atualização. O compromisso central de privacidade do Software é: **não realizar tratamento remoto dos Dados Coletados**.

5.7. **Registro local de aceite.** Para fins de rastreabilidade, o Software poderá **armazenar localmente, na sua própria máquina**, a versão deste Termo e a data/hora do aceite. Esse registro permanece **apenas no seu computador** e **não é enviado** a ninguém.

---

## 6. Proteção de Dados (LGPD) — Papéis e Responsabilidades

6.1. **Você é o Controlador.** Se você utilizar o Software para **coletar, registrar ou processar dados de Participantes**, **VOCÊ é o controlador** desses dados, nos termos do art. 5º, VI, da **Lei Geral de Proteção de Dados Pessoais — LGPD (Lei nº 13.709/2018)**, por ser quem decide sobre as finalidades e os meios do tratamento. (O termo "Operador do Software", usado neste documento, refere-se a "quem opera o programa" e **não** corresponde ao "operador" definido no art. 5º, VII, da LGPD.)

6.2. **O Autor não é controlador nem operador.** O Autor atua exclusivamente como **fornecedor de uma ferramenta de software de uso geral**, **não determina finalidades nem meios** de tratamento de dados pessoais de Participantes e, **por não ter acesso aos Dados Coletados**, **não é controlador nem operador** desses tratamentos (art. 5º, VI e VII, da LGPD). O Autor **não responde** por qualquer tratamento, vazamento, uso indevido ou descumprimento legal relacionado aos Dados Coletados por você.

6.3. **Dados pessoais sensíveis (biossinais).** Você reconhece que biossinais coletados de pessoas identificadas ou identificáveis (EEG, EMG, ECG, EoG e similares) constituem, em regra, **DADOS PESSOAIS SENSÍVEIS** — dados referentes à **saúde** e/ou **dados biométricos** —, nos termos do **art. 5º, II, da LGPD**, sujeitos ao **regime reforçado do art. 11**. Como controlador, cabe a você assegurar base legal específica para dados sensíveis, medidas de segurança compatíveis com o risco e, quando aplicável, **Relatório de Impacto à Proteção de Dados Pessoais (RIPD)**.

6.4. **Responsabilidades do Controlador.** Como controlador dos Dados Coletados, **você é o único responsável** por:

a) **Definir e documentar a base legal adequada** para o tratamento (art. 7º e, para dados sensíveis, art. 11 da LGPD), que poderá ser o **consentimento** ou outra hipótese legal aplicável ao seu contexto (por exemplo, realização de estudos por órgão de pesquisa) — e, quando a base for o consentimento, **obtê-lo de forma livre, informada e inequívoca** dos Participantes;

b) **Definir as finalidades** do tratamento e tratar os dados de forma compatível com elas;

c) Garantir **guarda, segurança, sigilo, anonimização ou pseudonimização** e a confidencialidade dos dados, adotando **medidas técnicas e administrativas de segurança** adequadas (art. 46 da LGPD);

d) **Definir prazos de retenção** e proceder à **eliminação** dos dados ao término do tratamento, ressalvadas as hipóteses legais de conservação (arts. 15 e 16 da LGPD);

e) **Atender aos direitos dos titulares** (art. 18 da LGPD — acesso, correção, eliminação, portabilidade etc.); tais pedidos, dirigidos aos Dados Coletados por você, são de sua exclusiva responsabilidade, **uma vez que o Autor não tem como atendê-los por não ter acesso aos dados**;

f) Em caso de **incidente de segurança** que possa acarretar risco ou dano relevante, realizar as **comunicações exigidas à ANPD e aos titulares** (art. 48 da LGPD);

g) Observar, em eventuais **transferências internacionais** dos dados, o disposto no **art. 33 da LGPD**;

h) Observar, ao coletar dados de **crianças e adolescentes**, o regime específico do **art. 14 da LGPD**, inclusive quanto ao consentimento de pais ou responsáveis;

i) Cumprir todas as demais **obrigações éticas e legais** aplicáveis à sua atividade e à sua jurisdição (incluindo, quando cabível, aprovações éticas ou institucionais que o seu contexto exigir).

6.5. **Uso lícito.** Você se compromete a usar o Software de forma **lícita** e em conformidade com as leis aplicáveis.

---

## 7. Isenção de Garantia

7.1. O Software é fornecido **"COMO ESTÁ" (*as-is*)** e **"conforme disponível"**, **sem garantias de qualquer espécie**, expressas ou implícitas.

7.2. **NA MÁXIMA EXTENSÃO PERMITIDA PELA LEI APLICÁVEL, O AUTOR REJEITA TODAS AS GARANTIAS, EXPRESSAS OU IMPLÍCITAS, INCLUINDO, SEM LIMITAÇÃO, AS GARANTIAS DE COMERCIABILIDADE, DE ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA E DE NÃO VIOLAÇÃO DE DIREITOS DE TERCEIROS.**

7.3. O Autor **não garante**, entre outros: a adequação a uma finalidade específica, a ausência de erros ou defeitos, a disponibilidade contínua, a compatibilidade com seu hardware ou sistema, nem a **exatidão, precisão, validade clínica ou metrológica, ou confiabilidade** de medidas, sinais, cálculos ou análises produzidos. As medições podem conter **ruído, artefatos e erros** e **não possuem validade clínica nem metrológica**.

7.4. O Autor **não garante** que o Software esteja livre de **vírus, malware ou código malicioso** introduzidos por terceiros (por exemplo, em cópias, *forks* ou builds não oficiais, ou na infraestrutura de download). Cabe a você **verificar a integridade** do código ou binário obtido, especialmente nas atualizações baixadas manualmente.

7.5. Você usa o Software **por sua própria conta e risco**.

---

## 8. Limitação de Responsabilidade

8.1. Na máxima extensão permitida pela lei aplicável, o Autor **não se responsabiliza** por quaisquer **danos diretos, indiretos, incidentais, especiais, consequenciais ou punitivos** decorrentes do uso ou da impossibilidade de uso do Software.

8.2. Isso inclui, sem limitação: **perda ou corrupção de dados** e de Dados Coletados, perda ou corrupção de sinais biológicos, **artefatos e erros de medição**, interrupção de atividades e **decisões tomadas com base nos resultados** gerados pelo Software.

8.3. **Versões modificadas e usos fora da finalidade.** O Autor **não responde** por danos decorrentes de **versões modificadas por terceiros**, *forks*, builds não oficiais, integrações de terceiros ou uso do Software fora da finalidade descrita na Seção 3.

8.4. **Limite de responsabilidade.** Por se tratar de Software **gratuito e sem contraprestação**, na medida máxima permitida pela lei aplicável, a **responsabilidade total** do Autor perante o Usuário, por qualquer causa relacionada ao Software, fica **limitada a R$ 0,00 (zero reais)**.

8.5. **Ressalva de ordem pública.** As isenções e limitações deste Termo **não afastam** as responsabilidades que a lei imperativamente não admita excluir ou limitar, como as decorrentes de **dolo**. Caso alguma limitação seja considerada inaplicável em determinado caso, ela será aplicada na **maior extensão permitida** pela lei, preservando-se as demais disposições (ver Seção 14).

8.6. Você é o único responsável por manter **cópias de segurança (backups)** dos seus dados e dos Dados Coletados.

---

## 9. Indenização (*Hold Harmless*)

9.1. Na máxima extensão permitida pela lei aplicável, você concorda em **indenizar, defender e isentar de responsabilidade** o Autor com relação a toda e qualquer reclamação, perda, dano, multa, sanção, ação judicial ou administrativa (inclusive perante a ANPD) e despesas razoáveis, incluindo **honorários advocatícios**, decorrentes de ou relacionados a:

a) o **uso do Software por você**;
b) a **violação deste Termo** por você;
c) o **tratamento de dados de Participantes** ou de quaisquer terceiros realizado por você;
d) a **violação de lei** ou de direitos de terceiros por você (incluindo a LGPD, direitos de personalidade e normas de ética em pesquisa).

9.2. Esta obrigação subsiste após o término do uso do Software.

---

## 10. Componentes e Licenças de Terceiros

10.1. O Software utiliza **bibliotecas e componentes de terceiros** de código aberto (por exemplo, bibliotecas do ecossistema Python e de interface gráfica), cada um sujeito às **suas próprias licenças**.

10.2. Essas licenças de terceiros permanecem válidas e aplicáveis aos respectivos componentes. O Autor **não detém** os direitos sobre esses componentes e **não responde** por eles.

10.3. Os avisos e textos das licenças de terceiros estão disponíveis em **https://github.com/rodrigooa43-create/OpenBionica/blob/main/THIRD-PARTY-LICENSES.md**. Recomenda-se consultá-los, especialmente quanto a componentes de interface gráfica, que podem estar sujeitos a licenças específicas (por exemplo, LGPL) com implicações para a redistribuição do conjunto.

---

## 11. Marcas e Sinais Distintivos

11.1. **"ROA"**, **"ROA"** e respectivos logotipos são **sinais distintivos** do projeto.

11.2. A Licença de código **não concede** direito de uso das marcas, do nome ou dos logotipos do projeto para **endossar, promover ou nomear** produtos derivados, *forks* ou versões não oficiais, sem autorização prévia do Autor. É vedado o uso do nome do projeto de modo que sugira endosso oficial ou induza terceiros a erro.

---

## 12. Atualizações, Suporte e Continuidade

12.1. Atualizações são **opcionais** e dependem de ação manual do Usuário (ver item 5.5).

12.2. Por se tratar de projeto **open source e sem fins lucrativos**, **não há obrigação** de fornecer suporte, manutenção, correções, novas versões ou continuidade do projeto. **Não há SLA**, prazo de resposta, nem obrigação de corrigir bugs ou falhas de segurança.

12.3. O Autor pode, a qualquer momento e sem aviso prévio, **descontinuar** o desenvolvimento, sem que isso gere qualquer direito a indenização. Você poderá continuar usando a versão que possui, nos termos da Licença **MIT**.

---

## 13. Conformidade Legal e Exportação

13.1. Você é responsável por utilizar o Software **em conformidade com as leis aplicáveis** na sua jurisdição, incluindo, quando cabível, **controles de exportação e importação, sanções** e **normas sobre pesquisa com seres humanos e animais**.

13.2. Você isenta o Autor de qualquer responsabilidade por usos do Software que **violem** tais normas.

---

## 14. Disposições Gerais

14.1. **Capacidade.** Ao aceitar este Termo, você declara ser **maior de 18 anos** (ou emancipado) e **plenamente capaz** nos termos do Código Civil. Caso aceite em nome de uma instituição, equipe ou outra pessoa jurídica, você declara possuir **poderes e representação** suficientes para vinculá-la a este Termo.

14.2. **Divisibilidade (*severability*).** Se qualquer disposição deste Termo for considerada inválida, ilegal ou inexequível, as **demais permanecerão em pleno vigor**, e a disposição afetada será interpretada e reduzida na medida mínima necessária para torná-la válida, preservando-se ao máximo a intenção original das partes.

14.3. **Acordo integral.** Este Termo, em conjunto com a Licença **MIT**, constitui o **acordo integral** entre você e o Autor quanto ao uso do Software, substituindo entendimentos ou comunicações anteriores sobre o tema.

14.4. **Alterações do Termo.** O Autor pode **revisar este Termo** em versões futuras. A versão aplicável é aquela **aceita no momento da instalação ou do uso** da respectiva versão do Software. O uso continuado de **nova versão** do Software, após a alteração do Termo, implica **aceite** da versão revista.

14.5. **Lei aplicável.** Este Termo é regido e interpretado de acordo com as leis da **República Federativa do Brasil**.

14.6. **Foro.** Fica eleito o foro da comarca de **o foro do domicílio do Autor (ressalvado o foro legalmente privilegiado, quando aplicável)** para dirimir controvérsias decorrentes deste Termo, **ressalvado** que, se por força de lei imperativa o Usuário for considerado consumidor ou houver foro legalmente privilegiado, **prevalecerá o foro determinado pela lei**.

14.7. **Idioma prevalente.** Em caso de tradução deste Termo para outros idiomas, a **versão em português** prevalecerá em caso de divergência.

14.8. **Não constitui aconselhamento jurídico.** Este Termo é um **modelo** de termo de uso e privacidade, redigido em linguagem acessível, e **não constitui aconselhamento jurídico**. Recomenda-se sua **revisão por profissional do Direito**, conforme a jurisdição e as necessidades específicas do Autor, antes da distribuição pública.

---

## 15. Aceite

15.1. Ao instalar e/ou usar o Software, você declara que **leu, entendeu e concorda** integralmente com este Termo de Consentimento e Uso do Software.

15.2. Caso **não concorde** com qualquer condição aqui descrita, **não instale e não utilize** o Software.

15.3. Para fins de registro, o Software poderá **armazenar localmente, na sua própria máquina**, a **versão deste Termo** e a **data/hora do aceite** (ver item 5.7). Esse registro fica **apenas no seu computador** e **não é enviado** a ninguém.

---

### Campos de Aceite

- **Versão deste Termo:** 1.0
- **Ano:** 2026
- **Data/hora do aceite:** (registrado automaticamente no aceite)
- **Identificação do Usuário (opcional, registro local):** (opcional)
- [ ] **Li, entendi e concordo** com o Termo de Consentimento e Uso do Software.

---

> **Aviso:** Este documento é um **modelo** de termo de uso e privacidade. Ele **não constitui aconselhamento jurídico**. Recomenda-se **revisão por profissional do Direito** conforme a jurisdição e as necessidades específicas do Autor antes da distribuição pública.

---
