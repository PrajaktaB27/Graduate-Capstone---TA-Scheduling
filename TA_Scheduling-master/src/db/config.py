from src.config import *
from os import environ

DB_CLUSTER = environ.get("CLUSTER")
DB_NAME = environ.get("DB_NAME")
