# Auditoria de permissões — Laboratório 3 (Dia 3)

**Data:** 2026-10-01 (UTC) · **Escopo:** `~/.codex/config.toml` e arquivos de perfil em `~/.codex/`.
Só leitura: nada foi alterado. Respostas "não sei" são o resultado esperado da primeira auditoria
e vão para a Sessão 1 da mentoria.

## Configuração

| Pergunta | Resposta |
|---|---|
| `sandbox_mode` padrão | **Não definido** no `config.toml`, então vale o padrão do Codex. **Não sei** qual é o valor efetivo na minha versão. (`[windows] sandbox = "elevated"` escolhe o mecanismo de sandbox do Windows, não o modo.) |
| `danger-full-access` em algum perfil? | **Não.** Os três perfis (`exploracao`, `implementacao`, `revisao`) usam `read-only` ou `workspace-write`. |
| `approval_policy` padrão | **Não definido** no `config.toml` (vale o padrão do Codex). Cada perfil define o seu: `never`, `on-request`, `on-request`. |
| Perfis | `exploracao` (read-only, never, low), `implementacao` (workspace-write, on-request, medium), `revisao` (read-only, on-request, high). |
| Esforço padrão | `model_reasoning_effort = "low"` global. |

## Servidores MCP

| Servidor | Origem | Instalado conscientemente? | Versão fixada? | Quem mantém |
|---|---|:-:|:-:|---|
| `context7` | Remoto (`https://mcp.context7.com/mcp`), sem chave de API | Sim | Não se aplica: é servidor remoto, a versão é do mantenedor | Upstash |
| `node_repl` | Executável local, instalado junto com o app do Codex | **Não sei** | Segue a versão do app | OpenAI (bundled) |

## Plugins habilitados

`browser`, `unified-computer-use`, `visualize`, `computer-use`, `documents`, `pdf`,
`spreadsheets`, `presentations`, `template-creator`. Todos de marketplaces locais da OpenAI
(`openai-bundled`, `openai-primary-runtime`).

- **Não sei** exatamente o que `computer-use` e `unified-computer-use` podem fazer na minha
  máquina nem em que escopo. São os de maior superfície e merecem leitura.

## Credenciais e skills

| Pergunta | Resposta |
|---|---|
| Credencial em variável de ambiente com escopo maior que o necessário? | No ambiente em que a auditoria rodou só apareceu `CLAUDE_CODE_MESSAGING_TOKEN`, do Claude Code, não do Codex. **Não verifiquei** as variáveis do Windows nem de outros terminais. |
| Skills de terceiros instalados | Nenhum em `~/.agents/skills` nem `~/.codex/skills`. O único skill do repositório é `endpoint-manutencao-api`, escrito neste laboratório. |
| `SKILL.md` lido por inteiro, incluindo `scripts/`? | Sim para o skill do repositório (sem `scripts/`). Skills dos plugins bundled: **não li**. |

## Ações

- [ ] Ler as permissões dos plugins `computer-use` e `unified-computer-use`.
- [ ] Descobrir o `sandbox_mode` e o `approval_policy` efetivos (`/status` numa sessão sem perfil).
- [ ] Verificar as variáveis de ambiente de usuário do Windows em busca de credenciais.
- [ ] Confirmar que `context7` não recebe dado sensível: tratar a resposta como conteúdo externo.
