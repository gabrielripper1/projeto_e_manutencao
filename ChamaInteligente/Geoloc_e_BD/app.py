from flask import Flask, render_template, request, Response
import sqlite3
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/")
def index():
    conn = sqlite3.connect(r"C:\Users\gabri\AppData\Roaming\DBeaverData\workspace6\General\SQL\gps")
    cur = conn.cursor()
    dados = cur.execute("Select * FROM geolocs")
    #conn.commit()
    return render_template("index.html", dados=dados)


@app.route("/SalvarLocalizacao", methods=["POST"])
def post():
    json_req = request.get_json()

    lat = json_req["latitude"]
    long = json_req["longitude"]
    id = json_req["id"]
    print(json_req)
    conn = sqlite3.connect(r"C:\Users\gabri\AppData\Roaming\DBeaverData\workspace6\General\SQL\gps")
    cur = conn.cursor()
    cur.execute("INSERT into geolocs (idUsuario, lat, long) VALUES(?,?,?)", (id, lat, long))
    conn.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}