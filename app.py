import json

from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

from src.services.ai import AI


load_dotenv('.env')
app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/")
def hello_world():
    return jsonify("Hello, World!")

@app.post('/api/get-big-o')
@cross_origin(supports_credentials=True)
def get_big_o():
    req = request.get_json()
    if 'code' not in req:
        return Response("Missing required parameter 'code'", status=422)
    if 'model' not in req:
        model = "claude-opus-4-20250514"
    else:
        model = req['model']
    code = req['code']

    
    llm_client= AI()
    big_o_data = llm_client.get_big_o(code,model)
    response = json.dumps(big_o_data)
    return Response(response, status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run()