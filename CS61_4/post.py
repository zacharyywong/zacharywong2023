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

def insertPermaLinkSchema(permaLink):
    db.permaLinks.insert_one(
        {
        "links":
            {
                "permaLink": permaLink
            }
        }
    )

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

    #insertPermaLinkSchema(permaLink)



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
    #insertPermaLinkSchema(permaLink)


def insertComment(blogName, userName, commentBody, timestamp, permaLink):
    db.comments.insert_one(
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

def insertReply(blogName, userName, commentBody, timestamp, permaLink):
    db.blogs.update_one(
        {
            "_id": blogName,
            "blogs.comments.permaLink": permaLink
        }, 
        {
        "$push":
            {
            "blogs.$.comments.$[commentEle].replies":
                {
                    "userName": userName,
                    "replyBody": commentBody,
                    "permaLink": timestamp
                }
            }
        },

        upsert = True,
        
        array_filters=
        [{"commentEle.permaLink": permaLink}]
        
            # {
            # "blogs.$.comments.replies":
            #     {
            #     "userName": userName,
            #     "replyBody": commentBody,
            #     "permaLink": timestamp
            #     }
            
            # }
        
    )


def post(blogName, userName, title, postBody, tags, timestamp):
    cursor = db.blogs.find({"_id": blogName})
    permaLink = createLink(blogName, title)
    if len(list(cursor)) == 0:
        print("inserting blog")
        insertBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)
    else:
        print("updating blog")
        updateBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)

def comment(blogName, permaLink, userName, commentBody, timestamp):
    cursor = db.blogs.find({"_id": blogName})
    if len(list(cursor)) == 0:
        raise ValueError("No blogs found")
   
    else:
        cursor1 = db.blogs.find({"_id": blogName, "blogs.comments.permaLink": permaLink})
        # for document in cursor:
        #     print(document)
        print(list(cursor1))

        documentsFound = len(list(cursor1.clone()))
        
        if documentsFound == 0:
            print('inserting comment')
            insertComment(blogName, userName, commentBody, timestamp, permaLink)
        else:
            print('inserting reply')
            insertReply(blogName, userName, commentBody, timestamp, permaLink)


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
    db.permaLinks.delete_many({})


    #add blogs to same blog name
    post("ridiculusmus", "Medge Burnett", "eu neque pellentesque massa lobortis", "rutrum eu, ultrices sit amet, risus. Donec nibh enim, gravida sit amet, dapibus id, blandit", "sandwiches, desserts, noodles, seafood", "Jul 20, 2021")
    post("ridiculusmus", "Cruz Hoover", "pharetra, felis eget varius ultrices", "Praesent luctus. Curabitur egestas nunc sed libero. Proin sed turpis nec mauris blandit mattis.", "Cras, stews", "Dec 24, 2021")

    # # add another blog name 
    post("vel", "Xavier Carr", "ante dictum cursus. Nunc mauris", "orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc", "noodles, sandwiches", "Sep 3, 2021")

    # #first comment on blog 
    # comment("vel", "vel.ante_dictum_cursus_Nunc_mauris", "Illana Frye", "Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida.", "Nov 13, 2021")

    # # reply to comment on blog 
    # comment("vel", "Nov 13, 2021", "Walter Buckley", "interdum ligula eu enim. Etiam,posuere cubilia Curae Donec tincidunt. Donec vitae erat vel pede blandit congue. In scelerisque scelerisque", "Dec 20, 2021")
    #comment("vel", "Dec 20, 2021", "asdf asdf", "asdfasdfasdfasdfasdfasfdasdffsdafdasdfasdf", "Jan 2, 2022")



    # Bad Tests

    # no blog called "vl"
    #comment("vl", "vel.ante_dictum_cursus_Nunc_mauris", "Illana Frye", "Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida.", "Nov 13, 2021")

    displayCollection(db)

# "elit, a feugiat tellus",Walter Buckley,interdum ligula eu enim. Etiam,posuere cubilia Curae Donec tincidunt. Donec vitae erat vel pede blandit congue. In scelerisque scelerisque,"noodles, seafood","Mar 6, 2021"
    