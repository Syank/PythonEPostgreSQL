import postgresql
import conexao
import pessoa

def registrarPessoa(nome, idade):
    pessoa.pessoa(nome, idade)



registrarPessoa("Rosangela", "37")


banco = conexao.conectar()

elementos = banco.selecionarElementos("pessoa")

print(elementos)

