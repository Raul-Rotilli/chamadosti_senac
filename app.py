from cgitb import html
from flask import Flask, redirect, render_template, request, url_for, flash, session
import mysql.connector
import logging


cnx = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password=''
)
cursor = cnx.cursor()
cursor.execute(
    'SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "chamadosti";')
num_results = cursor.fetchone()[0]
cnx.close()
if num_results > 0:
    print('O banco de dados chamadosti existe e esta pronto para uso.')
else:
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=''
    )

    cursor = cnx.cursor()
    cursor.execute('CREATE DATABASE chamadosti;')
    cnx.commit()

    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )

    cursor = cnx.cursor()
    cursor.execute('CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(50), email VARCHAR(123), senha VARCHAR(30), perfil VARCHAR(7), cargo VARCHAR(50), status varchar(20), justificativa varchar(120), data_just_ini datetime, data_just_fin datetime);')
    cursor.execute(
        'CREATE TABLE setores (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255));')
    cursor.execute('CREATE TABLE equipamentos (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(50), id_setor int(6), marca VARCHAR(100), conservacao VARCHAR(30), status varchar(100), justificativa varchar(120), data_cadastro datetime);')
    cursor.execute(
        'CREATE TABLE status (id INT AUTO_INCREMENT PRIMARY KEY,  id_equipamento int(6), status varchar(100), date_modificacao datetime);')
    cursor.execute('CREATE TABLE chamados (id INT AUTO_INCREMENT PRIMARY KEY, id_usuario int(6), id_equipamento int(6), descricao VARCHAR(123), id_setor int(6), data_abertura datetime, id_tecnico int(6), observacao varchar(123), data_fechamento datetime, urgencia varchar(20), solucao varchar(200));')
    cursor.execute('ALTER TABLE chamados ADD CONSTRAINT fk_chamados_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios (id), ADD CONSTRAINT fk_chamados_equipamentos FOREIGN KEY (id_equipamento) REFERENCES equipamentos (id)')

    cnx.commit()
    cnx.close()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TESTE'


@app.route('/paginainicial')
def pagina_inicial():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    return render_template('paginainicial.html')


@app.route('/chamados')
def pagina_chamados():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )
    cursor = cnx.cursor()
    if session.get('perfil') == 'tecnico':
        cursor.execute('Select * from chamados')
        chamados = cursor.fetchall()
    else:
        cursor.execute('Select * from chamados WHERE id_usuario = %s',
                       (session.get('usuario_id'),))
        chamados = cursor.fetchall()
    return render_template('chamados.html', chamados=chamados)


@app.route('/usuarios')
def pagina_usuarios():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )
    if session.get('perfil') == 'tecnico':
        cursor = cnx.cursor()
        cursor.execute(
            'SELECT * FROM usuarios WHERE perfil = %s', ('usuario',))
        usuarios = cursor.fetchall()
        return render_template("usuarios.html", usuarios=usuarios)
    else:
        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = %s',
                       (session.get('usuario_id'),))
        usuarios = cursor.fetchall()
        return render_template("usuarios.html", usuarios=usuarios)


@app.route('/tecnicos')
def pagina_tecnicos():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM usuarios')
    tecnicos = cursor.fetchall()
    return render_template("tecnicos.html", tecnicos=tecnicos)


@app.route('/setores')
def pagina_setores():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM setores')
    setores = cursor.fetchall()
    return render_template("setores.html", setores=setores)


@app.route('/cadastro_usuario', methods=['POST', 'GET'],)
def cadastro_usuario():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    perfil = request.form.get('perfil')
    if request.method != 'POST':
        return render_template('cadastro_usuario.html', error='Método HTTP inválido.')
    if not nome:
        return render_template('cadastro_usuario.html', error='O nome é obrigatório.')
    if not email:
        return render_template('cadastro_usuario.html', error='O e-mail é obrigatório.')
    if not perfil:
        return render_template('cadastro_usuario.html', error='O perfil é obrigatória.')
    if not senha:
        return render_template('cadastro_usuario.html', error='A senha é obrigatória.')
    if len(senha) < 8:
        return render_template('cadastro_usuario.html', error='A senha deve ter pelo menos 8 caracteres.')

    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )

    cursor = cnx.cursor()
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE email = %s;', (email,))
    existe = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    if existe > 0:
        return render_template('paginainicial.html', error='O usuário já existe.')
    else:
        try:
            cnx = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='chamadosti'
            )
            cursor = cnx.cursor()

            sql = 'INSERT INTO usuarios (nome, email, senha, perfil) values (%s, %s, %s, %s)'
            values = (nome, email, senha, perfil)

            cursor.execute(sql, list(values))
            cursor.close()
            cnx.commit()
            if perfil == 'usuario':
                return redirect(url_for('pagina_usuarios'))
            else:
                return redirect(url_for('pagina_tecnicos'))
        except mysql.connector.Error as e:
            return render_template('cadastro_usuario.html', error=str(e))


