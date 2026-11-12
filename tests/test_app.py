import pytest
from datetime import date, timedelta
import app as app_module


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    banco_teste = tmp_path / "teste.db"

    monkeypatch.setattr(app_module, "DB_PATH", banco_teste)

    app_module.inicializar_banco()
    app_module.app.config["TESTING"] = True

    return app_module.app.test_client()


def test_pagina_inicial(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200


def test_pagina_cadastro(cliente):
    resposta = cliente.get("/cadastro")
    assert resposta.status_code == 200


def test_pagina_estoque_vazio(cliente):
    resposta = cliente.get("/estoque")
    assert resposta.status_code == 200


def test_cadastro_produto(cliente):
    resposta = cliente.post("/cadastro", data={
        "nome": "Feijão 1 kg",
        "quantidade": "10",
        "data_validade": (date.today() + timedelta(days=20)).isoformat(),
        "estoque_minimo": "5"
    })

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/estoque")


def test_cadastro_quantidade_invalida(cliente):
    resposta = cliente.post("/cadastro", data={
        "nome": "Arroz 5 kg",
        "quantidade": "-3",
        "data_validade": (date.today() + timedelta(days=20)).isoformat(),
        "estoque_minimo": "5"
    })

    assert resposta.status_code == 200
    assert b"Confira os campos" in resposta.data


def test_excluir_produto(cliente):
    cliente.post("/cadastro", data={
        "nome": "Macarrão",
        "quantidade": "8",
        "data_validade": (date.today() + timedelta(days=20)).isoformat(),
        "estoque_minimo": "3"
    })

    resposta = cliente.post("/excluir/1")

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/estoque")
