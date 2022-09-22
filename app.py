# Import Flask, Pymongo, and scrape_mars
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Use the Flask app to set up the connection to the Mongo Database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Access the information from mongoDB
    mars_db_data = mongo.db.marsData.find_one()

    # Return template and data
    return render_template("index.html", mars_data = mars_db_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    # Create a collection (table) called marsData in mongoDB
    # We will call this collection marsTable here in App.py
    marsTable = mongo.db.marsData

    # Drop the table if it exists
    mongo.db.marsData.drop()

    # Test to call the scrape mars script
    mars_data = scrape_mars.scrape_all()

    # Take the dictionary and load it into mongoDB
    marsTable.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")

# Launch the Flask app
if __name__ == "__main__":
    app.run(host="localhost", port=4999, debug=True)