from modelos import TipoAtivo
from persistencia import banco_em_memoria, salvar_dados
#aleatorio

def cadastrar_ativo():
    print("\n--- CADASTRAR NOVO ATIVO ---")
    try:
        id_ativo = input("ID Único do Ativo (Apenas números inteiros): ").strip()

        if not id_ativo.isdigit():
            print("[!] Erro: O ID deve ser um número inteiro!")
            return

        id_ativo = int(id_ativo)

        if id_ativo in banco_em_memoria:
            print("[!] Erro: Já existe um ativo cadastrado com este ID!")
            return

        nome = input("Nome ou Hostname: ").strip()
        responsavel = input("Responsável: ").strip()
        localizacao = input("Setor/Localização: ").strip()

        print("\nTipos de Ativos disponíveis:")
        for tipo in TipoAtivo:
            print(f"[{tipo.value}] {tipo.name.replace('_', ' ').title()}")

        tipo_id = input("Código Numérico do Tipo de Ativo: ").strip()

        if not tipo_id.isdigit():
            print("[!] Erro: O código do tipo deve ser um número inteiro!")
            return

        tipo_id = int(tipo_id)

        tipo_nome = ""
        for tipo in TipoAtivo:
            if tipo.value == tipo_id:
                tipo_nome = tipo.name.replace('_', ' ').title()
                break

        if not tipo_nome:
            print("[!] Erro: Tipo de ativo inválido!")
            return

        if not nome or not responsavel or not localizacao:
            print("[!] Erro: Nenhum campo obrigatório de texto pode ficar vazio!")
            return

        banco_em_memoria[id_ativo] = {
            "id": id_ativo,
            "nome": nome,
            "responsavel": responsavel,
            "localizacao": localizacao,
            "tipo": tipo_nome,
            "vulnerabilidades": []
        }

        salvar_dados()
        print(f"[+] Ativo '{nome}' cadastrado com sucesso!")

    except ValueError:
        print("[-] Erro: Digitação inválida no cadastro.")


def consultar_ativo():
    print("\n--- CONSULTAR ATIVO ---")

    if not banco_em_memoria:
        print("[i] Nenhum ativo cadastrado na base de dados no momento.")
        return

    print("Dica: Deixe em branco e pressione ENTER para listar TODOS os ativos.")
    termo = input("Digite o ID ou Nome/Hostname para buscar: ").strip()

    encontrados = []

    if not termo:
        encontrados = list(banco_em_memoria.values())
        print(f"\n[*] Listando todos os {len(encontrados)} ativos cadastrados:")
    else:
        if termo.isdigit() and int(termo) in banco_em_memoria:
            encontrados.append(banco_em_memoria[int(termo)])
        else:
            for ativo in banco_em_memoria.values():
                if termo.lower() in ativo['nome'].lower():
                    encontrados.append(ativo)

    if encontrados:
        for ativo in encontrados:
            print("-" * 45)
            print(f"ID: {ativo['id']}")
            print(f"Nome/Hostname: {ativo['nome']}")
            print(f"Tipo: {ativo['tipo']}")
            print(f"Responsável: {ativo['responsavel']}")
            print(f"Localização: {ativo['localizacao']}")
            print(f"Vulnerabilidades registradas: {len(ativo['vulnerabilidades'])}")
        print("-" * 45)
    else:
        print("[-] Nenhum ativo encontrado com esses dados.")


def atualizar_ativo():
    print("\n--- ATUALIZAR ATIVO ---")
    try:
        id_ativo = input("Digite o ID do ativo a ser atualizado: ").strip()
        if not id_ativo.isdigit():
            print("[!] Erro: Digite um ID numérico válido.")
            return

        id_ativo = int(id_ativo)

        if id_ativo not in banco_em_memoria:
            print("[!] Erro: Ativo não encontrado na base de dados!")
            return

        ativo = banco_em_memoria[id_ativo]
        print(f"[*] Editando o ativo: {ativo['nome']}")
        print("Dica: Pressione ENTER sem digitar nada para manter o dado atual.")

        novo_responsavel = input(f"Novo Responsável [{ativo['responsavel']}]: ").strip()
        nova_localizacao = input(f"Nova Localização [{ativo['localizacao']}]: ").strip()
        novo_nome = input(f"Novo Hostname [{ativo['nome']}]: ").strip()

        if novo_responsavel: ativo['responsavel'] = novo_responsavel
        if nova_localizacao: ativo['localizacao'] = nova_localizacao
        if novo_nome: ativo['nome'] = novo_nome

        salvar_dados()
        print("[+] Dados do ativo atualizados com sucesso!")

    except ValueError:
        print("[-] Erro: Digitação inválida.")


def remover_ativo():
    print("\n--- REMOVER ATIVO ---")
    try:
        id_ativo = input("Digite o ID do ativo a ser removido: ").strip()
        if not id_ativo.isdigit():
            print("[!] Erro: Digite um ID numérico válido.")
            return

        id_ativo = int(id_ativo)

        if id_ativo in banco_em_memoria:
            ativo = banco_em_memoria.pop(id_ativo)
            salvar_dados()
            print(f"[+] O ativo '{ativo['nome']}' foi excluído da base (junto com suas {len(ativo['vulnerabilidades'])} vulnerabilidades).")
        else:
            print("[-] Erro: Ativo não encontrado!")
    except ValueError:
        print("[-] Erro: Digitação inválida.")