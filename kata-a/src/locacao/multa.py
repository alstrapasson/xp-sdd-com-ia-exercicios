"""Cálculo de multa por devolução atrasada.

TODO(LOC-4471): implementar `calcular_multa`.
"""

from __future__ import annotations

from decimal import Decimal

from .modelos import Contrato, Devolucao


def calcular_multa(contrato: Contrato, devolucao: Devolucao) -> Decimal:
    """Calcula a multa devida pela devolução atrasada de um equipamento.

    Args:
        contrato: Contrato de locação correspondente.
        devolucao: Evento de devolução registrado pelo pátio.

    Returns:
        O valor da multa em BRL, com duas casas decimais. Zero quando não há multa devida.
    """
    raise NotImplementedError("LOC-4471")
