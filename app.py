import os

from api import create_app
# from flask_bcrypt import Bcrypt




app = create_app(os.getenv('ENV') or 'dev')

if __name__=="__main__":

    app.run()