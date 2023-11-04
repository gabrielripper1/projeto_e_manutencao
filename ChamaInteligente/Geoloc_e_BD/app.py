from flask import Flask, render_template, request, Response
import sqlite3
import json
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def conexao():
    conn = psycopg2.connect(
        host="db-postgresql-nyc3-48541-do-user-15044691-0.c.db.ondigitalocean.com",
        port='25060',
        database="defaultdb",
        user='doadmin',
        password='AVNS_ve5zp3SIE-Dy_p5nEfh'      
    )
    return conn

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
    print(dados)
    conn.commit()
    cur.close()
    conn.close()
    return render_template("login.html")

@app.route("/move_cadastro", methods=["POST","GET"])
def move_cadastro():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    matricula = request.form.get('matricula')
    print(nome)
    print(senha)
    print(matricula)
    conn = conexao()    
    cur = conn.cursor()
    cur.execute("INSERT into aluno (nome, matricula, senha) VALUES(%s,%s,%s)", (nome, matricula, senha))
    conn.commit()
    cur.close()
    conn.close()

    return render_template('cadastro.html')

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