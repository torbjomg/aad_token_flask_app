import json
import os
import uuid
from flask import Flask, redirect, url_for, session, request, render_template
import msal
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.environ.get("AAD_CLIENT_ID")
TENANT_ID = os.environ.get("AAD_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/"
SCOPE = ["https://sparebank1-fremtind-sandbox.snowflakecomputing.com/session:role-any"]
SESSION_KEY = "user"
REDIRECT_URI = "http://localhost:1234/redirect"


@app.route("/")
def index():
    if not session.get(SESSION_KEY):
        return redirect(url_for("login"))

    return render_template(
        "token.html",
        token=json.dumps(session[SESSION_KEY], indent=4, separators=(",\n", ":\n")),
    )


@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(state=session["state"])
    return redirect(auth_url)


@app.route("/redirect")
def authorized():
    if request.args.get("state", "") != session.get("state"):
        return "State does not match", 400
    if "error" in request.args:
        return f"{request.args.get('error')}: {request.args.get('error_description')}"

    result = _build_msal_app().acquire_token_by_authorization_code(
        request.args["code"],
        scopes=SCOPE,
        redirect_uri=url_for("authorized", _external=True),
    )

    if "error" in result:
        return f"{result['error']}: {result['error_description']}"

    session[SESSION_KEY] = result
    return redirect(url_for("index"))


def _build_auth_url(scope=None, state=None):
    return _build_msal_app().get_authorization_request_url(
        SCOPE, state=state, redirect_uri=REDIRECT_URI
    )


def _build_msal_app():
    return msal.PublicClientApplication(
        client_id=CLIENT_ID, authority=AUTHORITY, token_cache=None
    )


if __name__ == "__main__":
    app.run(debug=False, port=1234)
