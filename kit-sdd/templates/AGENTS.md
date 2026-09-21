<!--
TEMPLATE — AGENTS.md
Capacitação XP + SDD com IA (Codex) · Strapa Tecnologia

Onde colocar:
  ~/.codex/AGENTS.md              suas preferências, todos os projetos
  <repo>/AGENTS.md                convenções deste repositório      <- este template
  <repo>/<subdir>/AGENTS.md       regras de uma área específica

O mais específico refina o mais geral. O nível de subdiretório é o mais subutilizado e
resolve o caso mais comum: uma pasta com regra diferente do resto (legado, código gerado,
área sensível).

REGRA DE TAMANHO: se este arquivo está repetindo o README, corte. O README apresenta o
projeto a quem VAI contribuir. Este arquivo instrui quem JÁ vai contribuir. São documentos
diferentes, com públicos diferentes.
-->

# AGENTS.md — <NOME DO REPOSITÓRIO>

<Uma frase: o que este serviço faz.>

---

## Como rodar

> Comandos exatos e copiáveis. Nunca "veja o README".

```bash
# instalar
<comando>

# testar
<comando>

# lint e tipos
<comando>

# subir localmente
<comando>
```

## Convenções

- **Tipagem:** <regra>
- **Nomenclatura:** <identificadores em inglês; documentação em pt-BR; padrão de nomes de teste>
- **Estrutura:** <onde vai router, service, modelo, teste>
- **Erros:** <como erro de domínio é levantado e traduzido na borda>
- **Datas:** <UTC em todo lugar; conversão local só na apresentação>
- **Dinheiro:** <Decimal, nunca float; arredondamento explícito no fim>

## Sensível

> O que exige revisão humana obrigatória, e onde não mexer sem falar com alguém.

- `<caminho>` — <por quê, e com quem falar>
- Migração de dados nunca é aplicada por agente sem aprovação explícita.
- Nenhum segredo entra em contexto. `.env` e credenciais estão fora do alcance.

## NÃO se aplica

> **A seção que quase ninguém escreve — e a que dá mais retorno por minuto investido.**
>
> Aqui vão as funções, módulos e padrões que existem no repositório e que o agente **não**
> deve usar por inferência. Sempre dizendo o que usar no lugar.
>
> Como preencher, três perguntas que produzem o conteúdo:
>   1. Que função existe aqui que *parece* genérica mas serve a um caso só?
>   2. Que padrão antigo ainda está no código e não deve ser copiado em código novo?
>   3. Que erro você já corrigiu no agente **duas vezes**?
>
> A segunda correção é o gatilho: a primeira pode ser acaso, a quinta já custou caro.

- `<modulo.funcao()>` serve **apenas** a `<contexto>`. Não use em `<outro contexto>` —
  ali a regra é `<qual>`.
- `<padrão legado>` existe em `<caminho>` por razões históricas. **Não replique** em código
  novo; use `<alternativa>`.
- <Biblioteca presente no lockfile como dependência transitiva, que não deve ser importada
  diretamente.>

## Fluxo de trabalho

- Uma spec por fatia vertical entregável. Specs em `specs/`, versionadas com o código.
- Tarefa de teste antes da tarefa de implementação.
- **Execute uma task por vez.** Ao concluir, pare e reporte — não siga para a próxima.
- **Nunca altere um teste existente para fazê-lo passar**, nem marque `skip`/`xfail`. Se o
  teste parecer errado, pare e pergunte.
- **"Pronto" exige evidência:** cole a saída do comando de teste, sem resumir.
- Todo PR referencia a spec e a task.
- Commits convencionais: `feat`/`fix`/`refactor`/`docs`/`test` com escopo.

## Sessão

- Ao iniciar: leia a spec ativa, o `tasks.md` e o `git log` recente. Resuma o estado antes de
  propor qualquer mudança.
- Antes de encerrar ou compactar: atualize o `tasks.md` e registre decisões e pendências.

## Antes de abrir PR

- [ ] Suíte verde, cobertura de regra de negócio não caiu.
- [ ] Diff lido integralmente — inclusive o que não estava no escopo.
- [ ] Nenhuma dependência nova sem justificativa no corpo do PR.
- [ ] Spec, plano e tasks no mesmo commit do código.
