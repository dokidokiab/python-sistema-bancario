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

def criar_usuario(usuarios):
    cpf = input("Digite seu CPF [apenas os números]:   ")
    
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\nErro: Usuário já foi cadastrado!\n")
        return
            

    nome = input("Digite seu nome completo: ")

    data_nascimento = input("Digite sua data de nascimento [dd-mm-aaaa] :  ")

    numero = input("Digite seu número de celular: ")

    logradouro = input("Digite seu logradouro: ")
    nro = input("Digite o numero da residência: ")
    bairro = input("Digite seu bairro: ")
    estado = input("Digite sua cidade/sigla do estado: ")

    endereco = f"{logradouro.capitalize()}, {nro} - {bairro.capitalize()} - {estado.capitalize()}"

    usuarios[cpf] = {"nome": nome, "numero":numero, "endereco":endereco, "data_nascimento":data_nascimento}
    

def filtrar_usuario(cpf, usuarios):
    #verificar se o cpf já foi cadastrado
    estaCpfCadastrado = [True for cpf_cadastrado in usuarios.keys() if cpf_cadastrado == cpf]
    return estaCpfCadastrado[0] if estaCpfCadastrado else None

def criar_conta_corrente(agencia, contas, usuarios):
    cpf = input("Digite o CPF do usuário:   ")

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
    
        conta_corrente = str(randint(00000000, 99999999))
        
        while conta_corrente in contas:    
            conta_corrente = str(randint(00000000, 99999999))
        
        
        
        print(f"""\nConta corrente gerada! 
                \nSua conta é {conta_corrente}.
                \nAgência: {agencia}.\n""")

        contas.append({"cpf":cpf, "agencia":agencia,"conta_corrente":conta_corrente, "dono":usuarios[cpf]["nome"]})
    else:
        print("\nErro: Usuário não encontrado!\n")


def saque(*, saldo, valor, extrato, limite, num_saques, limite_saques):

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = num_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        print("\n---Saque feito com sucesso!---\n")
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")
    

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        print("\n---Depósito feito com sucesso!---\n")
        return  valor, f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")

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

            valor, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            
            saque(saldo=saldo, 
                  valor=valor, 
                  extrato=extrato, 
                  limite=limite, 
                  num_saques=numero_saques, 
                  limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            extrato(saldo, extrato=extrato)

        elif opcao == "cp":
            criar_usuario(usuarios)

        elif opcao == "cc":
            criar_conta_corrente(AGENCIA, contas, usuarios)

        elif opcao == "q":
            break
        

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()