from Desafio3 import *
from random import *

def menu():
    menu = """

    [d] Depositar
    [s] Sacar

    [ss] Conferir Saldo
    
    [cp] Criar Usuário
    [cc] Criar Conta 

    [r] Ver relatório da conta

    [q] Sair

    => """
    return input(menu)

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
            valor = float(input("Informe o valor do depósito: "))

            try: 
                Deposito(valor).registrar(conta)
            except UnboundLocalError:
                print("\nErro: Não existe uma conta selecionada\nCrie uma conta!!\n")


        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            
            try: 
                Saque(valor).registrar(conta)
            except UnboundLocalError:
                print("\nErro: Não existe uma conta selecionada\nCrie uma conta!!\n")

        elif opcao == "ss":
            conta.checar_saldo()

        elif opcao == "cp":
            endereco = input("Digite seu endereço: ")
            nome = input("Digite seu nome: ")
            cpf = input("Digite seu CPF: ")
            data_nascimento = input("Digite sua data de nascimento (DD-MM-YYYY):")
            
            cliente = PessoaFisica(endereco, [], cpf, nome, data_nascimento)

        elif opcao == "cc":
            conta = ContaCorrente.nova_conta(cliente, str(randint(00000000, 99999999)))
            contas.append(conta)
            print("\nConta criada com sucesso!\n")

        elif opcao == "r":
            tipo = input("\nQuais transações quer ver? \n[d] depósito\n[s] saque\n[qualquer tecla] todas:  ")
            for i in conta.relatorio(tipo):
                print(i)

        #opção escondida
        elif opcao == "lc":
            for conta in ContaIterador(contas):
                print(conta)

        elif opcao == "q":
            break
        

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()