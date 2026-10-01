# Endpoints da API de Manutenção

Referência dos endpoints disponíveis na versão `0.3.0`.

- URL local: `http://127.0.0.1:8000`
- Formato de entrada e saída: JSON
- Autenticação: não exigida
- Swagger UI: `GET /docs`
- OpenAPI: `GET /openapi.json`

## Visão geral

| Método | Caminho | Descrição | Sucesso |
|---|---|---|---:|
| `GET` | `/saude` | Verifica a disponibilidade da API | `200` |
| `GET` | `/equipamentos` | Lista os equipamentos | `200` |
| `GET` | `/equipamentos/{equipamento_id}` | Consulta um equipamento | `200` |
| `POST` | `/ordens` | Abre uma ordem de serviço | `201` |
| `GET` | `/ordens` | Lista as ordens por prioridade | `200` |
| `GET` | `/ordens/{ordem_id}` | Consulta uma ordem | `200` |
| `PATCH` | `/ordens/{ordem_id}/status` | Altera o status de uma ordem | `200` |
| `POST` | `/ordens/{ordem_id}/reabrir` | Reabre uma ordem concluída | `200` |

## Valores aceitos

| Campo | Valores |
|---|---|
| `criticidade` | `A`, `B`, `C` |
| `tipo` | `corretiva`, `preventiva`, `preditiva` |
| `status` | `aberta`, `em_execucao`, `aguardando_peca`, `concluida`, `cancelada` |

Datas são retornadas no formato ISO 8601 e em UTC. A prioridade é calculada pela API, de `1`
(máxima) a `5` (mínima).

## Saúde

### `GET /saude`

Verifica se a aplicação está respondendo.

Resposta `200`:

```json
{
  "status": "ok"
}
```

## Equipamentos

### `GET /equipamentos`

Retorna todos os equipamentos cadastrados.

Resposta `200`:

```json
[
  {
    "id": "EQ-1",
    "tag": "BC-201",
    "setor": "Linha 1",
    "criticidade": "A",
    "horas_operacao": 18400
  }
]
```

### `GET /equipamentos/{equipamento_id}`

Retorna um equipamento pelo identificador.

Exemplo:

```http
GET /equipamentos/EQ-1
```

Resposta `200`:

```json
{
  "id": "EQ-1",
  "tag": "BC-201",
  "setor": "Linha 1",
  "criticidade": "A",
  "horas_operacao": 18400
}
```

Resposta `404` quando o equipamento não existe:

```json
{
  "detail": "Equipamento não encontrado"
}
```

## Ordens de serviço

### `POST /ordens`

Abre uma ordem. O identificador, o status inicial, o prazo e a prioridade são definidos pela
API. A descrição deve ter pelo menos 10 caracteres.

Corpo:

```json
{
  "equipamento_id": "EQ-1",
  "tipo": "corretiva",
  "descricao": "Ruído anormal no mancal do lado acoplado"
}
```

Resposta `201`:

```json
{
  "id": "OS-00004",
  "equipamento_id": "EQ-1",
  "tipo": "corretiva",
  "status": "aberta",
  "descricao": "Ruído anormal no mancal do lado acoplado",
  "aberta_em": "2026-10-01T18:00:00Z",
  "prazo": "2026-10-01T22:00:00Z",
  "concluida_em": null,
  "prioridade": 1,
  "reaberturas": 0
}
```

Erros:

- `404`: equipamento não encontrado.
- `422`: corpo inválido, campo obrigatório ausente, enum inválido ou descrição curta.

### `GET /ordens`

Lista as ordens, ordenadas pela regra de prioridade da aplicação. Aceita os filtros opcionais
abaixo, que podem ser combinados:

| Query parameter | Tipo | Exemplo |
|---|---|---|
| `status` | enum de status | `/ordens?status=aberta` |
| `equipamento_id` | string | `/ordens?equipamento_id=EQ-1` |

Exemplo com os dois filtros:

```http
GET /ordens?status=aberta&equipamento_id=EQ-1
```

Resposta `200`: array de ordens, que pode estar vazio.

```json
[
  {
    "id": "OS-00004",
    "equipamento_id": "EQ-1",
    "tipo": "corretiva",
    "status": "aberta",
    "descricao": "Ruído anormal no mancal do lado acoplado",
    "aberta_em": "2026-10-01T18:00:00Z",
    "prazo": "2026-10-01T22:00:00Z",
    "concluida_em": null,
    "prioridade": 1,
    "reaberturas": 0
  }
]
```

Um `status` fora dos valores aceitos retorna `422`.

### `GET /ordens/{ordem_id}`

Retorna uma ordem pelo identificador.

Exemplo:

```http
GET /ordens/OS-00001
```

Resposta `200`: uma ordem no mesmo formato apresentado acima.

Resposta `404`:

```json
{
  "detail": "Ordem não encontrada"
}
```

### `PATCH /ordens/{ordem_id}/status`

Altera o status de uma ordem.

Corpo:

```json
{
  "status": "concluida"
}
```

Resposta `200`: a ordem atualizada. Ao receber `concluida`, a API preenche `concluida_em`
com o instante atual em UTC.

Erros:

- `404`: ordem não encontrada.
- `409`: uma ordem cancelada não pode mudar de status.
- `422`: corpo ausente ou status inválido.

### `POST /ordens/{ordem_id}/reabrir`

Reabre uma ordem concluída. A operação não recebe corpo e:

- altera o status para `aberta`;
- incrementa `reaberturas`;
- limpa `concluida_em`;
- recalcula o prazo a partir do instante da reabertura;
- recalcula a prioridade;
- preserva a data original em `aberta_em`.

Exemplo:

```http
POST /ordens/OS-00004/reabrir
```

Resposta `200`: a ordem atualizada.

Erros:

- `404`: ordem não encontrada (ou equipamento associado não encontrado).
- `409`: a ordem não está concluída; isso inclui ordens abertas, em execução, aguardando peça
  ou canceladas.

## Modelo de ordem

| Campo | Tipo | Observação |
|---|---|---|
| `id` | string | Gerado no formato `OS-00001` |
| `equipamento_id` | string | Referência ao equipamento |
| `tipo` | enum | Tipo de manutenção |
| `status` | enum | Começa como `aberta` |
| `descricao` | string | Mínimo de 10 caracteres na criação |
| `aberta_em` | datetime | Data original da abertura |
| `prazo` | datetime ou `null` | Calculado conforme SLA |
| `concluida_em` | datetime ou `null` | Preenchido ao concluir e limpo ao reabrir |
| `prioridade` | inteiro ou `null` | Calculada; `1` é máxima e `5` é mínima |
| `reaberturas` | inteiro | Começa em `0` |

## Persistência

Os dados ficam somente em memória. Reiniciar o servidor apaga as ordens criadas durante a
execução e restaura os dados iniciais do laboratório.
