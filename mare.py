from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

import urllib3
import requests
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

app = Flask(__name__)
CORS(app)

BASE_URL = "https://tabuamare.api.br/api/v2"

# chave de api - necessita de conta no Tabua de Maré
# https://tabuamare.api.br/
API_KEY = os.getenv("api_key")

print("API_KEY carregada:", bool(API_KEY))

def consultar_mare(endpoint, params=None):

    headers = {
        "Accept":"application/json"
    }

    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=15,
        verify=False
    )

    print("URL: ", response.url)
    print("STATUS: ", response.status_code)
    print("RESPOSTA: ", response.text)

    response.raise_for_status()

    return response.json()

# rota estado
@app.route("/api/mare/estados", methods = ["GET"])
def estados():

    try:
        dados = consultar_mare("states")

        return jsonify(dados)

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e)
        }), 500 

# rota portos ma
@app.route("/api/mare/portos/ma", methods = ["GET"])
def portos_ma():

    try:
        dados = consultar_mare("harbor_names/ma")

        return jsonify(dados)
    
    except requests.exceptions.RequestException as e:

        return jsonify({
            "error": str(e)
        }), 500

# rota id
@app.route("/api/mare/porto/<ids>", methods = ["GET"])
def portos(ids):

    try:
        dados = consultar_mare(f"harbors/{ids}")

        return jsonify(dados)

    except requests.exceptions.RequestException as e:

        return jsonify({
            "error": str(e)
        }), 500

# tabua maré
@app.route("/api/mare/tabua/<harbor>/<int:month>/<days>",
           methods = ["GET"])
def tabua_mare(harbor, month, days):

    try:
        # se mes é valido
        if month < 1 or month > 12:

            return jsonify({
                "error": "O mês deve estar entre 1 e 12."
            }), 400

        dias_formatados = f"[{days}]"

        endpoint = (
            f"tabua-mare/"
            f"{harbor}/"
            f"{month}/"
            f"{dias_formatados}"
        )

        dados = consultar_mare(endpoint)

        return jsonify(dados)

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e)
        }), 500

# mare São Luís
@app.route("/api/mare/sao-luis", methods=["GET"])
def sao_luis():

    try:
        # harbor = request.args.get("harbor")
        month = request.args.get("month", type=int)
        days = request.args.get("days")

        # if not harbor:
        #     return jsonify({
        #         "error": "Informe o Harbor"
        #     })

        if not month:
            return jsonify({
                "error": "Informe o mês"
            })

        if not days:
            return jsonify({
                "error": "Informe o dia"
            })

        if month < 1 or month > 12:
        
            return jsonify({
                "error": "O mês deve estar entre 1 e 12."
            }), 400

        harbor = "ma01"

        dias_formatados = f"[{days}]"

        endpoint = (
            f"tabua-mare/"
            f"{harbor}/"
            f"{month}/"
            f"{dias_formatados}"
        )

        dados = consultar_mare(endpoint)

        return jsonify({
            "cidade":"Sao Luis",
            "harbor":harbor,
            "mes":month,
            "dias":days,
            "dados":dados
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

# portos
# http://localhost:5000/api/mare/portos/ma

# http://localhost:5000/api/mare/sao-luis?month=9&days=24