@app.route('/cadastro_setor', methods=['POST', 'GET'])
def cadastro_setor():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    nome = request.form.get('nome')
    if request.method != 'POST':
        return render_template('cadastro_setor.html', error='Método HTTP inválido.')
    if not nome:
        return render_template('cadastro_setor.html', error='O nome é obrigatório.')

    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )

    cursor = cnx.cursor()
    cursor.execute('SELECT COUNT(*) FROM setores WHERE nome = %s;', (nome,))
    existe = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    if existe > 0:
        return render_template('cadastro_setor.html', error='O setor já existe.')
    else:
        try:
            cnx = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='chamadosti'
            )
            cursor = cnx.cursor()

            cursor.execute('INSERT INTO setores (nome) values (%s)', (nome,))
            cursor.close()
            cnx.commit()

            return redirect(url_for('pagina_setores'))

        except mysql.connector.Error as e:
            return render_template('pagina_setores.html', error=str(e))


@app.route('/cadastro_chamado', methods=['POST', 'GET'])
def cadastro_chamado():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'usuario':
        return redirect(url_for('pagina_inicial'))
    id_usuario = session.get('usuario_id')
    descricao = request.form.get('descricao')
    id_setor = request.form.get('setor')
    if request.method != 'POST':
        return render_template('cadastro_chamado.html', error='Método HTTP inválido.')
    if not descricao:
        return render_template('cadastro_chamado.html', error='A descrição é obrigatória.')
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )

    cursor = cnx.cursor()
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()

        sql = 'INSERT INTO chamados (id_usuario, descricao, id_setor, data_abertura) values (%s, %s, %s, NOW())'
        values = (id_usuario, descricao, id_setor)

        cursor.execute(sql, list(values))
        cursor.close()
        cnx.commit()

        return redirect(url_for('pagina_chamados'))

    except mysql.connector.Error as e:
        return render_template('cadastro_chamado.html', error=str(e))


@app.route('/cadastrochamado', methods=['POST', 'GET'])
def pagina_cadastro_chamado():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'usuario':
        return redirect(url_for('pagina_inicial'))
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM setores')
    setores = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('cadastro_chamado.html', setores=setores)


