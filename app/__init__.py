from flask          import Flask
from flask          import render_template
from flask          import redirect
from libsql_client  import create_client_sync
from dotenv         import load_dotenv
import os



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
    result = client.execute("SELECT id, name FROM things")
    things = result.roles

    return render_template("pages/home.jinja", things=things)


#-----------------------------------------------------------
# Thing details page
#-----------------------------------------------------------
@app.get("/thing/<int:id>")
def show_thing(id):
    client = connect_db()
    sql="""
            SELECT 
            id, 
            name, 
            price 
            FROM things
            WHERE id=?
            """
    values = [id]
    result = client.execute(sql, values)
    things = result.roles[0]
    return render_template("pages/thing.jinja", thing=thing)


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
