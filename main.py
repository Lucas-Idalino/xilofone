from persistencia import carregar_dados
from ativos import (
    cadastrar_ativo,
    consultar_ativo,
    atualizar_ativo,
    remover_ativo,
)
from vulnerabilidades import gerenciar_vulnerabilidades


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