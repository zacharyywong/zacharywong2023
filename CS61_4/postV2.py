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
            "blogPosts": 
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

    insertPermaLinkSchema(permaLink)



def updateBlog(blogName, userName, title, postBody, tags, timestamp, permaLink):
    db.blogs.update_one(
        {"_id": blogName},
        {
        "$addToSet": 
            {
                "blogPosts":
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
    insertPermaLinkSchema(permaLink)


def insertComment(blogName, userName, commentBody, timestamp, permaLink):
    db.comments.insert_one(
        {
            "_id": blogName, 
            "blogDiscussion":
            [
                {
                    "originalPostLink": permaLink,
                    "newComment":
                    {
                        "userName": userName,
                        "commentBody": commentBody,
                        "timestamp": timestamp
                    }
                }
            
            ]
        }
    )

def insertReply(blogName, userName, commentBody, timestamp, permaLink):
    db.comments.update_one(
        {
            "_id": blogName
        }, 
        {
        "$push":
            {
                "blogDiscussion":
                {
                "originalPostLink": permaLink,
                "newComment":
                    {
                        "userName": userName,
                        "commentBody": commentBody,
                        "timestamp": timestamp
                    }
                }
            }
        }
    )


def post(blogName, userName, title, postBody, tags, timestamp):
    cursor = db.blogs.find({"_id": blogName})
    permaLink = createLink(blogName, title)
    if len(list(cursor)) == 0:
        print(f'\n{userName} inserting blog {title} in {blogName} at {timestamp}')
        insertBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)
    else:
        print(f'\n{userName} inserting blog {title} in {blogName} at {timestamp}')
        updateBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)

def comment(blogName, permaLink, userName, commentBody, timestamp):
    cursor = db.blogs.find({"_id": blogName})
    if len(list(cursor)) == 0:
        cursor1 = db.comments.find({"_id": blogName, "blogDiscussion.newComment.timestamp": permaLink})
        documentsFound = len(list(cursor1.clone()))
        if documentsFound == 0:
                raise ValueError("No blogs or comments found to comment on")
   
    else:
        cursor2 = db.comments.find({"_id": blogName, "blogDiscussion.newComment.timestamp": permaLink})

        documentsFound = len(list(cursor2.clone()))
        
        if documentsFound == 0:
            print(f'\n{userName} inserting comment in blog {blogName} at {timestamp}')
            insertComment(blogName, userName, commentBody, timestamp, permaLink)
        else:
            print(f'\n{userName} inserting reply to comment link {permaLink} in {blogName} at {timestamp}')
            insertReply(blogName, userName, commentBody, timestamp, permaLink)


def deleteBlog(db, blogName, permaLink, userName, timestamp):
    db.blogs.update_one(
        {
            "_id": blogName, 
            "blogPosts.permaLink": permaLink
        }, 
        {
            "$set":
            {
                "blogPosts.$.title": f"deleted by {userName}",
                "blogPosts.$.timestamp": timestamp
            }
        }
    )
    
def deleteComment(db, blogName, permaLink, userName, timestamp):
    db.comments.update_one(
        {
            "_id": blogName, 
            "blogDiscussion.newComment.timestamp": permaLink
        }, 
        {
            "$set":
            {
                "blogDiscussion.$.newComment.commentBody": f"deleted by {userName}",
                "blogDiscussion.$.newComment.timestamp": timestamp
            }
        }
    )

def delete(blogName, permaLink, userName, timestamp):
    cursor = db.blogs.find({"_id": blogName, "blogPosts.permaLink": permaLink})

    postsFound = len(list(cursor.clone()))

    if postsFound == 0:
        cursor1 = db.comments.find({"_id": blogName, "blogDiscussion.newComment.timestamp": permaLink})
        commentsFound = len(list(cursor1.clone()))
        if commentsFound == 0:
            raise ValueError("No blogs or comments found to delete")
        else:
            deleteComment(db, blogName, permaLink, userName, timestamp)
            print(f'\n{userName} deleting comment at link {permaLink} in {blogName} at {timestamp}')
    else:
        deleteBlog(db, blogName, permaLink, userName, timestamp)
        print(f'\n{userName} deleting blog at link {permaLink} in {blogName} at {timestamp}')

if __name__ == "__main__":   
    # Get the database
    db = get_database()


    db.blogs.delete_many({})
    db.permaLinks.delete_many({})
    db.comments.delete_many({})


    #add blogs to same blog name
    post("ridiculusmus", "Medge Burnett", "eu neque pellentesque massa lobortis", "rutrum eu, ultrices sit amet, risus. Donec nibh enim, gravida sit amet, dapibus id, blandit", "sandwiches, desserts, noodles, seafood", "Jul 20, 2021")
    post("ridiculusmus", "Cruz Hoover", "pharetra, felis eget varius ultrices", "Praesent luctus. Curabitur egestas nunc sed libero. Proin sed turpis nec mauris blandit mattis.", "Cras, stews", "Dec 24, 2021")

    # # add another blog name 
    post("vel", "Xavier Carr", "ante dictum cursus. Nunc mauris", "orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc", "noodles, sandwiches", "Sep 3, 2021")

    # #first comment on blog 
    comment("vel", "vel.ante_dictum_cursus_Nunc_mauris", "Illana Frye", "Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida.", "Nov 13, 2021")

    # # reply to comment on blog 
    comment("vel", "Nov 13, 2021", "Walter Buckley", "interdum ligula eu enim. Etiam,posuere cubilia Curae Donec tincidunt. Donec vitae erat vel pede blandit congue. In scelerisque scelerisque", "Dec 20, 2021")
    comment("vel", "Dec 20, 2021", "asdf asdf", "asdfasdfasdfasdfasdfasfdasdffsdafdasdfasdf", "Jan 2, 2022")

    # delete comment
    delete("vel",  "Nov 13, 2021", "qwer qwer", "June 19, 2022")

    #delete post
    delete("ridiculusmus", "ridiculusmus.eu_neque_pellentesque_massa_lobortis", "zxcv zxcv", "July 25, 2022")


    # Bad Tests

    # no blog called "vl"
    #comment("vl", "vel.ante_dictum_cursus_Nunc_mauris", "Illana Frye", "Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida.", "Nov 13, 2021")

    #displayCollection(db)

# "elit, a feugiat tellus",Walter Buckley,interdum ligula eu enim. Etiam,posuere cubilia Curae Donec tincidunt. Donec vitae erat vel pede blandit congue. In scelerisque scelerisque,"noodles, seafood","Mar 6, 2021"
    
