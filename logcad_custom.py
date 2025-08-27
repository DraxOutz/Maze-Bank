import sqlite3  # importa a sessão do Flask
import re                  # usado para validação de email e senha
from criptografia import Criptografar  # função para criptografar senhas
from flask import session

X = 0  # variável global usada para retornar códigos de erro (não ideal, mas funciona)

# ==========================
# CHECAGEM DE USUÁRIO EXISTENTE
# ==========================
def user_exists(email):
    """
    Verifica se um email já está cadastrado no banco de dados.
    
    Retorna:
        True  -> se o usuário existe
        False -> se o usuário não existe
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# ==========================
# CHECAGEM DE SENHA
# ==========================
def check_password(email, senha):
    """
    Verifica se a senha fornecida bate com a senha do usuário.
    Recebe o email e a senha (criptografada).
    
    Retorna:
        True  -> se a senha bate
        False -> se a senha está incorreta ou usuário não existe
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0] == senha
    return False

# ==========================
# VALIDAÇÃO DE EMAIL
# ==========================
def Check_Email(Email):
    """
    Valida o formato do email usando regex.
    
    Retorna:
        True  -> se o email é válido
        False -> se o email não é válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, Email) is not None

# ==========================
# VALIDAÇÃO DE SENHA
# ==========================
def Check_Password(Senha):
    """
    Valida se a senha atende aos critérios:
    - mínimo 8 caracteres
    - pelo menos 1 maiúscula
    - pelo menos 1 minúscula
    - pelo menos 1 caractere especial
    
    Retorna:
        True  -> se a senha é válida
        False -> se não atende os critérios
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$'
    return re.match(pattern, Senha) is not None

# ==========================
# CRIAÇÃO DE USUÁRIO NO BANCO
# ==========================
def Create_User(Email, Senha):
    """
    Cria um novo usuário no banco de dados.
    Criptografa a senha antes de salvar.
    Inicializa saldo com 0.
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    try:
        # Criptografa a senha
        Senha = Criptografar(Senha)
        
        # Insere o usuário no banco
        cursor.execute(
            "INSERT INTO usuarios (email, senha, saldo) VALUES (?, ?, ?)",
            (Email, Senha, 0)
        )
        conn.commit()
        print("Usuário cadastrado com sucesso")

    except sqlite3.IntegrityError:
        print("Email já cadastrado")

    finally:
        conn.close()

# ==========================
# FUNÇÃO DE LOGIN
# ==========================
def Login(Email, Senha):
    """
    Processa o login do usuário.
    - Inicializa contador de tentativas na session (5 tentativas)
    - Criptografa a senha para comparar
    - Verifica se usuário existe e se senha está correta
    - Decrementa tentativas em caso de senha errada
    Retorna códigos de erro:
        1 -> sucesso
        2 -> usuário não encontrado
        3 -> senha incorreta
        5 -> máximo de tentativas atingido
    """
    if "tentativas" not in session:
        session["tentativas"] = 5    
        # Não é eficaz contra ataques hackers, mas dá uma noção de como funciona a proteção contra repetição de senha incorreta
        # A forma eficaz para isso é salvar as tentativas de acesso no banco de dados e puxar-lo para melhor execução
        # Juntamente com isso coloque o hórario de acesso, ao passar o tempo minimo resetar as tentativas de acesso

    X = 1
    Senha = Criptografar(Senha)
    
    if not user_exists(Email):
        X = 2
    elif not check_password(Email, Senha):
        X = 3
        session["tentativas"] -= 1
    
    if session["tentativas"] < 0:
        X = 5
    
    return X

# ==========================
# FUNÇÃO DE CADASTRO
# ==========================
def Cadastro(Email, Senha1, Senha2):
    """
    Processa o cadastro de novo usuário.
    Valida:
        - senhas iguais
        - email válido
        - senha segura
        - usuário não existe
    Cria usuário se tudo estiver correto.
    
    Retorna códigos de erro:
        1 -> sucesso
        4 -> usuário já cadastrado
        5 -> senha insegura
        6 -> email inválido
        7 -> senhas não coincidem
    """
    X = 1
    
    if Senha1 != Senha2:
        X = 7
    elif not Check_Email(Email):
        X = 6
    elif not Check_Password(Senha1):
        X = 5
    elif user_exists(Email):
        X = 4
       
    print(X)
    
    if X == 1:
        Create_User(Email, Senha1)
    
    return X
