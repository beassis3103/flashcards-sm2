import time
from database import(
    conectar, criar_tabelas, criar_pasta, listar_pastas, criar_flashcard, 
    listar_flashcards_para_hoje, atualizar_flashcard, detectar_cartoes_problematicos, 
    exportar_csv, importar_csv, obter_ou_criar_pasta, resetar_tudo
)
#Executa o menu até que o usuário quit
def menu(conn):
    #Exibição do menu
    while True:
        print(f"-----rememBee - Estudo com flashcards-----\n")
        print(f"1. Revisar cartões de hoje \n2. Criar pasta \n3. Criar flashcard \n4. Importar CSV \n5. Exportar CSV \n6. Ver cartões problemáticos \n7. Resetar tudo \n0. Sair\n")
        
        #Tratamento de exceções: só recebe números
        try:
            escolha = int(input(f"Escolha uma opção: "))
        except ValueError:
            print(f"Apenas números, tente novamente!")
            continue

        if escolha == 1:
            #id_pasta = int(input(f"Digite o id da pasta que quer revisar: "))
            #print(listar_flashcards_para_hoje(conn, id_pasta))
            pass

        #Cria pasta
        elif escolha == 2:
            nome_pasta = input(f"Digite o nome da pasta: ")
            criar_pasta(conn, nome_pasta)
            print(f"Pasta '{nome_pasta}' criada com sucesso!")

        #Cria flashcard na pasta escolhida
        elif escolha == 3:
            id_pasta = int(input(f"Digite o id da pasta em que quer adicionar o flashcard: "))
            pergunta = input(f"Digite a pergunta do flashcard: ")
            resposta = input(f"Digite a resposta da pergunta: ")
            criar_flashcard(conn, id_pasta, pergunta, resposta)
            print(f"Flashcard criado com sucesso!")

        #Importa CSV
        elif escolha == 4:
            caminho = input(f"Digite o caminho do CSV: ")
            importar_csv(conn, caminho)

        #Exporta CSV
        elif escolha == 5:
            caminho = input(f"Digite o caminho do CSV: ")
            exportar_csv(conn, caminho)

        #Detecta e exibe os cartões problemáticos
        elif escolha == 6:
            resultado = detectar_cartoes_problematicos(conn)
            if resultado:
                print("\n Cartões que talvez precisem ser melhorados: ")
                
                for cartao in resultado:
                    print(f" - [{cartao[4]}] {cartao[1]} (errado {cartao[3]}x seguidas)")
            else:
                print(f"Nenhum cartão problemático!")

        #Reseta o programa
        elif escolha == 7:
            certeza = input(f"Essa é uma ação IRREVERSÍVEL, todos os dados serão apagados. Tem certeza que quer resetar? (S/N): ")
            if certeza.upper() == "S":
                resetar_tudo(conn)
        
        #Quit menu
        elif escolha == 0:
            print(f"Até logo!")
            break

        #Inválido
        else:
            print(f"Opção inválida! Tente novamente.")


#Cria o conn pra conectar os arquivos  
if __name__ == "__main__":
    conn = conectar()
    criar_tabelas(conn)
    menu(conn) #Passa o conn para o menu