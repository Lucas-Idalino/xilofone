from modelos import Ativo, Vulnerabilidade, TipoAtivo, Severidade


def escolher_opcao_enum(enum_cls, titulo, mensagem, valor_atual=None):
    print(f"\n{titulo}:")
    for item in enum_cls:
        print(f"[{item.codigo}] {item.rotulo}")

    if valor_atual is not None:
        atual_rotulo = valor_atual.rotulo if isinstance(valor_atual, enum_cls) else str(valor_atual)
        entrada = input(f"{mensagem} [{atual_rotulo}] (ENTER para manter): ").strip()
        if not entrada:
            return True, valor_atual
    else:
        entrada = input(f"{mensagem}: ").strip()

    if not entrada.isdigit():
        print("[!] Erro: Digite um número inteiro!")
        return False, None

    item = enum_cls.por_codigo(int(entrada))
    if item is None:
        print("[!] Erro: Opção inválida!")
        return False, None
    return True, item


class AppInventario:

    def __init__(self, inventario):
        self.inventario = inventario

    def executar(self):
        self.inventario.carregar()
        while True:
            self._exibir_menu()
            opcao = input("Escolha a opção desejada: ").strip()
            if opcao == "0":
                print("\nEncerrando sistema. Até logo!")
                break
            handler = self._handlers().get(opcao)
            if handler:
                handler()
            else:
                print("[-] Erro: Opção inválida. Digite um número do menu.")

    def _exibir_menu(self):
        print("\n" + "-" * 45)
        print("   INVENTÁRIO DE CIBERSEGURANÇA E ATIVOS   ")
        print("-" * 45)
        print("[ 1 ] Cadastrar Ativo de TI")
        print("[ 2 ] Consultar/Listar Ativos")
        print("[ 3 ] Atualizar Dados de Ativo")
        print("[ 4 ] Remover Ativo")
        print("[ 5 ] Gerenciar/Consultar Vulnerabilidades")
        print("[ 0 ] Sair")
        print("-" * 45)

    def _handlers(self):
        return {
            "1": self.cadastrar_ativo,
            "2": self.consultar_ativos,
            "3": self.atualizar_ativo,
            "4": self.remover_ativo,
            "5": self.gerenciar_vulnerabilidades,
        }

    def cadastrar_ativo(self):
        print("\n--- CADASTRAR NOVO ATIVO ---")
        id_ativo = self.inventario.gerar_id()
        print(f"[*] ID gerado automaticamente: {id_ativo}")

        nome = input("Nome ou Hostname: ").strip()
        responsavel = input("Responsável: ").strip()
        localizacao = input("Setor/Localização: ").strip()

        if not nome or not responsavel or not localizacao:
            print("[!] Erro: Nenhum campo obrigatório de texto pode ficar vazio!")
            return

        ok, tipo = escolher_opcao_enum(TipoAtivo, "Tipos de Ativos disponíveis", "Código do tipo")
        if not ok:
            return

        try:
            ativo = Ativo(id_ativo, nome, responsavel, localizacao, tipo)
            self.inventario.adicionar(ativo)
        except ValueError as e:
            print(f"[!] Erro: {e}")
            return

        self.inventario.salvar()
        print(f"[+] Ativo '{ativo.nome}' cadastrado com sucesso!")

    def consultar_ativos(self):
        print("\n--- CONSULTAR ATIVO ---")

        if len(self.inventario) == 0:
            print("[i] Nenhum ativo cadastrado na base de dados no momento.")
            return

        print("Dica: Deixe em branco e pressione ENTER para listar TODOS os ativos.")
        termo = input("Digite o ID ou Nome/Hostname para buscar: ").strip()

        if not termo:
            encontrados = self.inventario.todos()
            print(f"\n[*] Listando todos os {len(encontrados)} ativos cadastrados:")
        elif termo.isdigit() and self.inventario.obter(int(termo)):
            encontrados = [self.inventario.obter(int(termo))]
        else:
            encontrados = self.inventario.buscar_por_nome(termo)

        if encontrados:
            for ativo in encontrados:
                self._imprimir_ativo(ativo)
        else:
            print("[-] Nenhum ativo encontrado com esses dados.")

    @staticmethod
    def _imprimir_ativo(ativo):
        print("-" * 45)
        print(f"ID: {ativo.id}")
        print(f"Nome/Hostname: {ativo.nome}")
        print(f"Tipo: {ativo.tipo_rotulo}")
        print(f"Responsável: {ativo.responsavel}")
        print(f"Localização: {ativo.localizacao}")
        print(f"Vulnerabilidades registradas: {len(ativo.vulnerabilidades)}")
        print("-" * 45)

    def atualizar_ativo(self):
        print("\n--- ATUALIZAR ATIVO ---")
        id_input = input("Digite o ID do ativo a ser atualizado: ").strip()
        if not id_input.isdigit():
            print("[!] Erro: Digite um ID numérico válido.")
            return

        ativo = self.inventario.obter(int(id_input))
        if ativo is None:
            print("[!] Erro: Ativo não encontrado na base de dados!")
            return

        print(f"[*] Editando o ativo: {ativo.nome}")
        print("Dica: Pressione ENTER sem digitar nada para manter o dado atual.")

        novo_responsavel = input(f"Novo Responsável [{ativo.responsavel}]: ").strip()
        nova_localizacao = input(f"Nova Localização [{ativo.localizacao}]: ").strip()
        novo_nome = input(f"Novo Hostname [{ativo.nome}]: ").strip()

        if novo_nome and self.inventario.nome_existe(novo_nome, ignorar_id=ativo.id):
            print(f"[!] Erro: Já existe um ativo com o nome '{novo_nome.upper()}'.")
            return

        try:
            if novo_responsavel:
                ativo.responsavel = novo_responsavel
            if nova_localizacao:
                ativo.localizacao = nova_localizacao
            if novo_nome:
                ativo.nome = novo_nome
        except ValueError as e:
            print(f"[!] Erro: {e}")
            return

        self.inventario.salvar()
        print("[+] Dados do ativo atualizados com sucesso!")

    def remover_ativo(self):
        print("\n--- REMOVER ATIVO ---")
        id_input = input("Digite o ID do ativo a ser removido: ").strip()
        if not id_input.isdigit():
            print("[!] Erro: Digite um ID numérico válido.")
            return

        ativo = self.inventario.remover(int(id_input))
        if ativo is None:
            print("[-] Erro: Ativo não encontrado!")
            return

        self.inventario.salvar()
        print(f"[+] O ativo '{ativo.nome}' foi excluído da base (junto com suas {len(ativo.vulnerabilidades)} vulnerabilidades).")

    def gerenciar_vulnerabilidades(self):
        print("\n--- GESTÃO DE VULNERABILIDADES ---")
        id_input = input("Digite o ID numérico do ativo alvo: ").strip()
        if not id_input.isdigit():
            print("[!] Erro: Você deve digitar apenas números no ID.")
            return

        ativo = self.inventario.obter(int(id_input))
        if ativo is None:
            print("[-] Erro: Ativo não encontrado na base.")
            return

        print(f"\n[*] Ativo Selecionado: {ativo.nome}")
        print("[ 1 ] Cadastrar nova vulnerabilidade")
        print("[ 2 ] Visualizar vulnerabilidades cadastradas")
        print("[ 3 ] Editar uma vulnerabilidade")
        print("[ 4 ] Remover uma vulnerabilidade")

        escolha = input("Escolha uma opção: ").strip()
        handlers = {
            "1": lambda: self._cadastrar_vuln(ativo),
            "2": lambda: self._visualizar_vulns(ativo),
            "3": lambda: self._editar_vuln(ativo),
            "4": lambda: self._remover_vuln(ativo),
        }
        handler = handlers.get(escolha)
        if handler:
            handler()
        else:
            print("[-] Opção inválida.")

    def _cadastrar_vuln(self, ativo):
        desc = input("Descrição detalhada: ").strip()
        categoria = input("Categoria (ex: Senha fraca, Falha de configuração): ").strip()

        ok, severidade = escolher_opcao_enum(
            Severidade, "Severidades disponíveis", "Código da severidade"
        )
        if not ok:
            return

        status = input("Status atual (ex: Aberta, Corrigida, Aceita): ").strip()

        try:
            vuln = Vulnerabilidade(desc, categoria, severidade, status)
        except ValueError as e:
            print(f"[!] Erro: {e}")
            return

        ativo.vulnerabilidades.append(vuln)
        self.inventario.salvar()
        print("[+] Vulnerabilidade mapeada e cadastrada no ativo!")

    def _visualizar_vulns(self, ativo):
        vulns = ativo.vulnerabilidades
        if not vulns:
            print(f"\n[+] O ativo {ativo.nome} está SEM vulnerabilidades registradas no momento.")
            return

        print(f"\n[!] Vulnerabilidades do ativo {ativo.nome}:")
        for i, v in enumerate(vulns, 1):
            print(f"  [{i}] {v.descricao}")
            print(f"      Categoria: {v.categoria} | Severidade: {v.severidade_rotulo} | Status: {v.status}\n")

    def _editar_vuln(self, ativo):
        vulns = ativo.vulnerabilidades
        if not vulns:
            print("[-] Este ativo não possui vulnerabilidades para editar.")
            return

        print("\n[*] Qual vulnerabilidade deseja editar?")
        for i, v in enumerate(vulns, 1):
            print(f"  [{i}] {v.descricao} (Status atual: {v.status})")

        idx_input = input("\nDigite o número da vulnerabilidade: ").strip()
        if not idx_input.isdigit():
            print("[!] Erro: Digite um número válido.")
            return

        idx = int(idx_input)
        if not (1 <= idx <= len(vulns)):
            print("[-] Erro: Número de vulnerabilidade não encontrado.")
            return

        v = vulns[idx - 1]
        print("\nDica: Pressione ENTER sem digitar nada para manter o dado atual.")

        n_desc = input(f"Nova Descrição [{v.descricao}]: ").strip()
        n_cat = input(f"Nova Categoria [{v.categoria}]: ").strip()

        ok, n_sev = escolher_opcao_enum(
            Severidade, "Severidades disponíveis", "Nova severidade", valor_atual=v.severidade
        )
        if not ok:
            return

        n_status = input(f"Novo Status [{v.status}]: ").strip()

        try:
            if n_desc:
                v.descricao = n_desc
            if n_cat:
                v.categoria = n_cat
            v.severidade = n_sev
            if n_status:
                v.status = n_status
        except ValueError as e:
            print(f"[!] Erro: {e}")
            return

        self.inventario.salvar()
        print("[+] Vulnerabilidade atualizada com sucesso!")

    def _remover_vuln(self, ativo):
        vulns = ativo.vulnerabilidades
        if not vulns:
            print("[-] Este ativo não possui vulnerabilidades para remover.")
            return

        print("\n[*] Qual vulnerabilidade deseja remover?")
        for i, v in enumerate(vulns, 1):
            print(f"  [{i}] {v.descricao} (Status: {v.status})")

        idx_input = input("\nDigite o número da vulnerabilidade a ser excluída: ").strip()
        if not idx_input.isdigit():
            print("[!] Erro: Digite um número válido.")
            return

        idx = int(idx_input)
        if not (1 <= idx <= len(vulns)):
            print("[-] Erro: Número de vulnerabilidade não encontrado.")
            return

        removida = vulns.pop(idx - 1)
        self.inventario.salvar()
        print(f"[+] Vulnerabilidade '{removida.descricao}' removida com sucesso!")