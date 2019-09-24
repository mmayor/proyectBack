"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Request, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
import requests
from models import Receta
from models import Ingrediente
import copy
# from models import Receta_Ingrediente


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
# @app.errorhandler(Exception)
# def handle_invalid_usage(error):
#     print(error)

#     return error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_person():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/receta', methods=['GET'])
def handle_receta():

    headers = {"Content-type": "application/json"}
    # data = curl -i "https://api.edamam.com/search\?q\=fish\&app_id\=$\{YOUR_APP_ID\}\&app_key\=$\{YOUR_APP_KEY\}"
    # data = requests.get('https://api.edamam.com/search\?q\=fish\&app_id\=$\{YOUR_APP_ID\}\&app_key\=$\{YOUR_APP_KEY\}')
    url = 'https://api.edamam.com/search?q=pork&app_id=%24%7BYOUR_APP_ID%7D&app_key=%24%7BYOUR_APP_KEY%7D'
    response = requests.get(url=url)
    rJonson = response.json()

    response_body = {
        "hello": "receta"
    }

    arryRecetaName = []
    arrIngredientName = []
    dicReceta = {}

    dicReceta['name'] = ""
    dicReceta['ingredient'] = []
    dicReceta['calories'] = 0


    for x in rJonson['hits']:
        # arryRecetaName.append(x['recipe']['label'])
        dicReceta['name'] = x['recipe']['label']
        dicReceta['calories'] = x['recipe']['calories']
        for y in (x['recipe']['ingredients']):
           # arrIngredientName.append(x['recipe']['ingredients'])
            # print(y['food'])
            dicReceta['ingredient'].append(y['food'])

       # print(dicReceta)

        dicRecetaTemp = copy.deepcopy(dicReceta)
        arryRecetaName.append(dicRecetaTemp)

        dicReceta['ingredient'] = []


    # arryRecetaName.append(dicReceta)
    # print(arryRecetaName)
    # print ( ((rJonson['hits'])[0])['recipe'].keys() )
    # return jsonify(response), 200
    # return rJonson['hits']
    # print(len(arryRecetaName))
    # print(arryRecetaName)
    # print(arrIngredientName)
    ## INSERT  RECETA
    #receta1 = Contacts(full_name=body["full_name"], email=body["email"], agenda_slug=body["agenda_slug"], address=body["address"], phone=body["phone"])
    #db.session.add(user1)
    #db.session.commit()

    ## INSERT NEW Receta

    '''
    for receta in arryRecetaName:

            recetaTemp = Receta.query.filter_by(name=receta['name']).first()
            if recetaTemp is None:
                receta1 = Receta(name=receta['name'], image='image',  calory=receta['calories'])
                db.session.add(receta1)
                db.session.commit()
                recetaTemp = None

    '''
    ## INSERT NEW INGREDIENTE

    for receta in arryRecetaName:

        recetaTemp = Receta.query.filter_by(name=receta['name']).first()
        receta1 = Receta(name=receta['name'], image='image',  calory=receta['calories'])
        if recetaTemp is None:

                db.session.add(receta1)
                db.session.commit()
                recetaTemp = None


        for ingrediente in (receta['ingredient']):

            ingredienteTemp = Ingrediente.query.filter_by(name=ingrediente).first()
            ingrediente1 = Ingrediente(name=ingrediente,calory=10, category='meet', prices=[])
            if ingredienteTemp is  None:

                print(ingrediente1)
                db.session.add(ingrediente1)
                db.session.commit()
                ingredienteTemp = None

            ingrediente1.ingredientes.append(receta1)
            # receta1.ingredientes[ingrediente1]
            db.session.commit()

    ## INSERT Receta-Ingrediente

    return rJonson, 200

    # return arryTemp

# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
