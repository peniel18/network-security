import sys
import os 
import certifi 
from dotenv import load_dotenv 

load_dotenv()
MANGO_DB_URI = os.getenv("MANGO_DB_URI")
ca = certifi.where()
print(MANGO_DB_URI)
