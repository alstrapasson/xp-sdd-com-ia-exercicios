# Protocolo de Brownfield

**Entregável 6 da proposta.** Roteiro de adoção em base legada, usado no Dia 5 e nas duas
sessões de mentoria.

---

## Quando usar

Sempre que a mudança tocar código que:

- não tem cobertura de teste na área afetada, **ou**
- ninguém no time consegue explicar completamente, **ou**
- foi escrito por alguém que não está mais disponível, **ou**
- tem comentário do tipo "não mexer sem falar com o Fulano".

Um só desses critérios já basta.

---

## A ordem, e ela não é negociável

```
1. CONGELAR   →  characterization tests do comportamento ATUAL
2. ENTENDER   →  spec reversa a partir do código e dos testes
3. DELIMITAR  →  raio de impacto e dependências implícitas
4. ALTERAR    →  aí sim, com o ciclo normal de spec → teste → implementação
```

**Ninguém altera nada antes da etapa 1 estar verde.**

O erro mais comum é começar a melhorar o código durante a etapa 1 — os nomes são ruins, a
tentação é grande, e o agente faz isso espontaneamente se você não impedir.

---

## Etapa 1 — Congelar

### O que é um characterization test

Um teste que descreve o que o código **faz**, não o que deveria fazer.

> **Se você achar um bug enquanto escreve o teste, capture o bug.**
>
> Você não está corrigindo agora; está construindo a rede que vai permitir corrigir com
> segurança depois. Corrigir junto com caracterizar é trocar o pneu com o carro andando.

Marque cada suspeita com `# suspeito: <por quê>`. Elas viram a pauta da conversa com quem
conhece o negócio — não itens de correção.

### Procedimento

1. **Mapeie a superfície.** Assinatura pública, parâmetros, retorno, efeitos colaterais.

2. **Identifique as dimensões de entrada.** Cada enum, flag e faixa é uma dimensão; o produto
   cartesiano é a matriz mínima.
   > `3 criticidades × 3 tipos × 2 estados = 18 casos`

3. **Elimine dependência de relógio, rede e ordem.** Se a função chama `datetime.now()`
   internamente, **injete o instante de referência em todo teste**. Teste que depende do
   relógio passa hoje e falha amanhã.

4. **Registre o valor observado**, não o esperado. Rode a função e anote o que ela devolveu.

5. **Acrescente os limites:** valor exatamente no limiar, zero, negativo, vazio, `None`, e
   valores logo acima e logo abaixo de cada constante mágica do código.

6. **Rode e confirme que tudo passa.** Um teste de caracterização que falha na primeira
   execução foi escrito errado: descreve expectativa, não observação.

7. **Tabule a matriz completa.**

> **A etapa 7 é a que rende mais.** Tabular todas as combinações revela interações que
> nenhuma leitura do código pega: clamps que mascaram ajustes, condições que nunca disparam,
> regras que se anulam. No laboratório do Dia 5, é aqui que se descobre que um `+2` aplicado
> uniformemente produz efeito de 2, 1 ou **zero**, dependendo de onde o valor já estava —
> e que a regra que o negócio acredita existir não é a que está rodando há sete anos.

O agente é excelente nesta etapa: gerar 30 casos que cobrem a matriz é exatamente o trabalho
volumoso e mecânico em que ele ganha. Use o skill `gerar-characterization-tests`.

### Quanto caracterizar

**Não caracterize tudo.** Cobertura total de legado não é meta de ninguém e o esforço não se
paga. Caracterize:

- A função que você vai alterar.
- O que ela chama e o que a chama, um nível em cada direção.
- Qualquer coisa que compartilhe estado com ela.

---

## Etapa 2 — Entender

Com a suíte verde, peça ao agente:

> "A partir deste módulo e destes testes, escreva a spec que descreve as regras de negócio
> implementadas. Marque com ⚠ tudo que parecer inconsistente ou não intencional."

**Revise você mesmo o resultado.** O agente descreve bem o que o código faz; ele não sabe o
que o negócio queria.

### O que costuma aparecer

| Achado | Como tratar |
|---|---|
| Número mágico sem fonte documentada | Pergunta para o negócio, não correção |
| Condição que nunca dispara | Verificar se é código morto ou se a condição mudou |
| Default silencioso engolindo caso desconhecido | Risco real: falha sem sinal |
| Regra que contradiz outra regra | Pergunta para o negócio |
| Valor fora da escala declarada | Bug provável — registre, não corrija ainda |
| Interação não intencional entre ajustes | O achado mais valioso. Vem da tabulação da matriz |

**Cada ⚠ é uma pergunta, não uma correção.** Essa distinção é o conteúdo do protocolo.

