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
@login_required
def gerenciamento():
    cursos = Curso.query.filter_by(id_login=current_user.id).all()
    contas = Conta.query.filter_by(id_login=current_user.id).all()

    if request.method == 'POST':
        #* Verifica se os campos de conta estão preenchidos
        site_conta = request.form.get('site-conta')
        login_conta = request.form.get('login-conta')
        senha_conta = request.form.get('senha-conta')

        #* Cadastra conta se os campos necessários estiverem preenchidos
        if site_conta and login_conta and senha_conta:
            nova_conta = Conta(
                id_login=current_user.id,
                site_conta=site_conta,
                email_conta=login_conta,
                senha_conta=senha_conta
            )
            db.session.add(nova_conta)
            db.session.commit()
            flash('Conta cadastrada com sucesso!', 'success')

        #* Verifica se os campos de curso estão preenchidos
        nome_curso = request.form.get('nome-curso')
        desc_curso = request.form.get('descricao-curso')
        conta_pertence = request.form.get('id_conta')
        # imagem_curso = request.form.get('imagem-curso', '')  # Campo opcional

        #* Cadastra curso se os campos necessários estiverem preenchidos
        if nome_curso and conta_pertence:
            novo_curso = Curso(
                id_login=current_user.id,
                id_conta=conta_pertence,
                nome_curso=nome_curso,
                descricao_curso=desc_curso,
            )
            db.session.add(novo_curso)
            db.session.commit()
            flash('Curso cadastrado com sucesso!', 'success')
        else:
            flash("Curso não cadastrado", 'error')

        # Recarrega os dados após os cadastros
        cursos = Curso.query.filter_by(id_login=current_user.id).all()
        contas = Conta.query.filter_by(id_login=current_user.id).all()

    return render_template("gerenciamento.html", cursos=cursos, contas=contas)

@app.route('/excluir_conta/<int:id>', methods=['POST'])
@login_required
def excluir_conta(id):
    conta = Conta.query.get_or_404(id)
    db.session.delete(conta)
    db.session.commit()
    flash('Conta excluída com sucesso!', 'success')
    cursos = Curso.query.filter_by(id_login=current_user.id).all()
    contas = Conta.query.filter_by(id_login=current_user.id).all()
    return redirect(url_for('gerenciamento', cursos=cursos, contas=contas))

@app.route('/excluir_curso/<int:id>', methods=['POST'])
@login_required
def excluir_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    flash('Curso excluído com sucesso!', 'success')
    cursos = Curso.query.filter_by(id_login=current_user.id).all()
    contas = Conta.query.filter_by(id_login=current_user.id).all()
    return redirect(url_for('gerenciamento', cursos=cursos, contas=contas))


if __name__ == "__main__":
    app.run(debug=True)