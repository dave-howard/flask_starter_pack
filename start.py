from flaskr import app
from flaskr.models import db, User, session
from flaskr import views
import sys

if __name__ == "main":
    print("db.create_all()")
    db.create_all()  # create database if not already there

    users = session().query(User).all()
    print(users)

    print(f"app.run() sys.argv={sys.argv[1:]}")
    # start Flask web service
    if '--local' in sys.argv:
        app.run(host='127.0.0.1', debug=True, port=80)
    else:
        app.run(host='0.0.0.0', debug=True, port=80)
