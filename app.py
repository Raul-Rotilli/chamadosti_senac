from cgitb import html
from errno import errorcode
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
        'CREATE TABLE status (id INT AUTO_INCREMENT PRIMARY KEY,  id_equipamento int(6), id_usuario int(6), status varchar(100), date_modificacao datetime);')
    cursor.execute('CREATE TABLE chamados (id INT AUTO_INCREMENT PRIMARY KEY, id_usuario int(6), id_equipamento int(6), descricao VARCHAR(123), id_setor int(6), data_abertura datetime, id_tecnico int(6), observacao varchar(123), data_fechamento datetime, urgencia varchar(20), solucao varchar(200));')
    cursor.execute('ALTER TABLE chamados ADD CONSTRAINT fk_chamados_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios (id), ADD CONSTRAINT fk_chamados_equipamentos FOREIGN KEY (id_equipamento) REFERENCES equipamentos (id)')

    cnx.commit()
    cnx.close()

    #APAGARA ISSO DEPOIS, POPULANDO TABELAS POR TESTE
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()

        # Populando tabela de usuários
        add_usuario = ("INSERT INTO usuarios "
                    "(nome, email, senha, perfil, cargo, status, justificativa, data_just_ini, data_just_fin) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        usuario_data = [
            ('1', '1', '1', 'tecnico', 'Técnico de Manutenção', 'ativo', None, None, None),
            ('Técnico Fulano', 'fulano@example.com', 'senha123', 'tecnico', 'Técnico de Manutenção', 'ativo', None, None, None),
            ('Usuário Ciclano', 'ciclano@example.com', 'senha456', 'usuario', 'Usuário Comum', 'ativo', None, None, None)
        ]
        cursor.executemany(add_usuario, usuario_data)

        # Commit das alterações na tabela de usuários
        cnx.commit()

    except mysql.connector.Error as err:
        print(err)
        # Trate o erro conforme necessário

    finally:
        # Feche o cursor e a conexão
        cursor.close()
        cnx.close()


    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()

        # Populando tabela de setores
        add_setor = ("INSERT INTO setores "
                    "(nome) "
                    "VALUES (%s)")
        setor_data = [
            ('Manutenção',),
            ('Suporte',),
            ('Administração',)
        ]
        cursor.executemany(add_setor, setor_data)

        # Commit das alterações na tabela de setores
        cnx.commit()

    except mysql.connector.Error as err:
        print(err)
        # Trate o erro conforme necessário

    finally:
        # Feche o cursor e a conexão
        cursor.close()
        cnx.close()


    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()

        # Populando tabela de equipamentos
        add_equipamento = ("INSERT INTO equipamentos "
                        "(nome, id_setor, marca, conservacao, status, justificativa, data_cadastro) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        equipamento_data = [
            ('Computador', 1, 'Dell', 'Bom estado', 'ativo', None, '2024-02-21 10:00:00'),
            ('Impressora', 1, 'HP', 'Precisa de manutenção', 'inativo', 'Quebrada', '2024-02-21 11:00:00'),
            ('Telefone', 2, 'Panasonic', 'Ótimo estado', 'ativo', None, '2024-02-21 12:00:00')
        ]
        cursor.executemany(add_equipamento, equipamento_data)

        # Commit das alterações na tabela de equipamentos
        cnx.commit()

    except mysql.connector.Error as err:
        print(err)
        # Trate o erro conforme necessário

    finally:
        # Feche o cursor e a conexão
        cursor.close()
        cnx.close()


    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()

        # Populando tabela de chamados
        add_chamado = ("INSERT INTO chamados "
                    "(id_usuario, id_equipamento, descricao, id_setor, data_abertura, id_tecnico, observacao, urgencia, solucao) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        chamado_data = [
            (1, 1, 'Computador lento', 1, '2024-02-21 13:00:00', 1, 'N/A', 'baixa', 'Limpeza realizada'),
            (2, 2, 'Impressora não imprime', 1, '2024-02-21 14:00:00', None, 'Toner acabou', 'alta', 'Substituído toner'),
            (2, 2, 'Impressora não imprime', 1, '2024-02-21 14:00:00', None, 'Toner acabou', 'alta', 'Substituído toner'),
            (2, 3, 'Telefone com chiado', 2, '2024-02-21 15:00:00', None, 'Problema de linha', 'média', 'Verificada linha telefônica')
        ]
        cursor.executemany(add_chamado, chamado_data)

        # Commit das alterações na tabela de chamados
        cnx.commit()

    except mysql.connector.Error as err:
        print(err)
        # Trate o erro conforme necessário

    finally:
        # Feche o cursor e a conexão
        cursor.close()
        cnx.close()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TESTE'


@app.route('/paginainicial')
def pagina_inicial():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    return render_template('paginainicial.html')


