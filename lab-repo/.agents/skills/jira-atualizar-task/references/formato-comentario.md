# Formato do comentário no Jira

Texto simples, sem links externos além da spec e do commit.

```
Andamento — <data UTC>

Tasks: <feitas>/<total> concluídas
Feitas: T1, T2
Pendentes: T3
Bloqueadas: T4 (aguardando resposta sobre limite de reaberturas)

Testes: pytest verde (17 passed) em <hash curto do commit>
Spec: specs/KAN-<n>.md
```

- Não inclua trecho de código, caminho de máquina nem dado que não esteja no `tasks.md`.
- Sem evidência de teste, escreva "Testes: não executados nesta atualização".
