import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositorio import carregar_dados_iniciais, repositorio


@pytest.fixture
def cliente():
    repositorio.equipamentos.clear()
    repositorio.ordens.clear()
    carregar_dados_iniciais()
    with TestClient(app) as c:
        yield c


def test_saude(cliente):
    assert cliente.get("/saude").json() == {"status": "ok"}


def test_lista_equipamentos_iniciais(cliente):
    resposta = cliente.get("/equipamentos")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_abrir_ordem_calcula_prazo_e_prioridade(cliente):
    resposta = cliente.post(
        "/ordens",
        json={
            "equipamento_id": "EQ-1",
            "tipo": "corretiva",
            "descricao": "Ruído anormal no mancal do lado acoplado",
        },
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["prazo"] is not None
    assert corpo["prioridade"] is not None
    assert corpo["status"] == "aberta"


def test_abrir_ordem_para_equipamento_inexistente_retorna_404(cliente):
    resposta = cliente.post(
        "/ordens",
        json={"equipamento_id": "EQ-999", "tipo": "corretiva", "descricao": "Qualquer coisa"},
    )
    assert resposta.status_code == 404


def test_descricao_curta_e_rejeitada(cliente):
    resposta = cliente.post(
        "/ordens", json={"equipamento_id": "EQ-1", "tipo": "corretiva", "descricao": "quebrou"}
    )
    assert resposta.status_code == 422


def test_concluir_ordem_registra_data(cliente):
    ordem_id = next(iter(repositorio.ordens))
    resposta = cliente.patch(f"/ordens/{ordem_id}/status", json={"status": "concluida"})
    assert resposta.status_code == 200
    assert resposta.json()["concluida_em"] is not None


def test_ordem_cancelada_nao_muda_de_status(cliente):
    ordem_id = next(iter(repositorio.ordens))
    cliente.patch(f"/ordens/{ordem_id}/status", json={"status": "cancelada"})
    resposta = cliente.patch(f"/ordens/{ordem_id}/status", json={"status": "aberta"})
    assert resposta.status_code == 409


def test_filtro_por_status(cliente):
    resposta = cliente.get("/ordens", params={"status": "aberta"})
    assert resposta.status_code == 200
    assert all(o["status"] == "aberta" for o in resposta.json())


def _ordem_concluida(cliente, equipamento_id="EQ-1"):
    ordem = cliente.post(
        "/ordens",
        json={
            "equipamento_id": equipamento_id,
            "tipo": "corretiva",
            "descricao": "Vazamento recorrente na vedação",
        },
    ).json()
    cliente.patch(f"/ordens/{ordem['id']}/status", json={"status": "concluida"})
    return ordem["id"]


def test_reabrir_ordem_concluida(cliente):
    ordem_id = _ordem_concluida(cliente)
    original = repositorio.buscar_ordem(ordem_id)
    prazo_original = original.prazo

    resposta = cliente.post(f"/ordens/{ordem_id}/reabrir")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["status"] == "aberta"
    assert corpo["reaberturas"] == 1
    assert corpo["concluida_em"] is None
    assert repositorio.buscar_ordem(ordem_id).prazo > prazo_original


def test_reabrir_ordem_recalcula_prioridade(cliente):
    ordem_id = _ordem_concluida(cliente, "EQ-2")
    antes = repositorio.buscar_ordem(ordem_id).prioridade

    corpo = cliente.post(f"/ordens/{ordem_id}/reabrir").json()

    assert corpo["prioridade"] <= antes


def test_reabrir_ordem_nao_concluida_retorna_409(cliente):
    ordem_id = next(iter(repositorio.ordens))
    status_antes = repositorio.buscar_ordem(ordem_id).status

    resposta = cliente.post(f"/ordens/{ordem_id}/reabrir")

    assert resposta.status_code == 409
    assert repositorio.buscar_ordem(ordem_id).status == status_antes
    assert repositorio.buscar_ordem(ordem_id).reaberturas == 0


def test_reabrir_ordem_cancelada_retorna_409(cliente):
    ordem_id = next(iter(repositorio.ordens))
    repositorio.buscar_ordem(ordem_id).status = "cancelada"

    assert cliente.post(f"/ordens/{ordem_id}/reabrir").status_code == 409


def test_reabrir_ordem_inexistente_retorna_404(cliente):
    assert cliente.post("/ordens/OS-99999/reabrir").status_code == 404
