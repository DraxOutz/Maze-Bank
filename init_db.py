import sqlite3

# conecta (cria se não existir)
conn = sqlite3.connect("database.db")

# cria um cursor pra executar SQL
cursor = conn.cursor()

# cria tabela de usuáriosarru
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    saldo REAL DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso 🚀")
