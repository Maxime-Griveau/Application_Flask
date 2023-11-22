import dotenv #POUR INSTALLER DOTENV IL FAUT FAIRE : pip install python-dotenv
import os

version = "version 0.0.1"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))



class Config():
    DEBUG = os.environ.get("DEBUG")
    

