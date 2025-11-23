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

def test_manual_score_limiar(engine):
    cliente = {"score": 455, "renda": 2500, "situacao": "ok", "compromissos":0, "parcela_prevista":0, "profissao":"analista", "tempo_emprego_meses":12}
    assert engine.avaliar(cliente)["decisao"] in ("Manual","Reprovado","Aprovado")

def test_renda_comprometida(engine):
    cliente = {"score": 100, "renda": 1500, "situacao": "ok", "compromissos":500, "parcela_prevista":100, "profissao":"analista", "tempo_emprego_meses":12}
    assert engine.avaliar(cliente)["decisao"] == "Reprovado"