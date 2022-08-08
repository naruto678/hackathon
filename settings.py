## This is a global space for all the data. Will think of a better way next time 
## might cause data races and also might not be thread-safe .  
from collections.abc import Generator
from sqlite3 import Connection
from typing import Union, Dict
import utils
import sqlite3
import logging
from contextlib import contextmanager
## This will store all the settings data during the lifetime of the application 
## sqlite connections can only be used in a single thread  . 
## so have to create connection multiple times
class Context:

    connection = None 
    db_name : str = ''

    @staticmethod 
    def setup(db):
       Context.db_name = db 
       return 

    @classmethod
    @contextmanager
    def get_connection(cls)->Generator: 
        ## needs to be closed by the caller explicity
        conn = None
        try:
            if cls.db_name is None: 
                raise Exception("Db name cannot be none")
            conn = sqlite3.connect(cls.db_name)
            yield conn
        finally: 
            if conn:
                conn.commit()
                conn.close()

    

