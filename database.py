import sqlite3
from algorithm import calcula_proxima_revisao, ajustar_qualidade_tempo
import csv


#Conecta as chaves primárias
def conectar():
    conn = sqlite3.connect("flashcards.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


#Cria tabelas de pastas e flashcards
def criar_tabelas(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pastas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR (100) NOT NULL,
            dt_criacao DATE DEFAULT CURRENT_DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pasta INTEGER NOT NULL,
            pergunta VARCHAR(400) NOT NULL,
            resposta VARCHAR(400) NOT NULL,
            intervalo INTEGER DEFAULT 0,
            repeticoes INTEGER DEFAULT 0,
            ft_facil REAL DEFAULT 2.5,
            prox_rev DATE DEFAULT CURRENT_DATE,
            err_seg INTEGER DEFAULT 0,
            FOREIGN KEY (id_pasta) REFERENCES pastas(id) ON DELETE CASCADE
        )
    """)

    conn.commit()


#Função que cria um pasta
def criar_pasta(conn, nome):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pastas (nome) VALUES (?)", (nome,))
    conn.commit()
    return cursor.lastrowid


#Lista todas as pastas existentes
def listar_pastas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pastas")
    return cursor.fetchall()


#Função que cria um novo flashcard
def criar_flashcard(conn, pasta_id, pergunta, resposta):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flashcards (id_pasta, pergunta, resposta) VALUES (?, ?, ?)", (pasta_id, pergunta, resposta))
    conn.commit() 
    return cursor.lastrowid


#Lista todos os flahscrads de uma determinada pasta que devem ser revisados hoje
def listar_flashcards_para_hoje(conn, pasta_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards WHERE (id_pasta = ?) AND (prox_rev <= DATE('now'))", (pasta_id,))
    return cursor.fetchall()


#Atualiza os parâmetros que definem quando o cartão aparecerá novamente
def atualizar_flashcard(conn, flashcard_id, qualidade, tmp_sec):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards WHERE id = ?", (flashcard_id,))
    cartao = cursor.fetchone()

    #Chama a função de ajustar a qualidade pelo tempo de resposta
    qualidade_ajustada = ajustar_qualidade_tempo(qualidade, tmp_sec)

    #Atualiza variáveis chamando a função que calcula a próxima revisão já com a qualidade ajustada
    novo_interv, novas_rep, novo_fator, prox_data = calcula_proxima_revisao(qualidade_ajustada, cartao[5], cartao[4], cartao[6]) 

    #Atualiza o tempo em segundos que a    
    err_seg = cartao[8] + 1 if qualidade < 3 else 0

    cursor.execute("""UPDATE flashcards
                   SET intervalo = ?, repeticoes = ?, ft_facil = ?, prox_rev = ?, err_seg = ?
                   WHERE id = ?
                   """, (novo_interv, novas_rep, novo_fator, prox_data, err_seg, flashcard_id))
    
    conn.commit()


#Detecta cartões que o usuário errou mais de 3 vezes seguidas; significa que a pergunta/resposta pode ser reescrita de uma forma mais fácil
def detectar_cartoes_problematicos(conn, limite = 3):
    cursor = conn.cursor()
    cursor.execute("""SELECT f.id, f.pergunta, f.resposta, f.err_seg, p.nome
                   FROM flashcards f 
                   JOIN pastas p ON f.id_pasta = p.id
                   WHERE f.err_seg >= ?
                   ORDER BY f.err_seg DESC""", (limite,))
    return cursor.fetchall()


#Cria um CSV com os dados dos falshcards de uma pasta
def exportar_csv(conn, caminho):
    cursor = conn.cursor()
    cursor.execute("""SELECT p.nome, f.pergunta, f.resposta
                   FROM flashcards f
                   JOIN pastas p ON f.id_pasta = p.id""")
    linhas = cursor.fetchall()

    #Chama o "Escritor", quem passa os dados do código para o CSV 
    with open(caminho, "w", newline = "", encoding = "utf-8") as arquivo:
        writer = csv.writer(arquivo)
        
        #Cabeçalho do arqv
        writer.writerow(["pasta", "pergunta", "resposta"])   

        #Todos os flashcards
        writer.writerows(linhas)                             
    print(f"Exportado {len(linhas)} cartões para {caminho}")


#Lê um CSV e passa os dados para os flashcards de uma pasta 
def importar_csv(conn, caminho):
    importados = 0

    #Chama o "Leitor", quem lê os dados do CSV e passa para o código
    with open(caminho, "r", encoding = "utf-8") as arquivo:
        reader = csv.DictReader(arquivo)
        for linha in reader:
            pasta_id = obter_ou_criar_pasta(conn, linha ["pasta"])
            criar_flashcard(conn, pasta_id, linha["pergunta"], linha ["resposta"])
            importados += 1
    print(f"Importados {importados} cartões de {caminho}")


#Verifica se já existe uma pasta com determinado nome, se não, cria uma nova
def obter_ou_criar_pasta(conn, nome):
    cursor = conn.cursor()
    
    #Consulta pelo ID para evr se a pasta existe
    cursor.execute("SELECT id FROM pastas WHERE nome = ?", (nome,))     
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]     #Se a pasta existir, retorna o ID dela
    else:
        return criar_pasta(conn, nome)      #Se a pasta não existir, cria uma nova com o nome pesquisado
    

#Limpa os dados do programa
def resetar_tudo(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flashcards")
    cursor.execute("DELETE FROM pastas")           
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('flashcards', 'pastas')")                 
    conn.commit()
    conn.execute("VACUUM")

    print(f"Resetado com sucesso! Todas as pastas e flashcards foram removidos.")



    