from flask_auth import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Cria o banco de dados automaticamente ao iniciar
    app.run(debug=True)
