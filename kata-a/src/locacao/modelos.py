"""Modelos de domínio do módulo de locação.

Estes tipos já existem no sistema e são consumidos por outros módulos.
NÃO altere as assinaturas nem os campos.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

PLANO_STANDARD = "standard"
PLANO_PREMIUM = "premium"


@dataclass(frozen=True)
class Contrato:
    """Contrato de locação de um equipamento.

    Attributes:
        id: Identificador do contrato.
        cliente_id: Identificador do cliente.
        plano: PLANO_STANDARD ou PLANO_PREMIUM.
        valor_diaria: Valor cobrado por dia de locação, em BRL.
        dias_contratados: Duração contratada, em dias.
        devolucao_prevista: Instante previsto para a devolução. Sempre timezone-aware, em UTC.
        ocorrencias_anteriores: Quantas devoluções em atraso este cliente já teve antes desta.
    """

    id: str
    cliente_id: str
    plano: str
    valor_diaria: Decimal
    dias_contratados: int
    devolucao_prevista: datetime
    ocorrencias_anteriores: int


@dataclass(frozen=True)
class Devolucao:
    """Evento de devolução registrado pelo sistema de pátio.

    Attributes:
        contrato_id: Contrato ao qual a devolução se refere.
        devolvido_em: Instante da devolução. Sempre timezone-aware, em UTC.
    """

    contrato_id: str
    devolvido_em: datetime
