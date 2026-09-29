# Intenção — Reabertura de ordem de serviço

## Intenção
Permitir que o técnico reabra uma ordem concluída que voltou a apresentar o problema,
preservando o histórico em vez de criar uma ordem nova.

## Comportamento esperado
- Quando uma ordem `concluida` é reaberta, então ela volta ao status `aberta` e `reaberturas` incrementa em 1.
- Quando a ordem é reaberta, então o prazo (SLA) é recalculado a partir do instante da reabertura.
- Quando a ordem é reaberta, então a prioridade é recalculada (`priorizacao.calc` considera `reaberturas`).
- Quando a ordem é reaberta, então `concluida_em` é limpo e `aberta_em` original é preservado.
- Quando a ordem não está `concluida`, então a API responde 409 sem alterar a ordem.
- Quando a ordem não existe, então a API responde 404.

## Interface
`POST /ordens/{ordem_id}/reabrir` — sem corpo — retorna a `OrdemServico` atualizada.

## Fora de escopo
- Justificativa obrigatória da reabertura.
- Limite de reaberturas.
- Reabertura de ordem cancelada.
- Alterar `priorizacao.py` (legado, alvo do Dia 5).

## Decisões tomadas (respostas a "Ainda não sei")
- Só `concluida` pode ser reaberta; `cancelada` é terminal (coerente com `atualizar_status`).
- Status resultante: `aberta` (a ordem volta para a fila; o técnico assume depois).
- SLA reinicia na reabertura; o prazo original não é mantido.
- `concluida_em` não é preservado no modelo atual (sem campo de histórico); ver "Ainda não sei".

## Ainda não sei
- O prazo de uma reabertura deveria ser mais curto que o da abertura original?
- Precisamos de trilha de auditoria (quem reabriu, quando, por quê)?
- Reabertura repetida deve escalar para gestor?