@app.route('/chamados', methods=['POST', 'GET'],)
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
    
    if request.method == 'POST':
        if request.form['filtro'] == "fechados":
            if session.get('perfil') == 'tecnico':
                cursor.execute('Select * from chamados WHERE data_fechamento IS NOT NULL ORDER BY data_fechamento DESC')
                chamados = cursor.fetchall()
            else:
                cursor.execute('Select * from chamados WHERE id_usuario = %s AND data_fechamento IS NOT NULL ORDER BY data_fechamento DESC',
                            (session.get('usuario_id'),))
                chamados = cursor.fetchall()
        if request.form['filtro'] == "abertos":
            if session.get('perfil') == 'tecnico':
                if session.get('perfil') == 'tecnico':
                    cursor.execute('Select * from chamados WHERE data_fechamento IS NULL')
                    chamados = cursor.fetchall()
            else:
                cursor.execute('Select * from chamados WHERE id_usuario = %s AND data_fechamento IS NULL',
                            (session.get('usuario_id'),))
                chamados = cursor.fetchall()
        if request.form['filtro'] == "fechamento_desc":
            if session.get('perfil') == 'tecnico':
                cursor.execute('Select * from chamados WHERE data_fechamento IS NOT NULL ORDER BY data_fechamento DESC')
                chamados = cursor.fetchall()
            else:
                cursor.execute('Select * from chamados WHERE id_usuario = %s AND data_fechamento IS NOT NULL ORDER BY data_fechamento DESC',
                            (session.get('usuario_id'),))
                chamados = cursor.fetchall()
        if request.form['filtro'] == "fechamento_crec":
            if session.get('perfil') == 'tecnico':
                cursor.execute('Select * from chamados WHERE data_fechamento IS NOT NULL ORDER BY data_fechamento')
                chamados = cursor.fetchall()
            else:
                cursor.execute('Select * from chamados WHERE id_usuario = %s AND data_fechamento IS NOT NULL ORDER BY data_fechamento',
                            (session.get('usuario_id'),))
                chamados = cursor.fetchall()
        if request.form['filtro'] == "abertura_crec":
            if session.get('perfil') == 'tecnico':
                cursor.execute('Select * from chamados WHERE data_fechamento IS NULL ORDER BY data_abertura')
                chamados = cursor.fetchall()
            else:
                cursor.execute('Select * from chamados WHERE id_usuario = %s AND data_fechamento IS NULL ORDER BY data_abertura',
                            (session.get('usuario_id'),))
                chamados = cursor.fetchall()
        if request.form['filtro'] == "abertura_desc":
            if session.get('perfil') == 'tecnico':
                cursor.execute('Select * from chamados WHERE data_fechamento IS NULL ORDER BY data_abertura DESC')
                chamados = cursor.fetchall()
            else:
                cursor.execute('Select * from chamados WHERE id_usuario = %s AND data_fechamento IS NULL ORDER BY data_abertura DESC',
                            (session.get('usuario_id'),))
                chamados = cursor.fetchall()
    else:
        if session.get('perfil') == 'tecnico':
            cursor.execute('Select * from chamados WHERE data_fechamento IS NULL')
            chamados = cursor.fetchall()
        else:
            cursor.execute('Select * from chamados WHERE id_usuario = %s AND data_fechamento IS NULL',
                        (session.get('usuario_id'),))
            chamados = cursor.fetchall()
    return render_template('chamados.html', chamados=chamados, perfil=session.get('perfil'))


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
        return render_template("user.html", usuarios=usuarios)


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
    cursor.execute('SELECT * FROM usuarios WHERE perfil = %s', ('tecnico',))
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

@app.route('/equipamentos')
def pagina_equipamentos():
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
    cursor.execute('SELECT * FROM equipamentos')
    equipamentos = cursor.fetchall()
    return render_template("equipamentos.html", equipamentos=equipamentos)


@app.route('/cadastro_usuario', methods=['POST', 'GET'],)
def cadastro_usuario():
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

            sql = 'INSERT INTO usuarios (nome, email, senha, perfil, status) values (%s, %s, %s, %s, "inativo")'
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
        

