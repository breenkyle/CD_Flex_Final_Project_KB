from flask_app import app
from flask_app.controllers import mocs_controllers, users_controllers, sets_controller



if __name__=="__main__":
    app.run(debug=True)