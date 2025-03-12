from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from config import Config
from models import Login, db, Curso, Conta  #* Importa o SQLAlchemy configurado no models.py


app = Flask(__name__) #* Inicialização
app.config.from_object(Config)  #* Carrega as configurações do banco de dados
db.init_app(app)  #* Inicializa o SQLAlchemy com o app Flask

migrate = Migrate(app, db) #* Gereciamento de banco de dados

#* Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

@login_manager.user_loader
def load_user(user_id): #* Função que retorna o cadastro do usuario pelo user_id
    return db.session.get(Login, int(user_id))

#* Inicialização de rotas

@app.route("/") 
@app.route("/login", methods=['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = Login.query.filter_by(email=email).first()
        print(user)

        if user and user.check_senha(senha):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos!', 'error')
            return render_template("login.html")
    return render_template("login.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome_usuario = request.form.get('nome')

        if Login.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return redirect(url_for('cadastro'))

        novo_usuario = Login(email=email, nome_usuario=nome_usuario)
        novo_usuario.set_senha(senha)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template("cadastro.html")

@app.route("/logout")
@login_required #* login necessario
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route("/dashboard") 
@login_required #* login necessario
def dashboard(): 
    cursos = Curso.query.filter_by(id_login=current_user.id).all()
    print(len(cursos))
    return render_template("dashboard.html", cursos=cursos)


@app.route("/gerenciamento", methods=['GET', 'POST']) 
@login_required #* login necessario
def gerenciamento(): 
    cursos = Curso.query.filter_by(id_login=current_user.id).all()
    contas = Conta.query.filter_by(id_login=current_user.id).all()

    if request.method == 'POST':
        site_conta = request.form.get('site-conta')
        login_conta = request.form.get('login-conta')
        senha_conta = request.form.get('senha-conta')

        print(f"Informações da conta: \n{site_conta} \n {login_conta} \n {senha_conta} --\n")

        nome_curso = request.form.get('nome-curso')
        desc_curso = request.form.get('descricao-curso')
        conta_pertence = request.form.get('id_conta')

        print(f"Informações do curso: \n {nome_curso} \n {desc_curso} \n {conta_pertence} --\n")




    return render_template("gerenciamento.html", cursos=cursos, contas=contas)

if __name__ == "__main__":
    app.run(debug=True)