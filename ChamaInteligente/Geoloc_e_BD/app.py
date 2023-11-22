from flask import Flask, render_template, send_from_directory, request, Response, session
import sqlite3
import json
import psycopg2
import os
import datetime
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
app.secret_key = 'chave_secreta'
CORS(app)

"""
..######...#######..##....##.########.##.....##....###.....#######.
.##....##.##.....##.###...##.##........##...##....##.##...##.....##
.##.......##.....##.####..##.##.........##.##....##...##..##.....##
.##.......##.....##.##.##.##.######......###....##.....##.##.....##
.##.......##.....##.##..####.##.........##.##...#########.##.....##
.##....##.##.....##.##...###.##........##...##..##.....##.##.....##
..######...#######..##....##.########.##.....##.##.....##..#######.
"""
TIPO_DICT = {'aluno': 1, 'professor': 2}
TIPO_USER = 0
presenca_dict = {'ausente': 0, 'presente': 1, 'abono':2}

def conexao():
    conn = psycopg2.connect(
        host="db-postgresql-nyc3-48541-do-user-15044691-0.c.db.ondigitalocean.com",
        port='25060',
        database="defaultdb",
        user='doadmin',
        password='AVNS_ve5zp3SIE-Dy_p5nEfh'      
    )
    return conn




"""
....###.....######..########..######...######...#######.
...##.##...##....##.##.......##....##.##....##.##.....##
..##...##..##.......##.......##.......##.......##.....##
.##.....##.##.......######....######...######..##.....##
.#########.##.......##.............##.......##.##.....##
.##.....##.##....##.##.......##....##.##....##.##.....##
.##.....##..######..########..######...######...#######.
"""

def matricula_exists(tipo, matricula, conn, cur):
    query = "SELECT matricula FROM "+tipo+" WHERE matricula = %s;"
    cur.execute(query, [matricula])
    dados = cur.fetchall()
    x = True
    if len(dados) == 0:
        x = False
    return x


@app.route("/")
def index():    
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    tipo = request.form.get('tipo')
    conn = conexao()
    cur = conn.cursor()
    
    if TIPO_DICT[tipo] == 1:
        query = "SELECT nome, senha, id_aluno FROM aluno WHERE nome = %s;"    
        cur.execute(query, [nome])
        dados = cur.fetchall()
        if dados[0][1] == senha:
            x = False
            session["id_usuario"] = dados[0][2]
            query = "SELECT cod_disciplina, desc_turma, periodo, aluno_turma.id_turma FROM aluno_turma INNER JOIN turma ON aluno_turma.id_turma = turma.id_turma WHERE id_aluno = %s;"
            cur.execute(query, [session.get("id_usuario")])
            dados_turmas = cur.fetchall()
            session['dados'] = dados_turmas
            global TIPO_USER
            TIPO_USER = 1
            session['TIPO_USER'] = TIPO_USER
            conn.commit()
            cur.close()
            conn.close()            
            return render_template("turma.html")
        else:
            x = True
            return render_template("login.html", flag=x)

    elif TIPO_DICT[tipo] == 2:
        query = "SELECT nome, senha, id_professor FROM professor WHERE nome = %s;"    
        cur.execute(query, [nome])
        dados = cur.fetchall()
        if dados[0][1] == senha:
            x = False
            session["id_usuario"] = dados[0][2]
            query = "SELECT cod_disciplina, desc_turma, periodo, id_turma FROM turma WHERE id_professor = %s;"
            cur.execute(query, [session.get("id_usuario")])
            dados_turmas = cur.fetchall()
            session['dados'] = dados_turmas
            TIPO_USER = 2
            session['TIPO_USER'] = TIPO_USER
            conn.commit()
            cur.close()
            conn.close()
            return render_template("turma.html")
        else:
            x = True
            return render_template("login.html", flag=x)
      
    
    
    


@app.route("/move_cadastro", methods=["POST","GET"])
def move_cadastro():
    return render_template("cadastro.html")

