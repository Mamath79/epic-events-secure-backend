from dotenv import load_dotenv
import os
import logging

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Définir dynamiquement PYTHONPATH
current_path = os.getcwd()
os.environ["PYTHONPATH"] = current_path

# Désactiver complètement les logs SQLAlchemy
logging.getLogger("sqlalchemy.engine").propagate = False
logging.getLogger("sqlalchemy").propagate = False
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
