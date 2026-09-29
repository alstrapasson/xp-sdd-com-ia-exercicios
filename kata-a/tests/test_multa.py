from datetime import datetime, timezone
from decimal import Decimal

from locacao.modelos import Contrato, Devolucao, PLANO_PREMIUM, PLANO_STANDARD
from locacao.multa import calcular_multa


def contrato_base(**substituicoes):
    dados = {
        "id": "CT-1",
        "cliente_id": "CLI-1",
        "plano": PLANO_STANDARD,
        "valor_diaria": Decimal("100.00"),
        "dias_contratados": 5,
        "devolucao_prevista": datetime(2026, 3, 10, 14, 0, tzinfo=timezone.utc),
        "ocorrencias_anteriores": 1,
    }
    dados.update(substituicoes)
    return Contrato(**dados)


def devolucao_em(ano=2026, mes=3, dia=10, hora=14, minuto=0):
    return Devolucao(
        contrato_id="CT-1",
        devolvido_em=datetime(ano, mes, dia, hora, minuto, tzinfo=timezone.utc),
    )


def test_nao_cobra_quando_devolve_no_prazo_ou_antes():
    contrato = contrato_base()

    assert calcular_multa(contrato, devolucao_em(2026, 3, 10, 14, 0)) == Decimal("0.00")
    assert calcular_multa(contrato, devolucao_em(2026, 3, 10, 13, 59)) == Decimal("0.00")


def test_nao_cobra_atraso_dentro_da_tolerancia_standard():
    contrato = contrato_base()

    assert calcular_multa(contrato, devolucao_em(2026, 3, 10, 14, 30)) == Decimal("0.00")


def test_cobra_quinze_por_cento_da_diaria_por_dia_ou_fracao_de_atraso():
    contrato = contrato_base(valor_diaria=Decimal("200.00"))

    assert calcular_multa(contrato, devolucao_em(2026, 3, 12, 14, 1)) == Decimal("90.00")


def test_cobra_taxa_fixa_na_primeira_ocorrencia_de_atraso_standard():
    contrato = contrato_base(ocorrencias_anteriores=0)

    assert calcular_multa(contrato, devolucao_em(2026, 3, 10, 14, 31)) == Decimal("65.00")


def test_limita_multa_ao_teto():
    contrato = contrato_base(valor_diaria=Decimal("1000.00"), ocorrencias_anteriores=0)

    assert calcular_multa(contrato, devolucao_em(2026, 3, 20, 14, 1)) == Decimal("500.00")


def test_cliente_premium_tem_tolerancia_maior_desconto_e_sem_taxa_fixa():
    contrato = contrato_base(plano=PLANO_PREMIUM, ocorrencias_anteriores=0)

    assert calcular_multa(contrato, devolucao_em(2026, 3, 10, 16, 0)) == Decimal("0.00")
    assert calcular_multa(contrato, devolucao_em(2026, 3, 10, 16, 1)) == Decimal("7.50")


def test_compara_timestamps_em_utc_no_fuso_da_operacao():
    contrato = contrato_base(
        devolucao_prevista=datetime(2026, 3, 10, 2, 50, tzinfo=timezone.utc),
        ocorrencias_anteriores=1,
    )

    assert calcular_multa(contrato, devolucao_em(2026, 3, 10, 3, 21)) == Decimal("15.00")
