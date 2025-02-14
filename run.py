from app import create_app
from flask_migrate import upgrade, migrate, init
import os

app = create_app()

PORT = "5000"

if __name__ == "__main__":
    with app.app_context():
        migrations_folder = os.path.join(os.getcwd(), "migrations")
        #db.create_all() 
        # Se não existir a pasta "migrations", inicializa automaticamente
        if not os.path.exists(migrations_folder):
            print("[INFO] Criando diretório de migrations automaticamente...")
            init()

        # Gera uma nova migration automaticamente se houver mudanças
        print("[INFO] Verificando se há mudanças no banco...")
        migrate(message="Automated migration")

        # Aplica as migrations automaticamente ao iniciar
        print("[INFO] Aplicando migrations ao banco de dados...")
        upgrade()
        
    app.run(debug=True, host='0.0.0.0', port=PORT)
