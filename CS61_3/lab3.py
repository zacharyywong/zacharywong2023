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
    return total

    print("Question 2: " + str(total) + '\n')

def question3(db):
    total = db.zipcodes.count_documents({"state":{"$in":['CT', 'RI', 'MA', 'VT', 'NH', 'ME']}})
    #return total

    print(total)


def question4(db):
    cursor = db.zipcodes.aggregate([
        
        {
            "$group": {"_id": {'state': "$state"},'totalPop': {"$sum": '$pop'}}
        },

        {
             "$match": {"_id":{'state': 'RI'}}
         }
       
    ])
    for document in cursor:
        print (document['_id']['state'], document['totalPop'])
        #print(document['_id']['state'], document['totalPop'])
        #print("Question 4: " + str(document)+ '\n')

def question5(db):
    cursor = db.zipcodes.find({}, {"pop": 1}).sort("pop", 1).limit(1)
    for document in cursor: 
        minPop = document['pop']

    cursor1 = db.zipcodes.aggregate([
        {
            "$match":
            {
                "pop": minPop
            }
        }, 
        {
            "$project":
            {
                "_id": 1, 
                "city": 1, 
                "pop": 1
            }
        }
    ])
    
    for document in cursor1:
       print(document)

#where latitude is closest to 0 or smallest
# can't be negative 
def question6(db):
    cursor = db.zipcodes.aggregate([
        
        {
            "$project": 
                {
                    "loc": 1
                }
        }, 

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
        print("Question 6: " + str(document['_id']))
        #print("Question 6: " + str(document['_id'])+ '\n')

def question7(db):
    result = []
    cursor = db.zipcodes.aggregate([
        {
            "$group":
            {
                "_id": "$state", 
                "sumPop": {"$sum": "$pop"}
                
            }, 
        },

       {
           "$project":
           {
                "stateSubStr":
                {
                   "$substr": ["$_id", 0, 1]
               },
               "sumPop": 1,
           }
       },
 
       {
           "$match": {"stateSubStr": {"$eq": "M"}}
       }, 
       {
            "$group":
            {
                "_id": "$stateSubStr", 
                "avgPop": {"$avg": "$sumPop"}
                
            }, 
        }
       
   ])

    for document in cursor:
        print(f"Question 7: {document['avgPop']}")
    return result

def question8(db):
    cursor = db.zipcodes.find({"pop": {"$gt": 50000}}, {"_id": 1, "pop": 1})
    for document in cursor:
        #return document
        print(document['_id'])

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
                "_id": {"city": "$city"},
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

    for document in cursor:
        print(document["_id"])


def Part2Num1(db):
    cursor = db.zipcodes.aggregate([
        {
            "$match": 
            {
                "state": {"$eq": "LA"}
            }
        },
        {
            "$project":
            {
                "pop": 1
            }
        },
        {
            "$sort": {"pop": -1}
        }
    ])

    for document in cursor:
        print(document["_id"])

def Part2Num2(db):
    cursor = db.zipcodes.aggregate([
        {
            "$group":
            {
                "_id": {"state": "$state"}, 
                "countZipCodes": {"$count": {}}
            }
        }, 

        {
            "$project":
            {
                "countZipCodes": 1
            }
        },

        {
            "$sort": 
            {
                "countZipCodes": 1
            }
        },
        {
            "$limit": 1
        }
    ])

    for document in cursor:
        #return document
        print("Part2Num2: " + str(document)+ '\n')


def Part2Num3(db): 
    db.cardAmounts.drop();
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    
    
    for (transaction = 0; transaction < 100; transaction++){
        cardNumber = new String();
        let month = 0;
        let year = 0;
        for (let i = 0; i < 12; i++){
            cardNumber += characters.charAt(Math.floor(Math.random() * characters.length));
        };

        month = 1 + Math.floor(Math.random()* 12)
        year = 2000 + Math.floor(Math.random() * 21)
        var r = { 
                "cardNo": cardNumber,
                "expDate": {"mm": month, "yy": year},
                'amount': (Math.random()*10000).toFixed(2),
                "secCode": Math.round(Math.random()* 100)/1
                };   
        
        db.cardAmounts.insertOne(r);}

        db.cardAmounts.find({});

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


# finds smallest or largest latitude or longitude in zipcodes
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
       return document

# finds zip code nearest to a coordinate point
def findZip(db, middleLatitude, middleLongitude):
    db.zipcodes.create_index([("loc", GEO2D)])
    cursor = db.zipcodes.find({"loc": {"$near": [middleLongitude, middleLatitude]}}, {"plusFour": 0}).limit(1)
    for document in cursor:
       print("\nNearest Zipcode To Central Coordinates: " + str(document)+ '\n')
       

# exclude alaska and hawaii
# smallest latitude + ((largest latitude - smallest latittude) / 2)
# smallest longitude + ((largest longitude - smallest longitude) / 2)
def extraCredit(db):

    longitude = 0
    latitude = 1
    ascending = 1
    descending = -1

    mostSouthernLatitude = findLocation(db, latitude, ascending)
    mostNorthernLatitude = findLocation(db, latitude, descending)
    mostWesternLongitude = findLocation(db, longitude, ascending)
    mostEasternLongitude = findLocation(db, longitude, descending)
    middleLatitude = mostSouthernLatitude['loc'] + ((mostNorthernLatitude['loc'] - mostSouthernLatitude['loc'])/2)
    middleLongitude = mostWesternLongitude['loc'] + ((abs(mostWesternLongitude['loc']) - abs(mostEasternLongitude['loc']))/2)

    print("Central Coordinates: " + str(middleLatitude) + ', ' + str(middleLongitude))
    findZip(db, middleLatitude, middleLongitude)
    print("Most Southern Latitude: " + str(mostSouthernLatitude) + "\n\nMost Northern Latitude: " + str(mostNorthernLatitude) + '\n')
    print("Most Western Longitude: " + str(mostWesternLongitude) + "\n\nMost Eastern Longitude: " + str(mostEasternLongitude) + '\n')




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



    
