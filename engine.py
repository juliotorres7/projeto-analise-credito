# engine.py
import json
import logging
from typing import Dict, Any

logger = logging.getLogger("engine_credito")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class MotorCredito:
    def __init__(self, regras_path: str):
        with open(regras_path, "r", encoding="utf-8") as f:
            self.regras = json.load(f)

    def avaliar(self, cliente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recebe um dicionário cliente com keys:
        id, nome, idade, score, renda, compromissos, parcela_prevista, situacao, profissao, tempo_emprego_meses
        Retorna dict com 'decisao' e 'motivo'
        """
        try:
            # Normaliza entradas
            score = float(cliente.get("score", 0))
            renda = float(cliente.get("renda", 0))
            situacao = str(cliente.get("situacao", "")).lower()
            compromissos = float(cliente.get("compromissos", 0))
            parcela = float(cliente.get("parcela_prevista", 0))
            profissao = str(cliente.get("profissao", "")).lower()
            tempo_emprego = int(cliente.get("tempo_emprego_meses", 0))
        except Exception as e:
            logger.exception("Erro ao ler dados do cliente: %s", e)
            return {"decisao": "Erro", "motivo": "Dados inválidos"}

        # 1) Situacao cadastral
        if situacao in [s.lower() for s in self.regras["situacao_cadastral"]["nao_aceitos"]]:
            return {"decisao": "Reprovado", "motivo": "Restritivo cadastral"}

        # 2) Score alto -> aprova independente
        if score >= self.regras["score"]["limiar_alto"]:
            return {"decisao": "Aprovado", "motivo": "Score alto"}

        # 3) Score baixo com exceção por renda alta
        if score < self.regras["score"]["minimo_aprovacao"]:
            if renda >= self.regras["renda"]["excecao_score_baixo"]:
                return {"decisao": "Aprovado", "motivo": "Exceção por renda alta"}
            # se estiver entre limiar_excecao e minimo_aprovacao => avaliação manual
            if self.regras["score"]["limiar_excecao"] <= score < self.regras["score"]["minimo_aprovacao"]:
                return {"decisao": "Manual", "motivo": "Score limítrofe - avaliação manual"}
            return {"decisao": "Reprovado", "motivo": "Score baixo"}

        # 4) Renda mínima
        if renda < self.regras["renda"]["minimo"]:
            # exceção por profissão ou tempo de emprego
            if profissao in [p.lower() for p in self.regras.get("profissoes_excecao", [])] or tempo_emprego >= 60:
                return {"decisao": "Manual", "motivo": "Renda baixa - exceção por profissão/tempo emprego"}
            return {"decisao": "Reprovado", "motivo": "Renda insuficiente"}

        # 5) Comprometimento de renda
        comprometimento = (compromissos + parcela) / renda if renda > 0 else 1.0
        if comprometimento > self.regras.get("comprometimento_max", 0.35):
            return {"decisao": "Reprovado", "motivo": "Comprometimento de renda alto"}

        # Se passou por todas as regras
        return {"decisao": "Aprovado", "motivo": "Regras atendidas"}