@app.route('/cadastro_equipamento', methods=['POST', 'GET'])
def cadastro_equipamento():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        marca = request.form.get('marca')
        setor = request.form.get('setor')
        conservacao = request.form.get('conservacao')
        
        # Verifica se algum campo está vazio
        if not nome or not marca or not setor or not conservacao:
            return render_template('cadastro_equipamento.html', error='Todos os campos são obrigatórios.')
        
        try:
            cnx = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='chamadosti'
            )
            cursor = cnx.cursor()
            
            # Executa a inserção no banco de dados
            sql = 'INSERT INTO equipamentos (nome, id_setor, marca, conservacao) VALUES (%s, %s, %s, %s)'
            values = (nome, setor, marca, conservacao)
            cursor.execute(sql, values)
            
            cursor.close()
            cnx.commit()
            
            return redirect(url_for('pagina_equipamentos'))
        
        except mysql.connector.Error as e:
            return render_template('cadastro_equipamento.html', error=str(e))
    
    else:  # Se a solicitação não for POST, renderiza a página de cadastro com os setores
        try:
            cnx = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='chamadosti'
            )
            cursor = cnx.cursor()
            
            # Consulta os setores no banco de dados
            cursor.execute('SELECT * FROM setores')
            setores = cursor.fetchall()
            
            cursor.close()
            cnx.close()
            
            return render_template('cadastro_equipamento.html', setores=setores)
        
        except mysql.connector.Error as e:
            return render_template('cadastro_equipamento.html', error=str(e))

    
        
@app.route('/cadastro_chamado', methods=['POST', 'GET'])
def cadastro_chamado():
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'usuario':
        return redirect(url_for('pagina_inicial'))
    
    
    
    if request.method == 'POST':
        try:
            id_usuario = session.get('usuario_id')
            descricao = request.form.get('descricao')
            id_setor = request.form.get('setor')
            
            if not descricao:
                return render_template('cadastro_chamado.html', error='A descrição é obrigatória.')
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

    else:
        try:
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
        except mysql.connector.Error as e:
            return render_template('cadastro_chamado.html', error=str(e))
                


