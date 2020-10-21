import postgresql
from conexao import conectar

class carro():
    def __init__(self, modelo, placa, proprietario):
        self.modelo = modelo
        self.placa = placa
        self.proprietario = proprietario

        self.campos = {"modelo":"'" + self.modelo + "'",
                       "placa":"'" + self.placa + "'",
                       "proprietario":"'" + self.proprietario + "'"}

        self._conexao = conectar()

        tabelasNoBanco = self._conexao.listarTabelas()

        tabela = self.__class__.__name__
        if tabela not in tabelasNoBanco:
            print("Tabela correspondente não encontrada, criando a tabela '" + tabela + "'...")
            pk = {"placa":"varchar(10)"}
            campos = {"modelo":"varchar(100)", "proprietario":"varchar(100)"}
            self._conexao.criarTabela(tabela, pk, campos)


        self._conexao.inserirElementos(tabela, self.campos)

        self._conexao.desconectar()


    
