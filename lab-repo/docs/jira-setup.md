# Integração com o Jira — passo a passo

**Site:** `alstrapasson.atlassian.net` · **Projeto:** KAN · **Board:** https://alstrapasson.atlassian.net/jira/software/projects/KAN/boards/1

## O que existe

| Peça | Onde | Função |
|---|---|---|
| Servidor MCP `atlassian` | `.codex/config.toml` | Acesso ao Jira, com allowlist e aprovação nas escritas |
| Skill `jira-historia-para-spec` | `.agents/skills/` | Lê `KAN-n` e gera `specs/KAN-n.md` |
| Skill `jira-atualizar-task` | `.agents/skills/` | Comenta o andamento e move o status a partir de `specs/KAN-n.tasks.md` |
| Regras | `AGENTS.md`, seção "Integração com o Jira" | Limites que valem para qualquer sessão |

## 1. Login (uma vez, por você)

```powershell
cd C:\projects\codex-exercicios\lab-repo
codex mcp login atlassian
codex mcp list      # a linha "atlassian" deve mostrar Auth = OAuth
```

O login abre o navegador (OAuth 2.1). Nenhum token é gravado em arquivo do repositório. Autorize
**somente** o site `alstrapasson.atlassian.net`.

## 2. Conferir as ferramentas expostas

Numa sessão do Codex neste diretório, rode `/mcp` e confira que aparecem exatamente:

```
getAccessibleAtlassianResources, getJiraIssue, searchJiraIssuesUsingJql,
getTransitionsForJiraIssue, addCommentToJiraIssue, transitionJiraIssue
```

- A allowlist **falha fechada**: nome que não existir na versão do servidor não aparece. Se alguma
  ferramenta faltar, ajuste `enabled_tools` ao nome real, sem remover a allowlist.
- O servidor usa `?tools=all` para expor as ferramentas individuais. Se o endereço mudar, a
  documentação da Atlassian é a fonte (`https://mcp.atlassian.com/v2/mcp`).

## 3. Primeiro teste, só leitura

```powershell
codex --profile exploracao
```

> puxa a história KAN-1 e monta a spec

Esperado: `specs/KAN-1.md` no template, com "Perguntas abertas". No perfil `exploracao` (read-only)
o agente lê o ticket mas **não consegue gravar** o arquivo; para gravar, use `implementacao`.

## 4. Atualizar o andamento

Depois de concluir tasks, em `implementacao`:

> atualiza o KAN-1 no Jira com o andamento das tasks

O agente mostra o comentário e a transição propostos e **espera a sua aprovação** a cada escrita.

## Limites desta configuração

- **O OAuth concede o que a sua conta pode fazer no site**, não só o projeto KAN. A restrição ao KAN
  está nos skills e no `AGENTS.md` (texto), e a allowlist limita as ferramentas, não os projetos.
  Para restringir de fato, use uma conta ou grupo da Atlassian com acesso só ao KAN.
- A transição usa o **nome** devolvido por `getTransitionsForJiraIssue`. Os nomes dependem do
  workflow do projeto e não foram conferidos aqui.
- Os evals de **segurança** dos dois skills exigem o login feito e ainda não foram executados.
