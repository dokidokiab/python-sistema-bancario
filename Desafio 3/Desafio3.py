from abc import ABC
from datetime import *
import functools

def registro_de_hora(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'\n-------Transação do tipo {args[0].__class__.__name__} realizada na data de {datetime.now().strftime("%d/%m/%Y às %H:%M")}!\n')
        func(*args, **kwargs)
    
    return wrapper


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
    def __init__(self, cliente, numero, agencia="0001") -> None:
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
    
    def checar_saldo(self) -> str:
        return f"\nO saldo é {self._saldo:.2f}\n"
    
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

        print("====RELATÓRIO====")

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