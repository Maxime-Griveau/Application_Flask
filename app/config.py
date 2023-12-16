import dotenv #POUR INSTALLER DOTENV IL FAUT FAIRE : pip install python-dotenv
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #appel de notre fichier actuel (os va trouver son chemin à chaque fois pour éviter qu'il ne saute si on le modifie)
dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))#Charge .env en tant que Base_Dir donc .env sera lié à config sans que personne ne puisse savoir d'où provient .env (sécurité)



class Config(): 
    DEBUG = os.environ.get("DEBUG")

    

