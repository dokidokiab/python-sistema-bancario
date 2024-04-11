#variáveis utilizadas

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

"""

saldo_conta = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3 
#########################

#função para o extrato
def extrato():
    print("=======EXTRATO=======")
    print(f"\nO saldo da conta é R${saldo_conta:.2f}.")
    print("\nNenhuma transação foi realizada" if not extrato else extrato)

#função para o saque
def sacar(valor):
    if valor > 500:
        print("\nErro: Valor limite de saque excedido. Saque 500 reais ou menos apenas.")
    else:
        if numero_saques < 3 and saldo_conta >= valor:
            saldo_conta -= valor
            print(f"\nSaque no valor de R${valor} realizado com sucesso!")

            extrato += f"\nSaque no valor de R${valor} realizado"

            numero_saques += 1

        elif numero_saques == 3:
            print("\nErro: Quantidade limite diária de saques excedida. Tente novamente amanhã.")
        
        elif saldo_conta < valor:
            print("\nErro: Saldo insuficiente!")

#função para o depósito
def depositar(valor):
    print(f"\Depósito no valor de R${valor} realizado com sucesso!")
    extrato += f"\Depósito no valor de R${valor} realizado"
    saldo_conta += valor


#loop de organização de funcionamento
while True:
    opçao = input(menu).lower()

    if opçao == "s": 
        valor = input("\nDigite o valor a sacar: ")
        sacar(valor)

    elif opçao == "d":
        valor = input("\nDigite o valor a depositar: ")
        depositar(valor)

    elif opçao == "e":
        extrato()

    elif opçao == "q":
        print("Encerrando a sessão...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")