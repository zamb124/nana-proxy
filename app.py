from flask import Flask
from typing import Optional
from flask import Flask, request
from pydantic import BaseModel, validator
from enum import Enum
from flask_pydantic import validate
import json

app = Flask(__name__)

class CartItem(BaseModel):
    id: str
    quantity: float
    full_price: float
    title: Optional[str]
    stack_price: Optional[float]
    stack_full_price: Optional[float]

class Cart(BaseModel):
    items: CartItem
    cart_total_cost: Optional[float]
    cart_total_discount: Optional[float]

class PaymentType(str, Enum):
    cash = 'cash'
    online = 'online'

class Point(BaseModel):
    lat: float
    lon: float

class Location(BaseModel):
    position: Point
    place_id: str
    floor: Optional[str]
    flat: Optional[str]
    doorcode: Optional[str]
    doorcode_extra: Optional[str]
    entrance: Optional[str]
    building_name: Optional[str]
    doorbell_name: Optional[str]
    left_at_door: Optional[bool]
    meet_outside: Optional[bool]
    no_door_call: Optional[bool]
    postal_code: Optional[str]
    comment: Optional[str]

class RequestBodyModel(BaseModel):
  user_id: str
  user_phone: str
  cart: Cart
  payment_type: PaymentType
  location: Location








@app.route('/lavka/v1/integration-entry/v1/order/submit', methods=['POST'])
@validate()
def hello_world(body: RequestBodyModel):
    name = body.user_id
    nickname = body.user_id
    return json.dumps(body.dict())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
