# Laboratório 2 — Constitution, AGENTS.md e perfis

**Dia 2 · 30 min · em pares, no repositório REAL**

> Use o repositório que você vai levar para a mentoria. Se não trouxe, use o `lab-repo` — mas
> avise o instrutor, porque isso muda o que dá para fazer na Sessão 1.

---

## Objetivo

Sair com três artefatos funcionando no seu repositório: `constitution.md`, `AGENTS.md` com
contexto negativo, e perfis de `config.toml`.

---

## Parte 1 — `constitution.md` (10 min)

Gere o esqueleto:

```bash
codex
$speckit-constitution
```

Se o Spec Kit ainda não estiver instalado, escreva à mão — o conteúdo importa mais que a
ferramenta.

**Escreva de 5 a 8 princípios.** Não mais. Constitution longa não é lida nem cumprida.

### O teste de cada princípio

Para cada linha, responda: **um agente consegue verificar isso sozinho?**

| Se você escreveu | Reescreva como |
|---|---|
| "Código de qualidade" | "Toda função pública tem type hint e docstring com Args/Returns" |
| "Ter testes" | "Regra de negócio nova entra com teste na mesma alteração" |
| "Ser seguro" | "Nenhum segredo em código. Credencial vem de variável de ambiente" |
| "Boa performance" | "Endpoint de listagem é paginado, limite padrão 50, máximo 200" |

**Risque o que não passar no teste.** É melhor ter 5 princípios verificáveis que 12 desejos.

Cubra pelo menos: stack e versão · padrão de erro · política de teste · política de
dependência · o que exige revisão humana.

---

## Parte 2 — `AGENTS.md` (12 min)

Na raiz do repositório. Quatro seções — a quarta é a que quase ninguém escreve:

```markdown
# AGENTS.md

## Como rodar
Comandos exatos: instalar, testar, lint, subir. Copiáveis, sem "veja o README".

## Convenções
Tipagem, nomenclatura, estrutura, tratamento de erro, formato de data.

## Sensível
O que exige revisão humana. Onde não mexer sem falar com alguém.

## NÃO se aplica          <-- a seção que paga o laboratório
Funções, módulos e padrões que existem no repositório e que o agente NÃO deve
usar por inferência — dizendo o que usar no lugar.

## Sessão                 <-- harness contra a amnésia entre sessões (copie)
- Ao iniciar: leia a spec ativa, o tasks.md e o git log recente. Resuma o estado
  antes de propor qualquer mudança.
- Antes de encerrar ou compactar: atualize o tasks.md e registre decisões e pendências.
```

A seção **Sessão** não precisa ser adaptada: copie como está. Ela resolve o problema 3 dos
seis vistos no Dia 1 — o agente não esquece entre sessões, ele nunca soube.

### Como preencher "NÃO se aplica"

Três perguntas que produzem o conteúdo:

1. Que função existe aqui que **parece** genérica mas serve a um caso só?
   *(no `lab-repo`: `dias_uteis_entre()` serve a faturamento, não a SLA)*
2. Que padrão antigo ainda está no código e **não** deve ser copiado em código novo?
3. Que erro você já corrigiu no agente **duas vezes**?

> A segunda correção é o gatilho. A primeira pode ser acaso; a quinta já custou caro.

**Regra de tamanho:** se o `AGENTS.md` está repetindo o README, corte. Ele instrui quem já vai
contribuir — não apresenta o projeto.

### Se o repositório tem uma área com regra diferente

Crie um `AGENTS.md` de subdiretório. É o mecanismo mais subutilizado e resolve o caso mais
comum: pasta de legado, código gerado, ou área sensível.

---

## Parte 3 — perfis (6 min)

Em `~/.codex/config.toml`:

```toml
model = "gpt-5-codex"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[profiles.exploracao]
sandbox_mode = "read-only"
approval_policy = "never"
model_reasoning_effort = "low"

[profiles.implementacao]
sandbox_mode = "workspace-write"
approval_policy = "on-request"
model_reasoning_effort = "medium"

[profiles.revisao]
sandbox_mode = "read-only"
approval_policy = "on-request"
model_reasoning_effort = "high"
```

Teste:

```bash
codex --profile exploracao
```

**Para cada perfil, escreva uma frase justificando o sandbox escolhido.** Se você não
consegue justificar, você copiou — e no seu repositório o valor certo pode ser outro.

Lembre: **sandbox** é o estrago que você aceita; **aprovação** é a interrupção que você
aguenta. Nunca resolva incômodo de aprovação afrouxando o sandbox.

---

## Parte 4 — revisão cruzada (5 min)

Troque com o par. No material do outro, encontre:

- [ ] **Um** princípio que o agente não consegue verificar.
- [ ] **Uma** coisa no `AGENTS.md` que é só cópia do README.
- [ ] **Uma** coisa que falta na seção "NÃO se aplica".

Devolva os três apontamentos. Anote os que você recebeu.

---

## Entrega

Commit no seu repositório:

```bash
git add constitution.md AGENTS.md
git commit -m "docs: adiciona constitution e contexto de agente"
```

Guarde também o `config.toml` — ele é auditado na Sessão 1 da mentoria.

---

## Critério de pronto

- [ ] Todo princípio da constitution é verificável.
- [ ] `AGENTS.md` tem comandos copiáveis, não referências.
- [ ] "NÃO se aplica" tem ao menos duas entradas reais — ao menos uma delas um padrão legado
      que não deve ser replicado.
- [ ] Seção "Sessão" presente.
- [ ] Três perfis funcionando, cada um com justificativa escrita do sandbox.
- [ ] Apontamentos do par anotados.
