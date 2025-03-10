from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from config import Config
from models import Login, db  #* Importa o SQLAlchemy configurado no models.py


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
    return Login.query.get(int(user_id))

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
        nome_usuario = request.form.get('nome_usuario')

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

@login_required #* login necessario
@app.route("/dashboard") 
def dashboard(): 
    return render_template("dashboard.html")

@login_required #* login necessario
@app.route("/gerenciamento") 
def gerenciamento(): 
    return render_template("gerenciamento.html")

if __name__ == "__main__":
    app.run(debug=True)