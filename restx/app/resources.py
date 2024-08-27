import io
import base64
from flask import abort
from flask_cors import CORS
from flask_restx import Resource
from flask_restx import reqparse
from werkzeug.middleware.proxy_fix import ProxyFix
from app.utils.sdxl import init_pipe, generate_sapna
from app import api
from app import app


pipe = init_pipe()

app.wsgi_app = ProxyFix(app.wsgi_app)

CORS(app)


prompt_parser = reqparse.RequestParser()
prompt_parser.add_argument("prompt", type=str, location="json", required=True)


@api.route("/sapna")
class Predict(Resource):
    @api.expect(prompt_parser, validate=True)
    @api.doc(description="predict using base64")
    def post(self):
        prompt = prompt_parser.parse_args().get("prompt")
        prompt = "Realistic portrait ,a futuristic Indian "+ prompt +" talking to his floating holographic ai assistant, 8k"
        img64 = generate_sapna(prompt, pipe)
        return {"image": img64}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
