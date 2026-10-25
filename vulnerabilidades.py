from persistencia import banco_em_memoria, salvar_dados


def gerenciar_vulnerabilidades():
    print("\n--- GESTÃO DE VULNERABILIDADES ---")
    try:
        id_ativo = input("Digite o ID numérico do ativo alvo: ").strip()
        if not id_ativo.isdigit():
             print("[!] Erro: Você deve digitar apenas números no ID.")
             return

        id_ativo = int(id_ativo)

        if id_ativo not in banco_em_memoria:
            print("[-] Erro: Ativo não encontrado na base.")
            return

        ativo = banco_em_memoria[id_ativo]
        print(f"\n[*] Ativo Selecionado: {ativo['nome']}")
        print("[ 1 ] Cadastrar nova vulnerabilidade")
        print("[ 2 ] Visualizar vulnerabilidades cadastradas")
        print("[ 3 ] Editar uma vulnerabilidade")
        print("[ 4 ] Remover uma vulnerabilidade")

        escolha = input("Escolha uma opção: ").strip()

        # 1. CADASTRAR VULNERABILIDADE
        if escolha == '1':
            desc = input("Descrição detalhada: ").strip()
            categoria = input("Categoria (ex: Senha fraca, Falha de configuração): ").strip()
            severidade = input("Severidade (Baixa, Média, Alta, Crítica): ").strip()
            status = input("Status atual (ex: Aberta, Corrigida, Aceita): ").strip()

            if not desc or not categoria or not severidade or not status:
                print("[!] Erro: Nenhum campo de vulnerabilidade pode ficar vazio!")
                return

            ativo['vulnerabilidades'].append({
                "descricao": desc,
                "categoria": categoria,
                "severidade": severidade,
                "status": status
            })

            salvar_dados()
            print("[+] Vulnerabilidade mapeada e cadastrada no ativo!")

        # 2. VISUALIZAR VULNERABILIDADES
        elif escolha == '2':
            vulns = ativo['vulnerabilidades']

            if not vulns:
                print(f"\n[+] O ativo {ativo['nome']} está SEM vulnerabilidades registradas no momento.")
            else:
                print(f"\n[!] Vulnerabilidades do ativo {ativo['nome']}:")
                for i, v in enumerate(vulns, 1):
                    print(f"  [{i}] {v['descricao']}")
                    print(f"      Categoria: {v['categoria']} | Severidade: {v['severidade']} | Status: {v['status']}\n")

        # 3. EDITAR VULNERABILIDADE
        elif escolha == '3':
            vulns = ativo['vulnerabilidades']
            if not vulns:
                print("[-] Este ativo não possui vulnerabilidades para editar.")
                return

            print("\n[*] Qual vulnerabilidade deseja editar?")
            for i, v in enumerate(vulns, 1):
                print(f"  [{i}] {v['descricao']} (Status atual: {v['status']})")

            try:
                idx = input("\nDigite o número da vulnerabilidade: ").strip()
                if not idx.isdigit():
                    print("[!] Erro: Digite um número válido.")
                    return
                idx = int(idx)

                if 1 <= idx <= len(vulns):
                    v = vulns[idx - 1] # Ajusta o índice (o usuário vê 1, mas o Python lê 0)
                    print("\nDica: Pressione ENTER sem digitar nada para manter o dado atual.")

                    n_desc = input(f"Nova Descrição [{v['descricao']}]: ").strip()
                    n_cat = input(f"Nova Categoria [{v['categoria']}]: ").strip()
                    n_sev = input(f"Nova Severidade [{v['severidade']}]: ").strip()
                    n_status = input(f"Novo Status [{v['status']}]: ").strip()

                    if n_desc: v['descricao'] = n_desc
                    if n_cat: v['categoria'] = n_cat
                    if n_sev: v['severidade'] = n_sev
                    if n_status: v['status'] = n_status

                    salvar_dados()
                    print("[+] Vulnerabilidade atualizada com sucesso!")
                else:
                    print("[-] Erro: Número de vulnerabilidade não encontrado.")
            except ValueError:
                print("[-] Erro: Digitação inválida.")

        # 4. REMOVER VULNERABILIDADE
        elif escolha == '4':
            vulns = ativo['vulnerabilidades']
            if not vulns:
                print("[-] Este ativo não possui vulnerabilidades para remover.")
                return

            print("\n[*] Qual vulnerabilidade deseja remover?")
            for i, v in enumerate(vulns, 1):
                print(f"  [{i}] {v['descricao']} (Status: {v['status']})")

            try:
                idx = input("\nDigite o número da vulnerabilidade a ser excluída: ").strip()
                if not idx.isdigit():
                    print("[!] Erro: Digite um número válido.")
                    return
                idx = int(idx)

                if 1 <= idx <= len(vulns):

                    removida = vulns.pop(idx - 1)
                    salvar_dados()
                    print(f"[+] Vulnerabilidade '{removida['descricao']}' removida com sucesso!")
                else:
                    print("[-] Erro: Número de vulnerabilidade não encontrado.")
            except ValueError:
                print("[-] Erro: Digitação inválida.")

        else:
            print("[-] Opção inválida.")

    except ValueError:
        print("[-] Erro: Digitação inválida.")
        #coment