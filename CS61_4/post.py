import pymongo
import urllib.parse
from bson import ObjectId
import json
from pprint import pprint
import re
import datetime


def get_database():
    f = open (r'/Users/zacharywong/Documents/Work/Dartmouth/CS61/CS61/URI/URI.json')
    content = json.load(f)
    f.close()

    URI = content["user"] + urllib.parse.quote(content["password"]) + content["server"]
    client = pymongo.MongoClient(URI)
    
    db = client.lab4
    return db
def displayCollection(db):
    cursor = db.blogs.find({})
    for document in cursor:
        pprint(document)

def createLink(blogName, title):
    permaLink  = blogName+'.'+re.sub('[^0-9a-zA-Z]+', '_', title)
    return permaLink

def insertBlog(blogName, userName, title, postBody, tags, timestamp, permaLink):
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
                    "timestamp": timestamp,
                    "permaLink": permaLink
                }
            ]
        }
    )

def updateBlog(blogName, userName, title, postBody, tags, timestamp, permaLink):
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
                    "timestamp": timestamp,
                    "permaLink": permaLink
                }
            
            }
        }
    )

def insertComment(blogName, userName, commentBody, timestamp, permaLink):
    db.blogs.update_one(
        {
            "_id": blogName,
            "blogs.permaLink": permaLink
        }, 
        {
        "$push":
            {
            "blogs.$.comments":
            
                {
                "userName": userName,
                "commentBody": commentBody,
                "permaLink": timestamp
                }
            
            }
        } 
    )

def post(blogName, userName, title, postBody, tags, timestamp):
    cursor = db.blogs.find({"_id": blogName})
    permaLink = createLink(blogName, title)
    if len(list(cursor)) == 0:
        insertBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)
    else:
        print("updating blog")
        updateBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)

def comment(blogName, permaLink, userName, commentBody, timestamp):
    cursor = db.blogs.find({"_id": blogName})

    # if len(list(cursor)) == 1:
    #     print(len(list(cursor)))
    #     raise ValueError("No blogs found")

    # cursor.blogs.find({"_id": blogName, "blogs.permaLink": permaLink})
    insertComment(blogName, userName, commentBody, timestamp, permaLink)


    # if len(list(cursor)) == 0:
        # permaLink = datetime.datetime.now
        # updateComment(userName, commentBody, timestamp, permaLink)
        # cursor.blogs.find({{"_id": blogName, "blogs.comments": permaLink}})
        # if len(list(cursor)) == 0: 
        #     raise ValueError("No ")
        # else:
        #     updateComment(userName, commentBody, timestamp)


if __name__ == "__main__":   
    # Get the database
    db = get_database()
    db.blogs.delete_many({})
    post("ridiculusmus", "Medge Burnett", "eu neque pellentesque massa lobortis", "rutrum eu, ultrices sit amet, risus. Donec nibh enim, gravida sit amet, dapibus id, blandit", "sandwiches, desserts, noodles, seafood", "Jul 20, 2021")
    post("ridiculusmus", "Cruz Hoover", "pharetra, felis eget varius ultrices", "Praesent luctus. Curabitur egestas nunc sed libero. Proin sed turpis nec mauris blandit mattis.", "Cras, stews", "Dec 24, 2021")
    post("vel", "Xavier Carr", "ante dictum cursus. Nunc mauris", "orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc", "noodles, sandwiches", "Sep 3, 2021")
    comment("vel", "vel.ante_dictum_cursus_Nunc_mauris", "Illana Frye", "Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida.", "Nov 13, 2021")
    displayCollection(db)

# "quis, tristique ac, eleifend",Illana Frye,fringilla cursus purus. Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida. Aliquam,cereals,"Nov 13, 2021"
# "elit, a feugiat tellus",Walter Buckley,interdum ligula eu enim. Etiam,posuere cubilia Curae Donec tincidunt. Donec vitae erat vel pede blandit congue. In scelerisque scelerisque,"noodles, seafood","Mar 6, 2021"
    
