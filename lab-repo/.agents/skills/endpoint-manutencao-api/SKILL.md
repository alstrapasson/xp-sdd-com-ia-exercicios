---
name: endpoint-manutencao-api
description: Cria ou altera uma rota da API de manutenção (ordens de serviço e equipamentos) no padrão do repositório, com modelo Pydantic, router, teste e registro em main.py. Use ao adicionar, alterar ou remover endpoint, rota ou recurso da API, ou ao mudar o contrato de uma rota existente (entrada, saída, códigos de erro).
---

# Endpoint da API de manutenção

Padrão do `lab-repo` (`manutencao-api`). Leia antes `AGENTS.md` e `constitution.md`.

## Quando usar

- Adicionar rota nova em `/ordens` ou `/equipamentos`, ou criar um recurso novo.
- Alterar o contrato de rota existente: campo de entrada ou saída, status HTTP.
- Remover rota, com a depreciação correspondente.

## Quando NÃO usar

- Mudança só de regra de negócio, sem mudar contrato (SLA, prioridade): isso é `app/services/`.
- Qualquer alteração em `app/services/priorizacao.py`: legado, sem testes, com regra própria
  (characterization tests antes).
- Cliente que **consome** API de terceiro.
- Documentar endpoints que já existem.
- Otimizar consulta ou mexer em `repositorio.py`.
- Migração ou carga de dados.

## Passos

1. **Spec primeiro.** Contrato público muda, então precisa de spec em `specs/<slug>.md`
   (intenção, comportamento esperado, fora de escopo, "ainda não sei"). Sem spec, pare e diga.

2. **Modelos em `app/models.py`.** Pydantic v2. Modelo de entrada e de saída separados quando
   divergem. `Field(description=...)` em campo não óbvio.

3. **Router em `app/routers/<recurso>.py`:**
   - `router = APIRouter(prefix="/<recurso>", tags=["<recurso>"])`.
   - `response_model` sempre explícito; `status_code=201` em criação.
   - Acesso a dados só por `repositorio` (`from ..repositorio import repositorio`).
   - Erro de domínio vira `HTTPException` com status explícito:
     **404** recurso inexistente · **409** estado incompatível · **422** entrada inválida
     (o 422 de formato vem do Pydantic).
   - Mensagem de erro em pt-BR, sem detalhe interno.

4. **Regra nova em `app/services/`**, testável sem HTTP. Prazo vem de `sla.calcular_prazo`;
   prioridade vem de `priorizacao.calc`. **Chame as funções, não reimplemente.**

5. **Registre o router** em `app/main.py` (`app.include_router(...)`), se for novo.

6. **Teste em `tests/`** — padrão em [`references/padrao-de-teste.md`](references/padrao-de-teste.md).
   Cubra caminho feliz, 404, 409 (se houver estado) e 422 (se houver entrada). O nome do teste
   é o critério de aceite da spec.

7. **Rode `pytest` e cole a saída**, sem resumir.

## Padrões fixos

- `datetime` sempre timezone-aware em UTC: `datetime.now(timezone.utc)`.
- Type hint completo e docstring Args/Returns em função pública nova.
- Identificadores e comentários em inglês; mensagens ao usuário em pt-BR.
- A API guarda dados em memória: reiniciar o servidor apaga o que foi criado.

## Saída esperada

Spec, modelo, router, service (se houver regra), teste e registro em `main.py`, mais a linha do
OpenAPI que mudou (`/docs`). Se existir `postman/`, a requisição correspondente na coleção.
Nunca só o router.
