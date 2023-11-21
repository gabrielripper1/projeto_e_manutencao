from flask import Flask, render_template, send_from_directory, request, Response, session
import sqlite3
import json
import psycopg2
import os
import datetime
from flask_cors import CORS

app = Flask(__name__)
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
tipo_dict = {'aluno': 1, 'professor': 2}
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
    if tipo_dict[tipo] == 1:
        query = "SELECT nome, senha, id_aluno FROM aluno WHERE nome = %s;"    
        cur.execute(query, [nome])
        dados = cur.fetchall()
        if dados[0][1] == senha:
            x = False
            session["id_usuario"] = dados[0][2]
            query = "SELECT desc_turma, periodo FROM turma WHERE id_aluno = %s;"
            cur.execute(query, [session.get("id_usuario")])
            dados_turmas = cur.fetchall()
            session['dados'] = dados_turmas
            conn.commit()
            cur.close()
            conn.close()            
            return render_template("tela_aluno.html")
        else:
            x = True
            return render_template("login.html", flag=x)

    elif tipo_dict[tipo] == 2:
        query = "SELECT nome, senha, id_professor FROM professor WHERE nome = %s;"    
        cur.execute(query, [nome])
        dados = cur.fetchall()
        if dados[0][1] == senha:
            x = False
            session["id_usuario"] = dados[0][2]
            query = "SELECT desc_turma, periodo, id_turma FROM turma WHERE id_professor = %s;"
            cur.execute(query, [session.get("id_usuario")])
            dados_turmas = cur.fetchall()
            session['dados'] = dados_turmas            
            conn.commit()
            cur.close()
            conn.close()
            return render_template("tela_professor.html")
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
.########..######..########.####.##........#######...######.
.##.......##....##....##.....##..##.......##.....##.##....##
.##.......##..........##.....##..##.......##.....##.##......
.######....######.....##.....##..##.......##.....##..######.
.##.............##....##.....##..##.......##.....##.......##
.##.......##....##....##.....##..##.......##.....##.##....##
.########..######.....##....####.########..#######...######.
"""

@app.route("/use_login", methods=["GET"])
def use_login():
    return send_from_directory("templates", "styles/login.css")
@app.route("/use_basic_style", methods=["GET"])
def use_basic_style():
    return send_from_directory("templates", "styles/style.css")





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

@app.route("/gera_form_cria_turma", methods=["POST", "GET"])
def gera_form_cria_turma():    
    return render_template("tela_professor.html", flag_form=True)

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
    return render_template("tela_professor.html", flag_form=False)

@app.route("/show_turma/<idTurma>", methods=["POST", "GET"])
def show_turma(idTurma):

    conn = conexao()    
    cur = conn.cursor()
    query = "SELECT id_aula, dthr_ini_aula, dthr_fim_aula  FROM aula WHERE id_turma = %s;"
    cur.execute(query, [idTurma])
    aulas_turma = cur.fetchall()        
    conn.commit()
    cur.close()
    conn.close()
    return render_template("turma.html", aulas_turma=aulas_turma)

@app.route("/show_aula/<idAula>", methods=["POST","GET"])
def show_aula(idAula):

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
    return render_template("aula.html")

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

    return render_template("aula.html")

@app.route("/muda_fim_aula", methods=["GET", "POST"])
def muda_fim_aula():
    horario = request.form.get('horario')
    horario_anterior = request.form.get('horario_anterior')    
    horario_novo = horario_anterior + " " + horario + ":00.000"
    
    # conn = conexao()    
    # cur = conn.cursor()      
    # query = "UPDATE public.aluno_aula SET id_presenca_aluno_aula = %s WHERE id_aluno = %s;"
    # cur.execute(query, [presenca_dict[presenca], idAluno])

    return render_template("aula.html")