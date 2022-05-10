# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# Inisiation object Flask
app = Flask(__name__)

# Inisiation object API
api = Api(app)

# Inisiation object CORS
CORS(app)

# Create class for resource
class Etl(Resource):
        # Get method
        def get(self):
            response = {"msg":"success"}
            return response

# Resource setup
api.add_resource(Etl, '/etl', methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True)