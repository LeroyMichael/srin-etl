# import library
from flask import Flask, jsonify, request, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from petl import fromcsv, join, todataframe, distinct
import pandas as pd
import os 
import seaborn as sns 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Upload Path
os.makedirs('assets', exist_ok=True)  

# Inisiation object Flask
app = Flask(__name__)

# Inisiation object API
api = Api(app)

# Inisiation object CORS
CORS(app)

# Create class for resource
class Etl(Resource):        
        # Post method
        def post(self):
            # Extract
            customer = pd.read_csv(request.files['customer'])
            product = pd.read_csv(request.files['product'])
            final = pd.read_csv(request.files['final'])

            # Validation
            if customer.empty:
                return jsonify(message='Upload a customer CSV file')
            if product.empty:
                return jsonify(message='Upload a product CSV file')
            if final.empty:
                return jsonify(message='Upload a final CSV file')

            # Extract to local folder
            customer.to_csv('assets/Customer_ID_Superstore.csv',index=False)
            product.to_csv('assets/Product_ID_Superstore.csv',index=False)
            final.to_csv('assets/final_superstore.csv',index=False)
            
            # Convert to table
            customer = fromcsv('assets/Customer_ID_Superstore.csv')
            product = fromcsv('assets/Product_ID_Superstore.csv')
            final = fromcsv('assets/final_superstore.csv')

            # Transform - Joining data
            merge = join(final, customer, key='customer_id')
            merge = join(merge, product, key='product_id')

            # Transform - Data deduplication
            merge = distinct(merge)
            
            # Convert to dataframe
            df = todataframe(merge)

            # Transform - Data mapping
            df['order_date'] = pd.to_datetime(df['order_date'])
            df['quantity'] = df['quantity'].astype(int)

            # Transform - Derived Variables & Splitting
            df['year'] = pd.DatetimeIndex(df['order_date']).year

            # Transform - Aggregation & Data sorting & Filtering
            sales_category = df.groupby(['year','category']).sum()
            sales_category = sales_category.reset_index()
            latest_year = sales_category.sort_values(by=['year'],ascending=False)
            latest_year = latest_year['year'].iloc[0]
            sales_category = sales_category[sales_category['year'] == latest_year]
            sales_category = sales_category.sort_values(by=['category'])

            categories = df['category'].unique()
            categories = np.sort(categories)

            # Plotting
            plt.title('Product Sales Report per Category in ' + str(latest_year))
            bar_plot = sns.barplot(categories, sales_category['quantity'])

            # Save plot
            fig = bar_plot.get_figure()
            
            # Load to csv
            sales_category.to_csv('assets/output.csv',index=False)

            # Load to jpg
            fig.savefig("sales.jpg")

            # Close figure
            plt.close()

            # Load to jpg
            return send_file("sales.jpg", mimetype='image/jpg')

# Resource setup
api.add_resource(Etl, '/etl', methods=["get","post"])

if __name__ == "__main__":
    app.run(debug=True)