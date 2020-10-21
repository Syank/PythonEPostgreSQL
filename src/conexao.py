import postgresql

class conectar():
    _banco = None
    
    def __init__(self):
        credenciais = open("configs.txt", encoding = "UTF-8")
        infos = credenciais.readlines()
        credenciais.close()

        for linha in infos:
            if "usuario" in linha:
                self.usuario = linha[linha.index(' "') + 2:-2]
            elif "senha" in linha:
                self.senha = linha[linha.index(' "') + 2:-2]
            elif "database" in linha:
                self.nomeDoBanco = linha[linha.index(' "') + 2:-2]
            else:
                break
        
        try:
            self._banco = postgresql.open("pq://" + self.usuario + ":" + self.senha + "@localhost/" + self.nomeDoBanco)
            print("Conexão bem sucedida com o banco " + self.nomeDoBanco)

        except:
            print("Houve um erro ao criar a conexão.")
            raise


    def prepararSql(self, sql):
        try:
            resultado = self._banco.prepare(sql)
            return resultado
        except:
            print("Por favor verifique o SQL informado.")
            raise


    def listarTabelas(self):
        "Retorna uma lista contendo todas as tabelas do banco de dados conectado"
        
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"

        listaCrua = self._banco.prepare(sql)

        lista = []
        for linha in listaCrua:
            lista.append(linha[0])
            
        return lista


    def pegarInfosTabela(self, tabela):
        "Retorna uma lista com os campos da tabela dada, bem como o tipo e tamanho do campo"
        
        sql = "SELECT column_name, data_type, character_maximum_length FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '" + tabela + "'"

        listaCrua = self._banco.prepare(sql)

        lista = []
        for linha in listaCrua:
            listinha = []
            listinha.append(linha[0])
            listinha.append(linha[1])
            listinha.append(linha[2])
            lista.append(listinha)
        
        return lista
    
        
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

    
    def inserirElementos(self, nomeDaTabela, valores = {}, retorno = ""):
        "O formato de valores deve ser {'campo':'valor'}\nAo atribuir um valor ao retorno, a função retornará o valor do campo pedido"

        sql = "insert into " + nomeDaTabela + " ("

        
        # O for abaixo cria a parte das colunas
        for chave in valores:
            sql += chave + ", "
        sql = sql[:-2] + ") values ("

        # O for abaixo cria a parte dos valores
        for chave in valores:
            sql += valores[chave] + ", "
        sql = sql[:-2] + ")"

        if retorno == "":
            try:
                self._banco.execute(sql)
            except:
                raise
        else:
            sql += " returning " + retorno
            try:
                resultado = self._banco.prepare(sql)
                return resultado
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

        
    def selecionarElementos(self, tabela, condicao = "", orderBy = ""):
        "Retorna uma lista com os elementos selecionados\nExemplo condicao: 'valor = 1'"

        if condicao == "":
            sql = "select * from " + tabela
        else:
            sql = "select * from " + tabela + " where " + condicao
        if orderBy != "":
            sql += " order by " + orderBy
        
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
