# Governança — ROA

Projeto **open source, sem fins lucrativos**, para coleta, visualização e
análise de biossinais em **pesquisa e educação** (não é dispositivo médico).

## Papéis

- **Mantenedor(es):** revisam e integram contribuições, decidem o *roadmap* e
  fazem os *releases*. Listados no `README.md` / commits.
- **Contribuidores:** qualquer pessoa que abra *issues* ou *pull requests*
  (ver `CONTRIBUTING.md` e `CODE_OF_CONDUCT.md`).

## Decisões

- Mudanças pequenas: *pull request* + revisão de 1 mantenedor.
- Mudanças que afetam **integridade de dados** ou as **Regras de Ouro**
  (raw imutável, causal vs fase-zero, timestamp na origem, metadados
  obrigatórios, sem PII no dado, reprodutibilidade, degradação graciosa):
  exigem discussão em *issue* e aprovação explícita — têm precedência sobre
  qualquer outra mudança.
- Discordância persistente: decide o(s) mantenedor(es), registrando o porquê.

## Releases

- Versionamento **SemVer** (`MAJOR.MINOR.PATCH`), registrado no `CHANGELOG.md`.
- Cada *release* de código: *bump* de `APP_VERSION`, `version.json` com
  **SHA-256** do `.py`, *tag* Git e entrada no `CHANGELOG.md`.
- Atualização a quente (só o `.py`) para quem já instalou; *rebuild* do `.exe`
  quando muda dependência/binding.

## Qualidade & segurança

- Roteiro de revisão auditável (auditoria por IDs, ex.: `EEG-001`, `G-01`).
- Relato de vulnerabilidades: `SECURITY.md`.
- Backlog priorizado: `SUGESTOES.md` / `KNOWN_ISSUES.md`.
