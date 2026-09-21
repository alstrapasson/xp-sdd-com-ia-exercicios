# Kata baseline — Multa por devolução atrasada

**Tempo alvo: 15 minutos.** Feito em aula, no Dia 1, cronometrado.

Este é o seu **ponto de partida individual**. Não é prova, não vale nota e o resultado não é
compartilhado com a sua liderança. Ele existe para que, no fim do programa, você tenha um
número concreto para comparar — em vez de uma impressão.

Por isso, uma instrução contraintuitiva:

> **Trabalhe exatamente como você trabalha hoje.** Use a IA do jeito que já usa, com os
> atalhos que já toma. Não tente aplicar um método que você ainda não aprendeu, não capriche
> mais do que caprichar num dia normal, não escreva testes que normalmente não escreveria.
>
> Um baseline "caprichado" destrói a única coisa que este exercício mede.

---

## Como executar

1. **Anote o horário de início** em `registro-kata-baseline.md` (fornecido junto com este material).
2. Implemente a função `calcular_multa` em `src/locacao/multa.py`.
3. Pare quando considerar **pronto para abrir um PR** — não quando estiver perfeito.
4. **Anote o horário de término**, mesmo que não tenha concluído. Parar em 15 min sem concluir
   é um dado válido e útil — e é o que vai acontecer com a maior parte da turma.
5. Preencha o restante do registro e entregue ao instrutor **antes de a aula continuar**.

**Permitido:** qualquer IA, qualquer documentação, qualquer biblioteca padrão do Python.
**Não permitido:** conversar com os colegas ou perguntar ao instrutor durante os 15 minutos.
São quinze minutos de silêncio; depois a gente abre tudo, junto.

---

## O pedido

Chegou este item no backlog. É o texto que você recebeu, na íntegra:

> **[LOC-4471] Cobrar multa por devolução atrasada de equipamento**
>
> Hoje a devolução em atraso não gera cobrança e estamos perdendo receita.
>
> Regras que o time comercial passou:
>
> - Se o equipamento voltar depois da data/hora prevista no contrato, cobra multa.
> - A multa é de **15% da diária por dia de atraso**.
> - Tem também uma **taxa fixa de R$ 50** na primeira vez que o cliente atrasa.
> - Existe uma **tolerância** — atraso pequeno a gente não cobra, para não brigar com o cliente
>   por causa de trânsito.
> - A multa **não pode passar de um teto**, senão vira abuso e a gente perde na reclamação.
> - Cliente **premium** tem tratamento diferenciado.
>
> Devolveu no prazo ou adiantado, não cobra nada.
>
> Os timestamps chegam do sistema de pátio em UTC. A operação toda é no Brasil.

Assine a função conforme o stub em `src/locacao/multa.py`.

---

## O que já existe no repositório

```
src/locacao/
  modelos.py      Contrato e Devolucao (dataclasses). Não altere.
  calendario.py   Utilitários de data que já existem no sistema.
  multa.py        <- onde você trabalha
tests/
  test_smoke.py   Dois testes triviais que já passam. Sirva-se.
```

Rode os testes com:

```bash
python -m pytest
```

---

## Entrega

Considera-se entregue o que estiver em `src/locacao/multa.py` no momento em que você parar o
cronômetro. Testes que você tenha escrito por conta própria contam a favor e devem ser
enviados junto — mas **não são obrigatórios**, e não escrevê-los também é um dado.

Se você travou, entregue travado e registre onde travou. É informação melhor do que uma
entrega completa fora do tempo.
