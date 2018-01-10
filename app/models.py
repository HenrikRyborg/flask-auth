from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

accountUserRoles = db.Table('accountUserRoles',
    db.Column('roleID', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('accountUserID', db.Integer, db.ForeignKey('accountUser.id'), primary_key=True)
)

class account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

class accountUser(db.Model):
    __tablename__ = 'accountUser'
    __table_args__ = (db.UniqueConstraint("accountID", "userID"),)

    id = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

    roles = db.relationship('role', secondary=accountUserRoles, lazy='subquery',
                            backref=db.backref('accountUsers', lazy=True))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))

class role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))

class department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))

class group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))