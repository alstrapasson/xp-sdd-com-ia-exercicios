# Laboratório 5 — Brownfield: congelar, entender, alterar

**Dia 5 · 35 min · individual**
Alvo: `lab-repo/app/services/priorizacao.py`

---

## A situação

`priorizacao.py` foi migrado de um sistema antigo em 2019. Não tem teste. Os nomes são de uma
letra. Tem número mágico. Tem um `TODO` de alguém que não trabalha mais aqui e um comentário
mandando falar com o Marcelo antes de mexer.

E está em produção: `POST /ordens` e `GET /ordens` dependem dele.

**A demanda:** o planejamento quer que ordens `aguardando_peca` parem de ser despriorizadas
enquanto a peça não chega — hoje elas caem na fila, e ninguém sabe explicar por quê.

---

## A regra que não se negocia

```
1. Congelar   →  characterization tests do comportamento ATUAL
2. Entender   →  spec reversa
3. Delimitar  →  raio de impacto
4. Alterar    →  aí sim
```

**Ninguém altera nada antes da etapa 1 estar verde.** Se você se pegar refatorando na etapa 1,
pare — é o erro mais comum deste laboratório.

---

## Etapa 1 — Congelar (14 min)

Characterization test **não** descreve o que o código deveria fazer. Descreve o que ele faz,
inclusive o que estiver errado.

Crie `tests/test_priorizacao_caracterizacao.py`.

Peça ao agente — e note o enunciado, ele importa:

> "Escreva testes que capturam o comportamento **atual** de `priorizacao.calc`, sem corrigir
> nada. Cubra a matriz de criticidade (A/B/C) × tipo (corretiva/preventiva/preditiva) ×
> status (`aguardando_peca` ou não), mais variações de idade da ordem, de `reaberturas` e de
> `horas_operacao` acima e abaixo de 15000. Se algum resultado parecer errado, **capture-o
> assim mesmo** e marque com um comentário `# suspeito:`."

Rode e confirme verde:

```bash
pytest tests/test_priorizacao_caracterizacao.py -q
```

Anote: **quantos casos você capturou?** `______`

> A matriz mínima tem 18 combinações (3×3×2). Se você tem muito menos, faltou cobertura — e
> a rede que deveria te proteger tem buraco exatamente onde você não olhou.

### Cuidado com o `ref`

`calc` usa `datetime.now(timezone.utc)` quando `ref` não é passado. Teste que depende do
relógio quebra amanhã. **Sempre passe `ref` explícito.**

---

## Etapa 2 — Entender (8 min)

Com a suíte verde, peça:

> "A partir de `priorizacao.py` e dos testes de caracterização, escreva a spec que descreve as
> regras de negócio implementadas. Marque com `⚠` tudo que parecer inconsistente ou não
> intencional."

Revise a spec **você mesmo**. O agente descreve bem o que o código faz; ele não sabe o que o
negócio queria.

### O que procurar

Sem consultar a lista antes de tentar:

<details>
<summary>Abra só depois de escrever a sua</summary>

- `aguardando_peca` **soma** 2, despriorizando. Intencional (não adianta priorizar o que está
  bloqueado) ou herdado sem revisão?
- **O `+2` não vale 2 em todos os casos.** Por causa do teto em 5, o mesmo ajuste desloca a
  ordem em 2, em 1 ou em **nada**, dependendo de onde ela já estava. Uma corretiva em
  equipamento A anda 1; uma preventiva em C não anda nada. Ou seja: a regra que o negócio
  acha que existe ("aguardando peça cai duas posições") não é a que está implementada — e
  ninguém percebeu em 7 anos porque não havia teste que mostrasse a matriz inteira.
- `reaberturas` subtrai **sem piso**: uma ordem C preventiva reaberta 4 vezes chega a
  prioridade 1 — máxima — só por reabertura.
- `horas_operacao > 15000` é número mágico, sem fonte documentada.
- `FATORES.get(..., 5)` engole criticidade desconhecida silenciosamente.
- `ordenar()` devolve `99` para equipamento inexistente — fora da escala 1–5.
- `d = (ref - aberta_em).days` trunca: 7 dias e 23 horas ainda é `d == 7`.

</details>

**Cada `⚠` é uma pergunta para o Marcelo — não uma correção sua.** Anote-as; é a pauta da
conversa, e essa distinção é o conteúdo do dia.

---

## Etapa 3 — Delimitar (4 min)

```bash
grep -rn "priorizacao" app/ tests/
```

- [ ] Quem chama `calc`? E `ordenar`?
- [ ] A saída alimenta o quê? (resposta de API, ordenação de fila, algum relatório?)
- [ ] O campo `prioridade` é persistido na abertura **e** recalculado na listagem? Isso pode
      divergir?

Restrinja o agente à área:

```bash
codex --profile implementacao
```

Em uma frase, escreva o raio de impacto acordado:

```
Posso alterar: ______________________
Não posso alterar: ______________________
```

---

## Etapa 4 — Alterar (9 min)

**Só agora.** Aplique o ciclo do Dia 4 à demanda real:

> Ordens `aguardando_peca` não devem ser despriorizadas.

1. Escreva o **novo** critério de aceite.
2. Escreva o teste do novo comportamento — ele deve ficar **vermelho**.
3. Implemente a mudança mínima.
4. Rode a suíte inteira.

### O momento que importa

Alguns testes de caracterização vão quebrar. **Isso é o sistema funcionando**, não um problema.

Para cada um que quebrar, decida conscientemente e registre:

| Teste que quebrou | A mudança era pretendida? | Ação |
|---|:-:|---|
| | Sim | Atualizar o teste e dizer por quê no commit |
| | **Não** | **Reverter.** Você mudou algo que não pretendia |

> É exatamente isto que a rede compra: a diferença entre "mudei o que eu queria" e "mudei
> mais coisa e não vi". Sem a caracterização, os dois casos são indistinguíveis.

---

## Entrega

- `tests/test_priorizacao_caracterizacao.py`
- A spec reversa, com os `⚠`
- A lista de perguntas para o planejamento
- O raio de impacto escrito
- A alteração, com testes

---

## Critério de pronto

- [ ] Caracterização escrita **antes** de qualquer alteração.
- [ ] 18+ casos, cobrindo a matriz.
- [ ] Nenhum teste depende do relógio (`ref` sempre explícito).
- [ ] Spec reversa com ao menos 3 `⚠` identificados.
- [ ] Raio de impacto escrito.
- [ ] Teste do novo comportamento ficou vermelho antes de passar.
- [ ] Toda quebra de caracterização foi decidida e registrada, não apenas "consertada".

---

## Se terminar cedo

Aplique as etapas 1 a 3 ao arquivo legado que **você** trouxe do seu repositório. Não precisa
alterar nada — congelar e entender já é entregável, e é exatamente por onde a Sessão 1 da
mentoria vai começar.
