<!--
TEMPLATE — spec.md  (uma por fatia vertical entregável, NUNCA por projeto)
Capacitação XP + SDD com IA (Codex) · Strapa Tecnologia

Gerado por: $speckit-specify   ·   Refinado por: $speckit-clarify

O QUE VAI AQUI: comportamento observável, critérios testáveis, regras de negócio.
O QUE NÃO VAI:  nome de biblioteca, estrutura de tabela, nome de classe, cache, algoritmo.
                Tudo isso é plan.md. Tecnologia na spec faz o plan virar cópia da spec —
                e você perdeu a etapa que protege a escolha técnica.

TESTE DE QUALIDADE, e é literal: dê um critério de aceite a um colega e peça que escreva o
teste. Se ele precisar perguntar qualquer coisa, o critério ainda não está pronto.
-->

# Spec — <TÍTULO DA FATIA>

**ID:** `<001-nome-curto>` · **Autor:** ______ · **Data:** __/__/____
**Nível de rito:** [ ] completo · [ ] reduzido · [ ] leve — *ver matriz de calibragem*

---

## 1. Por que isto existe

<Uma ou duas frases. O problema real, na linguagem de quem tem o problema — não na
linguagem da solução. Se você não consegue escrever isso, provavelmente ainda não deveria
estar implementando.>

## 2. Comportamento esperado

<Descrição em prosa curta do que passa a ser possível depois desta fatia. Observável de fora:
o que o usuário, o sistema chamador ou o operador consegue fazer que antes não conseguia.>

## 3. Critérios de aceite

> Cada critério vira **um teste com o mesmo nome**. Numere — os testes e as tasks referenciam
> por número.

| # | Critério | Teste |
|:-:|---|---|
| 1 | Quando `<condição>`, então `<resultado observável>` | `test_<nome>` |
| 2 | Quando `<condição>`, então `<resultado observável>` | `test_<nome>` |
| 3 | Quando `<condição de erro>`, então `<erro específico e código>` | `test_<nome>` |

## 4. Regras de negócio

<As regras que governam o comportamento, com os valores explícitos. Se um valor não é
conhecido, ele NÃO vira suposição: vai para a seção 6.>

- <Regra, com o número, o limite ou a condição exata.>
- <Exceção à regra, e quando ela se aplica.>

## 5. Fora de escopo

> **A seção mais subutilizada — e a que impede o agente de expandir sozinho.**
> Expansão silenciosa é a queixa nº 1 de quem usa agente sem método.

- <O que deliberadamente NÃO é feito aqui, e em que fatia futura será feito — se for.>
- <Comportamento adjacente que alguém poderia assumir que está incluído, e não está.>

## 6. Ambiguidades e decisões

> Preenchida por `$speckit-clarify`. **A resposta volta para cá, não fica no chat** — daqui a
> seis meses ninguém lembra da conversa; a spec lembra.

| # | Pergunta | Resposta | Quem decidiu | Data |
|:-:|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

**Ainda em aberto** (bloqueia a implementação):

- [ ] <pergunta sem resposta — não implemente o que depende dela>

## 7. Impacto

- **Arquivos que mudam:** `<listar nomeadamente>`
- **Contratos afetados:** `<endpoint, evento, schema — e se a mudança é compatível>`
- **Migração de dados:** [ ] não · [ ] sim → `<descrever, e reavaliar o nível de rito>`
- **Reversível com `git revert`?** [ ] sim · [ ] não → `<por quê>`

---

## Checklist antes de seguir para o `plan`

- [ ] Nenhum nome de biblioteca, tabela ou classe nesta spec.
- [ ] Todo critério de aceite é verificável sem perguntar mais nada.
- [ ] "Fora de escopo" preenchido, não vazio.
- [ ] Nenhuma pergunta bloqueante em aberto.
- [ ] Cabe em uma fatia vertical — se não cabe, quebre agora, não depois.
