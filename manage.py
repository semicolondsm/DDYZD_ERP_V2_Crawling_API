from app import create_app
from app import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)

@manager.command
def deploy():
    from flask_migrate import upgrade
    upgrade()

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    manager.run()
