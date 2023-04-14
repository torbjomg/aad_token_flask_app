import os
import uuid
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
import msal
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.environ.get("AAD_CLIENT_ID")
TENANT_ID = os.environ.get("AAD_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/"
SCOPE = ["https://graph.microsoft.com/User.Read"]
SESSION_KEY = "user"

@app.route("/")
def index():
    if not session.get(SESSION_KEY):
        return redirect(url_for("login"))
    return render_template("token.html", token=session[SESSION_KEY]["access_token"])

@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(state=session["state"])
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def authorized():
    if request.args.get("state", "") != session.get("state"):
        return "State does not match", 400
    if "error" in request.args:
        return request.args.get("error") + ": " + request.args.get("error_description")

    result = _build_msal_app().acquire_token_by_authorization_code(
        request.args["code"],
        scopes=SCOPE,
        redirect_uri=url_for("authorized", _external=True)
    )

    if "error" in result:
        return result["error"] + ": " + result["error_description"]

    session[SESSION_KEY] = result
    return redirect(url_for("index"))

def _build_auth_url(scope=None, state=None):
    return _build_msal_app().get_authorization_request_url(
        SCOPE,
        state=state,
        redirect_uri=url_for("authorized", _external=True)
    )

def _build_msal_app():
    return msal.PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY, token_cache=None)

if __name__ == "__main__":
    app.run(debug=True, port=1234)
