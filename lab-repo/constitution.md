# Constitution — manutencao-api

**Versão:** 1.0 · **Última revisão:** 29/09/2026 (UTC) · **Aprovada por:** André Strapasson

Princípios inegociáveis deste repositório. Nenhuma spec, plano ou geração de código pode
violá-los. Alterações exigem acordo do time, não decisão individual nem de agente.

---

## 1. Stack e dependências

- Python **3.11+**, FastAPI e Pydantic **v2**. Versões mínimas declaradas em `pyproject.toml`.
- Dependência nova exige justificativa no PR: por que não dá com o que já existe.
- Nenhum segredo em código, em teste ou em arquivo versionado. Credencial vem de variável de ambiente.

## 2. Tipagem e documentação

- Toda função pública de módulo novo tem type hint completo e docstring com **Args** e **Returns**.
- Identificadores e comentários de módulo novo em **inglês**. O legado permanece como está.

## 3. Testes

- Regra de negócio nova entra **com teste, na mesma alteração**.
- Teste existente nunca é alterado, pulado (`skip`/`xfail`) ou removido para fazê-lo passar.
- A suíte (`pytest`) passa inteira antes do merge.

## 4. Erros

- Erro de domínio vira `HTTPException` com status explícito: **404** (não existe), **409**
  (estado incompatível) ou **422** (entrada inválida).
- Nunca `except:` nem `except Exception:` sem re-raise ou tratamento específico.

## 5. Datas

- Todo `datetime` é **timezone-aware, em UTC**.
- Conversão para horário local só na apresentação.

## 6. Prazo de atendimento (SLA)

- O prazo é calculado em **horas corridas**, conforme a norma MAN-014 rev. 3, em `app/services/sla.py`.
- Nunca em dias úteis: não desconta fim de semana nem feriado.

## 7. Código legado

- `app/services/priorizacao.py` só é alterado **depois** de characterization tests que fixam o
  comportamento atual.
- Refatoração e mudança de regra vão em commits separados.

## 8. Revisão

- Todo diff é lido integralmente por um humano antes do merge, inclusive o que não estava no
  escopo da spec.
- O agente não aprova o próprio diff.

---

## O que NÃO está aqui, e por quê

- Decisão que vale para uma fatia só: isso é spec (`specs/`).
- Estilo de formatação: quando houver formatador configurado, ele decide, não este arquivo.
- Regra que ninguém vai fazer cumprir.

---

## Histórico

| Versão | Data (UTC) | Mudança | Quem |
|---|---|---|---|
| 1.0 | 2026-09-29 | Versão inicial (Laboratório 2, Dia 2) | André Strapasson |