@app.route('/status_usuario/<id>', methods=['GET', 'POST'])
def status_usuario(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    if not id.isdigit:
        return render_template('status_usuario', error='ID inválido')
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = %s;', (id,))
        usuario = cursor.fetchone()
        if usuario[6] == "ativo":
            cursor.execute('UPDATE usuarios SET status = %s WHERE id = %s', ('inativo', id))
            cursor.execute('INSERT INTO status (id_usuario, status, date_modificacao) VALUES (%s, %s, NOW())', (id, 'inativo'))
        else:
            cursor.execute('UPDATE usuarios SET status = %s WHERE id = %s', ('ativo', id))
            cursor.execute('INSERT INTO status (id_usuario, status, date_modificacao) VALUES (%s, %s, NOW())', (id, 'ativo'))
        cursor.close()
        cnx.commit()
        if usuario[4] == "tecnico":
            return redirect(url_for('pagina_tecnicos'))
        else:
            return redirect(url_for('pagina_usuarios'))
    except mysql.connector.Error as e:
        return render_template('excluir-usuario.html', error=str(e))

from flask import request, redirect, url_for, session, render_template
import mysql.connector

@app.route('/status_equipamento/<id>', methods=['Get', 'POST'])
def status_equipamento(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='chamadosti'
        )
        cursor = cnx.cursor()

        cursor.execute('SELECT * FROM equipamentos WHERE id = %s;', (id,))
        equipamento = cursor.fetchone()

        if equipamento is None:
            cursor.close()
            cnx.commit()
            return render_template('equipamentos.html', error='Equipamento não encontrado.')
    except mysql.connector.Error as e:
        return render_template('equipamentos.html', error=str(e))
            
    if request.method == 'POST':
        
            if equipamento[5] == "ativo":
                conservacao = request.form.get('conservacao')
                justificativa = request.form.get('justificativa')
                cursor.execute('UPDATE equipamentos SET status = %s, conservacao = %s, justificativa = %s WHERE id = %s', ('inativo', conservacao, justificativa, id))
                cursor.execute('INSERT INTO status (id_equipamento, status, date_modificacao) VALUES (%s, %s, NOW())', (id, 'inativo'))
                cursor.close()
                cnx.commit()
                return redirect(url_for('pagina_equipamentos'))

            else:
                conservacao = request.form.get('conservacao')
                cursor.execute('UPDATE equipamentos SET status = %s, conservacao = %s, justificativa = %s WHERE id = %s', ('ativo', conservacao, None, id))
                cursor.execute('INSERT INTO status (id_equipamento, status, date_modificacao) VALUES (%s, %s, NOW())', (id, 'ativo'))
                cursor.close()
                cnx.commit()
                return redirect(url_for('pagina_equipamentos'))
    else:
        return render_template('status_equipamento.html', equipamento=equipamento)
    


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
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
        cursor.close()
        cnx.commit()
        return redirect(url_for('pagina_tecnicos'))
    except mysql.connector.Error as e:
        return render_template('tecnicos.html', error=str(e))


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
    if session.get('perfil')=='usuario':
        if session.get('usuario_id')!=id:
            return redirect(url_for('pagina_inicial'))
    if not id.isdigit():
        return render_template('editarusuario/<id>', error='ID inválido.')
    

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
    perfil = session.get('perfil')
    dados_usuario = cursor.fetchone()
    cursor.close()
    cnx.close()

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Valida o input
        if session.get('perfil') == 'tecnico':
            if not nome:
                flash('O nome é obrigatório.')
                return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not email:
            flash('O e-mail é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not senha:
            flash('A senha é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        # Realiza a atualização no banco de dados

        cnx = mysql.connector.connect(host='127.0.0.1',
                                      user='root',
                                      password='',
                                      database='chamadosti')
        cursor = cnx.cursor()
        if session.get('perfil') == 'tecnico':
            sql = 'UPDATE usuarios SET email = %s, senha=%s WHERE id = %s;'
            values = (email, senha, id)
        else:
            sql = 'UPDATE usuarios SET nome = %s, email = %s, senha=%s WHERE id = %s;'
            values = (nome, email, senha, id)
        cursor.execute(sql, values)
        cnx.commit()
        cursor.close()
        cnx.close()

        # Redireciona para a página inicial
        return redirect(url_for('pagina_usuarios'))

    # Exibe o formulário
    return render_template('editarusuario.html', id=id, usuario=dados_usuario, perfil=perfil)

@app.route('/editartecnico/<id>', methods=['GET', 'POST'])
def atualizartecnico(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil')!='tecnico':
        return redirect(url_for('pagina_inicial'))
 # Valida o ID do usuário
    if not id.isdigit():
        return render_template('editarusuario/<id>', error='ID inválido.')
    

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
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Valida o input
        if session.get('perfil') == 'tecnico':
            if not nome:
                flash('O nome é obrigatório.')
                return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not email:
            flash('O e-mail é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        if not senha:
            flash('A senha é obrigatório.')
            return render_template('editarusuario/<id>', dados_usuario=dados_usuario)
        # Realiza a atualização no banco de dados

        cnx = mysql.connector.connect(host='127.0.0.1',
                                      user='root',
                                      password='',
                                      database='chamadosti')
        cursor = cnx.cursor()
        if session.get('perfil') == 'tecnico':
            sql = 'UPDATE usuarios SET nome = %s, email = %s, senha=%s WHERE id = %s;'
            values = (nome, email, senha, id)
        else:
            sql = 'UPDATE usuarios SET email = %s, senha=%s WHERE id = %s;'
            values = (email, senha, id)
        cursor.execute(sql, values)
        cnx.commit()
        cursor.close()
        cnx.close()

        # Redireciona para a página inicial
        return redirect(url_for('pagina_tecnicos'))

    # Exibe o formulário
    return render_template('editartecnico.html', usuario=dados_usuario)

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

@app.route('/editarequipamento/<id>', methods=['GET', 'POST'])
def atualizarequipamento(id):
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
        SELECT * FROM chamados
        WHERE id = %s;
    """, (id,))
    dados_chamado = cursor.fetchone()
    cursor.close()
    cnx.close()

    # Processa o formulário
    if request.method == 'POST':
        try:
            conservacao = request.form.get('conservacao')
            justificativa = request.form.get('justificativa')
            cnx = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='chamadosti'
            )
            cursor = cnx.cursor()
            sql = 'UPDATE equipamentos SET conservacao = %s, justificativa = %sWHERE id = %s;'
            values = (conservacao, justificativa, id)
            cursor.execute(sql, values)
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('pagina_inicial'))
        except mysql.connector.Error as e:
            return render_template('paginainicial.html')
            # Redireciona para a página inicial

    return render_template('editarequipamento.html', id=id, chamado=dados_chamado)

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
    
@app.route('/finalizarchamado/<id>', methods=['GET', 'POST'])
def finalizarchamado(id):
    if not session.get('usuario_id'):
        return redirect(url_for('pagina_login'))
    if session.get('perfil') != 'tecnico':
        return redirect(url_for('pagina_inicial'))

    if not id.isdigit():
        return render_template('editarusuario/<id>', error='ID inválido.')

    # Processa o formulário
    if request.method == 'POST':
        try:
            solucao = request.form.get('solucao')
            cnx = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='chamadosti'
            )
            cursor = cnx.cursor()
            sql = 'UPDATE chamados SET solucao = %s, data_fechamento = NOW()  WHERE id = %s;'
            values = (solucao, id)
            cursor.execute(sql, values)
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('pagina_chamados'))
        except mysql.connector.Error as e:
            return render_template('paginainicial.html')
            # Redireciona para a página inicial

    return render_template('finalizarchamado.html', id=id)



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
        if usuario[6] != "ativo":
            return redirect(url_for('pagina_login'))
        else:
            session['usuario_id'] = usuario[0]
            session['perfil'] = usuario[4]
            return redirect(url_for('pagina_usuarios'))
    else:
        return redirect(url_for('pagina_login'))
        


if __name__ == '__main__':
        app.run(debug=True)
