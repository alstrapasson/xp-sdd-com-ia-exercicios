# Laboratório 3 — Skill de domínio com eval

**Dia 3 · 27 min · individual**

Use a **tarefa repetitiva** que você trouxe do Dia 2 — aquela que você explica ao agente
toda semana. Se não trouxe, use uma da lista no fim deste arquivo.

---

## Objetivo

Um skill que aciona sozinho nos casos certos, com eval que prova isso — incluindo os casos em
que ele **não** deve acionar.

---

## Parte 1 — o skill (12 min)

```bash
mkdir -p .agents/skills/<nome-do-skill>
```

`SKILL.md`:

```markdown
---
name: <nome-em-kebab-case>
description: <o que faz>. Use quando <situação>, <sinônimo>, <sigla>.
---

# <Nome>

## Quando usar
Casos concretos.

## Quando NÃO usar
Os casos vizinhos em que ele não se aplica. Esta seção reduz falso acionamento.

## Passos
1. ...
2. ...

## Saída esperada
Formato do resultado.
```

### A descrição é o produto

O corpo diz o que ele faz. A descrição decide **se ele será usado**. Skill excelente com
descrição ruim nunca dispara — e você não descobre, porque não dá erro.

Fórmula: **o que faz** + **quando usar**, com as palavras que a pessoa realmente digita.

| Ruim | Boa |
|---|---|
| "Ajuda com relatórios" | "Gera relatório pós-incidente no padrão da engenharia. Use quando o usuário mencionar postmortem, RCA ou análise de causa raiz" |
| "Skill de migration" | "Cria migration Alembic seguindo o padrão do projeto. Use ao adicionar, alterar ou remover tabela ou coluna" |

### Progressive disclosure

Se o `SKILL.md` passar de ~200 linhas, mova detalhe para `references/` e referencie de dentro
do corpo. Só `name` e `description` ficam sempre em contexto — é isso que permite ter muitos
skills sem penalidade. Enfiar tudo no `SKILL.md` "para facilitar" quebra o mecanismo.

---

## Parte 2 — o eval (10 min)

Crie `.agents/skills/<nome>/EVAL.md`:

```markdown
# Eval de acionamento — <nome>

| # | Prompt | Deve acionar? | Acionou? | OK? |
|---|---|:-:|:-:|:-:|
| 1 | <caso típico>                  | Sim | | |
| 2 | <mesma coisa, outras palavras> | Sim | | |
| 3 | <com a sigla do domínio>       | Sim | | |
| 4 | <tarefa VIZINHA, mas outra>    | **Não** | | |
| 5 | <mesmo substantivo, outro fim> | **Não** | | |
| 6 | <tarefa genérica do dia a dia> | **Não** | | |

Executado em: ____  ·  Versão do skill: ____
```

**Mínimo: 3 positivos e 3 negativos.** Os negativos são os que importam — positivos quase
sempre passam.

### Como rodar

Para cada linha:

1. **Sessão nova** (`codex`, contexto limpo). Contexto sujo invalida o teste.
2. Cole o prompt exato.
3. Observe se o skill acionou.
4. Preencha a tabela.

Se um negativo acionar, sua descrição está genérica demais: restrinja e adicione "Quando NÃO
usar". Se um positivo não acionar, faltam termos que a pessoa realmente usa.

**Rode de novo até a tabela fechar.** É esse ciclo que é o laboratório.

---

## Parte 3 — auditoria de permissões (5 min)

Sobre a sua configuração real:

```bash
cat ~/.codex/config.toml
```

- [ ] Qual `sandbox_mode` está ativo **por padrão**?
- [ ] Existe algum `danger-full-access` em algum perfil? Por quê?
- [ ] Qual `approval_policy` padrão?
- [ ] Que servidores MCP estão configurados? Você instalou todos conscientemente?
- [ ] Alguma credencial em variável de ambiente com escopo maior que o necessário?

Para cada skill ou servidor MCP de terceiro instalado:

- [ ] Você leu o `SKILL.md` inteiro, incluindo `scripts/`?
- [ ] Está fixado em versão, ou segue `latest`?
- [ ] Sabe quem mantém?

> Se alguma resposta for "não sei", isso não é falha pessoal — é o estado normal de quem
> nunca auditou. Anote e leve para a Sessão 1 da mentoria.

---

## Entrega

```
.agents/skills/<nome>/
├── SKILL.md
├── EVAL.md      (preenchido, com os negativos passando)
└── references/  (se aplicável)
```

Mais as respostas da auditoria.

---

## Critério de pronto

- [ ] A descrição diz o que faz **e** quando usar.
- [ ] Eval com 3+ positivos e 3+ negativos, todos conferidos.
- [ ] Nenhum negativo acionando.
- [ ] `SKILL.md` abaixo de 200 linhas, ou usando `references/`.
- [ ] Auditoria respondida, inclusive os "não sei".

---

## Se você não trouxe uma tarefa

- Gerar migration seguindo o padrão do projeto.
- Escrever relatório pós-incidente.
- Revisar PR contra a constitution do repositório.
- Gerar characterization tests de um módulo (prepara o Dia 5).
- Criar endpoint FastAPI no padrão do `lab-repo`: router, modelo, teste, OpenAPI.