### Produza a lista de perguntas

```
PARA <quem conhece o negócio>

1. <regra observada>. Isso é intencional?
2. <interação inesperada>. O time sabia disso?
3. <valor mágico>. Alguém lembra de onde veio esse número?
```

Leve a lista para uma conversa de quinze minutos. Ela costuma valer mais que a alteração.

---

## Etapa 3 — Delimitar

```bash
grep -rn "<nome_do_modulo>" .
```

Responda por escrito:

- [ ] Quem chama? (código, rotas, jobs, scripts)
- [ ] O que a saída alimenta? (resposta de API, relatório, integração, decisão automatizada)
- [ ] O valor é persistido **e** recalculado? Isso pode divergir?
- [ ] Há consumidor externo — outro time, cliente, contrato público?

### Restrinja o agente

```bash
codex --profile implementacao
```

E escreva o acordo, em uma linha cada:

```
Posso alterar:      ______________________
Não posso alterar:  ______________________
```

Isso não é burocracia: é o que torna verificável, na revisão, se o diff saiu do escopo.

---

## Etapa 4 — Alterar

Só agora. Aplique o ciclo normal:

1. Escreva o **novo** critério de aceite.
2. Escreva o teste do novo comportamento — ele deve ficar **vermelho**.
3. Implemente a mudança mínima.
4. Rode a suíte inteira.

### O momento que importa

Alguns testes de caracterização vão quebrar. **Isso é o sistema funcionando.**

Para cada um, decida conscientemente e registre:

| Teste que quebrou | A mudança era pretendida? | Ação |
|---|:-:|---|
| | Sim | Atualizar o teste, e dizer por quê no commit |
| | **Não** | **Reverter.** Você mudou algo que não pretendia |

> É exatamente isto que a rede compra: a diferença entre "mudei o que eu queria" e "mudei mais
> coisa e não vi". Sem caracterização, os dois casos são indistinguíveis — e o segundo só
> aparece em produção.

---

## Estratégia de adoção incremental

Para quem herda uma base grande sem testes, por onde começar:

| Ordem | Onde | Por quê |
|:-:|---|---|
| 1 | O módulo que você **já vai** alterar este mês | Esforço que já seria gasto, com retorno imediato |
| 2 | O módulo que mais aparece em incidente | Maior retorno por hora investida |
| 3 | O módulo com mais regra de negócio por linha | Onde o conhecimento tácito é mais denso |
| 4 | O que tem consumidor externo | Onde o erro custa mais caro |
| 5 | O resto | Só se e quando for tocado |

**O item 5 é uma decisão, não uma omissão.** Caracterizar código que ninguém vai tocar é
esforço sem retorno — e escrever isso explicitamente evita que a iniciativa morra por parecer
infinita.

### Cadência sustentável

- Caracterizar **junto** com a alteração, não em projeto separado. Projeto de "aumentar
  cobertura" é o primeiro a ser cortado quando o prazo aperta.
- Uma regra de time simples e verificável: *"módulo tocado sai com caracterização"*.
- Métrica de acompanhamento: proporção de **módulos alterados no mês** que tinham
  caracterização antes da alteração. Não cobertura global — ela é fácil de inflar e não diz
  nada sobre risco.

### Harnessability: o legado pede harness em ordem

Código legado é, por definição, difícil de equipar com guias e sensores. A ordem que
funciona (`runbook.md`, §42):

1. **Comandos que rodam** — sem teste que roda em um comando, não há sensor.
2. **Caracterização na área tocada** — o primeiro sensor instalável em código sem teste.
3. **Um guia por falha real** — a regra do gatilho do `AGENTS.md`; em legado, quase sempre
   um padrão antigo que não deve ser replicado.
4. **Sensores no CI** — onde o agente não os desliga.

**Atenção ao teste fake em legado:** na Etapa 4, teste de caracterização que quebra só é
atualizado por **decisão humana registrada**. Agente que "ajusta" caracterização para a suíte
ficar verde apagou exatamente a rede que este protocolo construiu.

---

## Checklist

- [ ] Caracterização escrita **antes** de qualquer alteração.
- [ ] Matriz de entrada coberta; contagem de casos registrada.
- [ ] Nenhum teste depende do relógio, de rede ou de ordem.
- [ ] Suíte de caracterização verde antes de começar.
- [ ] Spec reversa produzida e revisada por humano.
- [ ] Lista de ⚠ levada a quem conhece o negócio.
- [ ] Raio de impacto escrito e sandbox restrito.
- [ ] Teste do novo comportamento ficou vermelho antes de passar.
- [ ] Toda quebra de caracterização foi **decidida e registrada**, não apenas consertada.
