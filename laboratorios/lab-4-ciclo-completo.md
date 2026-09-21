# Laboratório 4 — Ciclo completo spec → teste → implementação

**Dia 4 · 40 min · individual, na sua história real**

O laboratório mais importante do programa: é o único momento em que você fecha o ciclo
inteiro com as próprias mãos, com acompanhamento.

---

## Antes de começar — valide o tamanho (2 min)

Sua história precisa caber em **uma fatia vertical**: comportamento observável, de ponta a
ponta, que caberia em menos de um dia de trabalho.

**Grande demais** — quebre agora:
- "Refatorar o módulo de faturamento"
- "Adicionar autenticação"
- "Migrar para a nova API"

**Do tamanho certo:**
- "Permitir reabertura de ordem concluída"
- "Bloquear cancelamento de ordem em execução"
- "Expor filtro por setor na listagem de equipamentos"

> Se você não tem certeza, chame o instrutor **agora**. Descobrir aos 30 minutos que a
> história era grande demais custa o laboratório inteiro.

Sem história própria? Use no `lab-repo`:

> **Registrar interrupção de ordem em execução.** Quando falta peça, o técnico precisa
> registrar a interrupção com motivo, e o tempo parado não conta para o SLA.

---

## Setup (2 min)

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
cd <seu-repo>
specify init --here --integration codex --integration-options="--skills"
```

---

## Etapa 1 — `specify` (7 min)

```
codex
$speckit-specify Permitir reabertura de ordem de serviço concluída, preservando
o histórico da ordem original.
```

Revise o que saiu. **Corrija estas três coisas, que quase sempre aparecem:**

| Problema | Correção |
|---|---|
| Tecnologia na spec | Tire. Nome de biblioteca, tabela ou classe é assunto do `plan` |
| Critério não testável | Reescreva como "quando X, então Y" |
| Sem "fora de escopo" | Adicione. É o que impede o agente de expandir sozinho |

**Teste de qualidade do critério:** você conseguiria escrever o teste sem perguntar mais nada?
Se não, o critério ainda não está pronto.

---

## Etapa 2 — `clarify` (5 min)

```
$speckit-clarify
```

Responda às perguntas. **A resposta volta para a spec** — esse é o ponto: a decisão fica
registrada, não perdida no chat.

> Se o `clarify` não levantar nada, desconfie. Ou sua spec está excelente, ou está genérica
> demais para ter ambiguidade detectável. Releia procurando o que **você** teria que decidir
> na hora de implementar.

Anote: **quantas ambiguidades apareceram?** `______`

No kata do Dia 1, quase ninguém perguntou nada. É a mesma lacuna — a diferença é que agora
existe uma etapa que a força.

---

## Etapa 3 — `plan` (5 min)

```
$speckit-plan
```

Confira:

- [ ] Respeita a constitution do Dia 2?
- [ ] Decisões registradas **com a alternativa descartada**?
- [ ] Contratos explícitos: entrada, saída, erro?
- [ ] Diz nomeadamente que arquivos existentes mudam?

---

## Etapa 4 — `tasks` (4 min)

```
$speckit-tasks
```

**Verifique o essencial: as tarefas de teste vêm ANTES das de implementação.** Se não vierem,
reordene à mão. É isso que dá alvo objetivo ao `implement`.

```
T001 [P] Teste: reabrir ordem concluída volta status para 'aberta'
T002 [P] Teste: reabertura incrementa contador e limpa concluida_em
T003 [P] Teste: reabrir ordem não-concluída retorna 409
T004     Implementar POST /ordens/{id}/reabertura
T005     Atualizar OpenAPI e README
     ── checkpoint: suíte verde, cobertura de services não caiu ──
```

---

## Etapa 5 — `analyze` (2 min)

```
$speckit-analyze
```

Corrija o que aparecer **antes** de implementar. Custa 30 segundos e roda antes da parte cara.

Anote: **quantas divergências?** `______`

---

## Etapa 6 — `implement` (10 min)

Peça **uma task por vez**, não a lista inteira:

```
$speckit-implement execute apenas T001 a T003 e pare
```

O texto depois do comando vai como instrução ao agente. Confira o vermelho. Depois:

```
$speckit-implement execute apenas T004 e pare
```

Enquanto roda, observe:

- [ ] Os testes ficaram **vermelhos** antes de existir implementação? (se não, o ciclo furou)
- [ ] O nome do teste corresponde ao critério de aceite?
- [ ] Apareceu algo no diff que não estava na spec?

**Três checagens de harness** — são três dos seis problemas do Dia 1:

- [ ] **One-shot hero:** o agente parou no checkpoint, ou seguiu executando tudo?
- [ ] **Teste fake:** algum arquivo de teste do bloco T001–T003 mudou durante a T004? Se
      mudou, pare: volte ao critério de aceite antes de aceitar a mudança.
- [ ] **Vitória prematura:** quando o agente disse "pronto", você viu a **saída** do comando
      ou só a afirmação?

Ao terminar, rode você mesmo — não aceite o relato:

```bash
pytest
git diff
```

**Leia o diff inteiro.** Procure especificamente: o que mudou aqui que eu não pedi?

---

## Etapa 7 — rastreabilidade (3 min)

Verifique a cadeia:

```
critério de aceite  →  nome do teste  →  task  →  commit  →  PR
```

Commit no padrão convencional, citando a task:

```bash
git add -A
git commit -m "feat(ordens): permite reabertura de ordem concluída

Implementa T001-T005 da spec 001-reabertura-ordem.
Critérios de aceite 1 a 3 cobertos por teste."
```

---

## Entrega

```
specs/001-<sua-feature>/
├── spec.md
├── plan.md
└── tasks.md
```
mais os testes, o código e o commit.

Guarde: **é o insumo da Sessão 2 da mentoria**, onde este ciclo é avaliado.

---

## Critério de pronto

- [ ] Spec sem tecnologia, com "fora de escopo" preenchido.
- [ ] Todo critério de aceite tem um teste com nome correspondente.
- [ ] `clarify` executado e respostas incorporadas à spec.
- [ ] Tarefas de teste antes das de implementação.
- [ ] `analyze` sem divergências pendentes.
- [ ] Suíte verde — **rodada por você**, não relatada pelo agente.
- [ ] Nenhum teste do bloco de testes alterado durante a implementação.
- [ ] Diff lido inteiro; nada fora do escopo.
- [ ] Spec, plan e tasks versionados **no mesmo commit** do código.

---

## Se terminar cedo

1. Rode `$speckit-analyze` de novo — sempre aparece algo depois de implementar.
2. Aplique a **matriz de calibragem** à sua história: o rito completo valeu, ou ela pedia
   rito reduzido? Justifique com tamanho, risco e reversibilidade.
3. Escreva em duas linhas o que você faria diferente se a mesma história voltasse amanhã.
