#!/usr/bin/python

import argparse
import shutil
import sys
import utils 
import app
import logging
from sqlite3 import Error
from faker import Faker
from models.models import User, Project
from settings import Context
from client import Crawler
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(title = 'command', dest = 'command')

# TODO: Write this in a more clean way look at argparser docs more 

# create db parser 
create_db_parser = subparser.add_parser("create-db")
create_db_parser.add_argument("--db", type= str, default = "sqlite.db", help='Name of the db that would be created')

# Get the port number from the user as an argument 
server_parser = subparser.add_parser("start-server")
server_parser.add_argument("--port",type=int, default=5000, help="Port on which to start the flask server")
server_parser.add_argument("--db", type = str, default = "sqlite.db", help = "specify the db name for the http server")


clean_db_parser = subparser.add_parser('clean-db')
clean_db_parser.add_argument("--db" , type=str, default ="sqlite.db",  help ='Name of the database to delete' )


drop_db_parser = subparser.add_parser('drop-db')
drop_db_parser.add_argument('--db',type = str ,default = 'sqlite.db', help = 'Name of the database that we want to drop')
subparser.add_parser('stop-server')
subparser.required = True

generate_data_parser = subparser.add_parser("generate-data")
generate_data_parser.add_argument("--db", type = str, default = 'sqlite.db', help = 'name of the database that we want to generate data in')
generate_data_parser.add_argument("--data_size",  type= int, default = "10", help = 'number of data that you want to generate')


start_crawler_parser = subparser.add_parser("start-crawler")
start_crawler_parser.add_argument("--title",type = str, help ='title of the page that you want the crawler you start from')
start_crawler_parser.add_argument("--space", type = str, help = 'name of the space that you want to crawl')
start_crawler_parser.add_argument("--db", type= str,default = 'sqlite.db', help ='name of the db to dump the data ')

def create_db(args):
    db_name = args.db
    utils.create_db_util(db_name, './sql-scripts/create_tables.sql')

def start_server(args): 
    print(f'Listening for all incoming connections  at 0.0.0.0:{args.port}')
    app.start_server(args)

def stop_server(args):
    logging.debug(args)
    logging.info("Stopping server. Press Ctrl+c dude . What do you want me to do . Find the service process id and then kill it . Do not be lazy 😀 ")
    return 

def drop_db(args): 
    yes_or_no = input(f"Are you sure you want to delete the db {args.db} ? y/n")
    if yes_or_no.strip()=='y':
        import os 
        os.remove(args.db)
        return 
    
def clean_db(args): 
    db_name = args.db
    Context.setup(db_name)
    conn = Context.get_connection()
    cursor = conn.cursor()
    try:
        print("Starting clean up of all tables")
        with open('./sql-scripts/clean-tables.sql') as file: 
            lines = '\n'.join(file.readlines())
            cursor.executescript(lines)
        conn.commit()
        print("Cleaned all the tables")
        return 
    except Error as e: 
        logging.error(e)


def start_crawler(args):
    Context.setup(args.db)
    crawler = Crawler(page_title = args.title, space_key = args.space)
    crawler()

def generate_data(args):
    db_name = args.db 
    size = args.data_size
    Context.setup(db_name)
    conn = Context.get_connection()
    if not conn: 
        logging.error(f'Cannot get connection to ${db_name}')
        return 
    fake = Faker()

    for _ in range(size):
       proj = Project()
       proj.name = fake.word()+'-'+fake.word()
       proj.description = fake.text()
       proj.business_tags = fake.text()
       proj.project_link = 'https://'+fake.hostname()
       utils.insert_project(proj)

    for _ in range(size): 
        user = User()
        user.name = fake.name()
        user.email = fake.email()
        user.is_logged_in = False 
        user.hashed_password =  "random_passowrd"
        utils.insert_user(user)


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    args = parser.parse_args(sys.argv[1:])    
    if args.command == 'create-db': create_db(args)
    elif args.command == 'start-server':  start_server(args)
    elif args.command == 'stop-server':  stop_server(args)
    elif args.command == 'drop-db' : drop_db(args)
    elif args.command == 'generate-data':  generate_data(args)
    elif args.command == 'start-crawler' : start_crawler(args)
    elif args.command == 'clean-db' : clean_db(args)

