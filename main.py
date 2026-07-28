import time
from database import(
    conectar, criar_tabelas, criar_pasta, listar_pastas, criar_flashcard, 
    listar_flashcards_para_hoje, atualizar_flashcard, detectar_cartoes_problematicos, 
    exportar_csv, importar_csv, obter_ou_criar_pasta, resetar_tudo
)
#Executa o menu até que o usuário quit
def menu():
    while True:
        print(f"-----rememBee - Estudo com flashcards-----\n")
        print(f"1. Revisar cartões de hoje \n2. Criar pasta \n3. Criar flashcard \n4. Importar CSV \n5. Exportar CSV \n6. Ver cartões problemáticos \n7. Resetar tudo \n0. Sair\n")
        
        try:
            escolha = int(input(f"Escolha uma opção: "))
        except ValueError:
            print(f"Apenas números, tente novamente!")
            continue

        if escolha == 1:
            id_pasta = input(f"Digite o id da pasta que quer revisar: ")
            print(listar_flashcards_para_hoje(conn, id_pasta))

        elif escolha == 2:
            nome_pasta = input(f"Digite o nome da pasta: ")
            criar_pasta(conn, nome_pasta)
            print(f"Pasta '{nome_pasta}' criada com sucesso!")

        elif escolha == 3:
            id_pasta = input(f"Digite o id da pasta em que quer adicionar o flashcard: ")
            pergunta = input(f"Digite a pergunta do flashcard: ")
            resposta = input(f"Digite a resposta da pergunta: ")
            criar_flashcard(conn, id_pasta, pergunta, resposta)
            print(f"Flashcard criado com sucesso!")

        elif escolha == 4:
            pass
        elif escolha == 5:
            pass
        elif escolha == 6:
            pass
        elif escolha == 7:
            pass
        elif escolha == 0:
            print(f"Até logo!")
            break
        else:
            print(f"Opção inválida! Tente novamente.")
   