from . import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(15))


class ClubTag(db.Model):
    __tablename__ = 'club_tag'
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))


class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    total_budget = db.Column(db.Integer)
    current_budget = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    gcn = db.Column(db.String(10))
    email = db.Column(db.String(50))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))


class Supply(db.Model):
    __tablename__ = 'supplys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    status = db.Column(db.Integer)
    message = db.Column(db.String(200))
    count = db.Column(db.Integer)
    link = db.Column(db.String(300))
    invoice = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))


class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    script = db.Column(db.String(200))
    supply_id = db.Column(db.Integer, db.ForeignKey('supplys.id'))