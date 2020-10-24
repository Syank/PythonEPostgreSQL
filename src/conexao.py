import postgresql


class conectar():
    _banco = None
    
    def __init__(self):
        configs = open("configs.txt", encoding = "UTF-8")
        infos = configs.readlines()
        configs.close()

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
        
        sql = "select table_name from information_schema.tables where table_schema='public' and table_type='BASE TABLE'"

        listaCrua = self._banco.prepare(sql)

        lista = []
        for linha in listaCrua:
            lista.append(linha[0])

        print("SQL executado: " + sql)
        return lista


    def alterarTabela(self, tabela, novosCampos, operacao = ""):
        """Operações de add, rename e drop
        O formato de novosCampos deve ser [['nomeColuna','tipo'], ...] para: add
        O formato de novosCampos deve ser [['nomeColuna','novoNomeColuna'], ...] para: rename
        O formato de novosCampos deve ser ['colunaAApagar', ...] para: drop
        """

        sql = "alter table " + tabela + " "

        if operacao == "add":
            for coluna in novosCampos:
                sql += "add column " + coluna[0] + " " + coluna[1] + ", "
                
        elif operacao == "rename":
            for coluna in novosCampos:
                sql += "rename column " + coluna[0] + " to " + coluna[1] + ", "

        elif operacao == "drop":
            for coluna in novosCampos:
                sql += "drop column " + coluna + ", "

        sql = sql[:-2]

        try:
            self._banco.execute(sql)
            print("SQL executado: " + sql)
        except:
            raise


    def pegarInfosTabela(self, tabela):
        "Retorna uma lista com os campos da tabela dada, bem como o tipo e tamanho do campo"
        
        sql = "select column_name, data_type, character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name = '" + tabela + "'"

        listaCrua = self._banco.prepare(sql)

        lista = []
        for linha in listaCrua:
            listinha = []
            listinha.append(linha[0])
            listinha.append(linha[1])
            listinha.append(linha[2])
            lista.append(listinha)

        print("SQL executado: " + sql)
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
            print("SQL executado: " + sql)
            self._banco.execute(sql)
        except:
            raise


    def deletarElementos(self, nomeDaTabela, condicao = ""):
        "Deleta um elemento da tabela onde a condição seja verdadeira\nO formato de condicao deve ser 'campo = valor'"

        sql = "delete from " + nomeDaTabela + " where " + condicao

        try:
            print("SQL executado: " + sql)
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
                print("SQL executado: " + sql)
            except:
                raise
        else:
            sql += " returning " + retorno
            try:
                resultado = self._banco.prepare(sql)
                print("SQL executado: " + sql)
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
            print("SQL executado: " + sql)
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
            print("SQL executado: " + sql)
            return lista
        except:
            print("Por favor verifique o SQL informado.")
            raise

    
    def desconectar(self):
        print("Desconectando do banco...")
        self._banco.close()
        print("Desconectado!")
