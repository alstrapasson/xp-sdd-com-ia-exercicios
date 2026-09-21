# Playbooks

Entregáveis 5, 6 e 7 da proposta. Documentos de consulta permanente, entregues ao cliente.

| Documento | Entregável | Público | Quando usar |
|---|:-:|---|---|
| `governanca-e-seguranca.md` | 5 | Segurança, jurídico, liderança | Aprovação interna antes da adoção ampla |
| `protocolo-brownfield.md` | 6 | Engenharia | Toda vez que se toca legado |
| `guia-boas-praticas.md` | 7 | Engenharia | Consulta contínua |

---

## Ordem de leitura

**Para quem vai aprovar a adoção:** `governanca-e-seguranca.md`, inteiro. É o único escrito
para leitor não técnico e é o que responde às perguntas de segurança e jurídico.

**Para quem vai programar:** `guia-boas-praticas.md`, a seção 1 (as dez regras) e depois o que
a situação pedir. Não foi escrito para leitura linear — tem índice e tabela de sintomas. Quando
o agente falhar de um jeito que parece "azar", vá à seção 11: os seis modos de falha e a peça
de harness que responde a cada um.

**Para quem herdou código legado:** `protocolo-brownfield.md`, inteiro, antes de tocar em
qualquer coisa.

---

## `governanca-e-seguranca.md` — o que a Actionsys precisa preencher

O documento é um **modelo**. Ele não pode ser aprovado como está, e os campos abaixo dependem
de informação que só o cliente tem:

| Seção | O que falta | Quem responde |
|---|---|---|
| §3 | Classificação dos repositórios em A, B ou C | Segurança + Engenharia |
| §4.2 | Política de retenção e treinamento do fornecedor do modelo | Jurídico, a partir do contrato |
| §4.3 | Posição sobre propriedade do código gerado | Jurídico |
| §5.2 | Quem mantém o repositório central de skills | Engenharia |
| §8 | Nomes dos papéis | Liderança |
| §9 | Canal de resposta a incidentes | Segurança |
| §10 | Periodicidade de revisão | Engenharia |

> **§4.2 é a seção que o jurídico vai ler primeiro, e é a única que o fornecedor do
> treinamento não pode preencher.** Ela depende do contrato entre a Actionsys e o fornecedor
> do modelo. Levantar isso cedo evita que a aprovação trave no fim.

---

## Relação com o restante do material

```
guia-boas-praticas.md          ← resumo operacional de tudo
    ├── matriz de calibragem   → 04-kit-sdd/matriz-de-calibragem.md
    ├── templates              → 04-kit-sdd/templates/
    ├── protocolo de legado    → protocolo-brownfield.md
    ├── política de segurança  → governanca-e-seguranca.md
    ├── skills                 → 05-skills/
    ├── harness (teoria)       → runbook.md, Parte XI
    └── autoavaliação          → 02-avaliacao/rubrica-competencias.md
```
