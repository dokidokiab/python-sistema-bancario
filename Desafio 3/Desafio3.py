from abc import ABC
from datetime import *

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
        pass

    def adicionar_conta(self, conta):
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
    def __init__(self, numero, agencia, cliente, historico) -> None:
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
        return cls()
    
    def __str__(self) -> str:
        return f"\nO saldo é {self._saldo}\n"
    
    def sacar(self, valor):
        if self._saldo >= valor:
            self._saldo -= valor
            return True
        else:
            return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False
    

class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, historico, limite=800, limite_saques=3) -> None:
        super().__init__(saldo, numero, agencia, cliente, historico)
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
            if i["tipo"] == Saque:
                quantidade_saques += 1
        
        if quantidade_saques >= self._limite_saques:
            print("\nErro: Não foi possível concluir a operação! Limite de saques ultrapassado!\n")
        elif valor > self._limite:
            print("\nErro: Não foi possível concluir a operação! Valor limite ultrapassado!\n")
        else:
            return super().sacar(valor)

        return False
    

class Transacao(ABC):
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @classmethod
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
        self.transacoes_historico.append({"tipo":transacao.__class__, "valor":transacao.valor, "data":datetime.now().strftime("%d/%m/%Y - %H:%M")})