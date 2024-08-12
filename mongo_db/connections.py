import os
from urllib.parse import quote_plus
from pymongo import MongoClient

username = quote_plus(os.environ['MONGO_USER'])
password = quote_plus(os.environ['MONGO_PASSWORD'])
cluster = quote_plus(os.environ['MONGO_CLUSTER'])
db_name = quote_plus(os.environ['MONGO_DB'])
app_name = quote_plus(os.environ['MONGO_APP_NAME'])
mongo_uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + '/?retryWrites=true&w=majority&appName=' + app_name + '&Database=' + db_name
from_address = os.getenv("YOUR_EMAIL")
password = os.getenv("YOUR_EMAIL_PASS")

class Database:

    def __init__(self) -> None:
        pass

    def create_client(self):
        client = MongoClient(mongo_uri)
        self.client = client
        return client[db_name]
    
    def close_client(self):
        self.client.close()