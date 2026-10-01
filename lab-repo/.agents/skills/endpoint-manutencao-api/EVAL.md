# Eval de acionamento — `endpoint-manutencao-api`

| # | Prompt | Deve acionar? | Acionou? | OK? |
|:-:|---|:-:|:-:|:-:|
| 1 | "adiciona um endpoint para cancelar uma ordem de serviço" | Sim | Sim | OK |
| 2 | "cria a rota GET /equipamentos/{id}/ordens" | Sim | Sim | OK |
| 3 | "preciso expor o prazo de SLA numa rota nova da API" | Sim | Sim | OK |
| 4 | "muda o contrato do PATCH de status pra aceitar um motivo" | Sim | Sim | OK |
| 5 | "remove a rota de listagem de equipamentos" | Sim | Sim | OK |
| 6 | "ajusta o cálculo de prioridade no priorizacao.py" | **Não** | Não | OK |
| 7 | "escreve um cliente pra consumir a API dos Correios" | **Não** | Não | OK |
| 8 | "documenta os endpoints que já existem" | **Não** | Não | OK |
| 9 | "otimiza a consulta de listagem de ordens no repositório" | **Não** | Não | OK |
| 10 | "cria um script de migração de dados das ordens antigas" | **Não** | Não | OK |

Executado em: 2026-10-01 18:27 UTC  ·  Versão do skill: 1.0  ·  Por: codex exec -p exploracao (scripts/rodar_eval_skill.py)

---

## As fronteiras

- **Caso 6:** "ordens" e "prioridade" aparecem na API, mas `priorizacao.py` é legado e vai pelo
  fluxo de characterization tests, não por este skill.
- **Caso 7:** "API" nos dois lados, tarefas opostas: expor e consumir.
- **Caso 8:** criar rota não é documentar rota.
- **Caso 9:** mexer por dentro de uma rota existente não muda contrato.
- **Caso 10:** "ordens" como substantivo, outro fim.

## Como rodar

Sessão nova (`codex`) para cada linha, prompt exato, sem reformular. Se um negativo acionar,
restrinja a descrição e acrescente a fronteira em "Quando NÃO usar". Se um positivo não acionar,
faltam termos que a pessoa realmente digita. **Rode a tabela inteira de novo** depois de cada
ajuste.
