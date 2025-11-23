import csv
from typing import List, Dict, Any
from engine import MotorCredito

def carregar_clientes_csv(path: str) -> List[Dict[str, Any]]:
    clientes = []
    with open(path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            #converte tipos numericos
            for key in ["score","renda","compromissos","parcela_prevista","tempo_emprego_meses","idade"]:
                if key in row and row[key] != '':
                    try:
                        row[key] = float(row[key]) if '.' in row[key] or ',' in row[key] else int(row[key])
                    except:
                        pass

            clientes.append(row)

        return clientes
    
def avaliar_lote(regra_path: str, csv_file: str) -> List[Dict[str, Any]]:
    engine = MotorCredito(regra_path)
    clientes = carregar_clientes_csv(csv_file)
    resultados = []
    for c in clientes:
        res = engine.avaliar(c)
        item = {**c, **res}
        resultados.append(item)
    return resultados

if __name__ == "__main__":
    import json
    resultados = avaliar_lote("regras.json", "./dados/dados_clientes.csv")
    print(json.dumps(resultados, ensure_ascii=False, indent=2))