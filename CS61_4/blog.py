import pymongo
import urllib.parse
from bson import ObjectId
import json
from pprint import pprint
import re
from operator import itemgetter

import datetime
import textwrap




def get_database():
    f = open (r'/Users/zacharywong/Documents/Work/Dartmouth/CS61/CS61/URI/URI.json')
    content = json.load(f)
    f.close()

    URI = content["user"] + urllib.parse.quote(content["password"]) + content["server"]
    client = pymongo.MongoClient(URI)
    
    db = client.lab4
    return db

def addIndent(str, indentMultiplier):
    str = '   ' * indentMultiplier + str
    return str


def displayCollection(db):
    cursor = db.blogs.find({})
    # for document in cursor:
    #     pprint(document)

def createLink(blogName, title):
    permaLink  = blogName+'.'+re.sub('[^0-9a-zA-Z]+', '_', title)
    return permaLink

def insertOrderDisplay(orderDisplayList, newTimeStamp, oldTimeStamp):

    if oldTimeStamp == None:
        for i in range(len(orderDisplayList)):
            if orderDisplayList[i] > newTimeStamp:
                orderDisplayList.insert(i-1, newTimeStamp)
                return orderDisplayList
        orderDisplayList.append(newTimeStamp)
        return orderDisplayList

    for i in range(len(orderDisplayList)):
        if orderDisplayList[i] == oldTimeStamp:
            if i == len(orderDisplayList)-1:
                orderDisplayList.append(newTimeStamp)
            else:
                orderDisplayList.insert(i+1, newTimeStamp)
            return orderDisplayList
   
    orderDisplayList.append(newTimeStamp)
    return orderDisplayList

def checkPostTitleTimeStamp(blogName, title, timestamp):
    cursor = db.blogs.find(
        {"blogName": blogName, 
        "$or": [
            {"blogPosts.title": title}, 
            {"blogPosts.timestamp": timestamp}
            ]
            })
    if len(list(cursor.clone())) == 0:
        return True
    else:
        return False

def checkCommentTimeStamp(blogName, timestamp): 
    cursor = db.comments.find(
        {"blogName": blogName, "blogDiscussion.permaLink": timestamp})

    if len(list(cursor.clone())) == 0:
        return True
    else:
        return False
# def insertPermaLinkSchema(permaLink):
#     db.permaLinks.insert_one(
#         {
#         "links":
#             {
#                 "permaLink": permaLink
#             }
#         }
#     )

