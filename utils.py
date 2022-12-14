import logging
import sqlite3 
from sqlite3 import Error, Connection, Cursor  
from pathlib import Path
from typing import Dict, Union, List
from models.models import Project , User, BaseModel
from flask import make_response
from json import JSONEncoder
from settings import Context
from flask import session
def create_response(): 
    res =  make_response()
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res

class CustomEncoder(JSONEncoder): 
    def default(self, o: Union[BaseModel, List[BaseModel]])->List[Dict]: 
        if isinstance(o, BaseModel): 
            return [o.toJSON()]
        elif isinstance(o, list): 
            data = []
            for model in o: 
                data.append(model.toJSON())
            return data
        else: 
            raise NotImplemented("Expected data type to be of BaseModel or a list of BaseModel class")
        

def create_db_util(db_name: str, path_to_sql_script: str): # used only as the manager before startup  
    conn = None 
    Context.setup(db_name)
    with Context.get_connection() as conn: 
        with open(path_to_sql_script, 'r') as f: 
            content = '\n'.join(f.readlines())
            conn.executescript(content)
            logging.info(f'Executed the script {Path(path_to_sql_script).name}')
 
def insert_user(user: User)->User: 
    logging.info(f'Inserting user ${user.toJSON()}')
    if user.hashed_password is None: 
        raise Exception("password cannot be none")
    user.hashed_password = Context.bcrypt.generate_password_hash(user.hashed_password, 10)
    logging.debug(user.hashed_password)
    insert_stmt = 'insert into users(name, email, hashed_password) values(?, ?,?)' 
    with  Context.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_stmt,(user.name, user.email,user.hashed_password))
        if cursor.lastrowid:
            user.id = cursor.lastrowid
    return user 

def get_all_projects()->List[Project]:
    stmt = 'select name, description , project_link, business_tags from projects'
    with Context.get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute(stmt)
        rows = cursor.fetchall()
        projects = []
        for row in rows: 
            proj = Project()
            proj.business_tags = row[3]
            proj.project_link = row[2]
            proj.description = row[1]
            proj.name = row[0]
            projects.append(proj)
        
    return projects


def insert_project(project:Project)->Project:
    logging.info(f'Inserting Project ${project.toJSON()}')
    insert_stmt = 'insert into projects(name, description, project_link, business_tags) values(? ,?,?, ?)' 
    
    with Context.get_connection() as conn:  
        cursor = conn.cursor()
        cursor.execute(insert_stmt, (project.name, project.description, project.project_link, project.business_tags))
        if cursor.lastrowid:
            project.id = cursor.lastrowid
    return project 
    

def get_project_by_id(id:int)->Project: 
    stmt ='select name, description, project_link, business_tags from projects where id = ?'
    
    with Context.get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute(stmt, (id,))
        row = cursor.fetchone()
        project  = Project()
        project.name = row[0]
        project.description = row[1]
        project.project_link = row[2]
        project.business_tags = row[3]
    return project

def get_project_by_name(name: str)->List[Project]: 
    stmt ='select name, description, project_link, business_tags from projects where name = ?'
    with Context.get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute(stmt, (name,))
        rows = cursor.fetchall()
        projects = []
        for row in rows: 
            project  = Project()
            project.name = row[0]
            project.description = row[1]
            project.project_link = row[2]
            project.business_tags = row[3]
            projects.append(project)
        return projects

def get_project_by_description(descr:Union[str, None])->List[Project]: 
    logging.debug(descr)
    logging.debug("To be implemented by amlan")
    return get_all_projects() 

def get_project_by_tags(tag_list: str)->List[Project]: 
    # tag_list is split by commas 
    # also functional logic
    tags = [tag.strip() for tag in tag_list.split(',')]
    return get_all_projects()


def get_all_users()->List[User]:
    stmt = 'select id, name, email, hashed_password, is_logged_in from users'
    with Context.get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute(stmt)
        user_list = []
        for row in cursor.fetchall():
            user = User()
            user.id = row[0]
            user.name = row[1]
            user.email = row[2]
            user.hashed_password = row[3]
            user.is_logged_in = row[4]
            user_list.append(user)
    return user_list


def get_users_by_name(name: str)->List[User]: 
    stmt = 'select id, name, email, hashed_passwords, is_logged_in from users where name = ?'
    with Context.get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute(stmt)
        user_list = []
        for row in cursor.fetchall(): 
            user = User()
            user.id = row[0]
            user.name = row[1]
            user.email = row[2]
            user.hashed_password = row[3]
            user.is_logged_in = row[4]
            user_list.append(user)
    return user_list 

## email should be unique but should be okay for now
def get_users_by_mail(mail: str)->List[User]:
    user_list = []
    stmt = 'select id, name, email, hashed_passwords, is_logged_in from users where email = ?'
    with Context.get_connection() as conn: 
        cursor = conn.cursor()
        cursor.execute(stmt, mail.strip())
        for row in cursor.fetchall(): 
            user = User()
            user.id = row[0]
            user.name = row[1]
            user.email = row[2]
            user.hashed_password = row[3]
            user.is_logged_in = row[4]
            user_list.append(user)
    return user_list 

 

def authenticate_and_login_user(payload: Union[Dict, None])->bool:
    if payload is None: 
        return False
    ## very bad idea . no time . 
    stmt = 'select count(*) from users where name = ? and hashed_passwords = ?'
    
    with Context.get_connection() as conn: 
        name = payload['name']
        password = payload['password']
        encrypted_pwd = Context.bcrypt.generate_password_hash(password)
        cursor = conn.cursor()
        row = cursor.fetchone(stmt, (name, password))
        if row[0]==1:
            session['username'] = name 
            return True
        else: 
            return False 

    

