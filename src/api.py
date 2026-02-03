"""

Endpoints:
- `GET /state` -> current game state
- `POST /click` -> JSON body `{ "r": int, "c": int }` to place obstacle and step frog
- `POST /reset` -> reset the game

This file is intentionally small so it can be used during development.
"""
from __future__ import annotations

from flask import Flask, jsonify, request, send_from_directory
from typing import Any, Dict

from src.game_logic import GameLogic
from pathlib import Path

# Base directory (project root) so we can serve the existing Index.html, css, and js
BASE_DIR = Path(__file__).resolve().parents[1]

app = Flask(__name__)

GAME = GameLogic(rows=11, cols=11)


def create_response(payload: Dict[str, Any], status: int = 200):
    resp = jsonify(payload)
    # Allow simple CORS for development so a local JS frontend can call this server
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp, status


@app.route("/state", methods=["GET"])
def state():
    return create_response(GAME.get_state())


@app.route("/click", methods=["POST"])
def click():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return create_response({"error": "expected JSON body"}, status=400)

    r = data.get("r")
    c = data.get("c")
    if not isinstance(r, int) or not isinstance(c, int):
        return create_response({"error": "`r` and `c` must be integers"}, status=400)

    result = GAME.step_after_click(r, c)
    payload = {"result": result, "state": GAME.get_state()}
    return create_response(payload)

@app.route("/reset", methods=["POST"])
def reset():
    GAME.reset()
    return create_response({"state": GAME.get_state()})


@app.route("/", methods=["GET"])
def index():
    # Serve the project's Index.html so opening / runs the existing front-end.
    return send_from_directory(str(BASE_DIR), "Index.html")


@app.route("/css/<path:filename>")
def css_static(filename: str):
    return send_from_directory(str(BASE_DIR / "css"), filename)


@app.route("/js/<path:filename>")
def js_static(filename: str):
    return send_from_directory(str(BASE_DIR / "js"), filename)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(str(BASE_DIR), "favicon.ico")


if __name__ == "__main__":
    # Run in debug mode for development.
    app.run(host="127.0.0.1", port=5000, debug=True)
