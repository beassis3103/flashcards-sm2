import sqlite3
from algorithm import clacula_proxima_revisao, ajustar_qualidade_tempo

def conectar():
    conn = sqlite3.connect("flashcards.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

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
            err_seg INTEGER DEFAULT 0
            FOREIGN KEY (id_pasta) REFERENCES pastas(id) ON DELETE CASCADE
        )
    """)

    conn.commit()

def criar_pasta(conn, nome):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pastas (nome) VALUES (?)", (nome,))
    conn.commit()
    return cursor.lastrowid

def listar_pastas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pastas")
    return cursor.fetchall()

def criar_flashcard(conn, pasta_id, pergunta, resposta):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flashcards (pasta_id, pergunta, resposta) VALUES (?, ?, ?)", (pasta_id, pergunta, resposta))
    conn.commit() 
    return cursor.lastrowid

def listar_flashcards_para_hoje(conn, pasta_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards WHERE (pasta_id = ?) AND (prox_rev <= DATE('now))", (pasta_id,))
    return cursor.fetchall()

def atualizar_flashcard(conn, flashcard_id, qualidade, tmp_sec):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards WHERE id = ?", (flashcard_id,))
    cartao = cursor.fetchone()

    

    cursor.execute("""UPDATE flashcards
                   SET intervalo = ?, repeticoes = ?, ft_facil = ?, prox_rev = ?, err_seg = ?
                   WHERE id = ?
                   """)