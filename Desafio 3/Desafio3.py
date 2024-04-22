from abc import ABC
from datetime import *
import functools


def registro_de_hora(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'\n-------{func.__name__} : {datetime.now().strftime("%d/%m/%Y - %H:%M")}-------\n')
        func(*args, **kwargs)
    
    return wrapper

_clientes = []

class Cliente:
    def __init__(self, endereco, contas=[]) -> None:
        self._endereco = endereco
        self._contas = contas
    
    @property
    def contas(self):
        return self._contas
    
    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, conta, transacao):
        LIMITE_TRANSACOES = 10

        if len(conta._historico.transacoes_do_dia()) >= LIMITE_TRANSACOES:
            print("\nErro: Não foi possível concluir a operação! Você excedeu o limite de transações de hoje!\n")
        else:
            transacao.registrar(conta)

    def adicionar_conta(self, conta):
        print(conta)
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, contas, cpf, nome, data_nascimento) -> None:
        super().__init__(endereco, contas)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    def __str__(self) -> str:
        return f"\nNúmero: {self._numero} // Agência: {self._agencia} // Saldo: {self._saldo} //"
    
    def sacar(self, valor) -> bool:
        if self._saldo >= valor:
            self._saldo -= valor
            return True
        else:
            return False
    
    def depositar(self, valor) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, agencia="0001", limite=800, limite_saques=3) -> None:
        super().__init__(numero, cliente, agencia)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor):
        quantidade_saques = 0
        
        for i in Historico.transacoes_historico:
            if i["tipo"] == 'Saque':
                quantidade_saques += 1
        
        if quantidade_saques >= self._limite_saques:
            print("\nErro: Não foi possível concluir a operação! Limite de saques ultrapassado!\n")
        elif valor > self._limite:
            print("\nErro: Não foi possível concluir a operação! Valor limite ultrapassado!\n")
        else:
            return super().sacar(valor)

        return False
    
    def relatorio(self, tipo=None):
        match tipo:
            case "d":
                filtro = 'Deposito'
            case "s":
                filtro = 'Saque'
            case _:
                filtro = None

        if not self._historico.transacoes_historico:
            print("\nNão foram realizadas transações!!!\n")
        if filtro:
            for transacao in self._historico.transacoes_historico:
                if transacao['tipo'] == filtro:
                    yield f"Data: {transacao['data']} // Tipo: {transacao['tipo']} // Valor: {transacao['valor']:.2f}"
        else:
             for transacao in self._historico.transacoes_historico:
                    yield f"Data: {transacao['data']} // Tipo: {transacao['tipo']} // Valor: {transacao['valor']:.2f}"


class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self.contador = 0
    def __iter__(self):
        return self
    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return conta
        except IndexError:
            raise StopIteration

class Transacao(ABC):
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @registro_de_hora
    def registrar(self, conta):
        transacao_feita = conta.depositar(self.valor)

        if transacao_feita:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    @registro_de_hora
    def registrar(self, conta):
        transacao_feita = conta.sacar(self.valor)

        if transacao_feita:
            conta.historico.adicionar_transacao(self)

    

class Historico:
    transacoes_historico = []

    @property
    def transacoes(self):
        return self.transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes_historico.append({"tipo":transacao.__class__.__name__, "valor":transacao.valor, "data":datetime.now().strftime("%d/%m/%Y - %H:%M")})

    def transacoes_do_dia(self):
        hoje = datetime.now().date()
        transacoes_hoje = []
        for transacao in self.transacoes_historico:
            if datetime.strptime(transacao['data'], "%d/%m/%Y").date() == hoje:
                transacoes_hoje.append(transacao)
        return transacoes_hoje

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

def criar_pessoa_fisica():
    cpf = input("Digite seu CPF: ")
    cliente = filtrar_cliente(cpf, _clientes)

    if cliente:
        print("\nErro: Cliente já existe!")
        return

    endereco = input("Digite seu endereço: ")
    nome = input("Digite seu nome: ")
    
    data_nascimento = input("Digite sua data de nascimento (DD/MM/YYYY):")

    cliente = PessoaFisica(endereco, [], cpf, nome, data_nascimento)

    _clientes.append(cliente)
    
    return cliente


def filtrar_cliente(cpf, clientes):
    cliente_encontrado = [cliente for cliente in clientes if cliente._cpf == cpf]
    return cliente_encontrado[0] if cliente_encontrado else None

def exibir_extrato():
        extrato = ""
        cpf = input("Digite o CPF do cliente:  ")

        cliente = filtrar_cliente(cpf, _clientes)
        conta = selecionar_conta(cliente)

        tipo = input("\nQuais transações quer ver? \n[d] depósito\n[s] saque\n[qualquer tecla] todas:  ")
        for transacao in conta.relatorio(tipo):
            extrato += transacao
        
        if not extrato:
           extrato = "Não foram realizadas movimentações." 


        print("\n================ EXTRATO ================")
        print(extrato)
        print(f"\nSaldo: R$ {conta.saldo:.2f}")
        print("==========================================")

def selecionar_conta(cliente:Cliente):
    if len(cliente._contas) == 0:
        print("\nNão existe nenhuma conta pertecente a este cliente. Crie uma!\n")
        return
    elif len(cliente._contas) == 1:
        return cliente._contas[0]
    else:
        cont = 0
        print("=========Suas Contas========")
        for conta in cliente._contas:
            print(f"{cont} - {str(conta)}\n")
            cont += 1

        print("====Selecione uma conta=====")
        selecao = int(input("Digite o id da conta:  "))
        return cliente._contas[selecao]
            
def todas_contas():
    return [cliente._contas for cliente in _clientes]
