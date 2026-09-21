"""Endpoints de equipamentos."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models import Equipamento
from ..repositorio import repositorio

router = APIRouter(prefix="/equipamentos", tags=["equipamentos"])


@router.get("", response_model=list[Equipamento])
def listar_equipamentos() -> list[Equipamento]:
    return repositorio.listar_equipamentos()


@router.get("/{equipamento_id}", response_model=Equipamento)
def obter_equipamento(equipamento_id: str) -> Equipamento:
    equipamento = repositorio.buscar_equipamento(equipamento_id)
    if equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    return equipamento
