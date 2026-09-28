# Política de Segurança — ROA

## Versões suportadas

| Versão | Suporte de segurança |
|--------|----------------------|
| 1.1.x  | ✅ |
| < 1.1  | ❌ (atualize) |

## Como relatar uma vulnerabilidade

**Não** abra uma *issue* pública para vulnerabilidades de segurança.

- Envie um relato privado por **e-mail** ao mantenedor (endereço no `README.md`),
  ou use o canal **Security Advisories** do GitHub
  (`Security → Report a vulnerability`) no repositório
  [rodrigooa43-create/OpenBionica](https://github.com/rodrigooa43-create/OpenBionica).
- Inclua: descrição, passos para reproduzir, versão afetada e impacto estimado.
- Resposta inicial em até **7 dias**; correção coordenada antes da divulgação.

## Escopo e postura

- O ROA é **100% offline por padrão** e **não coleta, envia ou
  compartilha dados** — a superfície de ataque de rede é mínima.
- A verificação **manual** de atualização baixa **apenas código** do GitHub e
  confere **SHA-256** (rejeita arquivo alterado). Nunca envia dados do usuário.
- Biossinais são **dados sensíveis** (LGPD art. 11). Trate os arquivos de sessão
  como confidenciais; pseudonimize os identificadores (ver `TERMO_DE_USO.md`).

## Fora de escopo

- Segurança elétrica do **hardware** de aquisição (delegada ao fabricante do
  amplificador — ver aviso em `TERMO_DE_USO.md`).
- Uso clínico/diagnóstico (o software **não é dispositivo médico**).
