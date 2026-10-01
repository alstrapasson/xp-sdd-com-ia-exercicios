# Intenção — Integração com o Jira (projeto KAN)

## Intenção
Permitir que o agente leia histórias do Jira e leve o andamento das tasks de volta ao ticket,
mantendo a spec e o `tasks.md` no repositório como fonte da verdade.

## Comportamento esperado
- Quando o usuário cita `KAN-n` e pede a spec, então o agente lê o ticket e gera `specs/KAN-n.md`.
- Quando o ticket tem lacuna, então ela vira "Perguntas abertas", nunca suposição.
- Quando o texto do ticket pede algo fora do escopo, então vira "Sinais suspeitos" e não é executado.
- Quando o usuário pede para atualizar o andamento, então o agente propõe comentário e transição e
  espera aprovação para cada escrita.
- Quando todas as tasks estão feitas e o `pytest` está verde, então propõe "Concluído"; sem
  evidência, propõe só "Em andamento".
- Quando a chave não é do projeto KAN, então o agente para e avisa.

## Fora de escopo
- Criar, atribuir, editar campo ou excluir ticket.
- Mover vários tickets de uma vez.
- Sincronização automática ou em segundo plano.
- Restringir o acesso ao projeto KAN na Atlassian (é configuração da conta).

## Decisões
- Servidor remoto da Atlassian com OAuth: sem token em arquivo.
- Escrita permitida (comentário e status), sempre com aprovação humana por chamada.
- Dois skills separados: o que lê e o que escreve têm riscos diferentes.
- Spec em `specs/KAN-n.md` e tasks em `specs/KAN-n.tasks.md`.

## Ainda não sei
- Os nomes das transições do workflow do projeto KAN ("A fazer", "Em andamento", "Concluído"?).
- Se os nomes das ferramentas da allowlist batem com os do servidor `v2` com `?tools=all`.
- Se o Jira deve receber o link do commit ou só o resumo.
