import pymongo
import urllib.parse
from bson import ObjectId
import json
from pprint import pprint


def get_database():
    f = open (r'/Users/zacharywong/Documents/Work/Dartmouth/CS61/CS61/URI/URI.json')
    content = json.load(f)
    f.close()

    URI = content["user"] + urllib.parse.quote(content["password"]) + content["server"]
    client = pymongo.MongoClient(URI)
    
    db = client.lab4
    return db

def createIndex():
    db.blogs.create_index([
    
    {
        "blogs": 1
    },
    {
        "unique": True,
        "sparse": True
    }
    ]
)

def insertBlog(blogName, userName, title, postBody, tags, timestamp):
    db.blogs.insert_one(
        {
            "_id": blogName,
            "blogs": 
            [
                {
                    "userName": userName,
                    "title": title,
                    "postBody": postBody,
                    "tags": tags,
                    "timestamp": timestamp
                }
            ]
        }
    )

def updateBlog(blogName, userName, title, postBody, tags, timestamp):
    db.blogs.update_one(
        {"_id": blogName},
        {
        "$addToSet": 
            {
            "blogs":
                {
                    "userName": userName,
                    "title": title,
                    "postBody": postBody,
                    "tags": tags,
                    "timestamp": timestamp
                }
            }
        }
    )

def post(blogName, userName, title, postBody, tags, timestamp):
    #db.blogs.delete_many({})

    cursor = db.blogs.find({"_id": blogName})

    if len(list(cursor)) == 0:
        insertBlog(blogName, userName, title, postBody, tags, timestamp)

    else:
        updateBlog(blogName, userName, title, postBody, tags, timestamp)

    cursor = db.blogs.find({})
    for document in cursor:
        pprint(document)

if __name__ == "__main__":   
    # Get the database
    db = get_database()
    post("ridiculus mus", "Medge Burnett", "eu neque pellentesque massa lobortis", "rutrum eu, ultrices sit amet, risus. Donec nibh enim, gravida sit amet, dapibus id, blandit", "sandwiches, desserts, noodles, seafood", "Jul 20, 2021")
    post("ridiculus mus", "Cruz Hoover", "pharetra, felis eget varius ultrices", "Praesent luctus. Curabitur egestas nunc sed libero. Proin sed turpis nec mauris blandit mattis.", "Cras, stews", "Dec 24, 2021")
    #

# feugiat. Sed nec metus,Cruz Hoover,"pharetra, felis eget varius ultrices,",Praesent luctus. Curabitur egestas nunc sed libero. Proin sed turpis nec mauris blandit mattis. Cras,stews,"Dec 24, 2021"
# "vel, faucibus id, libero.",Xavier Carr,ante dictum cursus. Nunc mauris,"orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc","noodles, sandwiches","Sep 3, 2021"
# "quis, tristique ac, eleifend",Illana Frye,fringilla cursus purus. Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida. Aliquam,cereals,"Nov 13, 2021"
# "elit, a feugiat tellus",Walter Buckley,interdum ligula eu enim. Etiam,posuere cubilia Curae Donec tincidunt. Donec vitae erat vel pede blandit congue. In scelerisque scelerisque,"noodles, seafood","Mar 6, 2021"
    
