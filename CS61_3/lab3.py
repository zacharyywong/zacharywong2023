import pymongo
import urllib.parse
from bson import ObjectId
import json


def get_database():
    f = open (r'/Users/zacharywong/Documents/Work/Dartmouth/CS61/CS61/URI/URI.json')
    content = json.load(f)
    f.close()

    URI = content["user"] + urllib.parse.quote(content["password"]) + content["server"]
    client = pymongo.MongoClient(URI)
    
    db = client.lab3
    return db

#Assumes every document id equals city zip code and is unique 
def question2(db):
    total = db.zipcodes.count_documents({})
    # total = 0
    # for document in cursor:
    #      total += 1
    print("Question 2: " + str(total))
    return total

def question3(db):
    total = db.zipcodes.count_documents({"state":{"$in":['CT', 'RI', 'MA', 'VT', 'NH', 'ME']}})
    print("Question 3: " + str(total))
    return total


def question4(db):
    cursor = db.zipcodes.aggregate([
        
        {
            "$group": {"_id": {'state': "$state"},'total': {"$sum": '$pop'}}
        },

        {
             "$match": {"_id":{'state': 'RI'}}
         }
       
    ])
    for document in cursor:
        print("Question 4: " + str(document))

def question5(db):
    cursor = db.zipcodes.find({"loc": 0}).sort("pop", 1).limit(1)
    
    for document in cursor:
        print("Question 5: " + str(document))

#where latitude is closest to 0 or smallest
# can't be negative 
def question6(db):
    cursor = db.zipcodes.aggregate([
        {
            "$unwind": "$loc"
        },

        {
            "$match": {"loc": {"$gt": 0}}
        },

        {
            "$sort": {"loc": 1}
        },

        {
            "$limit": 1
        }
    ])
    for document in cursor:
        print("Question 6: " + str(document))

def question7(db):
    cursor = db.zipcodes.aggregate([
        {
            "$project": 
            {
                 "stateSubStr": 
                 {
                    "$substr": ["$state", 0, 1]
                },
                "city": 1,
                "state": 1,
                "pop": 1
            }
        },

        {
            "$match": {"stateSubStr": {"$eq": "M"}}
        },

        {
            "$group": {"_id": "$stateSubStr", "avgPop": {"$avg": "$pop"}}
        }
    ])
    for document in cursor:
        print("Question 7: " + str(document))

def question8(db):
    cursor = db.zipcodes.find({"pop": {"$gt": 50000}}, {"loc": 0}).limit(5)
    for document in cursor:
        print("Question 8: " + str(document))

def question9(db):
    cursor = db.zipcodes.aggregate([
        {
            "$project": 
            {
                "state": 1,
                "city": 1
            }
        },

        {
            "$group": 
            {
                "_id": {"city": "$city", "state": "$state"},
                "count": {"$count": {}}
            }
        },

        {
            "$sort": 
            {
                "count": -1
            }
        }, 
        
        {
            "$limit": 5
        }
    
    ])

    for document in cursor:
        print("Question 9: " + str(document))


def Part2Num1(db):
    cursor = db.zipcodes.aggregate([
        {
            "$match": 
            {
                "state": {"$eq": "LA"}
            }
        },
        {
            "$sort": {"pop": -1}
        },
        {
            "$limit": 5
        }
    ])

    for document in cursor:
        print("Part2Num1: " + str(document))

def Part2Num2(db):
    cursor = db.zipcodes.aggregate([

        {
            "$group":
            {
                "_id": {"state": "$state"}, 
                "count": {"$count": {}}
            }
        }, 
        {
            "$sort": 
            {
                "count": -1
            }
        },
        {
            "$limit": 1
        }
    ])

    # cursor = db.stateZipCount.aggregate([

    #     {
    #         "$group":
    #         {
    #             "_id": None, 
    #             "total": {"$sum": "$count"}
    #         }
    #     }
    
    # ])

    for document in cursor:
        print("Part2Num2: " + str(document))


def Part2Num3(db): 
    


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    db = get_database()
    answer2 = question2(db)
    answer3 = question3(db)
    answer4 = question4(db)
    answer5 = question5(db)
    answer6 = question6(db)
    answer7 = question7(db)
    answer8 = question8(db)
    answer9 = question9(db)
    answerPart2Num1 = Part2Num1(db)
    answerPart2Num2 = Part2Num2(db)
    answerPart2Num2 = Part2Num3(db)


    
