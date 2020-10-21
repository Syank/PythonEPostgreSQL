import postgresql
import conexao

class pessoa():
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

        self.campos = {"nome":"'" + self.nome + "'", "idade":"'" + self.idade + "'"}

        self._conexao = conexao.conectar()

        tabelasNoBanco = self._conexao.listarTabelas()

        tabela = self.__class__.__name__
        if tabela not in tabelasNoBanco:
            print("Tabela correspondente não encontrada, criando a tabela '" + tabela + "'...")
            pk = {"id":"serial"}
            campos = {"nome":"varchar(100)", "idade":"varchar(3)"}
            self._conexao.criarTabela(tabela, pk, campos)

        resultado = self._conexao.inserirElementos(tabela, self.campos, "id")

        self.id = resultado.first()
        resultado.close()

        self._conexao.desconectar()

