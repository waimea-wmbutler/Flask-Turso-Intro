from flask          import Flask
from flask          import render_template
from flask          import redirect
from libsql_client  import create_client_sync
from dotenv         import load_dotenv
import os


# Load Turso environment variables from the .env file
load_dotenv()
TURSO_URL = os.getenv https://things-waimea-wmbutler.aws-ap-northeast-1.turso.io
TURSO_KEY = os.getenv eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NDg1NzkyMzcsImlkIjoiMTg3MzU5ZDktNTgwYy00MTA1LTliNmItMjZiNzMyMzQwMTk3IiwicmlkIjoiOTc1NjY4MzUtMWJiMS00OTBkLWI1NmUtYzcwNjg3Zjc5NThkIn0.H2dVQXhnzkXXR8t6EPm3t3UVn-edwVFiGJ1gPxTtbaFkhhxI-cVq2LGO9hT0lIhPpocefW13fv3-7RAFpw7dCw

# Create the Flask app
app = Flask(__name__)


# Track the DB connection
client = None

#-----------------------------------------------------------
# Connect to the Turso DB and return the connection
#-----------------------------------------------------------
def connect_db():
    global client
    if client == None:
        client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)
    return client


#-----------------------------------------------------------
# Home Page with list of things
#-----------------------------------------------------------
@app.get("/")
def home():
    client = connect_db()
    result = client.execute("SELECT * FROM things")
    print(result.rows)

    return render_template("pages/home.jinja")


#-----------------------------------------------------------
# Thing details page
#-----------------------------------------------------------
@app.get("/thing/<int:id>")
def show_thing(id):
    return render_template("pages/thing.jinja")


#-----------------------------------------------------------
# New thing form page
#-----------------------------------------------------------
@app.get("/new")
def new_thing():
    return render_template("pages/thing-form.jinja")


#-----------------------------------------------------------
# Thing deletion
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_thing(id):
    return redirect("/")


#-----------------------------------------------------------
# 404 error handler
#-----------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return render_template("pages/404.jinja")
