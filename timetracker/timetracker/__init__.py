import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
app.config['WHOOSH_BASE'] = 'whoosh'

#### bootstrap config #####
Bootstrap(app)

############

#################################
#### DATABASE SETUPS ############
################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


Migrate(app, db)

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our timetracker to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.


from timetracker.users.views import users
from timetracker.admin.views import admin
from timetracker.core.views import core
app.register_blueprint(users)
app.register_blueprint(admin)
app.register_blueprint(core)

login_manager.login_view = "users.login"
