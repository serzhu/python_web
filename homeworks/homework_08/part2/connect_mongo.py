from mongoengine import connect
from pymongo.server_api import ServerApi
import configparser
from pathlib import Path

p = Path(__file__)
config = configparser.ConfigParser()
config.read(p.parents[1] / 'config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True, server_api=ServerApi('1'))