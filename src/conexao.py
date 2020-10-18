import postgresql

class conectar():
    _banco = None
    
    def __init__(self, nomeDoBanco, senha, usuario = "postgres"):
        self.usuario = usuario
        self.senha = senha
        self.nomeDoBanco = nomeDoBanco

        
        try:
            self._banco = postgresql.open("pq://" + self.usuario + ":" + self.senha + "@localhost/" + nomeDoBanco)
            print("Conexão bem sucedida com o banco " + self.nomeDoBanco)

        except:
            print("Houve um erro ao criar a conexão.")
            raise

    def executarSql(self, sql):
        "Função utilizada para criar tabelas, inserir elementos, atualizar e outros SQLs em geral"
        try:
            self._banco.execute(sql)
        except:
            print("Por favor verifique o SQL informado.")
            raise

        
    def selecionarElementos(self, tabela, condicao = ""):
        "Retorna uma lista com os elementos selecionados\nExemplo condicao: 'valor = 1'"

        if condicao == "":
            sql = "select * from " + tabela
        else:
            sql = "select * from " + tabela + " where " + condicao
        
        try:
            preparacao = self._banco.prepare(sql)
            lista = []
            for linha in preparacao:
                lista.append(linha)
            return lista
        except:
            print("Por favor verifique o SQL informado.")
            raise
    
    
    def desconectar(self):
        print("Desconectando do banco...")
        self._banco.close()
        print("Desconectado!")
