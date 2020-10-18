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
        try:
            self._banco.execute(sql)
        except:
            print("Por favor verifique o SQL informado.")
            raise


    def atualizarElementos(self, nomeDaTabela, novosValores = {}, condicao = ""):
        "O formato de novosValores deve ser {'campo':'valor'}\nO formato de condicao, caso tenha, deve ser 'campo = valor'"

        sql = "update " + nomeDaTabela + " set "

        for chave in novosValores:
            sql += chave + " = " + novosValores[chave] + ", "

        sql = sql[:-2]

        if condicao != "":
            sql += " where " + condicao
            
        try:
            self._banco.execute(sql)
        except:
            raise


    def deletarElementos(self, nomeDaTabela, condicao = ""):
        "Deleta um elemento da tabela onde a condição seja verdadeira\nO formato de condicao deve ser 'campo = valor'"

        sql = "delete from " + nomeDaTabela + " where " + condicao

        try:
            self._banco.execute(sql)
        except:
            raise

    
    def inserirElementos(self, nomeDaTabela, valores = {}):
        "O formato de valores deve ser {'campo':'valor'}"

        sql = "insert into " + nomeDaTabela + " ("

        # O for abaixo cria a parte das colunas
        for chave in valores:
            sql += chave + ", "
        sql = sql[:-2] + ") values ("

        # O for abaixo cria a parte dos valores
        for chave in valores:
            sql += valores[chave] + ", "
        sql = sql[:-2] + ")"

        try:
            self._banco.execute(sql)
        except:
            raise


    def criarTabela(self, nomeDaTabela, chavePrimaria = {}, campos = {}):
        "Os campos devem ser um dicionário no formato {'nomeDoCampo':'tipo'}\nO conteúdo dos dicionários deve ser uma String"

        for chave in chavePrimaria:
            sqlCampos = " (" + chave + " " + chavePrimaria[chave] + " primary key, "
        
        for chave in campos:
            sqlCampos += chave + " " + campos[chave] + ", "

        sqlCampos = sqlCampos[:-2] + ")"
        
        sql = "create table " + nomeDaTabela + sqlCampos
        
        try:
            self._banco.execute(sql)
        except:
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
