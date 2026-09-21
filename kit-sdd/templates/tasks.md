<!--
TEMPLATE — tasks.md
Gerado por: $speckit-tasks

A REGRA QUE NÃO SE NEGOCIA:
  A tarefa de TESTE vem antes da tarefa de IMPLEMENTAÇÃO.
  Não é preferência de estilo — é o que faz o $speckit-implement ter alvo objetivo, em vez
  de "o que parecer razoável". Se o gerador não produzir nessa ordem, reordene à mão.

[P] = pode rodar em paralelo com as outras [P] do mesmo bloco.

HARNESS:
  Execute uma task por vez e pare no checkpoint (contra o one-shot hero).
  Um checkpoint só é marcado com a SAÍDA do comando colada, não com "passou" (contra a
  vitória prematura). Testes do Bloco 1 não mudam durante o Bloco 2 (contra o teste fake).
  Este arquivo é o estado da fatia: atualize antes de encerrar a sessão (contra a amnésia).
-->

# Tasks — <TÍTULO DA FATIA>

**Spec:** `<001-nome-curto>` · **Plan:** `plan.md`

---

## Bloco 1 — Testes (vermelhos)

| ID | [P] | Tarefa | Critério |
|---|:-:|---|:-:|
| T001 | [P] | Teste: `<nome que é o critério de aceite>` | #1 |
| T002 | [P] | Teste: `<nome que é o critério de aceite>` | #2 |
| T003 | [P] | Teste: `<caso de erro>` | #3 |

> **Checkpoint 1** — todos os testes acima falham, e falham **pelo motivo certo**.
> Teste que falha por `ImportError` não é teste vermelho: é teste quebrado.
>
> Evidência (saída do comando, resumida às linhas de falha): `<colar>`

## Bloco 2 — Implementação

| ID | Depende de | Tarefa | Arquivo |
|---|:-:|---|---|
| T004 | T001–T003 | `<implementar o comportamento>` | `<caminho>` |
| T005 | T004 | `<ajustar o que for consequência>` | `<caminho>` |

> **Checkpoint 2** — suíte verde. Cobertura de regra de negócio não caiu. Nenhum teste do
> Bloco 1 foi alterado ou silenciado.
>
> Evidência (saída do comando): `<colar>`

## Bloco 3 — Consolidação

| ID | Depende de | Tarefa |
|---|:-:|---|
| T006 | T005 | Atualizar contrato público (`<OpenAPI / schema / doc>`) |
| T007 | T005 | Refatorar com testes verdes — **commit separado** |
| T008 | T006 | Rodar `$speckit-analyze` e resolver divergências |

> **Checkpoint 3 — Definition of Done.** Ver `06-playbooks/guia-boas-praticas.md`.

---

## Rastreabilidade

> Preencher durante a execução. É o que responde à pergunta que vocês vão ouvir de verdade:
> *por que esse código é assim?*

| Critério | Teste | Task | Commit |
|:-:|---|:-:|---|
| #1 | `test_<...>` | T001, T004 | `<sha>` |
| #2 | `test_<...>` | T002, T004 | `<sha>` |
| #3 | `test_<...>` | T003, T004 | `<sha>` |

**Critérios sem task:** `<nenhum>` — se houver algum, alguém vai esquecer de implementar.
**Tasks sem critério:** `<nenhuma>` — se houver alguma, é escopo inventado.

## Estado da sessão

> Atualizar antes de encerrar ou compactar. É o que a próxima sessão lê primeiro.

- **Última task concluída:** `<T00x>`
- **Decisões tomadas fora da spec:** `<registrar aqui, ou levar para a spec>`
- **Pendências e bloqueios:** `<...>`

---

## Modelo de mensagem de commit

```
feat(<escopo>): <o que passa a ser possível>

Implementa T001-T005 da spec <001-nome-curto>.
Critérios de aceite 1 a 3 cobertos por teste.
```
