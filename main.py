from flask import Flask, render_template, request, session, redirect, url_for   # funções de login e cadastro
import init_db                       # módulo que cria a tabela do banco de dados
from logcad_custom import Login,Cadastro
print(Login, Cadastro)

# Inicializa o Flask
app = Flask(__name__)

# Secret key usada para assinar sessões (cookies)
app.secret_key = "a1b2c3d4e5f6g7h8i9j0klmnopqrstuvwxyz1234567890"

# Nome do site/banco
Website_Name = "Maze Bank"

# Variável global para checar se o usuário está logado (pode ser checada via session)
logado = False

# Mensagens de erro para mostrar ao usuário
Mensagens = {
    0: "Nenhum dado foi retornado, erro do sistema.",
    2: "Usuário não encontrado. Verifique suas credenciais e tente novamente.",
    3: "Senha incorreta. Por favor, verifique e tente novamente.",
    4: "Usuário já cadastrado. Utilize outro identificador ou faça login.",
    5: "A senha deve ter 8+ caracteres, com maiúscula, minúscula e um caractere especial.",
    6: "Informe um endereço de e-mail válido.",
    7: "As senhas inseridas não coincidem.",
    8: "Máximo de tentativas atingido. Tente mais tarde.",
}

# ==========================
# ROTA DA HOMEPAGE
# ==========================
@app.route("/")
def homepage():
    """
    Página inicial do site.
    Verifica se o usuário está logado via session e renderiza a homepage.
    """
    logado = "usuario" in session  # Checa se há usuário logado na sessão
    print(logado)
    return render_template(
        "homepage.html",
        Tipo="Início",
        Website_Name=Website_Name,
        logado=logado
    )

# ==========================
# ROTA DE LOGIN
# ==========================
@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Página de login.
    - GET: mostra o formulário de login.
    - POST: processa o login, verifica credenciais e seta a session.
    """
    if request.method == 'POST':
        # Recebe dados do formulário
        email = request.form['email']
        senha = request.form['senha']
        
        # Chama a função Login do módulo logcad
        Result = Login(email, senha)
        print(Result)
        
        if Result != 1:
            # Se houver erro, retorna a página de login com mensagem de erro
            return render_template("login.html", Erro=Mensagens[Result])
        else:
            # Login bem-sucedido, salva o usuário na sessão
            session["usuario"] = email
            return render_template(
                "conta.html",
                Tipo="Conta",
                Website_Name=Website_Name
            )
    
    # Se não for POST, apenas mostra a página de login
    logado = "usuario" in session
    print(logado)
    if not logado:
        return render_template("login.html", Tipo="Login", Website_Name=Website_Name)
    else:
        # Se o usuário já estiver logado, redireciona para a página da conta
        return redirect(url_for("conta"))

# ==========================
# ROTA DE CADASTRO
# ==========================
@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    """
    Página de cadastro de novos usuários.
    - GET: mostra o formulário de cadastro.
    - POST: processa o cadastro e cria novo usuário no banco.
    """
    if request.method == 'POST':
        # Recebe dados do formulário
        email = request.form['email']
        senha = request.form['senha']
        senha2 = request.form['senha2']
        
        # Chama a função Cadastro do módulo logcad
        Result = Cadastro(email, senha, senha2)
        
        if Result != 1:
            # Se houver erro, retorna a página de cadastro com mensagem
            return render_template("cadastro.html", Erro=Mensagens[Result])
        else:
            # Cadastro bem-sucedido, salva o usuário na sessão
            session["usuario"] = email
            return render_template(
                "conta.html",
                Tipo="Conta",
                Website_Name=Website_Name
            )
    
    # GET: mostra formulário de cadastro
    logado = "usuario" in session
    print(logado)
    if not logado:
     return render_template("cadastro.html", Tipo="Cadastro", Website_Name=Website_Name)
    else:
        # Se o usuário já estiver logado, redireciona para a página da conta
       return redirect(url_for("conta"))

@app.route("/conta", methods=['GET', 'POST'])
def conta():
    logado = "usuario" in session
    print(logado)
    if not logado:
     return redirect(url_for("/"))
    else:
     return render_template("conta.html", Tipo="Conta", Website_Name=Website_Name)

# ==========================
# EXECUÇÃO DO FLASK
# ==========================
if __name__ == "__main__":
    # Roda o servidor em modo debug
    app.run(debug=True)
