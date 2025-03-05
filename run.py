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
    """Executa os testes automatizados antes de iniciar o servidor."""
    import pytest
    print("[INFO] Aplicando migrations no banco de dados de testes...")
    with app.app_context():
        upgrade()  # Aplica as migrations no banco de dados de testes
    print("[INFO] Executando testes automatizados...")
    pytest.main(["-q", "--disable-warnings", "tests/"])

def main():
    """Ponto de entrada para execução do servidor."""
    run_tests()
    run_migrations()
    app.run(debug=True, host=os.getenv("FLASK_RUN_HOST","0.0.0.0"), port=int(os.getenv("FLASK_RUN_PORT", 5000)))

if __name__ == "__main__":
    main()
