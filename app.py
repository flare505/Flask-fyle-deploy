from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fyle:test123@localhost/fyledb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)
db = SQLAlchemy(app)

from models import Bank

@app.route("/")
def hello():
    return """
        ****Fyle Assignment****
        
        To generate token: /login
        To fetch all records: /getall
        To fetch data by ifsc: /get/<ifsc>
        To fetch data by name &| city: /get?name=<bank_name>&city=<city>
        
        Note: pass limit or offset as params
        ***
    """

@app.route('/login', methods=['POST'])
def login():
    if request.json:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username != 'admin' or password != 'admin':
            return jsonify({"msg": "Invalid username or password"}), 401
        expires = datetime.timedelta(seconds = 300)
        ret = {'access_token': create_access_token(username,expires_delta=expires)}
        return jsonify(ret), 200
    else:
        return jsonify({"msg": "missing username and password"})

@app.route("/getall")
@jwt_required
def get_all():
    args = request.args
    offset_ = args.get('offset') if 'offset' in args else 0
    limit_ = args.get('limit') if 'limit' in args else None
    try:
        banks = Bank.query.order_by(Bank.ifsc).offset(offset_).limit(limit_).all()
        return  jsonify([e.serialize() for e in banks])
    except Exception as e:
        return(str(e))

@app.route("/get/<ifsc_>")
@jwt_required
def get_by_ifsc(ifsc_):
    ifsc_ = ifsc_.upper()
    if len(ifsc_) == 11:
        try:
            bank = Bank.query.filter_by(ifsc=ifsc_).first()
            return jsonify(bank.serialize())
        except Exception as e:
            return(str(e))
    else:
        return jsonify({"msg": "Invalid IFSC code"})

@app.route("/get")
@jwt_required
def get_by_nameORcity():
    args = request.args
    name_ = args.get('name').strip('\'"').upper() if 'name' in args else None
    city_ = args.get('city').strip('\'"').upper() if 'city' in args else None

    offset_ = args.get('offset') if 'offset' in args else 0
    limit_ = args.get('limit') if 'limit' in args else None

    if name_ and city_:
        try:
            banks = Bank.query.filter_by(bank_name = name_, city = city_).order_by(Bank.ifsc).offset(offset_).limit(limit_).all()
            return jsonify([e.serialize() for e in banks])
        except Exception as e:
            return(str(e))
    elif name_:
        try:
            banks = Bank.query.filter_by(bank_name = name_).order_by(Bank.ifsc).offset(offset_).limit(limit_).all()
            return jsonify([e.serialize() for e in banks])
        except Exception as e:
            return(str(e))
    elif city_:
        try:
            banks = Bank.query.filter_by(city = city_).order_by(Bank.ifsc).offset(offset_).limit(limit_).all()
            return jsonify([e.serialize() for e in banks])
        except Exception as e:
            return(str(e))
    else:
        return jsonify({"msg": "Missing name and city"})



if __name__ == '__main__':
    app.run()