from flask import Flask, redirect, render_template, url_for
from flask import session
import logging
from flask_restx import Api, Resource, Namespace, fields
from flask_restx.reqparse import HTTPStatus
from settings import Context
import utils
import json
from models.models import User, Project
from flask import session
from flask_bcrypt import Bcrypt
project_ns = Namespace('projects',description='Contains all the project operations')
user_ns = Namespace('users', description='Contains all the user operations')


app = Flask(__name__)

api = Api(app, version = "0.1" , title = 'Automation-Api-Wells-Fargo', description = 'One stop for all wells fargo tools hosted on marketplace docs/swagger pages ')


api.add_namespace(project_ns)
api.add_namespace(user_ns)

user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='user unique identifier'),
    'name': fields.String(required=True, description='user name') , 
    'email': fields.String(required=True, description="user email"),
    'hashed_password' : fields.String(readonly=True, description = 'password'), 
    'is_logged_in': fields.Boolean(readonly=True, description='gets if the user is logged in or not')
})

project_model = api.model('Project',  {
    'id' : fields.Integer(readonly=True, description='project unique identifier'), 
    'name' : fields.String(required=True, description='name of project'), 
    'description': fields.String(), 
    'project_link': fields.String(required=True, description='link to your project documentation page'), 
    'business_tags' : fields.String(description = 'Business tags for seo stuff ')
})


add_model = api.model("Metadata",{
    'id': fields.Integer(required = True, description = 'id of the project '),
    'key' : fields.String(required= True, description = 'key of the project model to which the value would be added to'), 
   'value' : fields.String(required  = True, description = 'value that would be added to the key column ')

})

description_model = api.model("Description", {
    'descr': fields.String(required= True, description = "keywords separated by commas in order of relevance")
})

tags_model = api.model("Tags", {
    'tags' : fields.String(required =True, description = "Tags separated by commas in order of relevance")
})


@project_ns.route("/search/name/<name>")
class ProjName(Resource):
    @project_ns.response(200, 'Success',[project_model])
    @project_ns.doc("search a project by name")
    def get(self, name):
        res = utils.create_response()
        projects = utils.get_project_by_name(name)
        res.set_data(json.dumps(projects, cls = utils.CustomEncoder))
        return res 


@project_ns.route("/insert")
class ProjInsert(Resource):
    @project_ns.response(200, 'Success', [project_model])
    @project_ns.expect(project_model)
    @project_ns.doc("insert a project")
    @project_ns.marshal_with(project_model, code = HTTPStatus.CREATED)
    def post(self):
        body = api.payload
        project = Project()
        project.set_values(body)
        utils.insert_project(project)
        return project 
        
@project_ns.route("/<int:id>/update/description")
class ProjDescUpdate(Resource):
    def put(self, id: int, new_descr:str):
        ### TODO: Implement this later 
        pass 
    

@project_ns.route("/add")
class ProjKeyAdd(Resource):
    @project_ns.response(200, 'Success', project_model)
    @project_ns.doc("Add description/business tag to already existing project")
    @project_ns.expect(add_model)
    @project_ns.marshal_with(add_model, code =HTTPStatus.CREATED)
    def post(self):
        ## TODO: to be added later 
        pass 


@project_ns.route("/delete/id/<id>")
class ProjDelete(Resource): 
    def delete(self, id:int): 
        ### TODO : implement this later 
        logging.debug(f'Deleting project with ${id}')

    
@user_ns.route("/id/<id>")
class UserDelete(Resource): 
    def delete(self, id: int): 
        pass


@user_ns.route("/insert")
class UserInsert(Resource): 
    @user_ns.expect(user_model)
    @user_ns.response(200, 'Success', user_model)
    @user_ns.marshal_with(user_model, code = HTTPStatus.CREATED)
    def post(self):
        user = User()
        user.set_values(api.payload)
        utils.insert_user(user)
        return user

@user_ns.route("/update")
class UserUpdate(Resource): 
    def post(self, key, value): 
        pass 

@project_ns.route("/search/description")
class ProjDesc(Resource):
    @project_ns.response(200, 'Success' ,[project_model])
    @project_ns.expect(description_model)
    def post(self): 
        res = utils.create_response()
        descr = api.payload['descr']
        projects = utils.get_project_by_description(descr)
        res.set_data(json.dumps(projects, cls = utils.CustomEncoder))
        return res 


@project_ns.route("/search/tags/")
class ProjTag(Resource):
    @project_ns.response(200, 'Success',[project_model])
    @project_ns.expect(tags_model)
    def post(self):
        res = utils.create_response()
        tags = api.payload['tags']
        projects = utils.get_project_by_tags(tags)
        res.set_data(json.dumps(projects, cls = utils.CustomEncoder))
        return res 

@project_ns.route("/id")
class ProjId(Resource): 
    @project_ns.response(200,'Success', [project_model])
    @project_ns.param("id", "Id of the project")
    def get(self, id): 
        res = utils.create_response()
        project = utils.get_project_by_id(id)
        res.set_data(json.dumps(project, cls = utils.CustomEncoder))
        return res 


@user_ns.route("/filter")
class UserList(Resource): 
    @user_ns.response(200, 'Success', [user_model])
    def get(self): 
        res = utils.create_response()
        users = utils.get_all_users()
        res.set_data(json.dumps(users, cls = utils.CustomEncoder))
        return res 

@user_ns.route("/name")
class  UserName(Resource): 
    @user_ns.response(200, 'Success', [user_model])
    @user_ns.param("name", "Name of the project")
    def get(self, name: str): 
        res = utils.create_response()
        users  = utils.get_users_by_name(name)
        res.set_data(json.dumps(users,cls = utils.CustomEncoder))
        return res 

@user_ns.route("/email")
class UserEmail(Resource): 
    @user_ns.response(200, 'Success', [user_model])
    @user_ns.param("email", "Email of the user")
    def get(self, email): 
        res = utils.create_response()
        users = utils.get_users_by_mail(email)
        res.set_data(json.dumps(users, cls = utils.CustomEncoder))
        return res

@user_ns.route("/login-user")
class UserLogin(Resource):
    @user_ns.param("name", "username")
    @user_ns.param("password", "password")
    @user_ns.response(200, "Success")
    def post(self):
        if utils.authenticate_and_login_user(api.payload): 
            return
        pass 

@user_ns.route("/logout-user")
class UserLogout(Resource): 
    @user_ns.param("name")
    def post(self):
        name = api.payload['name']
        utils.logout_user(name)
        res = utils.create_response()
        res.set_data(f"User {name} successfully logged in")
        return res

    
     

@app.route("/ui")
def show_ui():
    return render_template('index.html')


def start_server(args):
    Context.setup(args.db, Bcrypt(app))
    app.run("0.0.0.0", port = args.port)
    
if __name__ =='__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug= True)
