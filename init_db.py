import sqlite3
import os

# conecta (cria se não existir)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# cria tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    saldo REAL DEFAULT 0
)
""")

print(os.path.abspath("database.db"))

# adiciona coluna ultimo_acesso se não existir
try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN ultimo_acesso TEXT DEFAULT '0000-00-00 00:00:00'")
except sqlite3.OperationalError:
    pass  # coluna já existe

# adiciona coluna tentativa_de_acesso se não existir
try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN tentativa_de_acesso TEXT DEFAULT '0000-00-00 00:00:00'")
except sqlite3.OperationalError:
    pass  # coluna já existe

conn.commit()
conn.close()

print("Banco atualizado/criado com sucesso 🚀")
