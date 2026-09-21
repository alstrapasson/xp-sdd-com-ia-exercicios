<!--
TEMPLATE — plan.md
Gerado por: $speckit-plan

O QUE VAI AQUI: as decisões técnicas. Arquitetura, tecnologia, contratos, modelo de dados.
O QUE NÃO VAI:  a intenção (isso é spec) e os passos (isso é tasks).

O plano OBEDECE à constitution. Se uma decisão aqui contraria um princípio de lá, ou a
decisão muda, ou a constitution muda em reunião — não no meio da implementação.
-->

# Plan — <TÍTULO DA FATIA>

**Spec:** `<001-nome-curto>` · **Autor:** ______ · **Data:** __/__/____

---

## 1. Abordagem

<Dois ou três parágrafos: como isto será construído. O suficiente para alguém do time
discordar antes de existir código.>

## 2. Decisões

> **Decisão sem alternativa descartada vale pouco.** "Escolhemos X" não permite revisão;
> "escolhemos X em vez de Y porque Z" permite. Daqui a um ano, quando Z não for mais
> verdade, alguém saberá que é hora de revisitar.

| # | Decisão | Alternativa descartada | Por quê |
|:-:|---|---|---|
| 1 | | | |
| 2 | | | |

## 3. Contratos

### `<MÉTODO /caminho>` — <o que faz>

**Entrada**
```json
{ }
```

**Saída — 200**
```json
{ }
```

**Erros**

| Status | Quando | Corpo |
|:-:|---|---|
| 400 | | |
| 404 | | |
| 409 | | |
| 422 | Validação de schema | Padrão do framework |

## 4. Modelo de dados

<Campos novos ou alterados, com tipo e obrigatoriedade. Se não há mudança, escreva
"sem alteração" — explicitamente, para que a revisão saiba que foi considerado.>

| Campo | Tipo | Obrigatório | Observação |
|---|---|:-:|---|
| | | | |

**Migração:** [ ] não necessária · [ ] necessária → `<estratégia, e como reverter>`

## 5. Arquivos afetados

| Arquivo | O que muda |
|---|---|
| `<caminho>` | `<criado / alterado / removido>` — `<o quê>` |

## 6. Aderência à constitution

> Cite os princípios que esta fatia toca. Se algum é violado, isso precisa ser decisão
> consciente e registrada — não descoberta na revisão.

| Princípio | Como esta fatia atende |
|---|---|
| `<§3 Testes>` | |
| `<§5 Dados e tempo>` | |

**Violações conscientes:** `<nenhuma / descrever e justificar>`

## 7. Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|---|:-:|:-:|---|
| | | | |

---

## Checklist antes de seguir para `tasks`

- [ ] Toda decisão tem alternativa descartada e justificativa.
- [ ] Contratos completos: entrada, saída **e erros**.
- [ ] Arquivos afetados listados nomeadamente.
- [ ] Aderência à constitution verificada, violações registradas.
- [ ] Se há migração de dados, o nível de rito foi reavaliado.
