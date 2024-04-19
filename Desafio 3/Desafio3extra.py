from Desafio3 import *
from random import *

def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    
    [cp] Criar Usuário
    [cc] Criar Conta 

    [q] Sair

    => """
    return input(menu)


def extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    usuarios = {}
    contas = []

    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            if conta:
                Deposito(valor).registrar(conta)
            else:
                print("Erro: Não existe uma conta selecionada")


        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            
            if conta:
                Saque(valor).registrar(conta)
            else:
                print("Erro: Não existe uma conta selecionada")

        elif opcao == "e":
            print(conta)

        elif opcao == "cp":
            endereco = input("Digite seu endereço: ")
            nome = input("Digite seu nome: ")
            cpf = input("Digite seu CPF: ")
            data_nascimento = input("Digite sua data de nascimento (DD-MM-YYYY):")
            
            cliente = PessoaFisica(endereco, [], cpf, nome, data_nascimento)

        elif opcao == "cc":
            conta = ContaCorrente.nova_conta(cliente, str(randint(00000000, 99999999)))

        elif opcao == "q":
            break
        

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()