from flask import Flask, render_template, send_from_directory, request, Response
import sqlite3
import json
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)

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

@app.route("/login", methods=["POST"])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conn = conexao()
    cur = conn.cursor()
    query = "SELECT nome, senha FROM aluno WHERE nome = %s;"
    cur.execute(query, [nome])
    dados = cur.fetchall()    
    if dados[0][1] == senha:
        x = True
    else:
        x = False
    print(x)
    conn.commit()
    cur.close()
    conn.close()
    return render_template("login.html", flag=x)


@app.route("/move_cadastro", methods=["POST","GET"])
def move_cadastro():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    matricula = request.form.get('matricula')
    print(matricula)
    tipo = request.form.get('tipo')
    conn = conexao()    
    cur = conn.cursor()
    check_matricula = matricula_exists(tipo, matricula, conn, cur)
    if check_matricula:
        flag = check_matricula      
    else:
        flag = check_matricula
        if tipo == 'professor':
            cur.execute("INSERT into aluno (nome, matricula, senha, tipo) VALUES(%s,%s,%s,%s)", (nome, matricula, senha, '1'))
        elif tipo == 'aluno':
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
    print(json_req)
    conn = conexao()
    cur = conn.cursor()
    cur.execute("INSERT into geolocs (idUsuario, lat, long) VALUES(?,?,?)", (id, lat, long))
    conn.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


