from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

accountUserGroups = db.Table('accountUserGroups',
    db.Column('groupID', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('accountUserID', db.Integer, db.ForeignKey('accountUser.id'), primary_key=True)
)

class account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return '<Account %r>' % self.name

class accountUser(db.Model):
    __tablename__ = 'accountUser'
    __table_args__ = (db.UniqueConstraint("accountID", "userID"),)

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False)
    accountID = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('account', backref=db.backref('accountUsers', lazy=True))
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('user', backref=db.backref('accountUsers', lazy=True))
    passwordHash = db.Column(db.String(128), nullable=False)
    isSiteAdmin = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    isWriter = db.Column(db.Boolean, default=False)
    isReader = db.Column(db.Boolean, default=True)
    isValidated = db.Column(db.Boolean, default=False)
    isDeactivated = db.Column(db.Boolean, default=False)
    departmentID = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('department', backref=db.backref('accountUsers', lazy=True))

    groups = db.relationship('group', secondary=accountUserGroups, lazy='subquery',
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
    name = db.Column(db.String(60))

    def __repr__(self):
        return '<User %r>' % self.name

class department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Department %r>' % self.name

class group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Group %r>' % self.name

@login_manager.user_loader
def load_user(id):
    return accountUser.query.get(int(id))