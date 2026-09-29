# AGENTS.md — manutencao-api

API de ordens de serviço de manutenção industrial: equipamentos, prazo de atendimento (SLA)
e fila priorizada. Princípios inegociáveis em [`constitution.md`](constitution.md).

---

## Como rodar

```bash
# instalar
pip install -e ".[dev]"

# testar
pytest

# subir localmente (docs interativas em /docs)
uvicorn app.main:app --reload

# lint e tipos: ainda não configurados neste repositório
```

## Convenções

- **Tipagem:** função pública de módulo novo com type hint e docstring Args/Returns.
- **Nomenclatura:** módulo novo com identificadores e comentários em inglês; documentação em pt-BR.
- **Estrutura:** rota em `app/routers/`, regra de negócio em `app/services/`, modelo em
  `app/models.py`, teste em `tests/`.
- **Prazo:** vem de `app/services/sla.py`. Nunca calcule prazo dentro do router.
- **Erros:** `HTTPException` com 404, 409 ou 422.
- **Datas:** UTC, timezone-aware. Conversão local só na apresentação.
- **Persistência:** em memória (`app/repositorio.py`). Reiniciar o servidor apaga toda ordem criada
  depois da carga inicial, e o `--reload` reinicia a cada arquivo alterado.

## Sensível

- `app/services/priorizacao.py` — legado sem testes, em uso por `POST` e `GET /ordens`. Não altere
  sem characterization tests antes e revisão humana.
- Nenhum segredo entra em contexto: `.env` e credenciais ficam fora do alcance do agente.

## NÃO se aplica

- `priorizacao.calc()` e `ordenar()` são legado. **Não copie** o estilo deles (nomes de uma
  letra, números mágicos, sem tipagem) em código novo. O padrão a seguir é o de `sla.py`.
- Prazo **não** é em dias úteis: `sla.calcular_prazo()` trabalha em horas corridas. Não desconte
  fim de semana nem feriado.
- `repositorio.py` é armazenamento em memória para o laboratório. **Não** o trate como modelo de
  persistência e não adicione ORM nem banco.
- A regra de reaberturas já vive em `priorizacao.calc()`. **Não** a reimplemente no router: chame
  a função.

## Fluxo de trabalho

- Uma spec por fatia entregável, em `specs/`, versionada com o código.
- Teste antes da implementação.
- **Execute uma task por vez.** Ao concluir, pare e reporte.
- **Nunca altere um teste existente para fazê-lo passar**, nem marque `skip`/`xfail`. Se o teste
  parecer errado, pare e pergunte.
- "Pronto" exige evidência: cole a saída do `pytest`, sem resumir.
- Commits convencionais: `feat`/`fix`/`refactor`/`docs`/`test`, com escopo.

## Sessão

- Ao iniciar: leia a spec ativa, o `tasks.md` e o `git log` recente. Resuma o estado antes de
  propor qualquer mudança.
- Antes de encerrar ou compactar: atualize o `tasks.md` e registre decisões e pendências.

## Antes de abrir PR

- [ ] `pytest` verde.
- [ ] Diff lido integralmente, inclusive o que não estava no escopo.
- [ ] Nenhuma dependência nova sem justificativa no corpo do PR.
- [ ] Spec e código no mesmo commit.
