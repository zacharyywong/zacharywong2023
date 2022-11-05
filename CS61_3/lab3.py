import pymongo
import urllib.parse
from bson import ObjectId
import json
import math
from pymongo import GEO2D

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
    print("Question 2: " + str(total) + '\n')

def question3(db):
    total = db.zipcodes.count_documents({"state":{"$in":['CT', 'RI', 'MA', 'VT', 'NH', 'ME']}})
    print("Question 3: " + str(total)+ '\n')


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
        print("Question 4: " + str(document)+ '\n')

def question5(db):
    cursor = db.zipcodes.find({}).sort("pop", 1).limit(1)
    
    for document in cursor:
        print("Question 5: " + str(document)+ '\n')

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
        print("Question 6: " + str(document)+ '\n')

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
        print("Question 7: " + str(document)+ '\n')

def question8(db):
    cursor = db.zipcodes.find({"pop": {"$gt": 50000}}, {"loc": 0}).limit(5)
    for document in cursor:
        print("Question 8: " + str(document)+ '\n')

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
        print("Question 9: " + str(document)+ '\n')


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
        print("Part2Num1: " + str(document)+ '\n')

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
        print("Part2Num2: " + str(document)+ '\n')


def Part2Num3(db): 
    # db.cardAmounts.drop();
#     for (transaction = 0; transaction < 100; transaction++){
# ... var r = {'amount': Math.random()*100+1}
# ... db.cardAmounts.insertOne(r);}
    pass

def Part2Num4(db): 
#     use('lab3');

#     db.zipcodes.updateMany(
#     {}, 
#     {$set: {"plusFour": "0000"}}, 
#     upsert = false, 
#     multi = true
# )
    pass

# exclude alaska and hawaii
# smallest latitude + ((largest latitude - smallest latittude) / 2)
# smallest longitude + ((largest longitude - smallest longitude) / 2)
def findLocation(db, locIndex, smallLarge):

    cursor = db.zipcodes.aggregate([
        {
            "$unwind": 
            {
                "path": "$loc",
                "includeArrayIndex": "locIndex"
            }
        },

        {
            "$match":
            {
                "$and": [
                    {
                        "state": 
                            {"$nin": ['AK', 'HI']}
                        
                    }, 
                    {
                        "locIndex": locIndex
                    }

                ]
                
            }
        },
        {
            "$sort":
            {
                "loc": smallLarge
            }
        }, 
        {
            "$project":
            {
                "plusFour": 0, 
                "pop": 0

            }
        },
        {
            "$limit": 1
        }
    
    ])

    for document in cursor:
       #print("findLocation: " + str(document)+ '\n')
       return document
        #return document['loc']

def findZip(db, middleLatitude, middleLongitude):
    db.zipcodes.create_index([("loc", GEO2D)])
    #cursor = db.zipcodes.find({"loc": {"$near": [middleLongitude, middleLatitude]}}).limit(5)
    cursor = db.zipcodes.find({"loc": {"$near": [middleLongitude, middleLatitude]}}).limit(1)
    for document in cursor:
       print("findZip: " + str(document)+ '\n')
       
def extraCredit(db):

    longitude = 0
    latitude = 1
    ascending = 1
    descending = -1

    mostSouthernLatitude = findLocation(db, latitude, ascending)
    mostNorthernLatitude = findLocation(db, latitude, descending)
    mostWesternLongitude = findLocation(db, longitude, ascending)
    mostEasternLongitude = findLocation(db, longitude, descending)
    
    print("Most Southern Latitude: " + str(mostSouthernLatitude) + "\nMost Northern Latitude: " + str(mostNorthernLatitude) + '\n')
    print("Most Western Longitude: " + str(mostWesternLongitude) + "\nMost Eastern Longitude: " + str(mostEasternLongitude) + '\n')

    middleLatitude = mostSouthernLatitude['loc'] + ((mostNorthernLatitude['loc'] - mostSouthernLatitude['loc'])/2)
    middleLongitude = mostWesternLongitude['loc'] + ((abs(mostWesternLongitude['loc']) - abs(mostEasternLongitude['loc']))/2)

    print(str(middleLatitude) + ', ' + str(middleLongitude))

    findZip(db, middleLatitude, middleLongitude)




# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    db = get_database()
    question2(db)
    question3(db)
    question4(db)
    question5(db)
    question6(db)
    question7(db)
    question8(db)
    question9(db)
    Part2Num1(db)
    Part2Num2(db)
    Part2Num3(db)
    Part2Num4(db)
    extraCredit(db)



    
