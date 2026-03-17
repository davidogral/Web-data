import os
import sqlite3
from datetime import datetime
from typing import Optional

import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask import Flask, redirect, render_template_string, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

# Configurações básicas
DB_PATH = os.environ.get("NEWS_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "news.db"))
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "davi.specia@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "davi123456789")
SESSION_SECRET = os.environ.get("SESSION_SECRET", "dev-secret-change-me")


# ---------- Helpers de dados ----------
def get_conn():
    return sqlite3.connect(DB_PATH)


def ensure_schema(conn: sqlite3.Connection):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            source TEXT,
            link TEXT,
            summary TEXT,
            date TEXT
        )
        """
    )
    conn.commit()


def seed_admin(conn: sqlite3.Connection, email: str, password: str):
    ensure_schema(conn)
    cursor = conn.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return
    password_hash = generate_password_hash(password)
    conn.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
        (email, password_hash, "admin"),
    )
    conn.commit()


def load_news_df() -> pd.DataFrame:
    conn = get_conn()
    ensure_schema(conn)
    df = pd.read_sql_query("SELECT * FROM news", conn)
    conn.close()
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def authenticate(email: str, password: str) -> bool:
    conn = get_conn()
    ensure_schema(conn)
    row = conn.execute(
        "SELECT password_hash, role FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    if not row:
        return False
    password_hash, role = row
    if not check_password_hash(password_hash, password):
        return False
    session["user_email"] = email
    session["role"] = role
    session["logged_at"] = datetime.utcnow().isoformat()
    return True


def current_user_role() -> Optional[str]:
    return session.get("role")


# ---------- Flask + Dash ----------
server = Flask(__name__)
server.secret_key = SESSION_SECRET

# Seed admin user at startup
with get_conn() as conn:
    seed_admin(conn, ADMIN_EMAIL, ADMIN_PASSWORD)


@server.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if authenticate(email, password):
            return redirect(url_for("dash_index"))
        error = "Credenciais inválidas"

    return render_template_string(
        """
        <!doctype html>
        <html lang="pt-BR">
        <head>
            <meta charset="utf-8" />
            <title>Dashboard - Login</title>
            <style>
                body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc;
                       display:flex; align-items:center; justify-content:center; height:100vh; margin:0; }
                form { background:#111827; padding:24px; border-radius:12px; width:320px;
                       box-shadow:0 20px 45px rgba(0,0,0,0.45); }
                label { display:block; margin:10px 0 4px; color:#cbd5e1; }
                input { width:100%; padding:10px; border-radius:8px; border:1px solid #1f2937;
                        background:#0b1324; color:#f8fafc; }
                button { margin-top:14px; width:100%; padding:12px; border:none; border-radius:8px;
                         background:linear-gradient(135deg,#1dd1a1,#0ea5e9); color:#0b1222;
                         font-weight:700; cursor:pointer; }
                .error { color:#f87171; margin-top:10px; }
            </style>
        </head>
        <body>
            <form method="POST">
                <h2>Dashboard BPKnews</h2>
                <label for="email">E-mail</label>
                <input id="email" name="email" type="email" required>
                <label for="password">Senha</label>
                <input id="password" name="password" type="password" required>
                <button type="submit">Entrar</button>
                {% if error %}<div class="error">{{ error }}</div>{% endif %}
            </form>
        </body>
        </html>
        """,
        error=error,
    )


@server.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def protect_dash(dash_app: Dash):
    @dash_app.server.before_request
    def _auth_guard():
        path = request.path
        if path.startswith(dash_app.config.requests_pathname_prefix):
            if current_user_role() != "admin":
                return redirect(url_for("login"))


def create_dash_app(flask_server: Flask) -> Dash:
    dash_app = Dash(
        __name__,
        server=flask_server,
        url_base_pathname="/dashboard/",
        suppress_callback_exceptions=True,
    )
    protect_dash(dash_app)

    df = load_news_df()
    if df.empty:
        df = pd.DataFrame(
            columns=["title", "category", "source", "link", "summary", "date"]
        )

    category_counts = df.groupby("category").size().reset_index(name="count")
    timeline = (
        df.groupby("date").size().reset_index(name="count")
        if not df.empty
        else pd.DataFrame(columns=["date", "count"])
    )

    dash_app.layout = html.Div(
        style={"backgroundColor": "#0b1222", "color": "#f8fafc", "padding": "24px"},
        children=[
            html.H1("Dashboard BPKnews", style={"marginBottom": "8px"}),
            html.P("Somente admins autenticados podem visualizar.", style={"color": "#9fb3c8"}),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Notícias por categoria"),
                            dcc.Graph(
                                figure={
                                    "data": [
                                        {
                                            "x": category_counts["category"],
                                            "y": category_counts["count"],
                                            "type": "bar",
                                            "marker": {"color": "#1dd1a1"},
                                        }
                                    ],
                                    "layout": {"paper_bgcolor": "#0b1222", "plot_bgcolor": "#0b1222", "font": {"color": "#f8fafc"}},
                                }
                            ),
                        ],
                        style={"flex": "1", "padding": "12px", "background": "#111827", "borderRadius": "12px"},
                    ),
                    html.Div(
                        [
                            html.H3("Linha do tempo de publicações"),
                            dcc.Graph(
                                figure={
                                    "data": [
                                        {
                                            "x": timeline["date"],
                                            "y": timeline["count"],
                                            "type": "scatter",
                                            "mode": "lines+markers",
                                            "marker": {"color": "#0ea5e9"},
                                        }
                                    ],
                                    "layout": {"paper_bgcolor": "#0b1222", "plot_bgcolor": "#0b1222", "font": {"color": "#f8fafc"}},
                                }
                            ),
                        ],
                        style={"flex": "1", "padding": "12px", "background": "#111827", "borderRadius": "12px"},
                    ),
                ],
                style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
            ),
            html.Div(
                [
                    html.H3("Total de notícias"),
                    html.Div(
                        f"{len(df)} registros armazenados",
                        style={
                            "padding": "12px",
                            "background": "#111827",
                            "borderRadius": "12px",
                            "marginTop": "6px",
                        },
                    ),
                ],
                style={"marginTop": "16px"},
            ),
            html.Div(
                html.A("Sair", href="/logout", style={"color": "#f87171"}),
                style={"marginTop": "12px"},
            ),
        ],
    )
    return dash_app


dash_app = create_dash_app(server)


@server.route("/")
def dash_index():
    if current_user_role() != "admin":
        return redirect(url_for("login"))
    return redirect("/dashboard/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    server.run(host="0.0.0.0", port=port, debug=True)
