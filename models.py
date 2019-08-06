from app import db

class Bank(db.Model):
    __tablename__ = 'bank_branches'

    ifsc = db.Column(db.String(), primary_key=True)
    bank_id = db.Column(db.Integer())
    branch = db.Column(db.String())
    address = db.Column(db.String())
    city = db.Column(db.String())
    district = db.Column(db.String())
    state = db.Column(db.String())
    bank_name = db.Column(db.String())

    def serialize(self):
        return {
            'ifsc': self.ifsc,
            'name': self.bank_name,
            'branch': self.branch,
            'address': self.address,
            'city' : self.city,
            'district' : self.district,
            'state' : self.state
        }