from flask import Flask, session, request, redirect 

from conf.config import DEBUG, SECRET_KEY, PUBLIC_ACCESS_RESOURCES, RESET_DB
from views import User, Search
from utils import LOG
from cmd_.initialize import reset_db

reset_db()

LOG.info("Initializing APP...")

app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.secret_key = SECRET_KEY

@app.before_request
def require_login():
    if not 'user' in session and not request.endpoint in PUBLIC_ACCESS_RESOURCES:
        return redirect("/")

app.add_url_rule('/', view_func=Search().search, methods=['POST', 'GET'])
app.add_url_rule('/login', view_func=User().login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=User().logout)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)