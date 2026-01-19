import os
from flask import Flask, request, jsonify
from redis import Redis
from flasgger import Swagger
from functools import wraps

app = Flask(__name__)
swagger = Swagger(app)
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
ADMIN_KEY = os.getenv("ADMIN_KEY", "default_key")

APP_PORT = int(os.getenv("APP_PORT", 5000))
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_key = request.headers.get("Authorization")
        if not auth_key or auth_key != ADMIN_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# Endpoint: Service de recherche
@app.route('/search', methods=['GET'])
@require_auth
def search_quotes():
    """
    Rechercher des citations par mot-clé
    ---
    security:
      - APIKeyAuth: []
    parameters:
      - name: keyword
        in: query
        required: true
        type: string
    responses:
      200:
        description: Liste des citations correspondantes
    """
    keyword = request.args.get("keyword")

    if not keyword:
        return jsonify({"error": "Mot-clé requis"}), 400

    members = redis_client.smembers("quotes")
    filtered_quotes = []
    for member in members:
        quote_object = redis_client.hgetall(member)
        quote = quote_object.get("quote","")
        if keyword.lower() in quote.lower():
            filtered_quotes.append(quote)
    return jsonify(filtered_quotes), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT)