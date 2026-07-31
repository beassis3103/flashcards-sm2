"""
Tupla de um flashcard:
cartao[0] = id         → ex: 1
cartao[1] = pasta_id   → ex: 2
cartao[2] = pergunta   → ex: "O que é fotossíntese?"
cartao[3] = resposta   → ex: "Produção de energia pelas plantas"
cartao[4] = intervalo  → ex: 6
cartao[5] = repeticoes → ex: 2
cartao[6] = ft_facil   → ex: 2.5
cartao[7] = prox_rev   → ex: "2026-08-04"
cartao[8] = err_seg    → ex: 0

Tuplade uma pasta:
pasta[0] = id          → ex: 1
pasta[1] = nome        → ex: "Biologia"
pasta[2] = dt_criacao  → ex: "2026-07-29"

Tupla da função detectar_cartoes_problematicos():
cartao[0] = id
cartao[1] = pergunta
cartao[2] = resposta
cartao[3] = err_seg (erros seguidos)
cartao[4] = nome da pasta
"""


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
            #Mostra as pastas exsistentes
            pastas = listar_pastas(conn)
            if not pastas:
                print(f"Nenhuma pasta criada ainda!")
                continue

            print("\nPastas disponíveis:")
            for pasta in pastas:
                print(f"  {pasta[0]}. {pasta[1]}")

            #Usuário escolhe a pasta que quer revisar hoje
            id_pasta = int(input("Digite o ID da pasta desejada: "))
            cartoes = listar_flashcards_para_hoje(conn, id_pasta)

            #Lista os flashcards de hoje, se houver
            if not cartoes:
                print(f"Nenhum flashcard para hoje!")
                continue
            print(f"\n {len(cartoes)} cartões para hoje:")

            #Acumula o tempo total de resposta de cada cartão
            tempo_total = 0

            #Exibe os cartões
            for i, cartao in enumerate(cartoes):
                print(f"{'='*40}")
                print(f"Cartão {i+1} de {len(cartoes)}")
                print(f"{'='*40}")
                print(f"\nPergunta: \n{cartao[2]}")
                
                #Prepara o usuário pra receber a pergunta
                print("Prepare-se...\n")
                for seg in range (3, 0, -1):
                    print(f"{seg}...")
                    time.sleep(1)
                print("Vai!\n")

                #Começa a contar o timer
                start = time.time()
                input("Pressione ENTER quando souber a resposta!")
                tmp_sec = time.time() - start
                tempo_total += tmp_sec

                #Exibe a resposta
                print(f"Resposta: {cartao[3]}")
                print(f"Você respondeu em {tmp_sec:.1f} segundos.\n") 

                #Legenda a autoavaliação
                print("\nComo você se saiu?")
                print("\n0 - Não lembrei nada")
                print("\n1 - Errei, mas a resposta era familiar")
                print("\n2 - Errei, mas estava quase certo")
                print("\n3 - Acertei, mas com muito esforço")
                print("\n4 - Acertei com uma pequena hesitação")
                print("\n5 - Acertei imediatamente, sem esforço")

                #Recebe a nota do usuário e trata exceção
                try:
                    qualidade = int(input("Digite sua nota (0-5): "))
                except ValueError:
                    qualidade = 0
                
                #Atualiza a qualidade e o tempo do cartão de acordo de como o uauário se saiu dessa vez
                atualizar_flashcard(conn, cartao[0], qualidade, tmp_sec)
            
            #Mensagem de conclusão, o usuário reviu toda a pasta
            print(f"\n{'='*40}")
            print("\nSessão concluída, parabéns!! Você foi muito bem ;D")
            print(f"\n{len(cartoes)} cartões revisados")
            print(f"\nTempo total: {tempo_total:.0f} segundos")
            print(f"\nTempo médio por cartão: {tempo_total/len(cartoes):.1f}")

            #Exibe cartões problemáticos, se houver
            prob = detectar_cartoes_problematicos(conn)
            if prob:
                print("\nAlguns cartões que talvez precisem ser reescritos: ")
                for cartao in prob:
                    print(f" - [{cartao[4]}] {cartao[1]} (errado {cartao[3]}x seguidas)")

        #Cria pasta
        elif escolha == 2:
            nome_pasta = input(f"Digite o nome da pasta: ")
            criar_pasta(conn, nome_pasta)
            print(f"Pasta '{nome_pasta}' criada com sucesso!")

        #Cria flashcard na pasta escolhida
        elif escolha == 3:
            #Lista as pastas antes de pedir o id
            pastas = listar_pastas(conn)
            if not pastas:
                print("Nenhuma pasta criada ainda! Crie uma pasta primeiro.")
                continue
    
            print("\nPastas disponíveis:")
            for pasta in pastas:
                print(f"  {pasta[0]}. {pasta[1]}")

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