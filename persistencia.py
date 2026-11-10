import json
import os


class PersistenciaJSON:

    def __init__(self, caminho):
        self.caminho = caminho

    def carregar(self):
        if not os.path.exists(self.caminho):
            return {}
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def salvar(self, dados):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)