@app.route("/move_latlong", methods=["POST","GET"])
def move_latlong():
    return render_template("geolocs.html")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    matricula = request.form.get('matricula')    
    tipo = request.form.get('tipo')
    conn = conexao()    
    cur = conn.cursor()
    check_matricula = matricula_exists(tipo, matricula, conn, cur)
    if check_matricula:
        flag = check_matricula      
    else:
        flag = check_matricula
        if tipo == 'aluno':
            cur.execute("INSERT into aluno (nome, matricula, senha, tipo) VALUES(%s,%s,%s,%s)", (nome, matricula, senha, '1'))
        elif tipo == 'professor':
            cur.execute("INSERT into professor (nome, matricula, senha, tipo) VALUES(%s,%s,%s,%s)", (nome, matricula, senha, '2'))    
    conn.commit()
    cur.close()
    conn.close()
    return render_template('cadastro.html', flag=flag)



"""
..######...########..#######..##........#######...######...######.
.##....##..##.......##.....##.##.......##.....##.##....##.##....##
.##........##.......##.....##.##.......##.....##.##.......##......
.##...####.######...##.....##.##.......##.....##.##........######.
.##....##..##.......##.....##.##.......##.....##.##.............##
.##....##..##.......##.....##.##.......##.....##.##....##.##....##
..######...########..#######..########..#######...######...######.
"""
@app.route("/geolocs")
def geo_locs():
    conn = conexao()
    cur = conn.cursor()
    dados = cur.execute("Select * FROM geolocs")
    #conn.commit()
    return render_template("geolocs.html", dados=dados)


@app.route("/SalvarLocalizacao", methods=["POST"])
def post():
    json_req = request.get_json()

    lat = json_req["latitude"]
    long = json_req["longitude"]
    id = json_req["id"]    
    conn = conexao()
    cur = conn.cursor()
    cur.execute("INSERT into geolocs (idUsuario, lat, long) VALUES(?,?,?)", (id, lat, long))
    conn.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


"""
.########.##.....##.########..##.....##....###...
....##....##.....##.##.....##.###...###...##.##..
....##....##.....##.##.....##.####.####..##...##.
....##....##.....##.########..##.###.##.##.....##
....##....##.....##.##...##...##.....##.#########
....##....##.....##.##....##..##.....##.##.....##
....##.....#######..##.....##.##.....##.##.....##
"""


@app.route("/cria_turma", methods=["POST", "GET"])
def cria_turma():
    cod_disciplina = request.form.get('cod_disciplina')
    periodo = request.form.get('periodo')
    desc_turma = request.form.get('desc_turma')
    id_professor = session.get("id_usuario")   

    conn = conexao()    
    cur = conn.cursor()

    cur.execute("INSERT into turma (desc_turma, cod_disciplina, periodo, id_professor) VALUES(%s,%s,%s,%s)", (desc_turma, cod_disciplina, periodo, int(id_professor)))

    query = "SELECT desc_turma, periodo, id_turma FROM turma WHERE id_professor = %s;"
    cur.execute(query, [session.get("id_usuario")])
    dados_turmas = cur.fetchall()
    session['dados'] = dados_turmas
    conn.commit()
    cur.close()
    conn.close()
    return render_template("turma.html", flag_form=False)

# @app.route("/show_turma/<idTurma>", methods=["POST", "GET"])
# def show_turma(idTurma):

#     conn = conexao()
#     cur = conn.cursor()
#     query = "SELECT id_aula, dthr_ini_aula, dthr_fim_aula FROM aula WHERE id_turma = %s;"
#     cur.execute(query, [idTurma])
#     aulas_turma = cur.fetchall()
#     conn.commit()
#     cur.close()
#     conn.close()

#     return render_template("aula.html", aulas_turma=aulas_turma)



"""
....###....##.....##.##..........###...
...##.##...##.....##.##.........##.##..
..##...##..##.....##.##........##...##.
.##.....##.##.....##.##.......##.....##
.#########.##.....##.##.......#########
.##.....##.##.....##.##.......##.....##
.##.....##..#######..########.##.....##
"""

@app.route("/show_aula/<idTurma>", methods=["POST","GET"])
def show_aula(idTurma):

    conn = conexao()
    cur = conn.cursor()
    query = "SELECT desc_turma, id_aula, dthr_ini_aula, dthr_fim_aula FROM aula INNER JOIN turma ON turma.id_turma = aula.id_turma WHERE turma.id_turma = %s;"
    cur.execute(query, [idTurma])
    alunos_aula = cur.fetchall()
    if len(alunos_aula) == 0:
        alunos_aula = ['']
    status_aulas = []    
    for aula in alunos_aula:
        tempo_agora = datetime.datetime.now()        
        if aula[2] <= tempo_agora and (aula[3] >= tempo_agora):
            status_aulas.append(1)
        else:
            status_aulas.append(0)             
    session['dados'] = alunos_aula
    session['TIPO_USER'] = TIPO_USER
    conn.commit()
    cur.close()
    conn.close()
    return render_template("aula.html", status_aulas=status_aulas)


