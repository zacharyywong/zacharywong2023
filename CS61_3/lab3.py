import pymongo
import urllib.parse
from bson import ObjectId


def get_database():
 
   client = pymongo.MongoClient("mongodb+srv://zacharyywong:" + urllib.parse.quote("3Cs@CodeRed") + "@lab3.htmdfxa.mongodb.net/?retryWrites=true&w=majority")
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
            "$group": {"_id": {'state': "$state", 'population': '$population'},'total': {"$sum": '$pop'}}
        },

        {
             "$match": {"_id":{'state': 'RI'}}
         }
       
    ])
    for document in cursor:
        print("Question 4: " + str(document))


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
    # Get the database
    db = get_database()
    answer2 = question2(db)
    answer3 = question3(db)
    answer4 = question4(db)


    
