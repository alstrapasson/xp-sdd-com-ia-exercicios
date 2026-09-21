# Matriz de Calibragem

**Quando o rito completo de SDD vale — e quando é desperdício.**

Entregável 4 da proposta. Documento de consulta permanente; imprima e deixe visível.

---

## Por que esta matriz existe

Se o rito completo for aplicado a toda mudança, em três semanas ninguém aplica mais nada. O
método morre por excesso, não por falta.

Esta é a resposta operacional à crítica de Gojko Adzic — de que o SDD reintroduz a rigidez do
Waterfall. **A pergunta certa nunca foi "como fazer sempre". É quando vale.**

---

## A matriz

| Fator | Rito completo | Rito reduzido | Fluxo leve |
|---|---|---|---|
| **Tamanho** | Mais de 3 dias | 0,5 a 3 dias | Menos de 0,5 dia |
| **Risco de negócio** | Alto — dinheiro, compliance, dado de cliente | Médio | Baixo |
| **Reversibilidade** | Difícil — migração, contrato público, dado destrutivo | Média | Trivial (`git revert`) |
| **Pessoas afetadas** | Várias equipes | Uma equipe | Uma pessoa |
| **Regra de negócio nova** | Sim | Alguma | Nenhuma |
| **Quem consome** | Sistema externo, cliente | Outro time | Só este serviço |
| **Artefatos** | spec + clarify + plan + tasks + analyze | spec enxuta + tasks | Issue bem escrita + teste |
| **Tempo de cerimônia** | 45–90 min | 15–25 min | Menos de 5 min |

---

## A regra de desempate

> **Na dúvida entre dois níveis, olhe a reversibilidade.**
>
> Se dá para reverter com `git revert` sem consequência, use o rito **menor**.
> Se envolve dado, contrato público ou migração, use o **maior** — mesmo que a mudança seja
> pequena.

Reversibilidade domina tamanho. Uma migração de 20 linhas que apaga coluna merece rito
completo; um refactor de 800 linhas puramente interno, coberto por testes, não merece.

---

## Os dois erros, e são simétricos

| Erro | Como se manifesta | Consequência |
|---|---|---|
| **Rito pesado em coisa trivial** | Spec de três páginas para trocar um label | O time acha o método burocrático. Em três semanas, ninguém usa nada |
| **Fluxo leve em mudança irreversível** | Migração de dados sem spec; contrato público alterado sem critério escrito | O método não estava lá quando fez falta |

O segundo é mais comum do que parece, porque mudanças irreversíveis frequentemente **parecem**
pequenas. Uma linha de `ALTER TABLE` cabe num commit.

---

## Casos-limite resolvidos

Situações que geram discussão real, com a decisão já tomada:

| Situação | Nível | Por quê |
|---|:-:|---|
| Correção de bug de uma linha, com teste que reproduz | Leve | Reversível, escopo mínimo, o teste é a spec |
| Correção de bug de uma linha **em cálculo financeiro** | Reduzido | O risco não é o tamanho: é o dinheiro |
| Refactor grande, puramente interno, testes verdes | Reduzido | Grande, mas reversível e sem regra nova |
| Adicionar campo opcional em resposta de API | Reduzido | Compatível, mas há consumidor externo |
| Adicionar campo **obrigatório** em requisição de API | Completo | Quebra contrato. Irreversível para quem já integrou |
| Migração que só adiciona coluna com default | Reduzido | Reversível na prática |
| Migração que remove ou renomeia coluna | Completo | Destrutiva. Rito completo mesmo que sejam 3 linhas |
| Ajuste de texto, label, cor | Leve | — |
| Ajuste de texto **em documento legal ou contratual** | Reduzido | Baixo risco técnico, alto risco jurídico |
| Alterar módulo legado sem testes | Completo | **Mais o protocolo de brownfield.** Ver `06-playbooks/` |
| Spike / prova de conceito descartável | Leve | Desde que seja descartada de verdade — se virar produção, refaça com o rito |
| Atualização de dependência com CVE | Reduzido | Urgente não é sinônimo de sem critério |

---

## Como usar na prática

1. **Antes de abrir o editor**, marque o nível no cabeçalho da spec (ou na issue, no fluxo leve).
2. **Se algum fator puxar para cima, suba.** A matriz não é média: é o fator mais alto que manda.
   Uma mudança de meio dia que toca migração é rito completo.
3. **Registre a escolha.** No `analyze` ou na revisão, alguém pode discordar — e discordar de
   uma decisão registrada é barato.

### Reavaliação obrigatória

Suba o nível no meio do caminho quando:

- O `clarify` levantar mais de três ambiguidades reais.
- O `plan` revelar migração de dados que a spec não previa.
- O diff começar a tocar arquivos fora da lista de impacto.

Subir de nível no meio é sinal de que o método está funcionando — não de que você errou no
começo.

---

## O que a matriz não decide

- **Não dispensa teste.** Fluxo leve tem menos cerimônia, não menos teste. A linha
  "issue + teste" tem a palavra *teste* nela.
- **Não dispensa revisão.** Todo diff é lido por um humano, em qualquer nível.
- **Não dispensa `Definition of Done`.** O DoD é o mesmo nos três níveis.

O que muda entre os níveis é **quanto se escreve antes**, não **quanto se verifica depois**.
