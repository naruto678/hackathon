import logging 

class BaseModel:

    def toJSON(self):
        return self.__dict__


class User(BaseModel):
    id:int 
    name : str
    email : str
    hashed_password: str
    is_logged_in : bool  
    
    ## will think of a cleaner way to add this 
    def set_values(self, body):
        self.name = body.get("name", None)
        self.email = body.get("email", None)
        self.hashed_password = body.get("hashed_password",None)
        self.is_logged_in = body.get("is_logged_in")
    
class Project(BaseModel): 
    id: int
    description: str
    project_link: str 
    name: str
    business_tags: str

    def set_values(self, body):
        self.description = body.get('description', None)
        self.project_link = body.get('project_link', None)
        self.name = body.get('name', None)
        self.business_tags  = body.get("business_tags", None)
