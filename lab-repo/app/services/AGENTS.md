# app/services/AGENTS.md — regras desta pasta

Refinam o [`AGENTS.md`](../../AGENTS.md) da raiz. Aqui convivem dois regimes.

## `sla.py` — referência

Documentado e testado (`tests/test_sla.py`). Serviço novo copia este padrão: tipagem completa,
docstring, regra explícita em tabela e teste ao lado.

## `priorizacao.py` — LEGADO, não segue o padrão

- Não tem testes, e isso é deliberado. **Não** "limpe" o arquivo só porque passou por perto.
- Antes de qualquer mudança: gerar characterization tests que fixam a saída atual.
- Refatoração e mudança de regra vão em commits separados.
- Regra sem justificativa conhecida (ver o `TODO` no topo do arquivo): pergunte, não presuma.
