from src.db.config import DB_CLUSTER, DB_NAME
import certifi
from pymongo import MongoClient


def get_db():
    #should return an instance of DB
    client = MongoClient(DB_CLUSTER, tlsCAFile=certifi.where())
    return client[DB_NAME]
    
