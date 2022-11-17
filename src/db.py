from pymongo.server_api import ServerApi
import pymongo as pymongo
import os
from dotenv import load_dotenv

load_dotenv()

collection = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv('MONGODB_CREDENTIALS')}@cluster0.ybjnnvs.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi('1'))['yanajoj_db']['users']
