from Desafio3 import *
from random import *

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    contas = []

    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    while True:
        opcao = menu()

        if opcao == "d":
            conta_selecionada = selecionar_conta(cliente)
            valor = float(input("Informe o valor do depósito: "))
            try: 
                cliente.realizar_transacao(conta_selecionada, Deposito(valor))
            except UnboundLocalError:
                print("\nErro: Não existe uma conta selecionada\nCrie uma conta!!\n")


        elif opcao == "s":
            conta_selecionada = selecionar_conta(cliente)
            valor = float(input("Informe o valor do saque: "))
            
            try: 
                cliente.realizar_transacao(conta_selecionada, Saque(valor))
            except UnboundLocalError:
                print("\nErro: Não existe uma conta selecionada\nCrie uma conta!!\n")

        elif opcao == "cp":
            cliente = criar_pessoa_fisica()

        elif opcao == "cc":
            conta_selecionada = ContaCorrente.nova_conta(cliente, str(randint(00000000, 99999999)))
            cliente.adicionar_conta(conta_selecionada)
            print("\nConta criada com sucesso!\n")

        elif opcao == "e":
            exibir_extrato()

        #opção escondida
        elif opcao == "lc":
            for conta_selecionada in ContaIterador(todas_contas()):
                print(conta_selecionada)
            

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()