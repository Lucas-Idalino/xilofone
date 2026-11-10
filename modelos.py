from enum import Enum


class _EnumCodigo(Enum):

    def __init__(self, codigo, rotulo):
        self.codigo = codigo
        self.rotulo = rotulo

    @classmethod
    def por_codigo(cls, codigo):
        for item in cls:
            if item.codigo == codigo:
                return item
        return None

    @classmethod
    def por_rotulo(cls, rotulo):
        for item in cls:
            if item.rotulo == rotulo:
                return item
            if item.name.replace("_", " ").title() == rotulo:
                return item
        return None


class TipoAtivo(_EnumCodigo):
    NOTEBOOK = 1, "Notebook"
    SERVIDOR = 2, "Servidor"
    ROTEADOR = 3, "Roteador"
    SOFTWARE_LICENCIADO = 4, "Software Licenciado"
    APLICACAO_WEB = 5, "Aplicação Web"
    BANCO_DE_DADOS = 6, "Banco de Dados"
    IMPRESSORA_DE_REDE = 7, "Impressora de Rede"
    ESTACAO_TRABALHO = 8, "Estação de Trabalho"


class Severidade(_EnumCodigo):
    BAIXA = 1, "Baixa"
    MEDIA = 2, "Média"
    ALTA = 3, "Alta"
    CRITICA = 4, "Crítica"


def _texto_obrigatorio(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} não pode ser vazio.")
    return valor.strip()


class Vulnerabilidade:

    def __init__(self, descricao, categoria, severidade, status):
        self.descricao = descricao
        self.categoria = categoria
        self.severidade = severidade
        self.status = status

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = _texto_obrigatorio(valor, "Descrição")

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = _texto_obrigatorio(valor, "Categoria")

    @property
    def severidade(self):
        return self._severidade

    @severidade.setter
    def severidade(self, valor):
        if not isinstance(valor, (Severidade, str)):
            raise ValueError("Severidade inválida.")
        if isinstance(valor, str) and not valor.strip():
            raise ValueError("Severidade não pode ser vazia.")
        self._severidade = valor

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        self._status = _texto_obrigatorio(valor, "Status")

    @property
    def severidade_rotulo(self):
        if isinstance(self.severidade, Severidade):
            return self.severidade.rotulo
        return str(self.severidade)

    def to_dict(self):
        return {
            "descricao": self.descricao,
            "categoria": self.categoria,
            "severidade": self.severidade_rotulo,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, dados):
        severidade_raw = dados.get("severidade", "")
        severidade = Severidade.por_rotulo(severidade_raw) or severidade_raw
        return cls(
            descricao=dados["descricao"],
            categoria=dados["categoria"],
            severidade=severidade,
            status=dados["status"],
        )


class Ativo:

    def __init__(self, id, nome, responsavel, localizacao, tipo, vulnerabilidades=None):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID deve ser um inteiro positivo.")
        if not isinstance(tipo, (TipoAtivo, str)) or (isinstance(tipo, str) and not tipo.strip()):
            raise ValueError("Tipo de ativo inválido.")

        self._id = id
        self.nome = nome
        self.responsavel = responsavel
        self.localizacao = localizacao
        self.tipo = tipo
        self.vulnerabilidades = vulnerabilidades if vulnerabilidades is not None else []

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = _texto_obrigatorio(valor, "Nome/Hostname").upper()

    @property
    def responsavel(self):
        return self._responsavel

    @responsavel.setter
    def responsavel(self, valor):
        self._responsavel = _texto_obrigatorio(valor, "Responsável")

    @property
    def localizacao(self):
        return self._localizacao

    @localizacao.setter
    def localizacao(self, valor):
        self._localizacao = _texto_obrigatorio(valor, "Localização")

    @property
    def tipo_rotulo(self):
        if isinstance(self.tipo, TipoAtivo):
            return self.tipo.rotulo
        return str(self.tipo)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "responsavel": self.responsavel,
            "localizacao": self.localizacao,
            "tipo": self.tipo_rotulo,
            "vulnerabilidades": [v.to_dict() for v in self.vulnerabilidades],
        }

    @classmethod
    def from_dict(cls, dados):
        tipo_raw = dados.get("tipo", "")
        tipo = TipoAtivo.por_rotulo(tipo_raw) or tipo_raw
        vulns = [Vulnerabilidade.from_dict(v) for v in dados.get("vulnerabilidades", [])]
        return cls(
            id=int(dados["id"]),
            nome=dados["nome"],
            responsavel=dados["responsavel"],
            localizacao=dados["localizacao"],
            tipo=tipo,
            vulnerabilidades=vulns,
        )