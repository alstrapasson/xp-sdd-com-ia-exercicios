"""Cálculo de prazo de atendimento (SLA) de ordens de serviço.

Módulo de referência do repositório: documentado, testado e com regras explícitas.
Serve de contraste com `priorizacao.py`, que é o legado do Dia 5.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from ..models import Criticidade, TipoOrdem

# Prazo de atendimento em horas, por criticidade do equipamento e tipo de ordem.
# Fonte: Norma interna MAN-014, revisão 3.
PRAZOS_HORAS: dict[tuple[Criticidade, TipoOrdem], int] = {
    (Criticidade.A, TipoOrdem.CORRETIVA): 4,
    (Criticidade.A, TipoOrdem.PREVENTIVA): 168,
    (Criticidade.A, TipoOrdem.PREDITIVA): 336,
    (Criticidade.B, TipoOrdem.CORRETIVA): 24,
    (Criticidade.B, TipoOrdem.PREVENTIVA): 336,
    (Criticidade.B, TipoOrdem.PREDITIVA): 720,
    (Criticidade.C, TipoOrdem.CORRETIVA): 72,
    (Criticidade.C, TipoOrdem.PREVENTIVA): 720,
    (Criticidade.C, TipoOrdem.PREDITIVA): 1440,
}


def prazo_em_horas(criticidade: Criticidade, tipo: TipoOrdem) -> int:
    """Retorna o prazo de atendimento em horas para a combinação informada."""
    return PRAZOS_HORAS[(criticidade, tipo)]


def calcular_prazo(aberta_em: datetime, criticidade: Criticidade, tipo: TipoOrdem) -> datetime:
    """Calcula o instante limite de atendimento a partir da abertura da ordem.

    O prazo é corrido: não desconta fins de semana nem feriados. Manutenção corretiva
    em equipamento crítico não espera segunda-feira.
    """
    return aberta_em + timedelta(hours=prazo_em_horas(criticidade, tipo))


def esta_vencida(prazo: datetime, referencia: datetime) -> bool:
    """True se `referencia` ultrapassou o `prazo`."""
    return referencia > prazo
