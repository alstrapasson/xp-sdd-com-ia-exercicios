<!--
TEMPLATE — constitution.md
Capacitação XP + SDD com IA (Codex) · Strapa Tecnologia

Como usar:
  1. Copie para a raiz do repositório (ou .specify/memory/, se usar Spec Kit).
  2. Preencha entre 5 e 8 princípios. Não mais.
  3. Apague o que não se aplica. Princípio herdado de template não é lei — é enfeite.
  4. Apague estes comentários.

A REGRA DE OURO, e ela é única:
  Um princípio que o agente não consegue verificar não é princípio — é desejo.
  Antes de manter uma linha, pergunte: "um agente sozinho consegue dizer se isso foi
  cumprido?" Se a resposta for não, reescreva ou risque.
-->

# Constitution — <NOME DO PROJETO>

**Versão:** 1.0 · **Última revisão:** __/__/____ · **Aprovada por:** ____________

Estes são os princípios inegociáveis deste repositório. Nenhuma spec, plano ou geração de
código pode violá-los. Alterações aqui exigem acordo do time — não decisão individual e não
decisão de agente.

---

## 1. Stack e versões

- Linguagem: **<Python 3.11+>**. Não introduzir código em outra linguagem sem decisão registrada.
- Framework: **<FastAPI>**. Dependências principais: **<listar>**.
- Gerenciador de pacotes: **<uv / pip>**. Lockfile versionado e obrigatório.

## 2. Tipagem e documentação

- Toda função pública tem type hint completo em parâmetros e retorno.
- Toda função pública tem docstring com **Args** e **Returns**; **Raises** quando levanta exceção.
- Identificadores e comentários em **inglês**. Documentação voltada ao usuário em **pt-BR**.

## 3. Testes

- Regra de negócio nova entra **com teste, na mesma alteração**. Não em PR seguinte.
- O nome do teste corresponde ao critério de aceite que ele verifica.
- Cobertura de `<services/ | domain/>` não cai em relação à branch principal.
- Teste não depende de relógio, rede ou ordem de execução. Instante de referência é sempre
  injetado, nunca `datetime.now()` dentro do teste.

## 4. Erros

- Erro de domínio vira exceção tipada e é traduzido na borda para **<HTTPException com status explícito>**.
- Nunca `except:` nem `except Exception:` sem re-raise ou tratamento específico.
- Mensagem de erro não vaza detalhe interno (stack, query, caminho de arquivo) para o cliente.

## 5. Dados e tempo

- Todo instante é timezone-aware, armazenado e trafegado em **UTC**.
- Conversão para horário local acontece **só na borda de apresentação**.
- Valor monetário é `Decimal`, nunca `float`. Arredondamento explícito, uma única vez, no fim.

## 6. Segredos e credenciais

- Nenhum segredo em código, em teste ou em arquivo versionado.
- Credencial vem de variável de ambiente ou cofre. `.env` está no `.gitignore` e nunca entra
  em contexto de agente.
- Credencial usada por agente tem escopo próprio, mínimo e revogável.

## 7. Dependências

- Dependência nova exige justificativa explícita no PR: por que não dá com o que já existe.
- Toda dependência nova é revisada por humano antes do merge: mantenedor, última publicação,
  licença, tamanho da árvore transitiva.
- Versão fixada. Nunca `latest`.

## 8. Revisão

- Todo diff é lido integralmente por um humano antes do merge — inclusive, e principalmente,
  o que não estava no escopo da spec.
- Agente não aprova o próprio diff.
- `<Área sensível: listar diretórios que exigem revisão de pessoa específica>`.

---

## O que NÃO está aqui, e por quê

Esta constitution **não** contém:

- Decisão que vale para uma fatia só — isso é spec.
- Preferência de estilo que o formatador já resolve (`<black> / <ruff>` decide, não este arquivo).
- Regra que ninguém vai fazer cumprir. **Princípio não cumprido corrói a autoridade dos outros.**

---

## Histórico

| Versão | Data | Mudança | Quem |
|---|---|---|---|
| 1.0 | __/__/____ | Versão inicial | |
