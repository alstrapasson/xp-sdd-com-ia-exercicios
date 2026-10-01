# Formato do `specs/KAN-n.tasks.md`

```markdown
# Tasks — KAN-<n>: <título>

**Jira:** KAN-<n> · **Spec:** specs/KAN-<n>.md · **Atualizado em:** <data UTC>

- [x] T1 Teste: reabertura de ordem concluída retorna 200
- [x] T2 Implementação: endpoint POST /ordens/{id}/reabrir
- [ ] T3 Teste: ordem não concluída retorna 409
- [ ] T4 (bloqueada) Aguardando resposta sobre limite de reaberturas
```

- Uma linha por task, `- [x]` feita e `- [ ]` pendente.
- Bloqueio escrito na própria linha, com "(bloqueada)" e o motivo.
- Teste vem antes da implementação, conforme o `AGENTS.md`.
- O arquivo é a fonte da verdade do andamento; o Jira recebe um resumo dele.