@app.route('/excluir_usuario/<id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    if not id.isdigit:
        return render_template('excluir_usuario', error='ID invalido')
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        cursor.close()
        cnx.commit()
        return redirect(url_for('pagina_usuarios'))
    except mysql.connector.Error as e:
        return render_template('excluir-usuario.html', error=str(e))


@app.route('/excluir_tecnico/<id>', methods=['GET', 'POST'])
def excluir_tecnico(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    if not id.isdigit:
        return render_template('excluir_tecnico', error='ID invalido')
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM tecnicos WHERE id = %s', (id,))
        cursor.close()
        cnx.commit()
        return redirect(url_for('pagina_tecnicos'))
    except mysql.connector.Error as e:
        return render_template('excluir-tecnico.html', error=str(e))


@app.route('/excluir_setor/<id>', methods=['GET', 'POST'])
def excluir_setor(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    if not id.isdigit:
        return render_template('excluir_setor', error='ID invalido')
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()
        cursor.execute('DELETE FROM setores WHERE id = %s', (id,))
        cursor.close()
        cnx.commit()
        return redirect(url_for('pagina_setores'))
    except mysql.connector.Error as e:
        return render_template('excluir-setor.html', error=str(e))


@app.route('/editarusuario/<id>', methods=['GET', 'POST'])
def atualizarusuario(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
 # Valida o ID do usuário
    if not id.isdigit():
        return render_template('editarusuario/<id>', error='ID inválido.')
    if session.get('usuario_id') != id and not session.get('tecnico_id'):
        return render_template('paginainicial.html')

    # Obtém os dados do usuário do banco de dados
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti')
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT id, nome, email
        FROM usuarios
        WHERE id = %s;
    """, (id,))
    dados_usuario = cursor.fetchone()
    cursor.close()
    cnx.close()

    if dados_usuario[0] == session.get('usuario_id') and session.get('perfil') == 'usuario':
        return redirect(url_for('pagina_inicial'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Valida o input
        if not nome:
            flash('O nome é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not email:
            flash('O e-mail é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not email:
            flash('A senha é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        # Realiza a atualização no banco de dados

        cnx = mysql.connector.connect(host='127.0.0.1',
                                      user='root',
                                      password='',
                                      database='chamadosti')
        cursor = cnx.cursor()
        sql = 'UPDATE usuarios SET nome = %s, email = %s, senha=%s WHERE id = %s;'
        values = (nome, email, senha, id)
        cursor.execute(sql, values)
        cnx.commit()
        cursor.close()
        cnx.close()

        # Redireciona para a página inicial
        return render_template('paginainicial.html')

    # Exibe o formulário
    return render_template('editarusuario.html', id=id, usuario=dados_usuario)


@app.route('/editarchamado/<id>', methods=['GET', 'POST'])
def atualizarchamado(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))

    if not id.isdigit():
        return render_template('editarusuario/<id>', error='ID inválido.')

    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti')
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT `id`, `id_usuario`, `id_equipamento`, `descricao`, `id_setor`, `data_abertura`, `id_tecnico`, `observacao` `data_fechamento`, `urgencia`, `solucao`
        FROM chamados
        WHERE id = %s;
    """, (id,))
    dados_chamado = cursor.fetchone()
    cursor.close()
    cnx.close()

    # Processa o formulário
    if request.method == 'POST':
        try:
            id_equipamento = request.form.get('id_equipamento')
            id_setor = request.form.get('id_setor')
            observacao = request.form.get('observacao')
            # Realiza a atualização no banco de dados
            # Realiza a atualização no banco de dados
            cnx = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='chamadosti'
            )
            cursor = cnx.cursor()
            sql = 'UPDATE chamados SET id_equipamento = %s, id_setor = %s, observacao = %s WHERE id = %s;'
            values = (id_equipamento, id_setor, observacao, id)
            cursor.execute(sql, values)
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('pagina_chamados'))
        except mysql.connector.Error as e:
            return render_template('paginainicial.html')
            # Redireciona para a página inicial

    return render_template('editarchamado.html', id=id, chamado=dados_chamado)

@app.route('/atender_chamado/<id>', methods=['POST', 'GET'])
def atender_chamado(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))

    if not str(id).isdigit():
        return render_template('chamados/<id>', error='ID inválido.')
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti')
        cursor = cnx.cursor()
        sql = 'UPDATE chamados SET id_tecnico = %s WHERE id = %s;'
        values = (session.get('usuario_id'), id)
        cursor.execute(sql, values)
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('pagina_chamados'))
    except mysql.connector.Error as e:
        return render_template('paginainicial.html')
    



@app.route('/', methods=['POST', 'GET'])
def pagina_login():
    session.clear()
    session.pop('usuario_id', None)
    session.pop('perfil', None)
    return render_template("login.html")


@app.route('/validalogin', methods=['POST', 'GET'])
def login():

    email = request.form.get('email')
    senha = request.form.get('senha')

    # Validar as credenciais
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='chamadosti'
    )
    cursor = cnx.cursor()
    cursor.execute(
        ' SELECT * FROM usuarios WHERE email = %s AND senha = %s;', (email, senha,))
    usuario = cursor.fetchone()
    cursor.close()
    cnx.close()
    if usuario:
        session['usuario_id'] = usuario[0]
        session['perfil'] = usuario[4]
        return redirect(url_for('pagina_usuarios'))
    else:
        # Login inválido
        return redirect(url_for('pagina_login'))


if __name__ == '__main__':
    app.run(debug=True)
