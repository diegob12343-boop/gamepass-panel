from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="static")
CORS(app)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
ROBLOX_API_KEY  = os.environ.get("ROBLOX_API_KEY", "")

# ─── Serve o painel ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    # Tenta servir da pasta static, se não existir serve da raiz
    static_path = os.path.join(app.root_path, "static", "index.html")
    root_path = os.path.join(app.root_path, "index.html")
    if os.path.exists(static_path):
        return send_from_directory("static", "index.html")
    elif os.path.exists(root_path):
        return send_from_directory(app.root_path, "index.html")
    return "Painel não encontrado. Verifique se o index.html está na pasta static.", 404

# ─── Login ─────────────────────────────────────────────────────────────────────
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    if data.get("password") == ADMIN_PASSWORD:
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Senha incorreta"}), 401

# ─── Pegar userId pelo username ────────────────────────────────────────────────
@app.route("/api/get-user", methods=["POST"])
def get_user():
    data = request.json or {}
    username = data.get("username", "").strip()
    if not username:
        return jsonify({"ok": False, "error": "Username vazio"}), 400

    try:
        r = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            json={"usernames": [username], "excludeBannedUsers": False},
            timeout=10
        )
        result = r.json()
        users = result.get("data", [])
        if not users:
            return jsonify({"ok": False, "error": f"Jogador '{username}' não encontrado"}), 404
        user = users[0]
        return jsonify({"ok": True, "userId": user["id"], "displayName": user["displayName"]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ─── Conceder GamePass ─────────────────────────────────────────────────────────
@app.route("/api/grant", methods=["POST"])
def grant():
    data = request.json or {}
    user_id  = data.get("userId")
    pass_id  = data.get("passId")
    universe_id = data.get("universeId")

    if not all([user_id, pass_id, universe_id]):
        return jsonify({"ok": False, "error": "Dados incompletos"}), 400

    if not ROBLOX_API_KEY:
        return jsonify({"ok": False, "error": "ROBLOX_API_KEY não configurada no servidor"}), 500

    url = f"https://apis.roblox.com/game-passes/v1/games/{universe_id}/game-passes/{pass_id}/users/{user_id}"

    try:
        r = requests.post(
            url,
            headers={
                "x-api-key": ROBLOX_API_KEY,
                "Content-Type": "application/json"
            },
            timeout=10
        )

        if r.status_code == 200:
            return jsonify({"ok": True, "message": "GamePass concedida com sucesso!"})
        elif r.status_code == 409:
            return jsonify({"ok": True, "message": "Jogador já possui essa GamePass."})
        else:
            body = r.text
            return jsonify({"ok": False, "error": f"Erro Roblox ({r.status_code}): {body}"}), 400

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ─── Start ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
