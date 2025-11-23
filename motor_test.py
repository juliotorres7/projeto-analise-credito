# tests/test_engine.py
import pytest
from engine import MotorCredito

@pytest.fixture
def engine():
    return MotorCredito("regras.json")

def test_reprovado_restritivo(engine):
    cliente = {"score": 700, "renda": 5000, "situacao": "negativado", "compromissos":0, "parcela_prevista":0, "profissao":"analista", "tempo_emprego_meses":12}
    assert engine.avaliar(cliente)["decisao"] == "Reprovado"
    
def test_aprovado_restritivo(engine):
    cliente = {"score": 700, "renda": 1500, "situacao": "ok", "compromissos":0, "parcela_prevista":0, "profissao":"analista", "tempo_emprego_meses":12}
    assert engine.avaliar(cliente)["decisao"] == "Aprovado"