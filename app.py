from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ybaswijirarqwy:ed9097a844499b7b2c4cd407efc3259343e84eec47f1ce1150850dd02578bcde@ec2-107-22-222-161.compute-1.amazonaws.com:5432/d4ngqn3oem0js4'
# must change this config before accessing locally with local postgres user and dbs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)
db = SQLAlchemy(app)

from models import Bank

#index page
@app.route("/")
def hello():
    return """
        <pre>****Fyle Assignment****<br />To generate token: /login<br />To fetch all records: /getall<br />To fetch data by ifsc: /get/&lt;ifsc&gt;<br />To fetch data by name &amp;| city: /get?name=&lt;bank_name&gt;&amp;city=&lt;city&gt;<br /><br />Note: pass limit or offset as params<br />***</pre>
    """

# POST request to login with username and password : returns jwt token
@app.route('/login', methods=['POST'])
def login():
    if request.json:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username != 'admin' or password != 'admin':
            return jsonify({"msg": "Invalid username or password"}), 401
        expires = datetime.timedelta(days = 5)

        #generate jwt token for admin with validity of 5 days
        ret = {'access_token': create_access_token(username,expires_delta=expires),
               'validity' : str(expires)}
        return jsonify(ret), 200
    else:
        return jsonify({"msg": "missing username and password"})

# GET Request to access all records from bank_branches
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

# GET Request to access record by IFSC code
@app.route("/get/<ifsc_>")
@jwt_required
def get_by_ifsc(ifsc_):
    ifsc_ = ifsc_.upper() #case insensitive

    #IFSC must be of length 11 otherwise invalid
    if len(ifsc_) == 11:
        try:
            bank = Bank.query.filter_by(ifsc=ifsc_).first()
            if bank:
                return jsonify(bank.serialize())
            else:
                return jsonify({"msg": "IFSC not found"})
        except Exception as e:
            return(str(e))
    else:
        return jsonify({"msg": "Invalid IFSC code"})

# GET Request to access records by name and/or city
@app.route("/get")
@jwt_required
def get_by_nameORcity():

    # name and city is passed as params, also case insensitive
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
            banks = Bank.query.filter_by(bank_name=name_).order_by(Bank.ifsc).offset(offset_).limit(limit_).all()
            return jsonify([e.serialize() for e in banks])
        except Exception as e:
            return(str(e))
    elif city_:
        # for multiple cities seperated by comma
        cityls = city_.split(",")
        cityls = [x.strip() for x in cityls]
        try:
            banks = Bank.query.filter(Bank.city.in_(cityls)).order_by(Bank.ifsc).offset(offset_).limit(limit_).all()
            return jsonify([e.serialize() for e in banks])
        except Exception as e:
            return(str(e))
    else:
        return jsonify({"msg": "Missing name and city"})



if __name__ == '__main__':
    app.run()