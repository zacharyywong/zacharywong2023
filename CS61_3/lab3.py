import pymongo
import urllib.parse
from bson import ObjectId


def get_database():
 
   client = pymongo.MongoClient("mongodb+srv://zacharyywong:" + urllib.parse.quote("3Cs@CodeRed") + "@lab3.htmdfxa.mongodb.net/?retryWrites=true&w=majority")
   db = client.lab3 
   return db
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   

    
    # Get the database
    db = get_database()


    
    # cursor = db.zipcodes.find({"_id": "01001"})
    # for document in cursor:
    #     print(document)