@app.route("/show_alunos/<idAula>", methods=["POST","GET"])
def show_alunos(idAula):

    conn = conexao()
    cur = conn.cursor()
    query = "SELECT aluno.nome, aluno.id_aluno, aluno_aula.id_presenca_aluno_aula, aula.dthr_fim_aula  FROM aluno INNER JOIN aluno_aula ON aluno.id_aluno = aluno_aula.id_aluno INNER JOIN aula ON aluno_aula.id_aula = aula.id_aula WHERE aluno_aula.id_aula = %s;"
    cur.execute(query, [idAula])
    alunos_aula = cur.fetchall()
    session['dados'] = alunos_aula
    session['idAula'] = idAula
    
    conn.commit()
    cur.close()
    conn.close()   
    return render_template("lista_alunos.html")

@app.route("/muda_presenca", methods=["GET", "POST"])
def muda_presenca():
    presenca = request.form.get('presenca')
    idAluno = request.form.get('idAluno')
    idAula = session.get("idAula")
    
    conn = conexao()    
    cur = conn.cursor()      
    query = "UPDATE public.aluno_aula SET id_presenca_aluno_aula = %s WHERE id_aluno = %s;"
    cur.execute(query, [presenca_dict[presenca], idAluno])
    query = "SELECT aluno.nome, aluno.id_aluno, aluno_aula.id_presenca_aluno_aula  FROM aluno INNER JOIN aluno_aula ON aluno.id_aluno = aluno_aula.id_aluno WHERE aluno_aula.id_aula = %s;"
    cur.execute(query, [idAula])
    alunos_aula = cur.fetchall()
    session['dados'] = alunos_aula
    conn.commit()
    cur.close()
    conn.close() 

    return render_template("lista_alunos.html")

@app.route("/move_cria_chamada/<idTurma>", methods=["GET", "POST"])
def move_cria_chamada(idTurma):
    conn = conexao()    
    cur = conn.cursor()
    query = "SELECT desc_turma FROM turma WHERE id_turma = %s;"
    cur.execute(query, [idTurma])
    desc_turma = cur.fetchall()[0][0]    
    return render_template("iniciar_chamada.html", idTurma=idTurma, desc_turma=desc_turma)

@app.route("/cria_chamada", methods=["GET", "POST"])
def cria_chamada():
    data_ini = request.form.get('data_ini')
    hora_ini = request.form.get('hora_ini')
    data_fim = request.form.get('data_fim')
    hora_fim = request.form.get('hora_fim')
    idTurma = request.form.get('idTurma')
    geoloc = request.form.get('geoloc')
    
    horario_inico = data_ini + " " + hora_ini + ":00.000"
    horario_fim = data_fim + " " + hora_fim + ":00.000"

    conn = conexao()    
    cur = conn.cursor()
    
    cur.execute("INSERT into aula (dthr_ini_aula, dthr_fim_aula, local_aula, id_turma) VALUES(%s,%s,%s,%s)", (horario_inico, horario_fim, geoloc, idTurma))

    query = "SELECT id_aula FROM aula WHERE dthr_ini_aula = %s AND dthr_fim_aula = %s AND id_turma = %s;"
    cur.execute(query, [horario_inico, horario_fim, idTurma])
    idAula = cur.fetchall() 
    
    query = "SELECT id_aluno FROM aluno_turma WHERE id_turma = %s;"
    cur.execute(query, [idTurma])
    alunos_na_turma = cur.fetchall()       

    for aluno in alunos_na_turma:        
        cur.execute("INSERT into aluno_aula (id_aluno, id_aula, id_presenca_aluno_aula) VALUES(%s,%s,%s)", (aluno[0], idAula[0][0], 0))
        
    

    conn.commit()
    cur.close()
    conn.close()

    return render_template("turma.html")


