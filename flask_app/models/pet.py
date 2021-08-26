from flask_app.config.mysqlcontroller import connectToMySQL
from flask_app.models import user
from flask import flash
DATABASE = 'pet_db'

class Pet:
    def __init__( self , data ):
        self.id = data['id']
        self.breed = data['breed']
        self.age = data['age']
        self.name = data['name']
        self.gender = data['gender']
        self.weight = data['weight']
        self.description = data['description']
        self.adopter_old_enough = data['adopter_old_enough']
        self.adopter_stable_income= data['adopter_stable_income']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    def get_user(self):
        return user.User.getOneById(self.user_id)
        
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM pets "
        result = connectToMySQL(DATABASE).query_db(query)
        pets = []
        for pet in result:
            pets.append(cls(pet))
        return pets  
   
    @classmethod
    def create(cls,data):
        query ="INSERT INTO pets (breed, age, created_at, updated_at, name, gender, weight, description, user_id, adopter_old_enough, adopter_stable_income) VALUES (%(breed)s, %(age)s, NOW(), NOW(), %(name)s, %(gender)s, %(weight)s, %(description)s, %(user_id)s, %(adopter_old_enough)s, %(adopter_stable_income)s)"
        return connectToMySQL(DATABASE).query_db(query,data)
        
    @classmethod
    def getOnebyname(cls, name):
        query = "SELECT * FROM pets WHERE name = %(name)s"
        data = {'name':name}
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls( results[0])
    
    @classmethod
    def getOneById(cls, id):
        query = "SELECT * FROM pets WHERE id = %(id)s"
        data = {'id':id}
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def edit(cls,data):
        query = "UPDATE pets SET breed = %(breed)s, age = %(age)s, name = %(name)s,gender = %(gender)s,weight = %(weight)s ,description = %(description)s,adopter_old_enough = %(adopter_old_enough)s,adopter_stable_income = %(adopter_stable_income)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete(cls,id):
        query = "DELETE FROM pets WHERE id = %(id)s"
        data = {'id':id}
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validate_pet(data):
        is_valid = True 
   
        if len(data['name']) < 1:
            flash("* Name cannot be empty", "name")
            is_valid = False
        if len(data['breed']) < 1 :
            flash("* Breed cannot be empty", "breed")
            is_valid = False
        if data['age'] == "" :
            flash("* Age cannot be empty", "age")
            is_valid = False
        if len(data['gender']) < 1 :
            flash("* Gender cannot be empty", "gender")
            is_valid = False
        if data['weight'] == "":
            flash("* Weight cannot be empty", "weight")
            is_valid = False
        if len(data['description']) < 1 :
            flash("* Description cannot be empty", "description")
            is_valid = False
        if data['adopter_old_enough'] == "no":
            flash("* Sorry, you have to be older than 18 years of age to adopt a pet from us!", "adopter_old_enough")
            is_valid = False
        if data['adopter_stable_income'] == "no":
            flash("* Sorry, you have to have a stable source of income to adopt a pet from us!", "adopter_stable_income")
            is_valid = False
        if is_valid:
            flash("* Pet adopted successfully.")
        return is_valid
    