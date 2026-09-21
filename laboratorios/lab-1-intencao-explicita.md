# Laboratório 1 — Intenção explícita

**Dia 1 · 25 min · duplas ou individual**
Repositório: `lab-repo`

---

## Objetivo

Executar a **mesma tarefa duas vezes**, mudando uma única variável: se a intenção foi
declarada antes de pedir código.

Não é sobre ser mais rápido. É sobre descobrir o que você decide sem perceber.

---

## Preparação (2 min)

```bash
cd lab-repo
pip install -e ".[dev]"
pytest          # 12 testes devem passar
```

---

## A tarefa

> **Adicionar reabertura de ordem de serviço.**
> Quando uma ordem concluída volta a apresentar o problema, o técnico precisa reabri-la
> em vez de criar uma nova, para não perder o histórico.

É tudo o que você tem — e é tudo o que um ticket real costuma ter.

---

## Rodada 1 — como você faria hoje (8 min)

Trabalhe do jeito habitual. Sem método novo, sem capricho extra.

Ao terminar (ou ao acabar o tempo), **pare**. Anote:

```
Tempo até ter algo funcionando: ______ min
O agente decidiu sozinho:
  1.
  2.
  3.
```

> Se você não souber preencher a lista, olhe o código gerado e pergunte a cada linha de
> lógica: *"eu pedi isso?"*

**Não continue para a rodada 2 antes de preencher.**

---

## Rodada 2 — intenção antes (12 min)

Descarte o código da rodada 1 (`git checkout .` ou trabalhe em outra branch).

**Antes de pedir qualquer coisa ao agente**, escreva — em arquivo, não no chat:

```markdown
## Intenção
Por que isso existe, em uma frase.

## Comportamento esperado
- Quando ..., então ...
- Quando ..., então ...

## Fora de escopo
- ...

## Ainda não sei
- ...
```

A seção **"Ainda não sei"** é a mais importante deste laboratório. Escreva ali toda pergunta
que você não consegue responder sozinho.

Sugestões do que costuma aparecer — mas descubra as suas antes de ler:

<details>
<summary>Só abra depois de escrever a sua lista</summary>

- Ordem **cancelada** pode ser reaberta, ou só concluída?
- Existe limite de reaberturas?
- O prazo (SLA) é recalculado a partir da reabertura, ou o original é mantido?
- A prioridade é recalculada? (`priorizacao.calc` usa `reaberturas`)
- `concluida_em` é limpo ou preservado como histórico?
- Reabertura precisa de justificativa?
- Qual status a ordem assume: `aberta` ou `em_execucao`?

</details>

Agora sim: entregue essa intenção ao agente e peça a implementação.

Ao terminar, anote:

```
Tempo: ______ min
Perguntas que apareceram antes de escrever código: ______
Decisões que na rodada 1 o agente tomou por mim: ______
```

---

## Fechamento (3 min)

A pergunta do dia — e ela **não** é "foi mais rápido?":

> **Na rodada 2, o que você teve que decidir antes de escrever, que na rodada 1 foi decidido
> sem você perceber?**

---

## Entrega

Guarde na sua pasta de trabalho — vira insumo da Sessão 1 da mentoria:

- O arquivo de intenção da rodada 2.
- As duas anotações de tempo e decisões.

---

## Se sobrar tempo

Rode `git diff` da rodada 1 e conte quantas linhas de **lógica de negócio** você não pediu
explicitamente. Esse número costuma surpreender mais que o cronômetro.
