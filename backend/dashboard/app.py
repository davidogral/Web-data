import os
import sqlite3
from datetime import datetime
from typing import Optional

import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask import Flask, redirect, render_template_string, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from backend.scraper.storage import save_news_to_db

# Configurações básicas
DB_PATH = os.environ.get("NEWS_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "news.db"))
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "davi.specia@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "davi123456789")
SESSION_SECRET = os.environ.get("SESSION_SECRET", "dev-secret-change-me")
FRONTEND_HTML = os.environ.get("FRONTEND_HTML", os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "index.html"))


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
    seed_news_if_empty(conn)
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


def seed_news_if_empty(conn: sqlite3.Connection):
    cursor = conn.execute("SELECT COUNT(*) FROM news")
    count = cursor.fetchone()[0]
    if count > 0:
        return
    if os.path.exists(FRONTEND_HTML):
        html_content = open(FRONTEND_HTML, "r", encoding="utf-8").read()
        save_news_to_db(html_content, db_path=DB_PATH)
    else:
        conn.commit()


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
        external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"],
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
    source_counts = (
        df.groupby("source").size().reset_index(name="count").sort_values("count", ascending=False)
        if not df.empty
        else pd.DataFrame(columns=["source", "count"])
    )

    card_style = {
        "background": "#0f172a",
        "borderRadius": "14px",
        "padding": "16px",
        "boxShadow": "0 18px 40px -20px rgba(0,0,0,0.6)",
        "border": "1px solid rgba(255,255,255,0.06)",
    }
    title_style = {"margin": "0 0 8px 0", "letterSpacing": "-0.02em", "fontWeight": "700"}

    dash_app.layout = html.Div(
        style={
            "backgroundColor": "#0b1222",
            "color": "#f8fafc",
            "padding": "20px",
            "fontFamily": "Inter, sans-serif",
            "minHeight": "100vh",
            "background": "radial-gradient(circle at 10% 20%, rgba(29, 209, 161, 0.08), transparent 30%), radial-gradient(circle at 80% 0%, rgba(245, 158, 11, 0.08), transparent 30%), #0b1222",
        },
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.P("BPKnews • Dashboard", style={"color": "#9fb3c8", "margin": 0, "fontWeight": "600"}),
                            html.H1("Visão Geral de Notícias", style={"margin": "4px 0 0 0", "letterSpacing": "-0.01em"}),
                        ]
                    ),
                    html.Div(
                        [
                            html.A("Portal", href="/", style={"color": "#1dd1a1", "marginRight": "12px", "fontWeight": "700"}),
                            html.A("Sair", href="/logout", style={"color": "#f87171", "fontWeight": "700"}),
                        ]
                    ),
                ],
                style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "18px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Total de notícias", style={"color": "#9fb3c8", "margin": 0}),
                            html.H2(str(len(df)), style={"margin": "4px 0 0 0"}),
                        ],
                        style=card_style,
                    ),
                    html.Div(
                        [
                            html.P("Categorias únicas", style={"color": "#9fb3c8", "margin": 0}),
                            html.H2(str(category_counts.shape[0]), style={"margin": "4px 0 0 0"}),
                        ],
                        style=card_style,
                    ),
                    html.Div(
                        [
                            html.P("Fontes únicas", style={"color": "#9fb3c8", "margin": 0}),
                            html.H2(str(source_counts.shape[0]), style={"margin": "4px 0 0 0"}),
                        ],
                        style=card_style,
                    ),
                ],
                style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit,minmax(200px,1fr))", "gap": "12px", "marginBottom": "16px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Notícias por categoria", style=title_style),
                            dcc.Graph(
                                figure={
                                    "data": [
                                        {
                                            "x": category_counts["category"],
                                            "y": category_counts["count"],
                                            "type": "bar",
                                            "marker": {"color": "#1dd1a1", "line": {"color": "#0ea5e9", "width": 1}},
                                        }
                                    ],
                                    "layout": {
                                        "paper_bgcolor": "#0f172a",
                                        "plot_bgcolor": "#0f172a",
                                        "font": {"color": "#f8fafc"},
                                        "height": 320,
                                        "margin": {"l": 40, "r": 10, "t": 10, "b": 40},
                                    },
                                }
                            ),
                        ],
                        style=card_style,
                    ),
                    html.Div(
                        [
                            html.H3("Linha do tempo", style=title_style),
                            dcc.Graph(
                                figure={
                                    "data": [
                                        {
                                            "x": timeline["date"],
                                            "y": timeline["count"],
                                            "type": "scatter",
                                            "mode": "lines+markers",
                                            "marker": {"color": "#0ea5e9", "size": 9},
                                        }
                                    ],
                                    "layout": {
                                        "paper_bgcolor": "#0f172a",
                                        "plot_bgcolor": "#0f172a",
                                        "font": {"color": "#f8fafc"},
                                        "height": 320,
                                        "margin": {"l": 40, "r": 10, "t": 10, "b": 40},
                                    },
                                }
                            ),
                        ],
                        style=card_style,
                    ),
                    html.Div(
                        [
                            html.H3("Top fontes", style=title_style),
                            dcc.Graph(
                                figure={
                                    "data": [
                                        {
                                            "x": source_counts["count"],
                                            "y": source_counts["source"],
                                            "type": "bar",
                                            "orientation": "h",
                                            "marker": {"color": "#f59e0b", "line": {"color": "#1dd1a1", "width": 1}},
                                        }
                                    ],
                                    "layout": {
                                        "paper_bgcolor": "#0f172a",
                                        "plot_bgcolor": "#0f172a",
                                        "font": {"color": "#f8fafc"},
                                        "height": 320,
                                        "margin": {"l": 120, "r": 10, "t": 10, "b": 40},
                                    },
                                }
                            ),
                        ],
                        style=card_style,
                    ),
                ],
                style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit,minmax(320px,1fr))", "gap": "16px"},
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
