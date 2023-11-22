from flask import Flask #import de flask

app = Flask(__name__) #indiquer "name" veut dire que notre app prend le nomdu module courant

app.run() #lancement de l'app

#Si on exécute ce code notre app se lance 