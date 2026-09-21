# API de Manutenção — repositório de laboratório

Repositório usado nos cinco dias do treinamento **XP + SDD com IA (Codex)**.

É uma API de ordens de serviço de manutenção industrial: equipamentos com criticidade,
ordens corretivas/preventivas/preditivas, prazo de atendimento (SLA) e priorização de fila.

Pequeno o bastante para ser lido em 10 minutos, e realista o bastante para ter os problemas
que interessam ao curso — inclusive um módulo legado que ninguém quer tocar.

---

## Como rodar

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -e ".[dev]"

uvicorn app.main:app --reload    # API em http://127.0.0.1:8000
pytest                            # 12 testes
```

Documentação interativa em `http://127.0.0.1:8000/docs`.

> Se aparecer `StarletteDeprecationWarning` sobre `httpx`, ignore: é um aviso da versão do
> TestClient instalada, não afeta os laboratórios.

---

## Estrutura

```
app/
├── models.py                 Modelos Pydantic e enums do domínio
├── repositorio.py            Persistência em memória + dados de laboratório
├── routers/
│   ├── equipamentos.py       GET /equipamentos
│   └── ordens.py             POST /ordens, GET /ordens, PATCH /ordens/{id}/status
└── services/
    ├── sla.py                Prazo de atendimento — documentado e testado
    └── priorizacao.py        Cálculo de prioridade — LEGADO, ver abaixo
tests/
├── test_sla.py               4 testes
└── test_ordens.py            8 testes
```

### Sobre `app/services/priorizacao.py`

**Este módulo não tem testes, e isso é deliberado.**

Ele foi escrito para se parecer com o que existe de verdade em base legada: migrado de um
sistema antigo, nomes de uma letra, números mágicos, um `TODO` de alguém que não trabalha
mais aqui, um comentário dizendo para não mexer sem falar com uma pessoa, e regras de
negócio que ninguém sabe mais justificar.

Ele **funciona** e está em uso: `POST /ordens` e `GET /ordens` dependem dele.

É o alvo do laboratório do Dia 5 e do protocolo de brownfield da mentoria. Não o corrija
antes — a ordem do trabalho é justamente o conteúdo daquele dia.

---

## O que cada dia faz aqui

| Dia | Laboratório | Toca em |
|---|---|---|
| 1 | Primeiro ciclo com intenção explícita | `routers/ordens.py` |
| 2 | Escrever `constitution.md`, `AGENTS.md` e perfis | raiz do repositório |
| 3 | Construir um skill de domínio + auditar permissões | `.agents/skills/` |
| 4 | Ciclo Spec Kit completo em uma história real | `specs/`, `app/` |
| 5 | Brownfield sobre `priorizacao.py` | `services/priorizacao.py` |

Cada dia parte do estado deixado pelo anterior. Se você perder um dia, use a branch de
recuperação correspondente (`dia-N-inicio`) — ou peça ao instrutor.

---

## Regras de negócio conhecidas

Documentadas aqui porque **não** estão todas no código — parte do exercício é descobrir isso.

**SLA** (`services/sla.py`, norma interna MAN-014 rev. 3) — prazo em horas:

| Criticidade | Corretiva | Preventiva | Preditiva |
|:-:|:-:|:-:|:-:|
| A (para linha) | 4 | 168 | 336 |
| B (degrada capacidade) | 24 | 336 | 720 |
| C (sem impacto imediato) | 72 | 720 | 1440 |

O prazo é corrido: não desconta fim de semana nem feriado.

**Priorização** (`services/priorizacao.py`): 1 é a prioridade máxima, 5 a mínima. A regra
completa não está documentada em lugar nenhum — está só no código. Reconstruí-la é o
exercício do Dia 5.

---

## Convenções

- Python 3.11+, tipagem em toda assinatura pública.
- Identificadores e comentários em inglês nos módulos novos; o legado permanece como está.
- Datas sempre timezone-aware em UTC. Conversão para horário local só na borda de apresentação.
- Sem dependência nova sem justificativa no PR.
