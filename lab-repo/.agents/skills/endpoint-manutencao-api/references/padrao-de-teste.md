# Padrão de teste de endpoint — manutencao-api

Fixture em `tests/test_ordens.py`. Reutilize o mesmo desenho:

```python
@pytest.fixture
def cliente():
    repositorio.equipamentos.clear()
    repositorio.ordens.clear()
    carregar_dados_iniciais()
    with TestClient(app) as c:
        yield c
```

- O `with TestClient(app)` é obrigatório: sem ele o `lifespan` não roda.
- Limpar `repositorio` antes de cada teste evita dependência de ordem de execução.
- Dados iniciais: equipamentos `EQ-1` (criticidade A), `EQ-2` (B), `EQ-3` (C) e três ordens.

## O que cobrir

| Caso | Status | Exemplo existente |
|---|:-:|---|
| Caminho feliz | 200/201 | `test_abrir_ordem_calcula_prazo_e_prioridade` |
| Recurso inexistente | 404 | `test_abrir_ordem_para_equipamento_inexistente_retorna_404` |
| Estado incompatível | 409 | `test_reabrir_ordem_nao_concluida_retorna_409` |
| Entrada inválida | 422 | `test_descricao_curta_e_rejeitada` |

## Armadilhas

- Para criar ordem já concluída, abra a ordem e use `PATCH /ordens/{id}/status`: não monte o
  objeto à mão.
- Teste não depende do relógio: compare prazo novo com prazo antigo, não com `datetime.now()`.
- Ao final do 409, confira que a ordem **não mudou**.
