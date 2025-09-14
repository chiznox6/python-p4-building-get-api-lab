#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from server.models import db, Bakery, BakedGood


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)



@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries
@app.route('/bakeries')
def bakeries():
    bakeries = db.session.query(Bakery).all()
    return jsonify([bakery.to_dict() for bakery in bakeries])

# GET /bakeries/<id> (updated to avoid legacy warning)
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)  # ✅ Updated from Bakery.query.get_or_404
    if bakery is None:
        return jsonify({"error": "Bakery not found"}), 404
    return jsonify(bakery.to_dict())

# GET /baked_goods/by_price
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = db.session.query(BakedGood).order_by(BakedGood.price.desc()).all()
    return jsonify([bg.to_dict() for bg in baked_goods])

# GET /baked_goods/most_expensive
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = db.session.query(BakedGood).order_by(BakedGood.price.desc()).first()
    if baked_good:
        return jsonify(baked_good.to_dict())
    return jsonify({"error": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
