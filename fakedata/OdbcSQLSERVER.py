from os import environ
from dotenv import load_dotenv
import pyodbc

load_dotenv()
pyodbc.drivers()
pyodbc.drivers()

try:
    connection = pyodbc.connect(
    driver=environ.get("DRIVER"),
    server=environ.get("HOST"),
    database=environ.get("DATABASE"),
    user=environ.get("UID"),
    password=environ.get("PWD"),
    trusted_connection='no'
    )
except Exception as E:
    print(E)
    exit()

cursor = connection.cursor()