def insertBlog(blogName, userName, title, postBody, tags, timestamp, permaLink):
    db.blogs.insert_one(
        {
            "blogName": blogName,
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




def updateBlog(blogName, userName, title, postBody, tags, timestamp, permaLink):
    db.blogs.update_one(
        {"blogName": blogName},
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


def insertComment(blogName, userName, commentBody, timestamp, permaLink):
    db.comments.insert_one(
        {
            "blogName": blogName, 
            "blogDiscussion":
            [
                {
                    "originalPostLink": permaLink,
                    "userName": userName,
                    "commentBody": commentBody,
                    "permaLink": timestamp
                    
                }
            
            ]
        }
    )

def insertReply(blogName, userName, commentBody, timestamp, permaLink):
    db.comments.update_one(
        {
            "blogName": blogName
        }, 
        {
        "$push":
            {
                "blogDiscussion":
                {
                "originalPostLink": permaLink,
                "userName": userName,
                "commentBody": commentBody,
                "permaLink": timestamp
                    
                }
            }
        }
    )


def post(blogName, userName, title, postBody, tags, timestamp):
    cursor = db.blogs.find({"blogName": blogName})
    permaLink = createLink(blogName, title)
    if len(list(cursor.clone())) == 0:
        insertBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)
    elif checkPostTitleTimeStamp(blogName, title, timestamp) == True:
        print(f'{userName} inserting blog {title} in {blogName} at {timestamp}')
        updateBlog(blogName, userName, title, postBody, tags, timestamp, permaLink)
    else:
        raise ValueError(f"either post '{title}' already published in '{blogName}' or your post has the same timestamp ('{timestamp}') as another post")
        
    

    

def comment(blogName, permaLink, userName, commentBody, timestamp):
    cursor = db.blogs.find({"blogName": blogName})
    if len(list(cursor)) == 0:
        cursor1 = db.comments.find({"blogName": blogName, "blogDiscussion.permaLink": permaLink})
        documentsFound = len(list(cursor1.clone()))
        if documentsFound == 0:
                raise ValueError("No blogs or comments found to comment on")
    
    elif checkCommentTimeStamp(blogName, timestamp):
        cursor2 = db.comments.find({"blogName": blogName})
        documentsFound = len(list(cursor2.clone()))
        if documentsFound == 0:
            print(f'{userName} inserting comment in blog {blogName} at {timestamp}')
            insertComment(blogName, userName, commentBody, timestamp, permaLink)
        else:
            print(f'{userName} inserting reply to comment link {permaLink} in {blogName} at {timestamp}')
            insertReply(blogName, userName, commentBody, timestamp, permaLink)

    else:
        raise ValueError(f"Can't comment at the same time as another comment at '{timestamp}'")
        


def deleteBlog(blogName, permaLink, userName, timestamp):
    db.blogs.update_one(
        {
            "blogName": blogName, 
            "blogPosts.permaLink": permaLink
        }, 
        {
            "$set":
            {
                "blogPosts.$.postBody": f"deleted by {userName} at {timestamp}",
                "blogPosts.$.deletedTimestamp": timestamp
            }
        }
    )
    
def deleteComment(blogName, permaLink, userName, timestamp):
    db.comments.update_one(
        {
            "blogName": blogName, 
            "blogDiscussion.permaLink": permaLink
        }, 
        {   
            "$set":
            {
                "blogDiscussion.$.commentBody": f"deleted by {userName} at {timestamp}",
                "blogDiscussion.$.deletedTimestamp": timestamp
            }
        }
    )

def delete(blogName, permaLink, userName, timestamp):
    cursor = db.blogs.find({"blogName": blogName, "blogPosts.permaLink": permaLink})

    postsFound = len(list(cursor.clone()))

    if postsFound == 0:
        cursor1 = db.comments.find({"blogName": blogName, "blogDiscussion.permaLink": permaLink})
        commentsFound = len(list(cursor1.clone()))
        if commentsFound == 0:
            raise ValueError("No blogs or comments found to delete")
        else:
            deleteComment(blogName, permaLink, userName, timestamp)
            print(f'{userName} deleting comment at link {permaLink} in {blogName} at {timestamp}')
    else:
        deleteBlog(blogName, permaLink, userName, timestamp)
        print(f'{userName} deleting blog at link {permaLink} in {blogName} at {timestamp}')

def showPost(post, discussionsDisplay, commentsDisplayOrder, indentMultiplierBlogName, indentMultiplierPostBody, indentDictionary):
    title = post['title']
    userName = post['userName']
    tags = post['tags']
    timestamp = post['timestamp']
    permaLink = post['permaLink']
    postBody = post['postBody']

    discussionsDisplay.append([addIndent(f"title: {title}", indentMultiplierBlogName), 
                addIndent(f"userName: {userName}", indentMultiplierBlogName), 
                addIndent(f"tags: {tags}", indentMultiplierBlogName), 
                addIndent(f"timestamp: {timestamp}", indentMultiplierBlogName), 
                addIndent(f"permaLink: {permaLink}", indentMultiplierBlogName),
                addIndent(f"postBody: ", indentMultiplierBlogName), 
                addIndent(f"{postBody}", indentMultiplierPostBody), 
                addIndent(f"----", indentMultiplierPostBody)])
    indentDictionary[permaLink] = indentMultiplierBlogName
    commentsDisplayOrder.append(post)
    return discussionsDisplay, commentsDisplayOrder, indentDictionary

def showOriginalComment(comment, discussionsDisplay, indentMultiplierBlogComment, indentMultiplierBlogCommentBody, indentDictionary, commentsDisplayOrder):
    userName = comment['userName']
    commentBody = comment['commentBody']
    permaLink = comment['permaLink']

    discussionsDisplay.append([addIndent(f"userName: {userName}", indentMultiplierBlogComment), 
                addIndent(f"timestamp: {permaLink}", indentMultiplierBlogComment), 
                addIndent(f"commentBody: ", indentMultiplierBlogComment), 
                addIndent(f"{commentBody}", indentMultiplierBlogCommentBody), 
                addIndent(f"----", indentMultiplierBlogCommentBody)])
    indentDictionary[permaLink] = indentMultiplierBlogComment
    commentsDisplayOrder.append(comment)
    # print(f"original comment timestamp: {timestamp} by {userName}")

    return discussionsDisplay, indentDictionary, commentsDisplayOrder

def insertCommentDisplay(commentsDisplayOrder, reply, insertIndex, indentDictionary, discussionsDisplay, append):
    userName = reply['userName']
    commentBody = reply['commentBody']
    permaLink = reply['permaLink']
    indentMultiplier = indentDictionary[commentsDisplayOrder[insertIndex]['permaLink']] + 1

    if not append: 
        discussionsDisplay.insert(insertIndex+1, [addIndent(f'userName: {userName}', indentMultiplier),  
                    addIndent(f"timestamp: {permaLink}", indentMultiplier),
                        addIndent(f"commentBody: ", indentMultiplier), 
                        addIndent(f"{commentBody}", indentMultiplier+1), 
                        addIndent(f"----", indentMultiplier + 1)])
        commentsDisplayOrder.insert(insertIndex+1, reply)

    else:
        discussionsDisplay.append([addIndent(f'userName: {userName}', indentMultiplier),  
                    addIndent(f"timestamp: {permaLink}", indentMultiplier),
                        addIndent(f"commentBody: ", indentMultiplier), 
                        addIndent(f"{commentBody}", indentMultiplier+1), 
                        addIndent(f"----", indentMultiplier + 1)])
        commentsDisplayOrder.append(reply)

    return commentsDisplayOrder, discussionsDisplay, permaLink, indentDictionary, indentMultiplier


def updateCommentAndIndent(commentsDisplayOrder, reply, checkInsertIndex, indentDictionary, discussionsDisplay, append):
    commentsDisplayOrder, discussionsDisplay, permaLink, indentDictionary, indentMultiplier = insertCommentDisplay(commentsDisplayOrder, reply, checkInsertIndex, indentDictionary, discussionsDisplay, append)
    indentDictionary[permaLink] = indentMultiplier
    return discussionsDisplay, indentDictionary, commentsDisplayOrder


def showReplies(reply, commentsDisplayOrder, discussionsDisplay, indentDictionary):
    replyPermaLink = reply['originalPostLink']
    checkInsertIndex = 0
    while checkInsertIndex < len(commentsDisplayOrder):
        if commentsDisplayOrder[checkInsertIndex]['permaLink'] == replyPermaLink:
            if checkInsertIndex + 1 >= len(commentsDisplayOrder):
                discussionsDisplay, indentDictionary, commentsDisplayOrder = updateCommentAndIndent(commentsDisplayOrder, reply, checkInsertIndex, indentDictionary, discussionsDisplay, append = True)
                return discussionsDisplay, indentDictionary, commentsDisplayOrder
            if commentsDisplayOrder[checkInsertIndex+1]['permaLink'] != replyPermaLink:
                discussionsDisplay, indentDictionary, commentsDisplayOrder = updateCommentAndIndent(commentsDisplayOrder, reply, checkInsertIndex, indentDictionary, discussionsDisplay, append = False)
                return discussionsDisplay, indentDictionary, commentsDisplayOrder
            if reply['permaLink'] > commentsDisplayOrder[checkInsertIndex + 1]['permaLink']:
                discussionsDisplay, indentDictionary, commentsDisplayOrder = updateCommentAndIndent(commentsDisplayOrder, reply, checkInsertIndex, indentDictionary, discussionsDisplay, append = False)
                return discussionsDisplay, indentDictionary, commentsDisplayOrder
        checkInsertIndex += 1
    discussionsDisplay, indentDictionary, commentsDisplayOrder = updateCommentAndIndent(commentsDisplayOrder, reply, checkInsertIndex, indentDictionary, discussionsDisplay, append = False)
    return discussionsDisplay, indentDictionary, commentsDisplayOrder

def showDiscussion(blogName, blogPostsOrdered, discussionsDisplay, commentsDisplayOrder, indentMultiplierBlogComment,indentMultiplierBlogCommentBody, indentDictionary):
    cursor = db.comments.find({"blogName": blogName})
    originalComments = []
    replies = []
    for discussionThread in cursor:
        repliesOrderedAsc = sorted(discussionThread['blogDiscussion'], key = itemgetter('permaLink'), reverse=False)
        for reply in repliesOrderedAsc:
            discussionsDisplay, indentDictionary, commentsDisplayOrder = showReplies(reply, commentsDisplayOrder, discussionsDisplay, indentDictionary)

    # print(indentDictionary)
    return discussionsDisplay

def show(blogName):
    indentMultiplierBlogName = 0
    indentMultiplierPostBody = 1
    indentMultiplierBlogComment = 2
    indentMultiplierBlogCommentBody = 3
    
    #discussionsDisplay = []
    blogNameDisplay = []
    discussionsDisplay = []
    commentsDisplayOrder = []
    indentDictionary = {}

    result = []
    cursor = db.blogs.find({"blogName": blogName})
    blogNameDisplay.append([f'\nIn {blogName}\n'])
    for line in blogNameDisplay:
        result.append(line)

    for blog in cursor: 
        blogPostsOrdered = sorted(blog['blogPosts'], key = itemgetter('timestamp'), reverse=True)

    for post in blogPostsOrdered:
        discussionsDisplay, commentsDisplayOrder, indentDictionary = showPost(post, discussionsDisplay, commentsDisplayOrder, indentMultiplierBlogName, indentMultiplierPostBody, indentDictionary)
    
    showDiscussion(blogName, blogPostsOrdered, discussionsDisplay, commentsDisplayOrder, indentMultiplierBlogComment,indentMultiplierBlogCommentBody, indentDictionary)
    
    for block in discussionsDisplay:
        result.append(block)

    
    
    # for block in discussionsDisplay:
    #     result.append(block)

    for display in result: 
        for line in display:
            print(line)

def testBlogEngine(db):
    db.blogs.delete_many({})
    db.comments.delete_many({})


    #add blogs to same blog name
    post("ridiculusmus", "Medge Burnett", "eu neque pellentesque massa lobortis", "rutrum eu, ultrices sit amet, risus. Donec nibh enim, gravida sit amet, dapibus id, blandit", "sandwiches, desserts, noodles, seafood", datetime.datetime(2021,3,9))
    post("ridiculusmus", "Cruz Hoover", "pharetra, felis eget varius ultrices", "Praesent luctus. Curabitur egestas nunc sed libero. Proin sed turpis nec mauris blandit mattis.", "Cras, stews", datetime.datetime(2021, 12, 24))
    post("vel", "Xavier Carr", "ante dictum cursus. Nunc mauris", "orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc", "noodles, sandwiches", datetime.datetime(2021,3,9))
    post("vel", "idol", "tttt", "dddd", "octopus, fish", datetime.datetime(2022,1,20))
    
    comment("vel", "vel.ante_dictum_cursus_Nunc_mauris", "Illana Frye", "comment under vel.ante post", datetime.datetime(2021,11,13))
    comment("vel", "vel.ante_dictum_cursus_Nunc_mauris", "098098", "comment under vel.ante post", datetime.datetime(2022, 9,1))
    comment("vel", datetime.datetime(2021,11,13), "Walter Buckley", "reply under Illana Frye comment", datetime.datetime(2021,12,20))
    comment("vel", datetime.datetime(2021,12,20), "asdf asdf", "reply under Walter Buckley comment", datetime.datetime(2022,1,2))
    comment("vel", datetime.datetime(2021,11,13), "1234 1234", "reply under Illana Frye comment", datetime.datetime(2022,8,10))
    comment("vel", datetime.datetime(2022,1,2), "-=-=-=-=-=", "reply under asdf asdf comment", datetime.datetime(2022,9,10))
    comment("vel", datetime.datetime(2021,11,13), "zxcv,mn", "reply under Illana Frye comment", datetime.datetime(2022,11,10))
    comment("vel", datetime.datetime(2022, 9,1), "aaaaaaaa", "reply under 098098 comment", datetime.datetime(2022, 10,1))
    comment("vel", datetime.datetime(2022, 9,1), "bbbbbbbbb", "reply under 098098 comment", datetime.datetime(2022, 11,1))


    comment("vel", "vel.tttt", "husky", "comment under vel.tttt post in vel", datetime.datetime(2022,2,20))

    post("vel", "Clare Guerrero", "urna justo faucibus", "massa. Quisque porttitor eros nec tellus. Nunc lectus pede, ultrices", "bananas, monkeys", datetime.datetime(2022, 2, 15))
    comment("vel", "vel.urna_justo_faucibus", "Keefe Levine", "comment under vel.urna post", datetime.datetime(2022, 3, 1))
    comment("vel", datetime.datetime(2022, 3, 1), "Quamar Bullock", "reply under Keefe Levine comment", datetime.datetime(2022, 3, 21))
    comment("vel", "vel.urna_justo_faucibus", "Delilah Cox", "comment under vel.urna post", datetime.datetime(2022, 1, 1))
    
    comment("ridiculusmus", "ridiculusmus.eu_neque_pellentesque_massa_lobortis", "Derek Phelps", "a sollicitudin orci sem eget massa. Suspendisse eleifend. Cras sed", datetime.datetime(2021,11,13))

    # delete post and comment
    delete("vel",  "vel.urna_justo_faucibus", "qwer qwer", datetime.datetime(2022,6,9))
    delete("vel",  datetime.datetime(2022,3,21), "Kirk Mckay", datetime.datetime(2022,5,9))
if __name__ == "__main__":   
    # Get the database
    db = get_database()
    testBlogEngine(db)
    show("vel")


    # Tests for Invalid Actions/Inputs

    # no blog to comment on called "vl"
    #comment("vl", "vel.ante_dictum_cursus_Nunc_mauris", "Illana Frye", "Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida.", "Nov 13, 2021")

    # no comment found to reply on
    # comment("vl", datetime.datetime(1, 1, 1), "Illana Frye", "Nullam scelerisque,et nunc. Quisque ornare tortor at risus. Nunc ac sem ut dolor dapibus gravida.", "Nov 13, 2021")

    # cannot post a post with same title as another post
    # post("vel", "Timothy Ty", "ante dictum cursus. Nunc mauris", "orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc", "noodles, sandwiches", datetime.datetime(2021,3,9))

    # post with the same timestamp as another cannot be published
    # post("vel", "Frank Gerber", "Suspendisse commodo", "tincidunt nibh. Phasellus nulla. Integer vulputate, risus a", "frozen yogurt, salmon", datetime.datetime(2021,3,9))

    # comment with the same timestamp as another cannot be published
    # comment("vel", datetime.datetime(2021, 11, 13), "Alyssa Shu", "Quisque ac tincidunt nibh. Phasellus nulla. Integer vulputate, risus a", datetime.datetime(2022,3,1))

    
