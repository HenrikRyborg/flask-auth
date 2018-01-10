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

    if not account.query.filter_by(name='sysAdmin').first():
        acc = account(name='sysAdmin')
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
    acc = account.query.filter_by(name='sysAdmin').first()

    if not accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first():
        accUsr = accountUser(accountID=acc.id,
                             userID=usr.id,
                             password='password')
        db.session.add(accUsr)
        db.session.commit()
        print('accountUser added')

    if not 'siteAdmin' in accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first().roles:
        accUsr = accountUser.query.filter_by(accountID=acc.id, userID=usr.id).first()
        ro = role.query.filter_by(name='siteAdmin').first()
        accUsr.roles.append(ro)
        db.session.commit()
        print('role {} added to accountUser'.format(str(ro.name)))

if __name__ == '__main__':
    manager.run()