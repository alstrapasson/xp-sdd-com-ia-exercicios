from datetime import datetime, timedelta, timezone

from app.models import Criticidade, TipoOrdem
from app.services import sla


def test_corretiva_em_equipamento_critico_tem_prazo_de_quatro_horas():
    assert sla.prazo_em_horas(Criticidade.A, TipoOrdem.CORRETIVA) == 4


def test_prazo_e_corrido_e_nao_pula_fim_de_semana():
    # Sexta-feira 18h. Corretiva em equipamento B tem 24h -> sábado 18h, não segunda.
    sexta = datetime(2026, 3, 13, 18, tzinfo=timezone.utc)
    prazo = sla.calcular_prazo(sexta, Criticidade.B, TipoOrdem.CORRETIVA)
    assert prazo == sexta + timedelta(hours=24)
    assert prazo.weekday() == 5  # sábado


def test_vencimento_compara_com_a_referencia():
    prazo = datetime(2026, 3, 13, 18, tzinfo=timezone.utc)
    assert sla.esta_vencida(prazo, prazo + timedelta(seconds=1)) is True
    assert sla.esta_vencida(prazo, prazo) is False


def test_toda_combinacao_de_criticidade_e_tipo_tem_prazo():
    for criticidade in Criticidade:
        for tipo in TipoOrdem:
            assert sla.prazo_em_horas(criticidade, tipo) > 0
