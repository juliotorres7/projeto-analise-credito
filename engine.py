import json
import logging
from typing import Dict, Any

logger = logging.getLogger("engine-credito")

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

class MotorCredito:
    def __init__(self, path_regras: str):
        with open(path_regras, "r", encoding="utf-8") as f:
            self.regras = json.load(f)

    def avaliar(self,cliente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recebe um dicionário cliente com keys:
        id, nome, idade, score, renda, compromissos, parcela_prevista, situacao, profissao, tempo_emprego_meses
        Retorna dict com 'decisao' e 'motivo'
        """
        try:
            score = float(cliente.get("score", 0))
            renda = float(cliente.get("renda", 0))
            situacao = str(cliente.get("situacao", "")).lower()
            compromissos = float(cliente.get("compromissos", 0))
            parcela = float(cliente.get("parcela_prevista", 0))
            profissao = str(cliente.get("profissao", "")).lower()
            tempo_emprego = int(cliente.get("tempo_emprego_meses", 0))
        except Exception as e:
            logger.exception("Erro de leitura do cliente: %s", e)
            return {"decisao": "Erro", "motivo": "Dados invalidos"}
        
        # 1) Situacao cadastral
        if situacao in [s.lower() for s in self.regras["situacao_cadastral"]["nao_aceitos"]]:
            return {"decisao": "Reprovado", "motivo": "Restritivo cadastral"}

        # 2) Score alto -> aprova independente
        if score >= self.regras["score"]["limiar_alto"]:
            return {"decisao": "Aprovado", "motivo": "Score alto"}
        
        # 3)
        if score < self.regras ["score"]["minimo_aprovacao"]:
            if renda >= self.regras["renda"]["excecao_score_baixo"]:
                return {"decisao": "Aprovado", "motivo": "Score alto"}
        
        #4)
        if renda < self.regras ["renda"]["minimo"]:

            if profissao in [p.lower() for p in self.regras.get("profissoes_excecao", [])] or tempo_emprego >= 60:
                return {"decisao": "Manual", "motivo": "Renda baixa - exceção por profissão/tempo emprego"}
            return {"decisao": "Reprovado", "motivo": "Renda insuficiente"}

        #5)

        return {"decisao": "Reprovado", "motivo": "Regras Não Atendidas"}
        
motor = MotorCredito("regras.json")

cliente = {
    "id": 1,
    "nome": "Julio",
    "idade": 30,
    "score": 750,
    "renda": 900,
    "compromissos": 1200,
    "parcela_prevista": 300,
    "situacao": "regular",
    "profissao": "analista",
    "tempo_emprego_meses": 24
}

resultado = motor.avaliar(cliente)
print(resultado)



if __name__ == "__init__":
    print(MotorCredito("./regras.json"))