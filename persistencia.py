import json
import os


ARQUIVO_DB = "base_inventario.json"


banco_em_memoria = {}


def carregar_dados():
    
    if os.path.exists(ARQUIVO_DB):
        try:
            with open(ARQUIVO_DB, "r", encoding="utf-8") as f:
                dados = json.load(f)
                
                banco_em_memoria.clear()
                banco_em_memoria.update({int(k): v for k, v in dados.items()})
        except Exception:
            
            banco_em_memoria.clear()
    else:
        banco_em_memoria.clear()


def salvar_dados():
    
    with open(ARQUIVO_DB, "w", encoding="utf-8") as f:
        json.dump(banco_em_memoria, f, indent=4)