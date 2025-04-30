from app import create_app
from flask_migrate import upgrade, migrate, init
import os

app = create_app()

def run_migrations():
    """Executa as migrations automaticamente ao iniciar."""
    with app.app_context():
        migrations_folder = os.path.join(os.getcwd(), "migrations")

        if not os.path.exists(migrations_folder):
            print("[INFO] Criando diretório de migrations automaticamente...")
            init()

        print("[INFO] Verificando se há mudanças no banco...")
        migrate(message="Automated migration")

        print("[INFO] Aplicando migrations ao banco de dados...")
        upgrade()
        print("[INFO] Migrations aplicadas com sucesso!")

def run_tests():
    """Executa os testes automatizados com SQLite."""
    import pytest
    test_app = create_app(testing=True)  # Usa SQLite
    with test_app.app_context():
        from app import db
        db.create_all()  # Cria tabelas no SQLite em memória
    print("[INFO] Executando testes automatizados...")
    pytest.main(["-q", "--disable-warnings", "tests/"])

def main():
    """Ponto de entrada para execução do servidor."""
    # run_tests()
    run_migrations()
    app.run(debug=True, host=os.getenv("FLASK_RUN_HOST"), port=int(os.getenv("FLASK_RUN_PORT")))

if __name__ == "__main__":
    main()
