from model import *
import sqlite3 as dbapi
conn = dbapi.connect('vaja_seminarska_v4.db')

tab= vse_ekipe_sezona(conn,"2017/18")
