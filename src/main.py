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
from models import Receta, Ingrediente, Stock, Price, User
import copy
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

# from models import Receta_Ingrediente


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
# @app.errorhandler(Exception)
# def handle_invalid_usage(error):
#     print(error)

#     return error.status_code


@app.route('/login', methods=['POST'])
def login():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    usercheck = User.query.filter_by(email=email, password=password).first()
    if usercheck == None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email),'id': usercheck.id}
    return jsonify(ret), 200


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


# GET RECETA
@app.route('/recetanew', methods=['GET'])
def handle_recetanew():

        recetasTemp = Receta()

        # get all the people
        recetas_query = recetasTemp.query.all()

        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        all_recetas = list(map(lambda x: x.serializeReceta(), recetas_query))

        return jsonify(all_recetas), 200





# GET USER
@app.route('/user', methods=['GET'])
def handle_user():

        usersTemp = User()

        # get all the people
        users_query = usersTemp.query.all()

        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        all_users = list(map(lambda x: x.serializeUsers(), users_query))

        return jsonify(all_users), 200



# GET PRECIO
@app.route('/precio', methods=['GET'])
def handle_precio():

        preciosTemp = Price()

        # get all the people
        precios_query = preciosTemp.query.all()

        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        all_precios = list(map(lambda x: x.serializePrecios(), precios_query))

        return jsonify(all_precios), 200


#ADD A PRECIO
@app.route('/add_precio', methods=['POST'])
def add_precio():
    body = request.get_json()
    precio1 = Price(market_name=body["market_name"], price=body["price"], id_ingrediente=body["id_ingrediente"])
    db.session.add(precio1)
    db.session.commit()
    return "ok", 200


#ADD A STOCK
@app.route('/add_stock', methods=['POST'])
def add_stock():
    body = request.get_json()

    for ingreTemp in body:

        stock1 = Stock(id_profile=ingreTemp["id_profile"], id_ingrediente=ingreTemp["id_ingrediente"], quantity=ingreTemp["quantity"])
        db.session.add(stock1)
        db.session.commit()
    return "ok", 200


# GET STOCK
@app.route('/stock', methods=['GET'])
def handle_stock():

        stocksTemp = Stock()

        # get all the people
        stocks_query = stocksTemp.query.all()

        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        all_stocks = list(map(lambda x: x.serializeStocks(), stocks_query))

        return jsonify(all_stocks), 200



@app.route('/ingrediente', methods=['GET'])
def handle_ingrediente():

        ingredienteTemp = Ingrediente()

        # get all the people
        ingrediente_query = ingredienteTemp.query.all()
        # User.query.limit(1).all()
        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        # all_ingrediente = list(map(lambda x: x.serializeContact(), contacts_query))
        all_ingrediente = list(map(lambda x: x.serializeIngrediente(), ingrediente_query))
        '''
        assurances = []
        for assurance in ingredienteTemp.query.distinct(ingredienteTemp.name):
            assurances.append(assurance.name)
        '''

        # arrIngrediente = ingredienteTemp.query(ingredienteTemp.name).distinct()

        # ingredientes = []
        # ingredientes = [r.ingrediente for r in ingredienteTemp.query(Ingrediente.name).distinct()]



        # return arrIngrediente

        return jsonify(all_ingrediente), 200


@app.route('/receta', methods=['GET'])
def handle_receta():

    headers = {"Content-type": "application/json"}
    # data = curl -i "https://api.edamam.com/search\?q\=fish\&app_id\=$\{YOUR_APP_ID\}\&app_key\=$\{YOUR_APP_KEY\}"
    # data = requests.get('https://api.edamam.com/search\?q\=fish\&app_id\=$\{YOUR_APP_ID\}\&app_key\=$\{YOUR_APP_KEY\}')
    url = 'https://api.edamam.com/search?q=steak&app_id=%24%7BYOUR_APP_ID%7D&app_key=%24%7BYOUR_APP_KEY%7D&from=0&to=30&'
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
    dicReceta['ingredientLines'] = []


    for x in rJonson['hits']:
        # arryRecetaName.append(x['recipe']['label'])
        dicReceta['name'] = x['recipe']['label']
        dicReceta['calories'] = x['recipe']['calories']
        dicReceta['ingredientLines'] = x['recipe']['ingredientLines']
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

    ## INSERT NEW INGREDIENTE

    for receta in arryRecetaName:

        recetaTemp = None
        recetaTemp = Receta.query.filter_by(name=receta['name']).first()

        tempList = ''.join(receta['ingredientLines'])
        tempList  = str(tempList)
        print(tempList)

        receta1 = Receta(name=receta['name'], image='image',  calory=receta['calories'], guianew=tempList)
        if recetaTemp is None:


                db.session.add(receta1)
                db.session.commit()
                recetaTemp = receta1



        for ingrediente in (receta['ingredient']):

            recetaNew = db.session.query(Receta).filter_by(name=receta['name']).one()
            ingredienteTemp = None
            ingredienteTemp = Ingrediente.query.filter_by(name=ingrediente).first()
            ingrediente1 = Ingrediente(name=ingrediente,calory=10,  category='meet', prices=[])
            if ingredienteTemp is  None:

                # print(ingrediente1)

                db.session.add(ingrediente1)

               # print(ingrediente1.name)

                try:
                    session.commit()
                except:
                    # ignore error
                    pass

                ingredienteTemp = ingrediente1

            # ingrediente1.ingredientes.append(receta1)
                # ingredienteTemp1 = Ingrediente.query.filter_by(name=ingrediente).first()

            # db.session.commit()
            # ingredienteTemp = None

    ## INSERT Receta-Ingrediente

            # receta2 = Receta.query.filter_by(name=receta['name']).first()
            # ingrediente2 = Ingrediente.query.filter_by(name=ingrediente).first()


            # print(recetaNew.name)

            #ingrediente1.newTags.append(receta1)
            # print(db.session.dirty)

            # session.query(BlogPost).\  filter(BlogPost.keywords.any(keyword='firstpost')).\   all()
            # chat.query.join(user.chats).filter(user.id == 1).all()
            ingredienteTempNew = Ingrediente.query.filter_by(name=ingrediente).first()
            recetaTempNew = Receta.query.filter_by(name=receta['name']).first()
            rel = None
            find = False
            rel = Receta.query.join(Ingrediente.newTags).filter(Receta.id==recetaTempNew.id).first()


            if rel is not None:

                for seIng in rel.ingrediente:
                    if ingredienteTempNew == seIng:
                        find = True



            if rel is None or not find:

                ingredienteTempNew.newTags.append(recetaTempNew)
                # db.session.commit()
                try:
                    session.commit()
                except:
                    # ignore error
                    pass

    return rJonson, 200

    # return arryTemp

# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
