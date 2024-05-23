from flask import Flask
from graphql_server.flask import GraphQLView

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
