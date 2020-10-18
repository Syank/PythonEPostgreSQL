import postgresql
import conexao

banco = conexao.conectar("testespy", "admin")

lista = banco.selecionarElementos("cidade")
for elemento in lista:
    print(elemento)
    
banco.desconectar()
