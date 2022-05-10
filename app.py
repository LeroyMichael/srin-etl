# import library
from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from petl import fromcsv, look, join, tocsv

# Inisiation object Flask
app = Flask(__name__)

# Inisiation object API
api = Api(app)

# Inisiation object CORS
CORS(app)



# Create class for resource
class Etl(Resource):
        # Get method
        def post(self):
            # Extract
            customer = fromcsv('/assets/Customer_ID_Superstore.csv')
            product = fromcsv('/assets/Product_ID_Superstore.csv')
            final = fromcsv('/assets/final_superstore.csv')

            # Join table
            merge = join(final, customer, key='customer_id')
            merge = join(merge, product, key='product_id')
            
            # Load to csv
            tocsv(merge, 'output.csv')

            with open('output.csv') as output:
                response = Response(output, mimetype='text/csv')
                response.headers['Content-Disposition'] = u'attachment; filename=output.csv'

            return response

# Resource setup
api.add_resource(Etl, '/etl', methods=["post"])

if __name__ == "__main__":
    app.run(debug=True)