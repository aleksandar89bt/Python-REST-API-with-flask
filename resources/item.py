from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        required=True,
                        type=float,
                        help='This field cannot be empty')
    parser.add_argument('store_id',
                        required=True,
                        type=int,
                        help='Item needs belong to a store')

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_username(name)
        if item:
            return item.json()
        return {"message": "Item with this name not found"}, 404

    def post(self, name):
        item = ItemModel.find_by_username(name)
        if item:
            return {"message": "Item with name {} already exist.".format(name)}, 409
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting an item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_username(name)
        if item:
            item.delete_from_db()
            return {"message": "Item with name {} was deleted".format(name)}, 204
        return {"message": "Item not found"}, 404

    def put(self, name):
        item = ItemModel.find_by_username(name)
        data = Item.parser.parse_args()

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        # return {"items": [item.json() for item in ItemModel.query.all()]} # this also works
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
