import json
from enum import Enum
from typing import List
from typing import Optional
from uuid import uuid4

from flask import Flask
from flask_pydantic import validate
from pydantic import BaseModel
from functools import wraps
from flask import g, request, redirect, url_for, Response
app = Flask(__name__)


def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return Response(json.dumps({
                "code": "Auth",
                "message": "No Auth"
            }))
        return func(*args, **kwargs)

    return check_token

class CartItem(BaseModel):
    id: str
    quantity: float
    full_price: float
    title: Optional[str]
    stack_price: Optional[float]
    stack_full_price: Optional[float]

class Cart(BaseModel):
    items: List[CartItem]
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
  created_order_id: Optional[str]
  use_external_delivery: Optional[bool]


@app.route('/lavka/v1/integration-entry/v1/order/submit', methods=['POST'])
@validate()
#@require_api_token
def hello_world(body: RequestBodyModel):
    return json.dumps({
        "order_id": f'{uuid4().hex}',
        "newbie": False
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
