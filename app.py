import datetime
import json
import re
from enum import Enum
from functools import wraps
from random import randint
from typing import List
from typing import Optional

from flask import Flask
from flask import request, Response
from pydantic import BaseModel, validator
from pydantic import ValidationError, constr

try:
    from flask_restful import original_flask_make_response as make_response
except ImportError:
    pass

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS'] = True


class Numeric(str):
    pattern = r'^\d+(\.\d*)?$'

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError(f'str expected, got{type(v)}')
        if not re.match(pattern=cls.pattern, string=v):
            raise ValueError(f'Wrong value {v} for pattern {cls.pattern}')

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return Response(json.dumps({
                "code": "unauthorized",
                "message": "Auth Error",
            }), status=401, mimetype='application/json')
        return func(*args, **kwargs)

    return check_token


class CartItem(BaseModel):
    id: str
    quantity: Numeric
    full_price: Numeric
    title: Optional[str]
    stack_price: Optional[Numeric]
    stack_full_price: Optional[Numeric]


class Cart(BaseModel):
    items: List[CartItem]
    cart_total_cost: Optional[Numeric]
    cart_total_discount: Optional[Numeric]


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
@require_api_token
def hello_world():
    try:
        body = RequestOrder(**request.json)
    except ValidationError as e:
        return Response(json.dumps({
            "code": "bad_request",
            "message": str(e),
            "details": {
                "cart": None,
                "retry_after": 5
            }
        }), status=400)
    dat = datetime.date.today()
    return json.dumps({
        "order_id": f"{dat.strftime('%y%m%d')}-{randint(100000, 999999)}",
        "newbie": False,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
