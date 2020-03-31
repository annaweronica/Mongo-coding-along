from flask import Flask, render_template
import os
import env
import pymongo

app = Flask(__name__)


# set up - what cluster/server  - what database - what collection
MONGO_URI = os.environ.get("MONGO_URI") # what machine to speak to, who I am and my password (what database I want to deal with)
DBS_NAME = "myTestDB" # what database 
COLLECTION_NAME = "movies2" # what collection (what table)


# CONNECTING TO IT
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


# REPRESENTS THE DATABASE SERVER
conn = mongo_connect(MONGO_URI)


# REPRESENTS THE COLLECTION
coll = conn[DBS_NAME][COLLECTION_NAME]


@app.route("/")
def home():
    return render_template('hello.html')


# CRUD - creat, read, update, delete


# create
@app.route("/create")
def create():
    my_new_doc = {'title': 'Jaws',
                  'release_year': '1979',
                  'synopsis': 'Very relaxing movies about little fish.'}
    coll.insert_one(my_new_doc)
    return render_template('create.html', document=my_new_doc)



# read
@app.route("/read")
def read():
    documents = coll.find()
    return render_template('read.html', documents=documents)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)