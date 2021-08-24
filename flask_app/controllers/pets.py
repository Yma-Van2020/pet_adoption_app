from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.pet import Pet
from flask_app.models.user import User
from decimal import Decimal
import petpy
from bs4 import BeautifulSoup as bs
import os
import re
CITY_REGEX = re.compile(r"^[a-zA-z]{3,},\s?[a-zA-Z]{2,}$")

base=os.path.dirname(os.path.abspath(__file__))

@app.route("/new/application")
def create_application():
    if 'user_id' not in session:
        return redirect('/')
  
    return render_template("application.html")

@app.route("/create", methods=['POST'])
def add_new_re():
       
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    
    data = {
        "name" : request.form["name"],
        "breed" : request.form["breed"],
        "age" : request.form["age"],
        "gender" : request.form["gender"],
        "weight" : request.form["weight"],
        "description" : request.form["description"],
        "adopter_old_enough" : request.form["adopter_old_enough"],
        "adopter_stable_income" : request.form["adopter_stable_income"],
        "user_id" : session["user_id"]
        }  
 
    if not Pet.validate_pet(data):
        return redirect("/new/application")
   
    Pet.create(data)
    return redirect('/account')

@app.route("/pet/<int:pet_id>")
def view_instruct(pet_id):
    pet = Pet.getOneById(pet_id)
    user = User.getOneById(pet.user_id)
    return render_template("view_application.html", pet = pet, user = user)

@app.route("/pet/<int:pet_id>/edit")
def edit_pet(pet_id):
    if 'user_id' not in session:
        return redirect('/')
    
    pet = Pet.getOneById(pet_id)
    user = User.getOneById(pet.user_id)
    
    return render_template("edit_app.html", pet = pet, user = user)

@app.route("/edit/<int:pet_id>", methods =["POST"])
def update_one(pet_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": pet_id,
        "name" : request.form["name"],
        "breed" : request.form["breed"],
        "age" : request.form["age"],
        "gender" : request.form["gender"],
        "weight" : request.form["weight"],
        "description" : request.form["description"],
        "adopter_old_enough" : request.form["adopter_old_enough"],
        "adopter_stable_income" : request.form["adopter_stable_income"],
        "user_id" : session["user_id"]
        }   
   
    if not Pet.validate_pet(data):
        return redirect(f"/pet/{pet_id}/edit")
    Pet.edit(data)
    return redirect('/account')

@app.route("/pet/<int:pet_id>/delete")
def delete_one(pet_id):
    if 'user_id' not in session:
        return redirect('/')
    
    Pet.delete(pet_id)
    return redirect('/account')

@app.route("/william")
def william():
    return render_template("william.html")

@app.route("/gilbert")
def gilbert(): 
    return render_template("gilbert.html")

@app.route("/beatrice")
def beatrice(): 
    return render_template("Beatrice.html")

@app.route("/shadow")
def shadow():
    return render_template("Shadow.html")

@app.route("/zoey")
def zoey():
    return render_template("Zoey.html")

@app.route("/azalea")
def azalea():
    return render_template("Piggy.html")

@app.route("/fry")
def fry():
    return render_template("Fry.html")

@app.route("/gucci")
def gucci():
    return render_template("Gucci.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/input_search")
def search():
    return render_template("api_pets.html")

@app.route("/search" , methods=['POST'])
def input():
    session["valid"] = True   

    if not CITY_REGEX.match(request.form["location"]):
        flash("* Please follow the format of City, State (e.g. Seattle, WA)", "location")
        session["valid"] = False 
        return redirect("/input_search")
    
    if request.form["animal"] == "":
        flash("* Please choose an animal", "animal")
        session["valid"] = False 
        return redirect("/input_search")
    
    session["valid"] = True    
    session["animal"] = request.form["animal"]
    session["location"] = request.form["location"]
    return redirect("/api")
    

@app.route("/api")
def api():
    key = os.environ.get("FLASK_APP_API_KEY") 
    secret= os.environ.get("FLASK_APP_SECRET_KEY") 
    pf = petpy.Petfinder(key=key, secret=secret)
    print(session)
    cats = pf.animals(animal_type=session["animal"], status='adoptable', location=session["location"], distance=10,
                  results_per_page=12, pages=1)

    names = []
    pics = []
    urls = []
    ages =[]
    genders =[]
    breeds=[]
    sizes =[]
    for i in range(len(cats["animals"])):
        names.append(cats.get("animals")[i].get("name"))
        if(len(cats.get("animals")[i].get('photos')) > 0):
            pics.append(cats.get("animals")[i].get('photos')[0].get('full'))
        pass
        urls.append(cats.get("animals")[i].get("url"))
        ages.append(cats.get("animals")[i].get("age"))
        genders.append(cats.get("animals")[i].get("gender"))
        breeds.append(cats.get("animals")[i].get("breeds").get("primary"))
        sizes.append(cats.get("animals")[i].get("size"))
    
    
    return render_template("api_pets.html", names=names, pics= pics, urls=urls, ages=ages,genders=genders,breeds=breeds,sizes=sizes)

