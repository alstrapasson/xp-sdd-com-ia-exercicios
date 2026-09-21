"""Modelos de domínio da API de manutenção."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Criticidade(StrEnum):
    """Criticidade do equipamento para a operação."""

    A = "A"  # parada de linha
    B = "B"  # degradação de capacidade
    C = "C"  # sem impacto imediato


class TipoOrdem(StrEnum):
    CORRETIVA = "corretiva"
    PREVENTIVA = "preventiva"
    PREDITIVA = "preditiva"


class StatusOrdem(StrEnum):
    ABERTA = "aberta"
    EM_EXECUCAO = "em_execucao"
    AGUARDANDO_PECA = "aguardando_peca"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class Equipamento(BaseModel):
    id: str
    tag: str = Field(description="Identificação em campo, ex.: BC-201")
    setor: str
    criticidade: Criticidade
    horas_operacao: int = 0


class OrdemServico(BaseModel):
    id: str
    equipamento_id: str
    tipo: TipoOrdem
    status: StatusOrdem = StatusOrdem.ABERTA
    descricao: str
    aberta_em: datetime
    prazo: datetime | None = None
    concluida_em: datetime | None = None
    prioridade: int | None = Field(
        default=None, description="1 (máxima) a 5 (mínima). Calculada, não informada."
    )
    reaberturas: int = 0


class NovaOrdem(BaseModel):
    equipamento_id: str
    tipo: TipoOrdem
    descricao: str = Field(min_length=10)


class AtualizacaoStatus(BaseModel):
    status: StatusOrdem
