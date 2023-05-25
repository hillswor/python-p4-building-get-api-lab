#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries")
def bakeries():
    bakeries = [b.to_dict() for b in Bakery.query.all()]
    response = make_response(jsonify(bakeries))
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    response = make_response(jsonify(bakery.to_dict()))
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_goods_by_price = [
        bg.to_dict() for bg in BakedGood.query.order_by(BakedGood.price).all()
    ]
    response = make_response(jsonify(baked_goods_by_price))
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    response = make_response(jsonify(most_expensive_baked_good.to_dict()))
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
