from flask_script import Manager
from app import app, db
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import exc

# Flask-manager
manager = Manager(app)

# Flask-migrate
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def testDB():
    from app.models import account, user, accountUser, role

    if not account.query.filter_by(name='testAccount').first():
        acc = account(name='testAccount')
        db.session.add(acc)
        db.session.commit()
        print('account {} added'.format(str(acc.name)))

    if not user.query.filter_by(email='henrikryborg@gmail.com').first():
        usr = user(email='henrikryborg@gmail.com')
        db.session.add(usr)
        db.session.commit()
        print('user {} added'.format(str(usr.email)))  

    roleList = ['siteAdmin','admin','writer','reader']
    for r in roleList:
        if not role.query.filter_by(name=r).first():
            ro = role(name=r)
            db.session.add(ro)
            db.session.commit()
            print('role {} added'.format(str(r)))

    usr = user.query.filter_by(email='henrikryborg@gmail.com').first()
    acc = account.query.filter_by(name='testAccount').first()

    if not accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first():
        accUsr = accountUser(accountID=acc.id,
                             userID=usr.id,
                             password='password')
        db.session.add(accUsr)
        db.session.commit()
        print('accountUser added')

    if not 'admin' in accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first().roles:
        accUsr = accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first()
        ro = role.query.filter_by(name='admin').first()
        accUsr.roles.append(ro)
        db.session.commit()
        print('role {} added to accountUser'.format(str(ro.name)))

@manager.command
def testDB2():
    from app.models import accountUser, user, account
    usr = user.query.filter_by(email='henrikryborg@gmail.com').first()
    acc = account.query.filter_by(name='testAccount').first()
    accUsr = accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first()

    for r in accUsr.roles:
        print (r.name)

@manager.command
def deleteDB():
    if account.query.filter_by(name='testAccount').first():
        acc = account.query.filter_by(name='testAccount').first()
    else:
        acc = None

    if user.query.filter_by(email='henrikryborg@gmail.com').first():
        usr = user.query.filter_by(email='henrikryborg@gmail.com').first()
    else:
        usr = None

    roleList = ['siteAdmin','admin','writer','reader']
    roles = []
    for r in roleList:
        if role.query.filter_by(name=r).first():
            roles.append(role.query.filter_by(name=r).first())

    if accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first():
        accUser = accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first()
    else:
        accUser = None


if __name__ == '__main__':
    manager.run()