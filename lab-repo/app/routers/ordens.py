"""Endpoints de ordens de serviço."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from ..models import (
    AtualizacaoStatus,
    NovaOrdem,
    OrdemServico,
    StatusOrdem,
)
from ..repositorio import repositorio
from ..services import priorizacao, sla

router = APIRouter(prefix="/ordens", tags=["ordens"])


@router.post("", response_model=OrdemServico, status_code=201)
def abrir_ordem(dados: NovaOrdem) -> OrdemServico:
    equipamento = repositorio.buscar_equipamento(dados.equipamento_id)
    if equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")

    aberta_em = datetime.now(timezone.utc)
    ordem = OrdemServico(
        id=repositorio.proximo_id_ordem(),
        equipamento_id=dados.equipamento_id,
        tipo=dados.tipo,
        descricao=dados.descricao,
        aberta_em=aberta_em,
        prazo=sla.calcular_prazo(aberta_em, equipamento.criticidade, dados.tipo),
    )
    ordem.prioridade = priorizacao.calc(ordem, equipamento)
    return repositorio.adicionar_ordem(ordem)


@router.get("", response_model=list[OrdemServico])
def listar_ordens(
    status: StatusOrdem | None = Query(default=None),
    equipamento_id: str | None = Query(default=None),
) -> list[OrdemServico]:
    ordens = repositorio.listar_ordens(status=status, equipamento_id=equipamento_id)
    return priorizacao.ordenar(ordens, repositorio.equipamentos)


@router.get("/{ordem_id}", response_model=OrdemServico)
def obter_ordem(ordem_id: str) -> OrdemServico:
    ordem = repositorio.buscar_ordem(ordem_id)
    if ordem is None:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")
    return ordem


@router.patch("/{ordem_id}/status", response_model=OrdemServico)
def atualizar_status(ordem_id: str, dados: AtualizacaoStatus) -> OrdemServico:
    ordem = repositorio.buscar_ordem(ordem_id)
    if ordem is None:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")

    if ordem.status == StatusOrdem.CANCELADA:
        raise HTTPException(status_code=409, detail="Ordem cancelada não muda de status")

    ordem.status = dados.status
    if dados.status == StatusOrdem.CONCLUIDA:
        ordem.concluida_em = datetime.now(timezone.utc)
    return ordem
