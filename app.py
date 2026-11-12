from datetime import date, datetime, timedelta
from pathlib import Path
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "troque-esta-chave-em-um-projeto-real"
DB_PATH = Path(__file__).with_name("estoque.db")
DIAS_ALERTA_VALIDADE = 7


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
                data_validade TEXT NOT NULL,
                estoque_minimo INTEGER NOT NULL CHECK (estoque_minimo >= 0),
                data_cadastro TEXT NOT NULL
            )
        """)


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        quantidade_txt = request.form.get("quantidade", "").strip()
        validade = request.form.get("data_validade", "").strip()
        minimo_txt = request.form.get("estoque_minimo", "").strip()

        try:
            quantidade = int(quantidade_txt)
            minimo = int(minimo_txt)
            data_obj = date.fromisoformat(validade)
            if not nome or quantidade < 0 or minimo < 0:
                raise ValueError
        except (ValueError, TypeError):
            flash("Confira os campos. Quantidade e estoque mínimo devem ser números iguais ou maiores que zero.", "erro")
            return render_template("cadastro.html", valores=request.form)

        with conectar() as con:
            con.execute("""
                INSERT INTO produtos (nome, quantidade, data_validade, estoque_minimo, data_cadastro)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, quantidade, data_obj.isoformat(), minimo, date.today().isoformat()))

        flash(f'Produto "{nome}" cadastrado com sucesso!', "sucesso")
        return redirect(url_for("resultados"))

    return render_template("cadastro.html", valores={})


@app.route("/estoque")
def resultados():
    hoje = date.today()
    limite = hoje + timedelta(days=DIAS_ALERTA_VALIDADE)

    with conectar() as con:
        produtos = con.execute("""
            SELECT * FROM produtos
            ORDER BY data_validade ASC, nome COLLATE NOCASE ASC
        """).fetchall()

    itens = []
    for p in produtos:
        validade = date.fromisoformat(p["data_validade"])
        dias = (validade - hoje).days
        perto_validade = 0 <= dias <= DIAS_ALERTA_VALIDADE
        vencido = dias < 0
        estoque_baixo = p["quantidade"] <= p["estoque_minimo"]
        itens.append({
            **dict(p),
            "validade_formatada": validade.strftime("%d/%m/%Y"),
            "perto_validade": perto_validade,
            "vencido": vencido,
            "estoque_baixo": estoque_baixo,
            "dias_validade": dias
        })

    return render_template("estoque.html", produtos=itens, dias_alerta=DIAS_ALERTA_VALIDADE)


@app.route("/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
    # A exclusão é disponibilizada apenas para corrigir cadastros de demonstração.
    with conectar() as con:
        con.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    flash("Produto removido do cadastro.", "sucesso")
    return redirect(url_for("resultados"))


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
