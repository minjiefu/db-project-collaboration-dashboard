from pymongo import MongoClient
import pandas as pd

# Query 1. In put given year, generate top 10 keywords with most publications in that year.


def get_top_10_keywords(start_year=1982, end_year=2023):
    # Making Connection
    myclient = MongoClient("mongodb://localhost:27017/")
    # database
    db = myclient["academicworld"]

    # Created or Switched to collection
    publication = db["publications"]

    query = [
        {"$match": {"year": {"$gte": start_year, "$lte": end_year}}},
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords.name", "publication count": {"$sum": 1}}},
        {"$sort": {"publication count": -1}},
        {"$limit": 10}
    ]

    result = publication.aggregate(query)

    result_query = pd.DataFrame(result).rename(columns={"_id": "keywords", "publication count": "publication counts"})

    return result_query


