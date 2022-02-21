from multiprocessing import connection
import sqlite3

from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import Itemmodel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        #blank=True,
        help="This feild cannot be left blank"
    )

    parser.add_argument('store_id',
        type=int,
        #Required=True,
        help="Every item needs a store id"
    )
    @jwt_required()
    def get(self,name):
        #item = next(filter(lambda x: x['name'] == name,items),None)
        #return {'item': item},200 if item else 400

        item = Itemmodel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self,name):
        if Itemmodel.find_by_name(name):
            return {'message' : "An item wth name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()
        item =  Itemmodel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured inserting the item"}, 500

        return item.json(),201


    def delete(self,name):
        item = Itemmodel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item deleted'}
            
    
    def put(self,name):
        data =Item.parser.parse_args()

        item = Itemmodel.find_by_name(name)
        
        if item is None:
            item = Itemmodel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

class itemlist(Resource):
    def get(self):
        return {'items': [x.json() for x in Itemmodel.query.all()]}
        