# XP + SDD com IA — Guia de melhores práticas

**Entregável 7 da proposta.** Referência de consulta contínua, para depois do treinamento.

Organizado para ser **consultado**, não lido de ponta a ponta. Use o índice.

---

## Índice

1. [As dez regras](#1-as-dez-regras)
2. [Antes de pedir código](#2-antes-de-pedir-código)
3. [Contexto](#3-contexto)
4. [O ciclo](#4-o-ciclo)
5. [Testes](#5-testes)
6. [Revisão](#6-revisão)
7. [Legado](#7-legado)
8. [Segurança](#8-segurança)
9. [Métricas](#9-métricas)
10. [Sintomas e diagnósticos](#10-sintomas-e-diagnósticos)
11. [Harness: os seis modos de falha](#11-harness-os-seis-modos-de-falha)

---

## 1. As dez regras

Se você só lembrar de dez coisas:

1. **O defeito raramente está na geração; está na especificação.**
2. **Contexto é tudo que o agente alcança**, não o que você digita.
3. **Um princípio que não dá para verificar não é princípio — é desejo.**
4. **Uma spec por fatia vertical entregável**, não por projeto.
5. **O critério de aceite é o oráculo do teste.** Sem ele, o teste do agente é tautologia.
6. **A tarefa de teste vem antes da tarefa de implementação.**
7. **Delegue o que você sabe verificar.** Se não sabe verificar, está apostando.
8. **Em legado: congele antes de entender, entenda antes de alterar.**
9. **Todo conteúdo externo é entrada não confiável.**
10. **Percepção não é medida.** É hipótese, e hipótese se testa contra dado.

---

## 2. Antes de pedir código

### Escreva a intenção primeiro

Em arquivo, não no chat:

```markdown
## Intenção
Por que isso existe, em uma frase.

## Comportamento esperado
- Quando ..., então ...

## Fora de escopo
- ...

## Ainda não sei
- ...
```

**"Ainda não sei" é a seção que mais rende.** Toda pergunta ali é uma decisão que, sem o
registro, seria tomada por inferência do agente — e você não saberia que foi tomada.

### O teste do oráculo

Para cada critério de aceite:

> Eu conseguiria escrever o teste automatizado deste critério sem perguntar mais nada?

Se não, o critério não está pronto. Não é rigor excessivo: é o que separa uma spec de um
desejo.

### Calibre o rito

Consulte a matriz (`04-kit-sdd/matriz-de-calibragem.md`). Na dúvida entre dois níveis, olhe a
**reversibilidade**.

---

## 3. Contexto

### As três camadas

| Camada | Exemplo | Quem controla |
|---|---|---|
| O que você pede | O prompt | Você, sempre |
| O que você instrui | `AGENTS.md`, `constitution.md` | Você, se escrever |
| **O que ele encontra** | Código, README, issues, dependências | **Ninguém, por padrão** |

A terceira é onde moram os defeitos mais difíceis de diagnosticar.

### Contexto negativo

A seção "NÃO se aplica" do `AGENTS.md` é a de maior retorno por minuto investido.

**A regra do gatilho:** quando você corrigir o agente pela **segunda** vez pelo mesmo motivo,
aquilo vira linha no `AGENTS.md`. A primeira pode ser acaso; a quinta já custou caro.

### Orçamento de janela

| Situação | Ação |
|---|---|
| Tarefa longa, mesma linha de raciocínio | Compactar |
| Mudou de tarefa | **Reiniciar** |
| Agente em ciclo de erro | Reiniciar **e reformular o pedido** |
| Informação importa depois de amanhã | Escreva em arquivo. Não dependa do contexto |

Sintomas de saturação: "esquece" instrução do início; volta a sugerir o que já foi rejeitado;
faz alterações inconsistentes com o que ele mesmo escreveu.

### Perfis

**Sandbox** é o estrago que você aceita. **Aprovação** é a interrupção que você aguenta. São
dials independentes — nunca resolva incômodo de aprovação afrouxando o sandbox.

| Tarefa | Sandbox | Aprovação | Esforço |
|---|---|---|---|
| Explorar, entender | `read-only` | `never` | `low` |
| Implementar | `workspace-write` | `on-request` | `medium` |
| Revisar | `read-only` | `on-request` | `high` |
| Ler conteúdo externo | `read-only` | `untrusted` | `low` |

---

## 4. O ciclo

```
constitution → specify → clarify → plan → tasks → implement → PR
     ↑                                                 ↓
     └──────────────── analyze ────────────────────────┘
```

No Codex CLI: `$speckit-specify`, `$speckit-clarify`, `$speckit-plan`, `$speckit-tasks`,
`$speckit-implement`, `$speckit-analyze`. Em Copilot e Claude Code, os mesmos com `/speckit.`.

| Etapa | Erro comum | Correção |
|---|---|---|
| `specify` | Tecnologia na spec | Nome de biblioteca, tabela ou classe é assunto do `plan` |
| `specify` | "Fora de escopo" vazio | É o que impede a expansão silenciosa |
| `clarify` | Pular porque "está claro" | Se não levantou nada, releia procurando o que **você** teria que decidir |
| `plan` | Decisão sem alternativa descartada | "X em vez de Y porque Z" |
| `tasks` | Implementação antes do teste | Reordene à mão |
| `analyze` | Rodar só no fim | Custa 30s e roda antes da parte cara |

---

## 5. Testes

### O problema do oráculo

Quando o agente escreve o código **e** o teste, o teste prova que o código faz o que o código
faz. É tautologia com cobertura alta.

O critério de aceite é o oráculo, e precisa existir **antes**.

### A cadeia

```
critério de aceite → nome do teste → vermelho → código → verde → refatora
```

Quando o nome do teste é o critério, a suíte lê como a spec — e a spec para de envelhecer,
porque quebrar a regra quebra o teste.

### O que os testes de caminho feliz nunca pegam

Estes seis apareceram no kata e continuam aparecendo em produção:

- Fuso horário em regra de calendário.
- Limite inclusivo × exclusivo ("até 4 horas" inclui as 4?).
- Arredondamento de dinheiro (`float` × `HALF_EVEN` × `HALF_UP`).
- Condição composta em que só metade foi implementada.
- Limite (teto/piso) aplicado à parcela errada.
- Contagem de dias corridos × dias úteis.

Se a sua fatia toca qualquer um desses, escreva o teste **antes**.

### Teste que não se sustenta

- Depende do relógio (`datetime.now()` dentro do teste) → injete o instante.
- Depende de rede → isole.
- Depende da ordem de execução → cada teste monta seu estado.
- Só confirma a implementação → falta oráculo externo.

---

## 6. Revisão

### O que delegar e o que nunca

| Delegue | Nunca delegue |
|---|---|
| Gerar casos de teste a partir de critério escrito | Decidir qual é o critério |
| Refatoração mecânica com teste verde | Aprovar o próprio diff |
| Caracterização de legado | Julgar se o comportamento capturado está certo |
| Boilerplate, migration, scaffolding | Decisão arquitetural irreversível |
| Primeira leitura de PR grande | A leitura final antes do merge |

**O critério é um só: delegue o que você consegue verificar.**

### A pergunta que pega o que a atenção deixa passar

> **O que mudou aqui que eu não pedi?**

### Definition of Done

- [ ] Todo critério tem teste, e ele já esteve vermelho.
- [ ] Suíte verde; cobertura de regra não caiu.
- [ ] Diff lido integralmente por um humano.
- [ ] Nada fora do escopo da spec.
- [ ] Dependência nova justificada, ou nenhuma.
- [ ] Spec, plano e tasks no mesmo PR.
- [ ] Verificações determinísticas passaram.
- [ ] Se tocou legado: caracterização verde antes e depois.

Comece com três se o time resistir: **teste do critério, diff lido, nada fora do escopo.** Os
outros entram quando doerem.

### Approval fatigue

Nas primeiras horas você lê cada aprovação; ao fim do dia você clica. É previsível e não se
resolve com força de vontade.

- Sandbox correto **reduz a necessidade** de aprovação, em vez de exigir vigilância.
- Checkpoints em poucos pontos, em vez de aprovação contínua.
- Fatia menor: menos aprovações por unidade de trabalho.

> **Sinal de alerta:** rápido com sandbox permissivo e aprovação desligada não é autonomia.
> É ausência de fricção.

---

## 7. Legado

Resumo. Protocolo completo em `protocolo-brownfield.md`.

```
1. CONGELAR   →  characterization tests do comportamento ATUAL
2. ENTENDER   →  spec reversa
3. DELIMITAR  →  raio de impacto
4. ALTERAR    →  ciclo normal
```

- Achou um bug caracterizando? **Capture o bug.** Corrigir junto é trocar o pneu com o carro
  andando.
- Não caracterize tudo. Só a área que você vai tocar, mais um nível em cada direção.
- Tabule a matriz completa — é onde aparecem as interações que a leitura do código não pega.
- Teste de caracterização que quebra depois da alteração: **decida e registre**, não conserte
  no automático.

---

## 8. Segurança

### As quatro superfícies

| Superfície | Mitigação principal |
|---|---|
| Prompt injection por conteúdo externo | `read-only` em sessão que lê conteúdo externo |
| Supply chain de skills e MCP | Ler integralmente, fixar versão, segundo par de olhos |
| Segredos e exfiltração | Nunca em contexto; isolamento de rede; credencial dedicada |
| Dependências do agente | Justificativa no PR e revisão humana |

### Regras absolutas

- Segredo nunca entra em contexto, nem "só para entender a estrutura".
- `danger-full-access` não é default de ninguém em repositório com credencial válida.
- Skill de terceiro é dependência: leia o `SKILL.md` inteiro, `scripts/` incluído.
- Nunca `latest`. Sempre versão fixada.

Política completa em `governanca-e-seguranca.md`.

---

## 9. Métricas

| Métrica | Como medir | Cuidado |
|---|---|---|
| Lead time | Primeiro commit → produção | Isolado, incentiva pressa |
| Taxa de retrabalho | PRs que voltam / total | **Sobe antes de cair — é bom sinal** |
| Cobertura de regra | Cobertura de `services/`, não global | Global é fácil de inflar |
| Aderência à spec | Critérios com teste / total | O mais próprio do método |
| Estabilidade | Falha em mudança, tempo de restauração | **Nunca leia throughput sem isto** |

**As três regras:**

1. Sem baseline não há métrica — só número.
2. Throughput e estabilidade se leem juntos, sempre.
3. Percepção não é medida.

---

## 10. Sintomas e diagnósticos

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| "A IA piorou" | Janela saturada, ou skill novo interferindo | Reinicie a sessão; rode os evals dos skills |
| Agente usa função que não devia | Falta contexto negativo | Seção "NÃO se aplica" no `AGENTS.md` |
| Agente inventa método de biblioteca | Alucinação de API | *Usage spec* + verificação determinística |
| PR sempre volta na revisão | Critério de aceite fraco | Aplique o teste do oráculo antes de implementar |
| Diff traz coisa que ninguém pediu | "Fora de escopo" vazio na spec | Preencha a seção; rode `$speckit-analyze` |
| Testes passam e o bug chega em produção | Teste sem oráculo externo | Critério de aceite antes do código |
| Revisão virou carimbo | PR grande demais | Fatias menores. Não é problema de disciplina |
| Skill não dispara | Descrição sem os termos reais | Rode o eval; adicione sinônimos à `description` |
| Skill dispara onde não devia | Descrição genérica | Restrinja; reforce "Quando NÃO usar" |
| Método abandonado em 3 semanas | Rito pesado demais para o tamanho | Matriz de calibragem |
| Time diz que ficou rápido, lead time igual | O custo migrou para a revisão | Meça throughput **e** estabilidade |
| Legado quebrou depois de refatorar | Sem caracterização antes | Protocolo de brownfield |
| Sessão nova refaz decisão já tomada | Amnésia entre sessões | Estado em arquivo; seção "Sessão" no `AGENTS.md` |
| "Pronto" e a suíte está vermelha | Vitória prematura | Exija a saída do comando; suíte no CI |
| Teste mudou junto com o código | Teste fake | Volte ao critério; proteja o bloco de testes |
| "Revisei, está correto" na mesma sessão | Tudo no mesmo processo | Avaliação em sessão nova, perfil `revisao`, contra a spec |
| Código duplicado e padrão velho se espalhando | AI slop acumulado | Contexto negativo, lint do princípio, limpeza semanal pequena |

---

## 11. Harness: os seis modos de falha

**Agente = modelo + harness.** O harness é tudo que não é o modelo: **guias** atuam antes de o
agente agir (constitution, `AGENTS.md`, spec, skill); **sensores** atuam depois (teste, lint,
hook, CI, revisão). Guia sem sensor é esperança; sensor sem guia é retrabalho.

| # | Problema | Sintoma | Guia | Sensor |
|:-:|---|---|---|---|
| 1 | **One-shot hero** | Tudo num prompt; PR gigante; sessão estoura no meio | Tasks atômicas; "uma task por vez" | Suíte verde por task; commit por task; alerta de diff grande |
| 2 | **Vitória prematura** | "Pronto, todos os testes passam" — sem ter rodado | Conclusão definida como comando + resultado | Saída real do comando; suíte no CI; DoD |
| 3 | **Amnésia entre sessões** | Sessão nova desfaz o que a anterior decidiu | Estado em spec, tasks, commits, `AGENTS.md` | Resumo do estado ao iniciar, conferido |
| 4 | **Teste fake** | Suíte verde que não verifica nada | Teste do critério; "nunca altere teste para passar" | Teste esteve vermelho; diff de teste à parte; contagem e `skip` no CI |
| 5 | **Tudo no mesmo processo** | A sessão que implementou aprova a si mesma | Papéis separados por sessão e perfil | Avaliação em contexto limpo, contra a spec; CI fora do agente |
| 6 | **AI slop acumulado** | Nenhum PR é ruim; o repositório, em meses, é | Contexto negativo; constitution verificável | Lint do princípio; duplicação no CI; limpeza pequena e recorrente |

Nenhum dos seis se resolve com "prestar mais atenção". Quando um deles acontecer **pela segunda
vez**, a resposta é uma peça de harness — a mesma regra do gatilho do `AGENTS.md`.

Teoria completa: `runbook.md`, Parte XI.

---

## Para consultar

| Preciso de... | Onde |
|---|---|
| Decidir o nível de rito | `04-kit-sdd/matriz-de-calibragem.md` |
| Templates de spec, plan, tasks | `04-kit-sdd/templates/` |
| Auditar uma spec | Skill `revisar-spec` |
| Mexer em legado | `06-playbooks/protocolo-brownfield.md` |
| Política de segurança | `06-playbooks/governanca-e-seguranca.md` |
| Avaliar minha evolução | `02-avaliacao/rubrica-competencias.md` |
