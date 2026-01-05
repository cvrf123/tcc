from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'sua-chave-secreta-mude-isso'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///violencia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de dados para contatos/denúncias anônimas
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(120))
    mensagem = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contato {self.id}>'

# Modelo para recursos de apoio (delegacias, abrigos, etc)
class RecursoApoio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))  # delegacia, abrigo, psicológico, jurídico
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(300))
    horario = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Recurso {self.nome}>'

# Criar banco de dados
with app.app_context():
    db.create_all()

# ROTAS
@app.route('/')
def index():
    """Página inicial com informações gerais"""
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    """Sobre o projeto e a Lei Maria da Penha"""
    return render_template('sobre.html')

@app.route('/tipos-violencia')
def tipos_violencia():
    """Informações sobre os 5 tipos de violência"""
    tipos = [
        {
            'nome': 'Violência Física',
            'descricao': 'Qualquer ação que cause lesão, sofrimento físico ou morte.',
            'exemplos': 'Empurrões, tapas, socos, chutes, queimaduras, estrangulamento.'
        },
        {
            'nome': 'Violência Psicológica',
            'descricao': 'Ações que causem dano emocional, diminuição da autoestima ou controle de ações.',
            'exemplos': 'Humilhações, manipulação, isolamento, ameaças, vigilância constante.'
        },
        {
            'nome': 'Violência Sexual',
            'descricao': 'Ação que force a vítima a presenciar, manter ou participar de relação sexual não desejada.',
            'exemplos': 'Estupro, assédio, forçar práticas sexuais indesejadas, impedir uso de anticoncepcionais.'
        },
        {
            'nome': 'Violência Patrimonial',
            'descricao': 'Controle, retenção ou subtração de bens, valores e recursos econômicos.',
            'exemplos': 'Destruir documentos, controlar dinheiro, impedir de trabalhar, danificar objetos.'
        },
        {
            'nome': 'Violência Moral',
            'descricao': 'Ações que caluniem, difamem ou injuriem a honra ou reputação.',
            'exemplos': 'Acusações falsas, expor vida íntima, criticar perante outros, rebaixar publicamente.'
        }
    ]
    return render_template('tipos_violencia.html', tipos=tipos)

@app.route('/denuncia')
def denuncia():
    """Guia de como denunciar"""
    return render_template('denuncia.html')

@app.route('/rede-apoio')
def rede_apoio():
    """Lista de recursos locais de apoio"""
    recursos = RecursoApoio.query.all()
    return render_template('rede_apoio.html', recursos=recursos)

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    """Formulário de contato anônimo"""
    if request.method == 'POST':
        nome = request.form.get('nome', 'Anônimo')
        email = request.form.get('email', '')
        mensagem = request.form.get('mensagem')
        
        if not mensagem:
            flash('Por favor, escreva uma mensagem.', 'warning')
            return redirect(url_for('contato'))
        
        novo_contato = Contato(
            nome=nome,
            email=email,
            mensagem=mensagem
        )
        
        try:
            db.session.add(novo_contato)
            db.session.commit()
            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('contato'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao enviar mensagem. Tente novamente.', 'danger')
    
    return render_template('contato.html')

# Rota para adicionar recursos (você pode criar um admin depois)
@app.route('/admin/add-recurso', methods=['POST'])
def add_recurso():
    """Adicionar recurso de apoio - criar interface admin depois"""
    # Implementar autenticação antes de usar em produção
    pass

# Tratamento de erros
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')