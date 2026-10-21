from flask import Flask, render_template, request, redirect, url_for
from database import Base, engine, Session
from models import Usuario, Livro

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/usuario/novo", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        if nome and email:
            session = Session()
            usuario = session.query(Usuario).filter_by(email=email)

            if usuario is None:
                session.add(Usuario(nome=nome, email=email))
                session.commit()
            session.close()
            return redirect(url_for("listar_usuarios"))

    return render_template("cadastro.html")


@app.route("/usuarios/listar")
def listar_usuarios():
    session = Session()
    usuarios = session.query(Usuario).order_by(Usuario.nome).all()
    session.close()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/livros/novo", methods=["GET", "POST"])
def new_book():
    session = Session()
    usuarios = session.query(Usuario).order_by(Usuario.nome).all()

    if request.method == "POST":
        titulo = request.form["titulo"]
        usuario_id = request.form.get("usuario_id")

        if titulo and usuario_id:
            usuario = session.query(Usuario).filter_by(id=usuario_id)
            if usuario:
                session.add(Livro(titulo=titulo, usuario_id=usuario.id))
                session.commit()
                session.close()
                return redirect(url_for("listar_livros"))

    session.close()
    return render_template("cadastro_livro.html", usuarios=usuarios)


@app.route("/livros/listar")
def listar_livros():
    session = Session()
    livros = session.query(Livro).order_by(Livro.titulo).all()
    session.close()
    return render_template("livros.html", livros=livros)


if __name__ == "__main__":
    app.run(debug=True)