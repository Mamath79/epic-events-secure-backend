from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Définir dynamiquement PYTHONPATH
current_path = os.getcwd()
os.environ["PYTHONPATH"] = current_path

print(f"✅ PYTHONPATH défini sur : {os.environ['PYTHONPATH']}")