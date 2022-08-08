import datetime
import json
from enum import Enum
from typing import List
from typing import Optional
from random import randint

from flask import Flask
from flask_pydantic import validate
from pydantic import BaseModel, validator
from functools import wraps
from flask import request, Response
from pydantic import ValidationError

try:
    from flask_restful import original_flask_make_response as make_response
except ImportError:
    pass

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS'] = True


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

    @validator('lat')
    def lat_min_max(cls, lat):
        if lat > 90 or lat < -90:
            raise ValueError("minimum: -90 or maximum: 90")
        return lat

    @validator('lon')
    def lon_min_max(cls, lon):
        if lon > 180 or lon < -180:
            raise ValueError("minimum: -180 or maximum: 180")
        return lon


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


class RequestOrder(BaseModel):
    user_id: str
    user_phone: str
    cart: Cart
    payment_type: PaymentType
    location: Location
    created_order_id: Optional[str]
    use_external_delivery: Optional[bool]


@app.route('/lavka/v1/integration-entry/v1/order/submit', methods=['POST'])
# @validate(body=RequestOrder, response_many=True)
# @require_api_token
def hello_world():
    try:
        RequestOrder(**request.json)
    except ValidationError as e:
        return Response(json.dumps({
            "code": "bad_request",
            "message": str(e),
            "details": {
                "cart": None,
                "retry_after": 5
            }
        }), status=400, mimetype='application/json')
    dat = datetime.date.today()
    return json.dumps({
        "order_id": f"{dat.strftime('%y%m%d')}-{randint(100000, 999999)}",
        "newbie": False
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
