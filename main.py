import json
import os
from enum import Enum

# Define os tipos padronizados de ativos permitidos
class TipoAtivo(Enum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    SOFTWARE_LICENCIADO = 4
    APLICACAO_WEB = 5
    BANCO_DE_DADOS = 6
    IMPRESSORA_DE_REDE = 7
    ESTACAO_TRABALHO = 8

# Define o nome do arquivo para persistência de dados
ARQUIVO_DB = "base_inventario.json"

# Dicionário em memória para acesso rápido indexado por ID
banco_em_memoria = {}

def carregar_dados():
    # Verifica se o arquivo de banco de dados já existe
    if os.path.exists(ARQUIVO_DB):
        try:
            with open(ARQUIVO_DB, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # Limpa o dicionário atual e atualiza com os dados convertidos
                banco_em_memoria.clear()
                banco_em_memoria.update({int(k): v for k, v in dados.items()})
        except Exception:
            # Em caso de erro na leitura, inicia base vazia
            banco_em_memoria.clear()
    else:
        banco_em_memoria.clear()

def salvar_dados():
    # Persiste o dicionário atual da memória para o arquivo de texto em formato JSON
    with open(ARQUIVO_DB, "w", encoding="utf-8") as f:
        json.dump(banco_em_memoria, f, indent=4)

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


def menu():
   
    carregar_dados() 
    
   
    while True:
        print("\n" + "-"*45)
        print("   INVENTÁRIO DE CIBERSEGURANÇA E ATIVOS   ")
        print("-" * 45)
        print("[ 1 ] Cadastrar Ativo de TI")
        print("[ 2 ] Consultar/Listar Ativos")
        print("[ 3 ] Atualizar Dados de Ativo")
        print("[ 4 ] Remover Ativo")
        print("[ 5 ] Gerenciar/Consultar Vulnerabilidades")
        print("[ 0 ] Sair")
        print("-" * 45)
        
        opcao = input("Escolha a opção desejada: ").strip()
        
        if opcao == '1':
            cadastrar_ativo()
        elif opcao == '2':
            consultar_ativo()
        elif opcao == '3':
            atualizar_ativo()
        elif opcao == '4':
            remover_ativo()
        elif opcao == '5':
            gerenciar_vulnerabilidades()
        elif opcao == '0':
            print("\nEncerrando sistema. Até logo!")
            break 
        else:
            print("[-] Erro: Opção inválida. Digite um número do menu.")


if __name__ == "__main__":
    menu()