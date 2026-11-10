import random

from modelos import Ativo


class Inventario:

    def __init__(self, persistencia):
        self.persistencia = persistencia
        self.ativos = {}

    def carregar(self):
        dados = self.persistencia.carregar()
        self.ativos = {int(id_): Ativo.from_dict(info) for id_, info in dados.items()}

    def salvar(self):
        dados = {id_: ativo.to_dict() for id_, ativo in self.ativos.items()}
        self.persistencia.salvar(dados)

    def gerar_id(self):
        while True:
            novo = random.randint(100000, 999999)
            if novo not in self.ativos:
                return novo

    def nome_existe(self, nome, ignorar_id=None):
        if not nome or not nome.strip():
            return False
        nome_normalizado = nome.strip().upper()
        for ativo in self.ativos.values():
            if ignorar_id is not None and ativo.id == ignorar_id:
                continue
            if ativo.nome == nome_normalizado:
                return True
        return False

    def adicionar(self, ativo):
        if self.nome_existe(ativo.nome):
            raise ValueError(f"Já existe um ativo com o nome '{ativo.nome}'.")
        self.ativos[ativo.id] = ativo

    def obter(self, id_):
        return self.ativos.get(id_)

    def remover(self, id_):
        return self.ativos.pop(id_, None)

    def todos(self):
        return list(self.ativos.values())

    def buscar_por_nome(self, termo):
        termo_lower = termo.lower()
        return [a for a in self.ativos.values() if termo_lower in a.nome.lower()]

    def __len__(self):
        return len(self.ativos)